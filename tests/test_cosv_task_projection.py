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

if __name__=="__main__":
    unittest.main()
