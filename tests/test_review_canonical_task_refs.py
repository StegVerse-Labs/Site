"""Adversarial tests for the review canonical-task reference guard.

The first three are the three defects the first draft of the ephemeral-browser review actually
carried. Each mutates a deep copy of the real committed data.
"""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "reviewrefs", ROOT / "scripts/check_review_canonical_task_refs.py")
reviewrefs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reviewrefs)

REFS = json.loads((ROOT / "data/reviews/ephemeral-browser-llm-ecosystem-chat.v1.json").read_text(encoding="utf-8"))
SNAP = json.loads((ROOT / "data/economy/canonical-task-registry-snapshot.v1.json").read_text(encoding="utf-8"))

GHOST = "STEG-BROWSER-ECOSYSTEM-EPHEMERAL-001"
SUPERSEDED = "STEG-BROWSER-EPHEMERAL-RUNTIME-BINDING-001"
NO_RECORD = "SHWP-ECOSYSTEM-CHAT-INFERENCE-001"


def check(refs=None, snapshot=None):
    return reviewrefs.validate(copy.deepcopy(refs if refs is not None else REFS),
                               copy.deepcopy(snapshot if snapshot is not None else SNAP),
                               ROOT)


def cited(refs, task_id):
    return next(e for e in refs["cited_tasks"] if e["task_id"] == task_id)


def test_committed_review_is_valid():
    assert check() == []


def test_regression_citing_a_task_the_registry_does_not_carry():
    """First draft row 1: an anchor nobody registered."""
    r = copy.deepcopy(REFS)
    r["cited_tasks"].append({"task_id": GHOST, "asserted_state": "ACTIVE",
                             "role_in_review": "lease-bounded browser contract"})
    errors = check(r)
    assert any(GHOST in e and "not in the registry snapshot" in e for e in errors), errors


def test_regression_asserting_active_for_a_superseded_task():
    """First draft row 2: the state claim, which an existence check would have passed."""
    r = copy.deepcopy(REFS)
    cited(r, SUPERSEDED)["asserted_state"] = "ACTIVE"
    errors = check(r)
    assert any("asserts 'ACTIVE'" in e and "SUPERSEDED" in e for e in errors), errors


def test_regression_attributing_a_cosv_to_a_task_with_no_record():
    """First draft row 4: COSV 50000000100000 attributed to a task that has no record."""
    r = copy.deepcopy(REFS)
    r["cited_tasks"].append({"task_id": NO_RECORD, "asserted_state": "ACTIVE",
                             "cosv_task_vector": "50000000100000",
                             "role_in_review": "governed sovereign inference"})
    assert any(NO_RECORD in e and "not in the registry snapshot" in e for e in check(r))


def test_wrong_cosv_on_a_registered_task_is_rejected():
    r = copy.deepcopy(REFS)
    e = cited(r, "KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001")
    e["cosv_task_vector"] = "99999999999999"
    assert any("attributes COSV 99999999999999" in x for x in check(r))


def test_ended_task_must_name_its_continuation():
    r = copy.deepcopy(REFS)
    cited(r, SUPERSEDED).pop("continuation_task_id", None)
    errors = check(r)
    assert any("continues under" in e for e in errors), errors


def test_continuation_must_match_the_registry():
    r = copy.deepcopy(REFS)
    cited(r, SUPERSEDED)["continuation_task_id"] = "SOME-OTHER-TASK-001"
    assert any("continues under" in e for e in check(r))


def test_reference_block_may_not_drift_from_the_document():
    """A citation the prose does not make is not a citation."""
    r = copy.deepcopy(REFS)
    r["cited_tasks"].append({"task_id": "ORGANIZATION-BATCH-CUSTODY-REPLAY-001",
                             "asserted_state": "ACTIVE", "role_in_review": "duplicate"})
    assert any("cited twice" in e for e in check(r))


def test_task_declared_but_absent_from_the_document_is_rejected():
    r = copy.deepcopy(REFS)
    absent = next(t for t in SNAP["registered_task_ids"]
                  if t not in (ROOT / REFS["review_document"]).read_text(encoding="utf-8"))
    r["cited_tasks"].append({"task_id": absent,
                             "asserted_state": SNAP["task_states"][absent]["coordination_state"],
                             "role_in_review": "never mentioned in the prose"})
    assert any("absent from" in e for e in check(r))


def test_unregistered_id_that_becomes_registered_is_rejected():
    """If someone registers the ghost id, the review must be revisited, not silently right."""
    s = copy.deepcopy(SNAP)
    s["registered_task_ids"] = sorted(s["registered_task_ids"] + [GHOST])
    s["task_states"][GHOST] = {"coordination_state": "ACTIVE", "cosv_task_vector": None,
                               "continuation_task_id": None, "supersession_reason": None}
    assert any("snapshot now carries it" in e for e in check(None, s))


@pytest.mark.parametrize("field", ["disposition", "action"])
def test_unregistered_entry_needs_disposition_and_action(field):
    r = copy.deepcopy(REFS)
    r["cited_but_unregistered"][0][field] = "" if field == "action" else "SOMETHING_ELSE"
    assert check(r)


def test_missing_review_document_is_rejected():
    r = copy.deepcopy(REFS)
    r["review_document"] = "docs/NO_SUCH_REVIEW.md"
    assert any("review document not found" in e for e in check(r))


@pytest.mark.parametrize("field,value", [
    ("authority", "AUTHORIZING"),
    ("grants_completion", True),
    ("emits_cosv", True),
])
def test_reference_block_may_not_claim_authority(field, value):
    r = copy.deepcopy(REFS)
    r[field] = value
    assert check(r), f"mutating {field} to {value!r} was accepted"


def test_snapshot_must_stay_non_authorizing():
    s = copy.deepcopy(SNAP)
    s["authority"] = "AUTHORIZING"
    assert any("non-authorizing" in e for e in check(None, s))


def test_snapshot_must_record_its_provenance():
    for key in ("repository", "commit", "registry_generation"):
        s = copy.deepcopy(SNAP)
        s["observed_from"][key] = None
        assert any(f"observed_from.{key}" in e for e in check(None, s)), key


def test_stale_snapshot_surfaces_as_failure():
    """Dropping a cited task must fail, so snapshot staleness is visible."""
    s = copy.deepcopy(SNAP)
    tid = REFS["cited_tasks"][0]["task_id"]
    s["registered_task_ids"] = [t for t in s["registered_task_ids"] if t != tid]
    del s["task_states"][tid]
    assert any("not in the registry snapshot" in e for e in check(None, s))


def test_benchmark_binding_guard_still_passes_on_the_extended_snapshot():
    """The snapshot gained task_states; the guard that already reads it must be unaffected."""
    spec = importlib.util.spec_from_file_location(
        "binding", ROOT / "scripts/check_public_release_benchmark_task_binding.py")
    binding = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(binding)
    data = json.loads((ROOT / "data/economy/public-release-benchmarks.v1.json").read_text(encoding="utf-8"))
    assert binding.validate(data, copy.deepcopy(SNAP)) == []
