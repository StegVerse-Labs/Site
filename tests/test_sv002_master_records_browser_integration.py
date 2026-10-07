from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class SV002MasterRecordsBrowserIntegrationTests(unittest.TestCase):
    def test_observer_runs_independent_master_records_worker(self):
        obs=(ROOT/"assets/sv002-observe.js").read_text(encoding="utf-8")
        worker=(ROOT/"assets/master-records-sv002-reconstruction-worker.js").read_text(encoding="utf-8")
        verifier=(ROOT/"assets/master-records-sv002-reconstruction.js").read_text(encoding="utf-8")
        self.assertIn("reconstructWithMasterRecords",obs)
        self.assertIn("MASTER_RECORDS_RECONSTRUCTING",obs)
        self.assertIn("PRINCIPAL EXECUTION PASS / RECONSTRUCTION PASS",obs)\n        self.assertIn("RECONSTRUCTION_UNAVAILABLE_NON_GATING",obs)\n        self.assertNotIn("MASTER RECORDS FAIL_CLOSED",obs)
        self.assertIn("MASTER_RECORDS_READY",worker)
        self.assertIn("MASTER_RECORDS_PASS",worker)
        self.assertIn("same_execution_bound:true",verifier)
        self.assertIn('reconstruction_owner:"master-records/orchestration"',verifier)

if __name__=="__main__":
    unittest.main()
