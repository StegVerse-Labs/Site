from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_hil_intr_node_sync",
    ROOT / "scripts/check_hil_intr_node_sync.py",
)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class HILInTrNodeSyncTests(unittest.TestCase):
    def test_repository_source_contract_passes(self) -> None:
        markers = mod.validate(ROOT)
        self.assertIn("STEGOS_NODE_HIL_INTR_SYNC_SOURCE_PASS", markers)
        self.assertIn("STEGOS_NODE_HIL_INTR_SYNC_TARGET_FAIL_CLOSED_PASS", markers)
        self.assertIn("STEGOS_NODE_HIL_INTR_SYNC_NO_EXECUTION_AUTHORITY_PASS", markers)

    def test_default_target_cannot_claim_unobserved_runtime(self) -> None:
        with self.assertRaisesRegex(mod.HILInTrNodeSyncError, "target_ingress_url_mismatch"):
            mod.validate_target_projection({
                "schema": "stegos.site.hil_intr_sync_target.v1",
                "state": "AWAITING_SOVEREIGN_INTR_INGRESS",
                "transport_origin": "STEGOS_NODE_OUTBOX",
                "ingress_url": "https://example.invalid/intr/materialization",
                "runtime_ingress_observed": False,
                "credential_authority": "TV/TVC",
                "credential_requirement": "NONE",
                "github_token_runtime_authority": "NONE",
                "execution_authority": "NONE",
                "authority_effect": "NONE_DISCOVERY_ONLY",
            })

    def test_default_target_cannot_claim_runtime_observed(self) -> None:
        with self.assertRaisesRegex(mod.HILInTrNodeSyncError, "target_runtime_ingress_observed_mismatch"):
            mod.validate_target_projection({
                "schema": "stegos.site.hil_intr_sync_target.v1",
                "state": "AWAITING_SOVEREIGN_INTR_INGRESS",
                "transport_origin": "STEGOS_NODE_OUTBOX",
                "ingress_url": None,
                "runtime_ingress_observed": True,
                "credential_authority": "TV/TVC",
                "credential_requirement": "NONE",
                "github_token_runtime_authority": "NONE",
                "execution_authority": "NONE",
                "authority_effect": "NONE_DISCOVERY_ONLY",
            })


if __name__ == "__main__":
    unittest.main()
