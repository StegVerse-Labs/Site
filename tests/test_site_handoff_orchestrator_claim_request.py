"""D-P4: a branch with no active claim but a queued claim request fails closed with six fields.

The request never satisfies the pre-work claim gate; it only makes the gate's refusal carry its repair.
"""
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("site_handoff_orchestrator", ROOT / "scripts" / "site_handoff_orchestrator.py")
orchestrator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(orchestrator)
SIX = list(orchestrator.ACTIONABLE_FIELDS)
REQUEST = ROOT / "data" / "session-work-claim-requests.d" / "site-workspace-interoperability-20260831.request.json"


class QueuedClaimRequestTests(unittest.TestCase):
    def test_requested_branch_yields_six_field_fail_closed(self):
        record = orchestrator.queued_claim_request("claude/1509-wu2-rehydration-six-fields")
        self.assertIsNotNone(record)
        self.assertEqual(record["disposition"], "FAIL_CLOSED")
        self.assertEqual(record["authority_effect"], "NONE_REQUEST_ONLY")
        self.assertEqual(record["request_ref"], str(REQUEST.relative_to(ROOT)))
        self.assertEqual(list(record["actionable_disposition"]), SIX)
        self.assertEqual(record["actionable_disposition"]["failure_code"], "WORKERCOORDINATOR_CLAIM_NOT_GRANTED")
        self.assertTrue(record["actionable_disposition"]["retry_entrypoint"].startswith(str(REQUEST.relative_to(ROOT))))

    def test_unrequested_branch_has_no_record(self):
        self.assertIsNone(orchestrator.queued_claim_request("feature/not-requested"))

    def _queue(self, request):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / "x.request.json").write_text(json.dumps(request), encoding="utf-8")
        return root

    def test_request_claiming_authority_or_missing_fields_is_ignored(self):
        base = json.loads(REQUEST.read_text(encoding="utf-8"))
        branch = base["requested_branch_bindings"][0]["branch"]
        granting = dict(base, request_grants_claim_authority=True)
        partial = json.loads(json.dumps(base))
        del partial["actionable_disposition"]["next_attempt"]
        not_requested = dict(base, state="GRANTED")
        for name, req in {"granting": granting, "partial": partial, "state": not_requested}.items():
            with self.subTest(name):
                root = self._queue(req)
                self.assertIsNone(orchestrator.queued_claim_request(branch, root=root), name)

    def test_gate_still_fails_and_summary_carries_the_record(self):
        record = orchestrator.queued_claim_request("claude/1509-org-emp-kv-gate-consumer")
        with tempfile.NamedTemporaryFile("r+", suffix=".md") as summary:
            os.environ["GITHUB_STEP_SUMMARY"] = summary.name
            try:
                orchestrator.write_step_summary(record)
            finally:
                del os.environ["GITHUB_STEP_SUMMARY"]
            text = Path(summary.name).read_text(encoding="utf-8")
        self.assertIn("FAIL_CLOSED (claim requested, not granted)", text)
        for key in SIX:
            self.assertIn(f"- {key}: ", text)


if __name__ == "__main__":
    unittest.main()
