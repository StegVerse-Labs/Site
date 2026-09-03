from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "project_hil_intr_sync_target",
    ROOT / "scripts/project_hil_intr_sync_target.py",
)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def profile() -> dict:
    return {
        "schema": "stegverse.hil-intr-materialization-ingress-profile/v1",
        "state": "ACTIVE_SOVEREIGN_INTR_INGRESS",
        "protocol": "InTr",
        "profile_path": "/intr/profile",
        "materialization_path": "/intr/materialization",
        "supported_origins": ["STEGOS_NODE_OUTBOX", "TVC_RELAY_EGRESS"],
        "direct_node_credential_requirement": "NONE",
        "direct_node_tvc_authorization_required": False,
        "relay_tvc_authorization_required": True,
        "event_triggered": True,
        "always_on_receiver_required": False,
        "second_user_device_required": False,
        "exact_request_validation_required": True,
        "write_once_queue_admission": True,
        "tls_enabled": True,
        "runtime_execution_attempted": False,
        "hil_receiver_readiness_claimed": False,
        "hil_custody_claimed": False,
        "g18_required": False,
        "credential_authority": "TV/TVC",
        "github_token_runtime_authority": "NONE",
        "execution_authority": "NONE",
        "authority_effect": "NONE_DISCOVERY_EVIDENCE_ONLY",
    }


def observation() -> dict:
    value = profile()
    return {
        "schema": "stegverse.hil-intr-ingress-observation/v1",
        "observation_state": "OBSERVED_HTTPS_PROFILE",
        "observed_profile_url": "https://ingress.stegverse.org/intr/profile",
        "observed_at": "2026-08-29T20:55:00Z",
        "https_observed": True,
        "http_status": 200,
        "credential_used": False,
        "profile": value,
        "profile_sha256": mod.sha256_hex(value),
        "evidence_ref": "stegverse://runtime-observation/HIL-INTR-001",
        "github_token_runtime_authority": "NONE",
        "execution_authority": "NONE",
        "authority_effect": "NONE_OBSERVATION_ONLY",
    }


class HILInTrTargetProjectorTests(unittest.TestCase):
    def test_authentic_https_profile_projects_non_authorizing_target(self) -> None:
        target = mod.project_target(observation())
        self.assertEqual(target["state"], "CONFORMING_SOVEREIGN_INTR_INGRESS")
        self.assertEqual(target["ingress_url"], "https://ingress.stegverse.org/intr/materialization")
        self.assertTrue(target["runtime_ingress_observed"])
        self.assertEqual(target["credential_authority"], "TV/TVC")
        self.assertEqual(target["credential_requirement"], "NONE")
        self.assertEqual(target["github_token_runtime_authority"], "NONE")
        self.assertEqual(target["execution_authority"], "NONE")
        self.assertFalse(target["hil_execution_observed"])
        self.assertFalse(target["hil_receiver_readiness_observed"])
        self.assertFalse(target["hil_custody_observed"])
        self.assertFalse(target["g18_completion_required"])

    def test_http_observation_cannot_project_target(self) -> None:
        value = observation()
        value["observed_profile_url"] = "http://ingress.stegverse.org/intr/profile"
        with self.assertRaisesRegex(mod.HILInTrTargetProjectionError, "requires_https"):
            mod.project_target(value)

    def test_profile_hash_tamper_fails_closed(self) -> None:
        value = observation()
        value["profile_sha256"] = "0" * 64
        with self.assertRaisesRegex(mod.HILInTrTargetProjectionError, "profile_sha256_mismatch"):
            mod.project_target(value)

    def test_non_tls_profile_cannot_project_target(self) -> None:
        value = observation()
        value["profile"] = copy.deepcopy(value["profile"])
        value["profile"]["tls_enabled"] = False
        value["profile_sha256"] = mod.sha256_hex(value["profile"])
        with self.assertRaisesRegex(mod.HILInTrTargetProjectionError, "profile_tls_enabled_mismatch"):
            mod.project_target(value)

    def test_profile_cannot_claim_receiver_readiness(self) -> None:
        value = observation()
        value["profile"] = copy.deepcopy(value["profile"])
        value["profile"]["hil_receiver_readiness_claimed"] = True
        value["profile_sha256"] = mod.sha256_hex(value["profile"])
        with self.assertRaisesRegex(mod.HILInTrTargetProjectionError, "profile_hil_receiver_readiness_claimed_mismatch"):
            mod.project_target(value)

    def test_direct_node_must_remain_credentialless(self) -> None:
        value = observation()
        value["profile"] = copy.deepcopy(value["profile"])
        value["profile"]["direct_node_credential_requirement"] = "TVC_TOKEN"
        value["profile_sha256"] = mod.sha256_hex(value["profile"])
        with self.assertRaisesRegex(mod.HILInTrTargetProjectionError, "profile_direct_node_credential_requirement_mismatch"):
            mod.project_target(value)

    def test_source_default_target_remains_unobserved(self) -> None:
        import json
        current = json.loads((ROOT / "stegos-node/hil-intr-sync-target.json").read_text(encoding="utf-8"))
        self.assertEqual(current["state"], "AWAITING_SOVEREIGN_INTR_INGRESS")
        self.assertIsNone(current["ingress_url"])
        self.assertFalse(current["runtime_ingress_observed"])


if __name__ == "__main__":
    unittest.main()
