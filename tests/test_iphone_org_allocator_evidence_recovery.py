import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class AllocatorEvidenceRecoveryTests(unittest.TestCase):
    def test_recovery_surface_is_read_only_and_task_bound(self):
        text = (ROOT / "stegos-node" / "org-allocator-evidence-recovery-task0010-g6-v1.html").read_text()
        self.assertIn('EXPECTED_TASK="TASK-2026-0010"', text)
        self.assertIn('stegos.org_allocator_same_device_execution_receipt/v1', text)
        self.assertIn('RETAINED_CANONICAL_ALLOCATION_EVIDENCE_RECOVERED', text)
        self.assertIn('allocator_mutation_performed:false', text)
        self.assertNotIn('ALLOC_DB=', text)
        self.assertNotIn('atomicCompareAndSwap', text)
        self.assertNotIn('.allocate(', text)

    def test_immutable_execution_surface_checks_existing_journal_before_mutation(self):
        text = (ROOT / "stegos-node" / "org-allocator-bootstrap-task0010-g6-v2.html").read_text()
        self.assertIn('ORG_ALLOCATOR_RELEASE="task0010-g6-v2"', text)
        self.assertIn('function alreadyExecuted()', text)
        self.assertIn('TASK-2026-0010 already retained; no allocator mutation performed', text)
        self.assertIn('result.receipt.queued.indexOf(EXPECTED_TASK)===-1', text)
        self.assertIn('result.receipt.selected!==EXPECTED_TASK', text)
        self.assertNotIn('queued.length', text)


if __name__ == "__main__":
    unittest.main()
