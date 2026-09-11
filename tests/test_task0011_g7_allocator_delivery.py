from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
NODE = ROOT / "stegos-node"


class Task0011G7AllocatorDeliveryTests(unittest.TestCase):
    def test_successor_package_is_exactly_source_bound(self):
        pkg = json.loads((NODE / "org-allocator-current-iphone-task0011-package.json").read_text())
        self.assertEqual(pkg["schema"], "stegverse.org-allocator-task-successor-package/v1")
        self.assertEqual(pkg["successor_task_git_blob_sha"], "a9f90414e59e308d66faf7ff2d5c31173b1687ca")
        task = pkg["successor_task"]
        self.assertEqual(task["task_id"], "TASK-2026-0011")
        self.assertEqual(task["requested_at"], "2026-09-11T01:51:58Z")
        self.assertEqual(task["workspace"]["branch"], "claim/current-iphone-kv-testflight-static-bootstrap-r1")
        self.assertFalse(task["workspace"]["direct_push_allowed"])
        self.assertTrue(task["workspace"]["pull_request_required"])
        self.assertEqual(task["predecessor_provenance"]["allocator_generation"], 6)
        self.assertEqual(task["predecessor_provenance"]["allocator_fence"], 6)
        self.assertFalse(task["predecessor_provenance"]["reactivation_or_scope_widening_allowed"])
        self.assertEqual(task["authority"]["credential_authority"], "TV/TVC")
        self.assertEqual(task["authority"]["github_token_runtime_authority"], "NONE")
        self.assertFalse(task["authority"]["render_fallback_allowed"])

    def test_successor_allocator_preserves_selection_algorithm_and_adds_only_task0011_floor(self):
        source = (NODE / "org-allocator-portable-task0011.js").read_text()
        for marker in (
            'task_0011_git_blob_sha:"a9f90414e59e308d66faf7ff2d5c31173b1687ca"',
            'pkg.tasks.length!==5',
            'TASK-2026-0007|TASK-2026-0008|TASK-2026-0009|TASK-2026-0010|TASK-2026-0011',
            '"2026-09-11T01:51:58Z","site:current-iphone-kv-testflight-static-bootstrap"',
            'atomic organization allocator CAS lost race or stale state',
            'CLAIM_AUTHORITY_ONLY_WHEN_SELECTED_BY_CANONICAL_ALLOCATOR',
            'github_token_runtime_authority:"NONE"',
            'credential_authority:"TV/TVC"',
        ):
            self.assertIn(marker, source)
        self.assertNotIn("fetch(", source)
        self.assertNotIn("Render", source)

    def test_v1_remains_immutable_fail_closed_observation_surface(self):
        page = (NODE / "org-allocator-bootstrap-task0011-g7-v1.html").read_text()
        for marker in (
            'EXPECTED="TASK-2026-0011"',
            'EXPECTED_BLOB="a9f90414e59e308d66faf7ff2d5c31173b1687ca"',
            'function alreadyExecuted()',
            'TASK-2026-0011 already retained; no allocator mutation performed',
            'preview.receipt.selected!==EXPECTED',
            'predecessor_task_0010_scope_widened:false',
            'cache:"no-store"',
        ):
            self.assertIn(marker, page)

    def test_v2_reconciles_only_cryptographically_retained_predecessor_status(self):
        page = (NODE / "org-allocator-bootstrap-task0011-g7-v2.html").read_text()
        for marker in (
            'RELEASE="task0011-g7-v2-20260910"',
            'PREDECESSORS=["TASK-2026-0007","TASK-2026-0008","TASK-2026-0009","TASK-2026-0010"]',
            'function observedAllocatorTaskIds()',
            'r.schema==="stegos.org_allocator_same_device_execution_receipt/v1"',
            'r.canonical_allocator_receipt.selected===r.selected_task_id',
            'r.claim_observation.task_id===r.selected_task_id',
            'next.task_statuses[id]="active"',
            'retained TASK-2026-0010 allocator receipt required before successor reconciliation',
            'canon(expected)!==canon(normalized)',
            'canon(current)===canon(raw)',
            'canonical preview selected "+String(preview.receipt.selected||"none")+" instead of TASK-2026-0011 after journal reconciliation',
            'reconciliation_grants_claim_authority:false',
            'reconciliation_synthesizes_completion:false',
            'predecessor_task_0010_scope_widened:false',
            'credential_authority:"TV/TVC"',
            'github_token_runtime_authority:"NONE"',
        ):
            self.assertIn(marker, page)
        self.assertNotIn('next.task_statuses[id]="completed"', page)
        self.assertLess(page.index("var prior=alreadyExecuted()"), page.index("readRaw()"))

    def test_task0011_delivery_is_network_only(self):
        sw = (NODE / "service-worker.js").read_text()
        self.assertIn('stegos-node-shell-v14-task0011-g7-journal-reconciliation-v2', sw)
        for path in (
            "/stegos-node/org-allocator-bootstrap-task0011-g7-v1.html",
            "/stegos-node/org-allocator-bootstrap-task0011-g7-v2.html",
            "/stegos-node/org-allocator-portable-task0011.js",
            "/stegos-node/org-allocator-current-iphone-task0011-package.json",
        ):
            self.assertIn(path, sw)
        self.assertIn('fetch(event.request, {cache: "no-store"})', sw)


if __name__ == "__main__":
    unittest.main()
