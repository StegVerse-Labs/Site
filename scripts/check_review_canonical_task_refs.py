#!/usr/bin/env python3
"""Validate that a review document cites canonical tasks the registry actually carries.

A review that anchors on a task id nobody registered, or asserts ACTIVE for a task the
registry has superseded, reads as fact and is not checkable. Both happened in the first draft
of the ephemeral-browser review: one anchor did not exist at all, a second was SUPERSEDED with
a RETIRED continuation, and a third had no record to carry the COSV attributed to it.

Scanning prose for id-shaped tokens does not work here. Measured across 571 Site documents, a
canonical-id regex matches 338 distinct tokens of which only 39 are registered -- the rest are
section labels, cipher names and internal enumerations (AES-256, AI-001, COMP-003). Worse, an
existence check cannot catch the defect that matters: an id that exists but is not in the state
claimed. So a review declares its citations, and the declaration is checked against an observed
snapshot of the Task Registry, including coordination state.

Deterministic and offline: the snapshot is committed, so it going stale is itself a failure
rather than a silent pass. This checker cannot create, attest or verify a receipt, cannot emit
a COSV, and observing a citation here grants no execution authority.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/reviews/ephemeral-browser-llm-ecosystem-chat.v1.json"
SNAPSHOT = ROOT / "data/economy/canonical-task-registry-snapshot.v1.json"

SCHEMA = "stegverse.site.review-canonical-task-refs/v1"
SNAPSHOT_SCHEMA = "stegverse.site.canonical-task-registry-snapshot/v1"

# States whose task is no longer a live owner; citing one must name its continuation.
ENDED = {"SUPERSEDED", "RETIRED", "CLOSED", "COMPLETE", "COMPLETED", "INACTIVE"}


def validate(refs: dict, snapshot: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    if refs.get("schema") != SCHEMA:
        errors.append("wrong reference-block schema")
    if refs.get("authority") != "OBSERVED_NOT_AUTHORIZING":
        errors.append("reference block must remain observed and non-authorizing")
    for key in ("grants_completion", "emits_cosv"):
        if refs.get(key) is not False:
            errors.append(f"reference block must deny {key}")
    if snapshot.get("schema") != SNAPSHOT_SCHEMA:
        errors.append("wrong registry snapshot schema")
    if snapshot.get("authority") != "OBSERVED_NOT_AUTHORIZING":
        errors.append("registry snapshot must remain observed and non-authorizing")
    if refs.get("registry_snapshot_ref") != "data/economy/canonical-task-registry-snapshot.v1.json":
        errors.append("reference block must reference the committed registry snapshot")

    states = snapshot.get("task_states")
    registered = set(snapshot.get("registered_task_ids") or [])
    if not isinstance(states, dict) or not states:
        errors.append("registry snapshot carries no task states")
        return errors
    observed = snapshot.get("observed_from") or {}
    for key in ("repository", "commit", "registry_generation"):
        if not observed.get(key):
            errors.append(f"registry snapshot is missing observed_from.{key}")

    doc_path = refs.get("review_document")
    if not isinstance(doc_path, str) or not doc_path:
        errors.append("reference block names no review document")
        return errors
    doc_file = root / doc_path
    if not doc_file.is_file():
        errors.append(f"review document not found: {doc_path}")
        return errors
    doc = doc_file.read_text(encoding="utf-8")

    cited = refs.get("cited_tasks")
    if not isinstance(cited, list) or not cited:
        errors.append("reference block cites no tasks")
        return errors

    seen: set[str] = set()
    for entry in cited:
        tid = entry.get("task_id")
        if not isinstance(tid, str) or not tid:
            errors.append("cited task without a task_id")
            continue
        if tid in seen:
            errors.append(f"{tid}: cited twice")
        seen.add(tid)

        if tid not in registered or tid not in states:
            errors.append(f"{tid}: cited but not in the registry snapshot")
            continue
        actual = states[tid]

        asserted = entry.get("asserted_state")
        if asserted != actual.get("coordination_state"):
            errors.append(f"{tid}: review asserts {asserted!r} but the registry holds "
                          f"{actual.get('coordination_state')!r}")

        vec = entry.get("cosv_task_vector")
        if vec is not None and vec != actual.get("cosv_task_vector"):
            errors.append(f"{tid}: review attributes COSV {vec} but the registry holds "
                          f"{actual.get('cosv_task_vector')}")

        # A task that has ended is not a live owner; the review must name its continuation
        # so the dead anchor cannot be cited as if it were current.
        if actual.get("coordination_state") in ENDED:
            declared = entry.get("continuation_task_id")
            expected = actual.get("continuation_task_id")
            if expected and declared != expected:
                errors.append(f"{tid}: state {actual.get('coordination_state')} continues under "
                              f"{expected}, which the review does not name")

        # The block must not drift from the prose it describes.
        if tid not in doc:
            errors.append(f"{tid}: declared in the reference block but absent from {doc_path}")

    # An id recorded as unregistered must still be unregistered; if it lands in the registry,
    # the review is out of date and must be revisited rather than quietly staying right.
    for entry in refs.get("cited_but_unregistered") or []:
        cid = entry.get("cited_id")
        if not isinstance(cid, str) or not cid:
            errors.append("unregistered citation without an id")
            continue
        if cid in registered:
            errors.append(f"{cid}: recorded as NOT_IN_REGISTRY but the snapshot now carries it")
        if entry.get("disposition") != "NOT_IN_REGISTRY":
            errors.append(f"{cid}: invalid disposition {entry.get('disposition')!r}")
        if not str(entry.get("action") or "").strip():
            errors.append(f"{cid}: recorded without a stated action")
        if cid not in doc:
            errors.append(f"{cid}: recorded in the reference block but absent from {doc_path}")

    return errors


def main() -> int:
    refs_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    snapshot_path = Path(sys.argv[2]) if len(sys.argv) > 2 else SNAPSHOT
    errors = validate(
        json.loads(refs_path.read_text(encoding="utf-8")),
        json.loads(snapshot_path.read_text(encoding="utf-8")),
    )
    print(json.dumps({
        "refs": str(refs_path),
        "snapshot": str(snapshot_path),
        "valid": not errors,
        "errors": errors,
        "authority_effect": "NONE_SOURCE_VALIDATION_ONLY",
    }, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
