import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ece_projection", ROOT / "scripts" / "project_ecosystem_continuity.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def evaluation(state="CONTINUOUS"):
    return {
        "schema": "stegverse.ecosystem-continuity-evaluation.v1",
        "evaluation_id": "ece_0123456789abcdef01234567",
        "evaluated_at": "2026-09-11T22:00:00Z",
        "evaluator_version": "0.1.0",
        "registry_sha256": "a" * 64,
        "continuity_state": state,
        "completeness": {"registered_predicates": 1, "observed_predicates": 1, "evaluation_errors": 0},
        "authority_effect": "NONE_DIAGNOSTIC_ONLY",
        "findings": [{
            "schema": "stegverse.ecosystem-continuity-finding.v1",
            "finding_id": "ecef_0123456789abcdef01234567",
            "component_id": "sdk",
            "predicate_id": "route_available",
            "observation_state": "PASS",
            "severity": "INFO",
            "continuity_critical": True,
            "evidence": ["private://must-not-project"],
            "evidence_age_seconds": 3,
            "authority_owner": "StegVerse-org/StegVerse-SDK",
            "remediation_class": "NONE",
            "remediation_state": "UNASSIGNED",
            "detail": "sensitive detail must not project"
        }],
    }


class ProjectionTests(unittest.TestCase):
    def test_safe_projection_preserves_categorical_truth(self):
        result = MOD.project(evaluation("CONTINUOUS_WITH_DEGRADATION"))
        self.assertEqual(result["continuity_state"], "CONTINUOUS_WITH_DEGRADATION")
        self.assertEqual(result["authority_effect"], "NONE_READ_ONLY_PROJECTION")
        self.assertTrue(result["source_available"])
        self.assertNotIn("evidence", result["findings"][0])
        self.assertNotIn("detail", result["findings"][0])
        self.assertNotIn("remediation_class", result["findings"][0])

    def test_invalid_source_authority_fails_closed(self):
        source = evaluation()
        source["authority_effect"] = "EXECUTE"
        result = MOD.project(source)
        self.assertEqual(result["continuity_state"], "INDETERMINATE")
        self.assertFalse(result["source_available"])

    def test_invalid_observation_fails_closed(self):
        source = evaluation()
        source["findings"][0]["observation_state"] = "HEALTHY"
        result = MOD.project(source)
        self.assertEqual(result["continuity_state"], "INDETERMINATE")


if __name__ == "__main__":
    unittest.main()
