import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "stegos-node" / "index.html"
AUTO = ROOT / "stegos-node" / "org-allocator-bootstrap-auto.html"
IMMUTABLE = ROOT / "stegos-node" / "org-allocator-bootstrap-task0010-g6-v2.html"
RECOVERY = ROOT / "stegos-node" / "org-allocator-evidence-recovery-task0010-g6-v1.html"
SW = ROOT / "stegos-node" / "service-worker.js"


class StegOSNodeAllocatorAutoCarrierTests(unittest.TestCase):
    def test_normal_node_starts_carrier_only_after_registered_state(self):
        text = INDEX.read_text(encoding="utf-8")
        self.assertIn('if (allocatorCarrierStarted || stateNode.textContent !== "REGISTERED") return;', text)
        self.assertIn('if (registered) {', text)
        self.assertIn('startVerifiedAllocatorCarrier();', text)

    def test_legacy_auto_entry_retains_current_canonical_predicates(self):
        auto = AUTO.read_text(encoding="utf-8")
        self.assertIn('EXPECTED_TASK="TASK-2026-0010"', auto)
        self.assertIn('receipt.queued.indexOf(EXPECTED_TASK)===-1', auto)
        self.assertIn('receipt.selected!==EXPECTED_TASK', auto)
        self.assertNotIn('queued.length', auto)

    def test_immutable_execution_checks_journal_before_allocator_mutation(self):
        text = IMMUTABLE.read_text(encoding="utf-8")
        self.assertIn('ORG_ALLOCATOR_RELEASE="task0010-g6-v2"', text)
        self.assertIn('function alreadyExecuted()', text)
        self.assertIn('TASK-2026-0010 already retained; no allocator mutation performed', text)
        self.assertIn('receipt.queued.indexOf(EXPECTED_TASK)===-1', text)
        self.assertIn('receipt.selected!==EXPECTED_TASK', text)
        self.assertNotIn('queued.length', text)

    def test_recovery_surface_has_no_allocator_mutation_primitive(self):
        text = RECOVERY.read_text(encoding="utf-8")
        self.assertIn('EXPECTED_TASK="TASK-2026-0010"', text)
        self.assertIn('RETAINED_CANONICAL_ALLOCATION_EVIDENCE_RECOVERED', text)
        self.assertIn('allocator_mutation_performed:false', text)
        self.assertNotIn('ALLOC_DB=', text)
        self.assertNotIn('atomicCompareAndSwap', text)
        self.assertNotIn('.allocate(', text)

    def test_allocator_execution_and_recovery_paths_are_network_only(self):
        sw = SW.read_text(encoding="utf-8")
        self.assertIn('"/stegos-node/org-allocator-bootstrap-auto.html": true', sw)
        self.assertIn('"/stegos-node/org-allocator-bootstrap-task0010-g6-v2.html": true', sw)
        self.assertIn('"/stegos-node/org-allocator-evidence-recovery-task0010-g6-v1.html": true', sw)
        self.assertIn('"/stegos-node/org-allocator-portable.js": true', sw)
        self.assertIn('"/stegos-node/org-allocator-current-iphone-package.json": true', sw)


if __name__ == "__main__":
    unittest.main()
