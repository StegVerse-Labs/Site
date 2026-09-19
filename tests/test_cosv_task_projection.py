from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class SiteCOSVProjectionTests(unittest.TestCase):
    def test_projection_validator_passes(self):
        cp=subprocess.run([sys.executable,str(ROOT/"scripts/check_cosv_task_projection.py")],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        self.assertIn("SITE_COSV_TASK_PROJECTION_PASS",cp.stdout)

    def test_complete_tasks_do_not_claim_activation(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        bundle=json.loads((ROOT/"data/cosv/active-claim-projections.json").read_text())
        bundled={row["task_id"]:row for row in bundle["projections"]}
        for row in idx["tasks"]:
            rec = bundled[row["task_id"]] if row["binding_mode"]=="EXTERNAL_PROJECTION_ACTIVE_CLAIM_SOURCE" else json.loads((ROOT/row["vector_ref"]).read_text())
            if rec["exact_metrics"]["lifecycle"]=="COMPLETE":
                self.assertTrue(rec["exact_metrics"]["evidence_complete"])
                self.assertFalse(rec["exact_metrics"]["activated"])
                if row["binding_mode"]!="EXTERNAL_PROJECTION_RETIRED_CANONICAL_TASK":
                    self.assertFalse(rec["exact_metrics"]["propagated"])

    def test_machine_owned_external_projection_preserves_real_blocker(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        row=next(item for item in idx["tasks"] if item["task_id"]=="SITE-SEMANTIC-SHORTHAND-396-R2")
        self.assertEqual(row["binding_mode"],"EXTERNAL_PROJECTION_MACHINE_OWNED_SOURCE")
        self.assertEqual(row["vector"],"50000000101000")
        rec=json.loads((ROOT/row["vector_ref"]).read_text())
        self.assertEqual(rec["exact_metrics"]["lifecycle"],"MACHINE_OWNED")
        self.assertEqual(rec["exact_metrics"]["blocker_count"],1)
        self.assertFalse(rec["exact_metrics"]["evidence_complete"])

    def test_terminal_external_projection_matches_completed_source_without_reopening_it(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        row=next(item for item in idx["tasks"] if item["task_id"]=="SITE-CURRENT-NEWS-RELEASES-967")
        self.assertEqual(row["binding_mode"],"EXTERNAL_PROJECTION_TERMINAL_SOURCE")
        self.assertEqual(row["vector"],"71000000100100")
        task=json.loads((ROOT/row["task_ref"]).read_text())
        rec=json.loads((ROOT/row["vector_ref"]).read_text())
        self.assertEqual(task["state"],"PUBLICATION_VERIFIED_COMPLETE")
        self.assertTrue(task["publication_verified"])
        self.assertEqual(rec["vector"],"71000000100100")
        self.assertEqual(rec["exact_metrics"]["lifecycle"],"COMPLETE")
        self.assertTrue(rec["exact_metrics"]["archive_ready"])
        self.assertTrue(rec["exact_metrics"]["evidence_complete"])
        self.assertFalse(rec["exact_metrics"]["thread_required"])
        self.assertFalse(rec["exact_metrics"]["activated"])
        self.assertFalse(rec["exact_metrics"]["propagated"])
    def test_501_and_519_are_terminal_external_sources(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        for task_id in ("SITE-TASK-RUNNER-SEMANTIC-LIVE-501","SITE-MIRROR-WORKFLOW-VALIDATOR-519"):
            row=next(item for item in idx["tasks"] if item["task_id"]==task_id)
            self.assertEqual(row["binding_mode"],"EXTERNAL_PROJECTION_TERMINAL_SOURCE")
            self.assertEqual(row["vector"],"71000000100100")
            rec=json.loads((ROOT/row["vector_ref"]).read_text())
            self.assertEqual(rec["exact_metrics"]["lifecycle"],"COMPLETE")
            self.assertTrue(rec["exact_metrics"]["archive_ready"])
            self.assertTrue(rec["exact_metrics"]["evidence_complete"])

    def test_repository_vector_present_requires_zero_unindexed_active_denominator(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        cov=idx["coverage"]
        self.assertEqual(cov["active_owner_deferred_source_bindings"],4)
        self.assertEqual(cov["repository_active_claim_source_vectors"],43)
        self.assertEqual(cov["repository_retired_canonical_task_vectors"],1)
        self.assertEqual(cov["legacy_claim_deferred_tasks"],0)
        self.assertEqual(cov["explicit_cosv_surface_gap"],0)
        self.assertTrue(cov["repository_active_claim_denominator_nonzero"])
        self.assertFalse(cov["repository_unindexed_active_claim_tasks_present"])
        self.assertEqual(cov["repository_unindexed_active_task_ids_observed"],0)
        self.assertTrue(cov["repository_active_task_surface_audit_complete"])
        self.assertTrue(cov["repository_vector_present_claimed"])
        self.assertIsNone(cov["repository_vector_present_blocker"])


    def test_repository_wide_successor_is_indexed_and_zero_gap_promotes_vector_present(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        row=next(item for item in idx["tasks"] if item["task_id"]=="SITE-COSV-REPOSITORY-WIDE-ADOPTION-001")
        self.assertEqual(row["binding_mode"],"SOURCE_BOUND")
        self.assertEqual(row["vector"],"20010000101000")
        cov=idx["coverage"]
        self.assertEqual(cov["repository_effective_active_claims_observed"],48)
        self.assertEqual(cov["repository_effective_active_task_ids_observed"],48)
        self.assertEqual(cov["repository_unindexed_active_task_ids_observed"],0)
        self.assertTrue(cov["repository_vector_present_claimed"])


    def test_active_owner_external_projections_preserve_source_semantics(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        expected={
            "SITE-HPS-USER-FIRST-VALIDATOR-508",
            "SITE-UNIFIED-GOVERNED-VALIDATOR-510",
            "SITE-MIRROR-GOAL-VALIDATOR-517",
            "SITE-LLM-FREE-TIER-TRUST-USER-FIRST-523",
        }
        rows=[row for row in idx["tasks"] if row["task_id"] in expected]
        self.assertEqual({row["task_id"] for row in rows}, expected)
        for row in rows:
            self.assertEqual(row["binding_mode"],"EXTERNAL_PROJECTION_SOURCE_BINDING_DEFERRED_ACTIVE_OWNER")
            self.assertEqual(row["vector"],"20010000101000")
            rec=json.loads((ROOT/row["vector_ref"]).read_text())
            self.assertEqual(rec["exact_metrics"]["lifecycle"],"CLAIMED_IMPLEMENTATION")
            self.assertFalse(rec["exact_metrics"]["archive_ready"])
            self.assertEqual(rec["exact_metrics"]["blocker_count"],1)
            self.assertFalse(rec["exact_metrics"]["evidence_complete"])
            self.assertFalse(rec["exact_metrics"]["activated"])
            self.assertFalse(rec["exact_metrics"]["propagated"])
            self.assertFalse(rec["evidence"]["source_semantics_mutated"])

    def test_525_terminal_projection_matches_released_source(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        row=next(item for item in idx["tasks"] if item["task_id"]=="SITE-FINAL-ACTIVATION-PENDING-RECONCILIATION-525")
        self.assertEqual(row["binding_mode"],"EXTERNAL_PROJECTION_TERMINAL_SOURCE")
        task=json.loads((ROOT/row["task_ref"]).read_text())
        rec=json.loads((ROOT/row["vector_ref"]).read_text())
        self.assertEqual(task["state"],"RELEASED")
        self.assertEqual(task["disposition"],"SATISFIED_BY_EXISTING_STATE")
        self.assertEqual(task["remaining"],[])
        self.assertTrue(task["archive_eligible"])
        self.assertEqual(rec["exact_metrics"]["lifecycle"],"COMPLETE")
        self.assertTrue(rec["exact_metrics"]["evidence_complete"])


    def test_claim_source_projection_bundle_preserves_all_live_owner_states(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        bundle=json.loads((ROOT/"data/cosv/active-claim-projections.json").read_text())
        rows=[row for row in idx["tasks"] if row["binding_mode"]=="EXTERNAL_PROJECTION_ACTIVE_CLAIM_SOURCE"]
        self.assertEqual(len(rows),43)
        self.assertEqual(len(bundle["projections"]),43)
        by_task={row["task_id"]:row for row in bundle["projections"]}
        self.assertEqual(set(by_task),{row["task_id"] for row in rows})
        for row in rows:
            rec=by_task[row["task_id"]]
            self.assertEqual(rec["vector"],row["vector"])
            self.assertFalse(rec["source_semantics_mutated"])
            self.assertFalse(rec["completion_inferred"])
            self.assertFalse(rec["exact_metrics"]["archive_ready"])
            self.assertFalse(rec["exact_metrics"]["evidence_complete"])
            self.assertFalse(rec["exact_metrics"]["activated"])
            self.assertFalse(rec["exact_metrics"]["propagated"])

    def test_retired_erl_claim_is_terminalized_and_projected_from_canonical_state(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        row=next(item for item in idx["tasks"] if item["task_id"]=="SS-ERL-KV-PROPAGATION-VERIFICATION-001")
        self.assertEqual(row["binding_mode"],"EXTERNAL_PROJECTION_RETIRED_CANONICAL_TASK")
        self.assertEqual(row["vector"],"71000000100101")
        rec=json.loads((ROOT/row["vector_ref"]).read_text())
        self.assertEqual(rec["evidence"]["canonical_coordination_state"],"RETIRED")
        self.assertTrue(rec["evidence"]["canonical_completion_claimed"])
        self.assertTrue(rec["evidence"]["canonical_completion_validated"])
        self.assertTrue(rec["exact_metrics"]["propagated"])
        self.assertFalse(rec["exact_metrics"]["activated"])

if __name__=="__main__":
    unittest.main()
