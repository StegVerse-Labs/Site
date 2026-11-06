"""Durable-queue claim requests (D-P3): request bytes only, never claim authority.

A request under data/session-work-claim-requests.d/ asks the canonical organization allocator to bind
branches to an existing claim fragment. It grants nothing, edits no fragment, carries six actionable
fields while ungranted, and is materialized only by the allocator's own receipt.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "session-work-claim-requests.d"
SIX = ["failure_code", "failed_predicate", "required_evidence_or_repair", "retry_entrypoint",
       "owning_existing_goal", "next_attempt"]
SHA = re.compile(r"^[0-9a-f]{40}$")


def requests():
    return [(p, json.loads(p.read_text(encoding="utf-8"))) for p in sorted(QUEUE.glob("*.request.json"))]


class ClaimRequestQueueTests(unittest.TestCase):
    def test_queue_has_entries(self):
        self.assertTrue(requests())

    def test_requests_carry_no_claim_authority(self):
        for path, r in requests():
            with self.subTest(path.name):
                self.assertEqual(r["schema"], "stegverse.session-work-claim-request/v1")
                self.assertEqual(r["state"], "REQUESTED")
                self.assertEqual(r["authority_effect"], "NONE_REQUEST_ONLY")
                self.assertIs(r["request_grants_claim_authority"], False)
                self.assertIs(r["allocator_remains_claim_authority"], True)
                self.assertEqual(r["credential_authority"], "TV/TVC")
                self.assertIs(r["github_token_required"], False)
                self.assertEqual(r["github_token_runtime_authority"], "NONE")
                self.assertIs(r["network_source_fetch_allowed"], False)
                self.assertIs(r["second_machine_required"], False)

    def test_requests_target_an_existing_fragment_without_editing_it(self):
        for path, r in requests():
            with self.subTest(path.name):
                fragment = json.loads((ROOT / r["claim_fragment"]).read_text(encoding="utf-8"))
                self.assertEqual(fragment["registry_fragment_type"], "stegverse_session_work_claim_registry_fragment")
                self.assertIn(r["claim_id"], [c["claim_id"] for c in fragment["claims"]])
                self.assertIn("never edits the claim fragment", r["materialization"]["effect"])
                self.assertIn("ORGANIZATION_WORKER_CLAIM_GRANTED", r["materialization"]["on"])

    def test_branch_bindings_are_unique_and_pinned(self):
        for path, r in requests():
            with self.subTest(path.name):
                branches = [b["branch"] for b in r["requested_branch_bindings"]]
                self.assertEqual(len(branches), len(set(branches)))
                for b in r["requested_branch_bindings"]:
                    self.assertRegex(b["head_at_request"], SHA)
                    self.assertIsInstance(b["pull_request"], int)

    def test_no_task_projection_is_created_while_admission_is_suspended(self):
        for path, r in requests():
            with self.subTest(path.name):
                self.assertIsNone(r["canonical_allocator"]["target_task_projection"])
                self.assertIn("#167 r9", r["canonical_allocator"]["target_task_projection_reason"])

    def test_ungranted_request_is_fail_closed_with_six_fields(self):
        for path, r in requests():
            with self.subTest(path.name):
                d = r["actionable_disposition"]
                self.assertEqual(d["disposition"], "FAIL_CLOSED")
                for key in SIX:
                    self.assertIsInstance(d[key], str)
                    self.assertTrue(d[key].strip(), key)
                self.assertEqual(d["owning_existing_goal"], r["owning_existing_goal"])


if __name__ == "__main__":
    unittest.main()
