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

if __name__=="__main__":
    unittest.main()
