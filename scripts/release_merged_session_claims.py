#!/usr/bin/env python3
"""Release the active pre-work claims of a merged branch, deterministically.

The merge is the manifest: the caller passes the merged branch, pull request number,
merge commit and merge time exactly as the merge event records them. For every active
claim fragment row bound to that branch, only the release fields change (state,
pull_request, release_commit, claim_released_at), which is the shape the handoff
orchestrator accepts as terminalization-only maintenance. The COSV active-claim counts
are recomputed from the resulting registry, never hand-edited.

The script refuses (FAIL_CLOSED, exact predicate, no files changed) when a claim also
owns an active COSV projection, because retiring that projection is an atomic
terminalization this writer does not perform. After writing, the existing validators
run; if either fails, every file is restored.

It performs no network call, reads no credential and grants no authority. Per the
Site boundary, generated-state mutation runs on the StegVerse resident worker or a
session; GitHub-hosted workflows only validate the resulting change.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELEASABLE_STATES = {"CLAIMED", "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION", "CLAIMED_FOR_INTEGRATION"}
RELEASE_STATE = "RELEASED_COMPLETE"
_SHA = re.compile(r"^[0-9a-f]{40}$")
_TIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
VALIDATORS = ("scripts/check_session_work_claims.py", "scripts/check_cosv_task_projection.py")


class ReleaseRefused(Exception):
    def __init__(self, predicate: str, detail: str = "") -> None:
        super().__init__(predicate)
        self.predicate = predicate
        self.detail = detail


def released_row(claim: dict[str, Any], pull_request: int, merge_commit: str, merged_at: str) -> dict[str, Any]:
    """Return the claim with release fields placed after ``state``; nothing else changes."""
    release = {"state": RELEASE_STATE, "pull_request": pull_request,
               "release_commit": merge_commit, "claim_released_at": merged_at}
    out: dict[str, Any] = {}
    for key, value in claim.items():
        if key in ("pull_request", "release_commit", "claim_released_at"):
            continue
        if key == "state":
            out.update(release)
            continue
        out[key] = value
    return out


def active_projection_claim_ids(root: Path) -> set[str]:
    index = json.loads((root / "data/cosv/task-vector-index.json").read_text(encoding="utf-8"))
    bundle = json.loads((root / "data/cosv/active-claim-projections.json").read_text(encoding="utf-8"))
    owned = {row.get("claim_id") for row in bundle.get("projections", [])}
    owned |= {row.get("claim_id") for row in index.get("tasks", [])
              if row.get("binding_mode") != "HISTORICAL_RELEASED_SOURCE_CLAIM" and row.get("claim_id")}
    return {claim_id for claim_id in owned if isinstance(claim_id, str)}


def plan_release(root: Path, branch: str, pull_request: int, merge_commit: str, merged_at: str) -> dict[Path, dict[str, Any]]:
    """Return {fragment path: new fragment} for every active claim bound to ``branch``."""
    if not branch or branch == "main":
        raise ReleaseRefused("merged_branch_identity")
    if not isinstance(pull_request, int) or pull_request <= 0:
        raise ReleaseRefused("pull_request_number")
    if not _SHA.match(merge_commit):
        raise ReleaseRefused("merge_commit_sha")
    if not _TIME.match(merged_at):
        raise ReleaseRefused("merged_at_utc")
    projected = active_projection_claim_ids(root)
    # A fragment row can still read active while a tombstone has already terminalized it.
    live = {claim.get("claim_id") for claim in effective_active_claims(root)}
    planned: dict[Path, dict[str, Any]] = {}
    for path in sorted((root / "data/session-work-claims.d").glob("*.json")):
        fragment = json.loads(path.read_text(encoding="utf-8"))
        rows = fragment.get("claims")
        if not isinstance(rows, list):
            continue
        changed = False
        new_rows = []
        for row in rows:
            if (isinstance(row, dict) and row.get("branch") == branch
                    and row.get("state") in RELEASABLE_STATES and "terminalization_override_of" not in row
                    and row.get("claim_id") in live):
                if row.get("claim_id") in projected:
                    raise ReleaseRefused("active_cosv_projection_requires_atomic_terminalization", str(row.get("claim_id")))
                new_rows.append(released_row(row, pull_request, merge_commit, merged_at))
                changed = True
            else:
                new_rows.append(row)
        if changed:
            planned[path] = {**fragment, "claims": new_rows}
    return planned


def effective_active_claims(root: Path) -> list[dict[str, Any]]:
    """Active claims after canonical rows, fragments and terminalization tombstones merge."""
    import importlib

    if str(root / "scripts") not in sys.path:
        sys.path.insert(0, str(root / "scripts"))
    claims_mod = importlib.reload(importlib.import_module("check_session_work_claims"))
    claims_mod.ROOT = root
    claims_mod.REGISTRY = root / "data" / "session-work-claims.json"
    claims_mod.REGISTRY_FRAGMENT_ROOT = root / "data" / "session-work-claims.d"
    return claims_mod.active_claims(claims_mod.load_registry())


def recount_coverage(root: Path) -> dict[str, Any]:
    """Recompute the COSV active-claim counts from the registry as it now stands."""
    effective = effective_active_claims(root)
    index_path = root / "data/cosv/task-vector-index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    active_ids = {str(claim["task_id"]) for claim in effective}
    unindexed = active_ids - {row["task_id"] for row in index["tasks"]}
    cov = index["coverage"]
    cov["repository_effective_active_claims_observed"] = len(effective)
    cov["repository_effective_active_task_ids_observed"] = len(active_ids)
    cov["repository_unindexed_active_task_ids_observed"] = len(unindexed)
    cov["repository_active_claim_denominator_nonzero"] = bool(effective)
    cov["repository_unindexed_active_claim_tasks_present"] = bool(unindexed)
    cov["repository_vector_present_blocker"] = "UNINDEXED_ACTIVE_CLAIM_TASKS_REMAIN" if unindexed else None
    cov["repository_active_task_surface_audit_complete"] = not unindexed
    cov["repository_vector_present_claimed"] = not unindexed
    return index


def _dump(value: Any) -> str:
    return json.dumps(value, indent=2) + "\n"


def release(root: Path, branch: str, pull_request: int, merge_commit: str, merged_at: str,
            validators: tuple[str, ...] = VALIDATORS) -> dict[str, Any]:
    planned = plan_release(root, branch, pull_request, merge_commit, merged_at)
    if not planned:
        return {"disposition": "NO_ACTIVE_CLAIM_FOR_BRANCH", "branch": branch, "released": []}
    index_path = root / "data/cosv/task-vector-index.json"
    originals = {path: path.read_text(encoding="utf-8") for path in [*planned, index_path]}
    try:
        for path, fragment in planned.items():
            path.write_text(_dump(fragment), encoding="utf-8")
        index_path.write_text(_dump(recount_coverage(root)), encoding="utf-8")
        for validator in validators:
            result = subprocess.run([sys.executable, str(root / validator)], cwd=root, capture_output=True, text=True)
            if result.returncode != 0:
                raise ReleaseRefused("post_release_validation", f"{validator}: {(result.stdout + result.stderr).strip()[-400:]}")
    except Exception:
        for path, text in originals.items():
            path.write_text(text, encoding="utf-8")
        raise
    released = [row["claim_id"] for fragment in planned.values() for row in fragment["claims"]
                if row.get("state") == RELEASE_STATE and row.get("pull_request") == pull_request
                and row.get("release_commit") == merge_commit]
    return {"disposition": "RELEASED", "branch": branch, "pull_request": pull_request,
            "release_commit": merge_commit, "released": sorted(released),
            "changed_paths": sorted(str(path.relative_to(root)) for path in planned) + ["data/cosv/task-vector-index.json"],
            "authority_effect": "NONE"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--branch", required=True, help="merged head branch, as the merge event records it")
    parser.add_argument("--pull-request", required=True, type=int)
    parser.add_argument("--merge-commit", required=True, help="full 40-hex merge commit SHA")
    parser.add_argument("--merged-at", required=True, help="merge time, UTC, YYYY-MM-DDTHH:MM:SSZ")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        report = release(args.root.resolve(), args.branch, args.pull_request, args.merge_commit, args.merged_at)
    except ReleaseRefused as refusal:
        print(json.dumps({"disposition": "FAIL_CLOSED", "failed_predicate": refusal.predicate,
                          "detail": refusal.detail, "files_changed": False}, indent=2))
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
