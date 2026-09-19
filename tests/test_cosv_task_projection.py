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
        for row in idx["tasks"]:
            rec=json.loads((ROOT/row["vector_ref"]).read_text())
            if rec["exact_metrics"]["lifecycle"]=="COMPLETE":
                self.assertTrue(rec["exact_metrics"]["evidence_complete"])
                self.assertFalse(rec["exact_metrics"]["activated"])
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

    def test_repository_vector_present_remains_fail_closed_on_unindexed_active_denominator(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        cov=idx["coverage"]
        self.assertEqual(cov["active_owner_deferred_source_bindings"],0)
        self.assertEqual(cov["legacy_claim_deferred_tasks"],0)
        self.assertEqual(cov["explicit_cosv_surface_gap"],0)
        self.assertTrue(cov["repository_active_claim_denominator_nonzero"])
        self.assertTrue(cov["repository_unindexed_active_claim_tasks_present"])
        self.assertFalse(cov["repository_active_task_surface_audit_complete"])
        self.assertFalse(cov["repository_vector_present_claimed"])

    def test_denominator_snapshot_excludes_only_current_accounting_task(self):
        idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
        snap=idx["coverage"]["denominator_snapshot"]
        self.assertEqual(snap["effective_active_claims"],53)
        self.assertEqual(snap["effective_active_task_ids"],53)
        self.assertEqual(snap["unindexed_active_task_ids"],53)
        self.assertEqual(snap["prior_unindexed_active_task_ids"],55)
        self.assertEqual(snap["excludes_current_accounting_task_ids"],["SITE-COSV-ADOPTION-RETIREMENT-BATCH-001"])
        self.assertFalse(snap["repository_vector_present"])

if __name__=="__main__":
    unittest.main()
