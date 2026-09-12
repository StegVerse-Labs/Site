from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ece_materializer", ROOT / "scripts" / "materialize_ecosystem_continuity_current.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def projection():
    return {
        "schema": "stegverse.site-ecosystem-continuity-projection.v1",
        "source_evaluation_id": "ece_fixture",
        "evaluated_at": "2026-09-12T06:00:00Z",
        "evaluator_version": "0.1.0",
        "continuity_state": "AT_RISK",
        "source_available": True,
        "projection_error": None,
        "completeness": {"registered_predicates": 1, "observed_predicates": 0, "evaluation_errors": 0},
        "findings": [{"finding_id": "ecef_fixture", "component_id": "sdk", "predicate_id": "resident", "observation_state": "NOT_OBSERVED", "severity": "HIGH", "continuity_critical": True, "evidence_age_seconds": None, "authority_owner": "StegVerse", "remediation_state": "DETECTED"}],
        "authority_effect": "NONE_READ_ONLY_PROJECTION"
    }


class MaterializerTests(unittest.TestCase):
    def _fixture(self, root: Path):
        projection_path = root / "receipts" / "site-projection.latest.json"
        projection_path.parent.mkdir(parents=True)
        raw = (json.dumps(projection(), indent=2, sort_keys=True) + "\n").encode()
        projection_path.write_bytes(raw)
        cycle_path = root / "receipts" / "cycle.latest.json"
        cycle_path.write_text(json.dumps({
            "schema": "stegverse.healer-ecosystem-continuity-cycle/v1",
            "state": "COMPLETE",
            "site_projection_ref": str(projection_path.resolve()),
            "site_projection_sha256": hashlib.sha256(raw).hexdigest()
        }), encoding="utf-8")
        return cycle_path, projection_path, raw

    def test_exact_bytes_are_materialized_without_recalculation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cycle, source, raw = self._fixture(root)
            served = root / "served"
            result = MOD.materialize(cycle_receipt=cycle, projection=source, served_site_root=served)
            target = served / "data" / "ecosystem-continuity" / "current.json"
            self.assertEqual(target.read_bytes(), raw)
            self.assertTrue(result["exact_bytes_preserved"])
            self.assertFalse(result["continuity_recalculated"])
            self.assertFalse(result["live_publication_observed"])
            self.assertEqual(result["authority_effect"], "NONE_COPY_ONLY")

    def test_sha_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cycle, source, _ = self._fixture(root)
            data = json.loads(cycle.read_text())
            data["site_projection_sha256"] = "0" * 64
            cycle.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "CYCLE_PROJECTION_SHA256_MISMATCH"):
                MOD.materialize(cycle_receipt=cycle, projection=source, served_site_root=root / "served")

    def test_source_repository_writeback_is_forbidden(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cycle, source, _ = self._fixture(root)
            source_repo = root / "site-source"
            source_repo.mkdir()
            with self.assertRaisesRegex(ValueError, "SOURCE_REPOSITORY_WRITEBACK_FORBIDDEN"):
                MOD.materialize(cycle_receipt=cycle, projection=source, served_site_root=source_repo, source_site_root=source_repo)


if __name__ == "__main__":
    unittest.main()
