import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import release_merged_session_claims as rel  # noqa: E402

SHA = "a" * 40
AT = "2026-10-18T12:00:00Z"
# The COSV validator follows claim, task and vector refs anywhere under data/.
COPIED = ("data", "scripts/check_session_work_claims.py", "scripts/check_cosv_task_projection.py",
          "scripts/release_merged_session_claims.py")


def copy_repo() -> Path:
    root = Path(tempfile.mkdtemp())
    for rel_path in COPIED:
        src, dst = ROOT / rel_path, root / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        (shutil.copytree if src.is_dir() else shutil.copy2)(src, dst)
    return root


def add_claim(root: Path, branch: str, state: str = "CLAIMED_FOR_IMPLEMENTATION", task_id: str = "TEST-RELEASE-TASK-001") -> Path:
    path = root / "data/session-work-claims.d/test-release-claim.json"
    claim = {
        "claim_id": "TEST-RELEASE-CLAIM", "session_worker_id": "test", "task_id": task_id,
        "originating_goal": "test", "repository": "StegVerse-Labs/Site", "branch": branch, "role": "IMPLEMENTATION",
        "state": state, "normalized_work_key": "site:test-release", "dependency_surface_keys": [],
        "claimed_paths": ["data/session-work-claims.d/test-release-claim.json"], "handoff": "README.md",
        "handoff_revision": "T", "claim_created_at": AT, "claim_expires_when": "merge", "expected_evidence": [],
        "collision_boundaries": [], "next_task_after_release": "none",
    }
    path.write_text(json.dumps({"registry_fragment_type": "stegverse_session_work_claim_registry_fragment",
                                "schema_version": "1.0.0", "repository": "StegVerse-Labs/Site", "claims": [claim]}), encoding="utf-8")
    return path


class ReleaseMergedSessionClaimsTests(unittest.TestCase):
    def setUp(self):
        self.root = copy_repo()
        self.addCleanup(shutil.rmtree, self.root)

    def test_releases_only_release_fields_and_recounts(self):
        path = add_claim(self.root, "feature/x")
        before = json.loads(path.read_text(encoding="utf-8"))["claims"][0]
        report = rel.release(self.root, "feature/x", 42, SHA, AT, validators=())
        self.assertEqual(report["released"], ["TEST-RELEASE-CLAIM"])
        after = json.loads(path.read_text(encoding="utf-8"))["claims"][0]
        changed = {k for k in set(before) | set(after) if before.get(k) != after.get(k)}
        self.assertEqual(changed, {"state", "pull_request", "release_commit", "claim_released_at"})
        self.assertEqual(list(after)[list(after).index("state"):][:4], ["state", "pull_request", "release_commit", "claim_released_at"])
        self.assertEqual((after["state"], after["pull_request"], after["release_commit"]), ("RELEASED_COMPLETE", 42, SHA))

    def test_releasing_a_live_claim_passes_both_validators(self):
        projected = rel.active_projection_claim_ids(self.root)
        # The writer releases fragment rows only; a claim held solely in the canonical registry is not a candidate.
        fragmented = {row.get("claim_id") for path in (self.root / "data/session-work-claims.d").glob("*.json")
                      for row in json.loads(path.read_text(encoding="utf-8")).get("claims") or [] if isinstance(row, dict)}
        by_branch = {}
        for row in rel.effective_active_claims(self.root):
            if row.get("state") in rel.RELEASABLE_STATES and row.get("claim_id") in fragmented:
                by_branch.setdefault(row.get("branch"), []).append(row)
        candidates = [branch for branch, rows in sorted(by_branch.items())
                      if branch and branch != "main" and not any(r.get("claim_id") in projected for r in rows)]
        if not candidates:
            self.skipTest("no releasable active claim in the committed registry")
        report = rel.release(self.root, candidates[0], 42, SHA, AT)
        self.assertEqual(report["disposition"], "RELEASED")
        self.assertTrue(report["released"])

    def test_tombstoned_claim_is_not_released_again(self):
        path = add_claim(self.root, "feature/x")
        tomb = self.root / "data/session-work-claims.d/test-release-claim-terminal.json"
        tomb.write_text(json.dumps({"registry_fragment_type": "stegverse_session_work_claim_registry_fragment",
                                    "schema_version": "1.0.0", "repository": "StegVerse-Labs/Site", "claims": [{
                                        "claim_id": "TEST-RELEASE-CLAIM", "terminalization_override_of": "claim_fragment",
                                        "state": "RELEASED_COMPLETE", "pull_request": 7, "release_commit": "b" * 40,
                                        "claim_released_at": AT}]}), encoding="utf-8")
        original = path.read_text(encoding="utf-8")
        self.assertEqual(rel.release(self.root, "feature/x", 1, SHA, AT, validators=())["disposition"], "NO_ACTIVE_CLAIM_FOR_BRANCH")
        self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_unknown_branch_changes_nothing(self):
        before = {p: p.read_text(encoding="utf-8") for p in (self.root / "data").rglob("*.json")}
        self.assertEqual(rel.release(self.root, "no/such-branch", 1, SHA, AT)["disposition"], "NO_ACTIVE_CLAIM_FOR_BRANCH")
        self.assertEqual({p: p.read_text(encoding="utf-8") for p in (self.root / "data").rglob("*.json")}, before)

    def test_machine_owned_and_released_claims_are_not_touched(self):
        for state in ("MACHINE_OWNED", "RELEASED_COMPLETE"):
            with self.subTest(state=state):
                add_claim(self.root, "feature/x", state=state)
                self.assertEqual(rel.release(self.root, "feature/x", 1, SHA, AT, validators=())["released"], [])

    def test_manifest_fields_fail_closed(self):
        add_claim(self.root, "feature/x")
        for args, predicate in ((("main", 1, SHA, AT), "merged_branch_identity"), (("", 1, SHA, AT), "merged_branch_identity"),
                                (("feature/x", 0, SHA, AT), "pull_request_number"), (("feature/x", 1, "abc", AT), "merge_commit_sha"),
                                (("feature/x", 1, SHA, "yesterday"), "merged_at_utc")):
            with self.subTest(predicate=predicate):
                with self.assertRaises(rel.ReleaseRefused) as raised:
                    rel.release(self.root, *args, validators=())
                self.assertEqual(raised.exception.predicate, predicate)

    def test_claim_with_active_cosv_projection_is_refused(self):
        bundle = json.loads((self.root / "data/cosv/active-claim-projections.json").read_text(encoding="utf-8"))
        claim_id = bundle["projections"][0]["claim_id"]
        path = add_claim(self.root, "feature/x")
        fragment = json.loads(path.read_text(encoding="utf-8"))
        fragment["claims"][0]["claim_id"] = claim_id
        path.write_text(json.dumps(fragment), encoding="utf-8")
        original = path.read_text(encoding="utf-8")
        with self.assertRaises(rel.ReleaseRefused) as raised:
            rel.release(self.root, "feature/x", 1, SHA, AT, validators=())
        self.assertEqual(raised.exception.predicate, "active_cosv_projection_requires_atomic_terminalization")
        self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_failed_validation_restores_every_file(self):
        path = add_claim(self.root, "feature/x")
        index = self.root / "data/cosv/task-vector-index.json"
        originals = (path.read_text(encoding="utf-8"), index.read_text(encoding="utf-8"))
        failing = self.root / "scripts/always_fail.py"
        failing.write_text("raise SystemExit(1)\n", encoding="utf-8")
        with self.assertRaises(rel.ReleaseRefused) as raised:
            rel.release(self.root, "feature/x", 1, SHA, AT, validators=("scripts/always_fail.py",))
        self.assertEqual(raised.exception.predicate, "post_release_validation")
        self.assertEqual((path.read_text(encoding="utf-8"), index.read_text(encoding="utf-8")), originals)

    def test_cli_reports_fail_closed_without_changes(self):
        result = subprocess.run([sys.executable, str(self.root / "scripts/release_merged_session_claims.py"), "--root", str(self.root),
                                 "--branch", "main", "--pull-request", "1", "--merge-commit", SHA, "--merged-at", AT],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["failed_predicate"], "merged_branch_identity")


if __name__ == "__main__":
    unittest.main()
