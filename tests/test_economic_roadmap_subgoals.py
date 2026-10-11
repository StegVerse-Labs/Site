#!/usr/bin/env python3
"""Negative tests: Site source cannot award authenticated roadmap progress."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("economic_subgoals", ROOT / "scripts/project_economic_roadmap_subgoals.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class SubgoalProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((ROOT / "data/economy/public-release-benchmarks.v1.json").read_text())

    def test_exact_sixteen_no_verified_subgoals(self):
        output = module.project(self.source)
        self.assertEqual(output["benchmark_count"], 16)
        self.assertEqual(len({b["benchmark_id"] for b in output["benchmarks"]}), 16)
        self.assertEqual(output["authority_effect"], "NONE")
        for b in output["benchmarks"]:
            self.assertEqual(b["verified_subgoals"], 0)
            self.assertGreater(b["outstanding_subgoals"], 0)
            self.assertTrue(all(p["evidence_ref"] is None for p in b["acceptance_predicates"]))

    def test_ci_and_merge_claims_cannot_grant_proof(self):
        source = copy.deepcopy(self.source)
        source["source_merge"] = "SUCCESS"
        source["ci_checks"] = "SUCCESS"
        source["issue_closed"] = True
        source["synthetic_receipt"] = {"master_records_state": "RECORDED"}
        output = module.project(source)
        self.assertTrue(all(b["verified_subgoals"] == 0 for b in output["benchmarks"]))

    def test_binding_not_promoted_to_authority(self):
        output = module.project(self.source)
        bound = next(b for b in output["benchmarks"] if b["benchmark_id"] == "S1_CHATGPT")
        unbound = next(b for b in output["benchmarks"] if b["benchmark_id"] == "S1_MYKV_AI")
        self.assertEqual(bound["binding_state"], "OBSERVED_NOT_AUTHORIZING")
        self.assertEqual(unbound["binding_state"], "UNRESOLVED")
        self.assertIsNone(unbound["canonical_task_id"])

    def test_ephemeral_runtime_predicates_independent(self):
        output = module.project(self.source)
        for bid in ("S1_CHATGPT", "S1_CLAUDE"):
            gate = next(b for b in output["benchmarks"] if b["benchmark_id"] == bid)
            names = {p["predicate"] for p in gate["acceptance_predicates"]}
            self.assertIn("real_provider_request_and_usable_response", names)
            self.assertIn("terminal_ephemeral_session_destruction", names)
            self.assertIn("governed_publication_closure", names)

if __name__ == "__main__":
    unittest.main()
