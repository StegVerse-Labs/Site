"""Adversarial tests for the benchmark-to-canonical-task binding guard.

Each negative control mutates a deep copy of the real committed data and asserts the guard
rejects it. The first test is the defect this guard exists for: the exact dangling task id
that sat in two Stage 1 benchmarks while the Task Registry carried no such task.
"""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "binding", ROOT / "scripts/check_public_release_benchmark_task_binding.py")
binding = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(binding)

DATA = json.loads((ROOT / "data/economy/public-release-benchmarks.v1.json").read_text(encoding="utf-8"))
SNAP = json.loads((ROOT / "data/economy/canonical-task-registry-snapshot.v1.json").read_text(encoding="utf-8"))

DANGLING = "STEG-BROWSER-ECOSYSTEM-EPHEMERAL-001"


def check(data=None, snapshot=None):
    return binding.validate(copy.deepcopy(data if data is not None else DATA),
                            copy.deepcopy(snapshot if snapshot is not None else SNAP))


def benchmarks(data):
    return {b["id"]: b for s in data["stages"] for b in s["benchmarks"]}


def test_committed_projection_is_valid():
    assert check() == []


def test_the_dangling_task_id_is_gone_from_the_committed_file():
    assert DANGLING not in json.dumps(DATA)
    assert DANGLING not in SNAP["registered_task_ids"]


def test_regression_unregistered_task_in_prose_is_rejected():
    """The original defect: prose citing a task the registry does not carry."""
    d = copy.deepcopy(DATA)
    b = benchmarks(d)["S1_CHATGPT"]
    b["source"] = f"StegVerse-Labs/StegBrowser:{DANGLING}; existing WorkerCoordinator"
    errors = check(d)
    assert any(DANGLING in e and "unregistered" in e for e in errors), errors


def test_unregistered_bound_task_is_rejected():
    d = copy.deepcopy(DATA)
    benchmarks(d)["S1_CHATGPT"]["canonical_task_binding"]["task_id"] = "NO-SUCH-CANONICAL-TASK-001"
    assert any("binds unregistered canonical task" in e for e in check(d))


def test_disagreeing_with_the_registry_is_rejected():
    """Site may mirror the registry's assertion, never replace it."""
    d = copy.deepcopy(DATA)
    other = SNAP["registry_benchmark_bindings"]["S1_CLAUDE"]["task_id"]
    benchmarks(d)["S1_CHATGPT"]["canonical_task_binding"]["task_id"] = other
    errors = check(d)
    assert any("the registry asserts" in e for e in errors), errors


def test_dropping_a_registry_asserted_binding_is_rejected():
    d = copy.deepcopy(DATA)
    b = benchmarks(d)["S1_CHATGPT"]
    b["canonical_task_binding"] = None
    b["canonical_task_binding_pending_reason"] = "removed"
    assert any("Site records no binding" in e for e in check(d))


def test_missing_binding_key_is_rejected():
    d = copy.deepcopy(DATA)
    del benchmarks(d)["S2_CONSENT"]["canonical_task_binding"]
    assert any("does not declare canonical_task_binding" in e for e in check(d))


def test_unbound_without_reason_is_rejected():
    d = copy.deepcopy(DATA)
    del benchmarks(d)["S2_CONSENT"]["canonical_task_binding_pending_reason"]
    assert any("without a stated pending reason" in e for e in check(d))


def test_completion_without_an_identified_task_is_rejected():
    d = copy.deepcopy(DATA)
    benchmarks(d)["S2_CONSENT"]["status"] = "VERIFIED_COMPLETE"
    assert any("complete without an identified canonical task" in e for e in check(d))


def test_site_may_not_self_promote_to_registry_asserted():
    d = copy.deepcopy(DATA)
    benchmarks(d)["S1_NATIVE_KV"]["canonical_task_binding"]["provenance"] = binding.REGISTRY_ASSERTED
    assert any("no canonical task record in the snapshot names this benchmark" in e for e in check(d))


def test_registry_asserted_binding_must_not_be_downgraded():
    d = copy.deepcopy(DATA)
    benchmarks(d)["S1_CHATGPT"]["canonical_task_binding"]["provenance"] = binding.SITE_ASSERTED
    assert any("provenance must be REGISTRY_ASSERTED" in e for e in check(d))


def test_one_task_may_not_serve_two_benchmarks():
    d = copy.deepcopy(DATA)
    shared = benchmarks(d)["S1_NATIVE_KV"]["canonical_task_binding"]
    target = benchmarks(d)["S1_MYKV_AI"]
    target["canonical_task_binding"] = copy.deepcopy(shared)
    target.pop("canonical_task_binding_pending_reason", None)
    assert any("bound to multiple benchmarks" in e for e in check(d))


@pytest.mark.parametrize("field,value", [
    ("binding_authority", "AUTHORIZING"),
    ("grants_completion", True),
    ("cosv_status", "EMITTED"),
])
def test_binding_may_not_claim_authority(field, value):
    d = copy.deepcopy(DATA)
    benchmarks(d)["S1_CHATGPT"]["canonical_task_binding"][field] = value
    assert check(d), f"mutating {field} to {value!r} was accepted"


@pytest.mark.parametrize("field", [
    "every_benchmark_declares_binding", "cited_task_must_exist_in_snapshot",
    "registry_assertion_wins_over_site",
])
def test_contract_invariants_must_hold(field):
    d = copy.deepcopy(DATA)
    d["canonical_task_binding_contract"][field] = False
    assert any(field in e for e in check(d))


@pytest.mark.parametrize("field", ["binding_grants_completion", "binding_emits_cosv"])
def test_contract_denials_must_hold(field):
    d = copy.deepcopy(DATA)
    d["canonical_task_binding_contract"][field] = True
    assert any(field in e for e in check(d))


def test_snapshot_must_stay_non_authorizing():
    s = copy.deepcopy(SNAP)
    s["authority"] = "AUTHORIZING"
    assert any("non-authorizing" in e for e in check(None, s))


def test_snapshot_must_record_its_provenance():
    for key in ("repository", "commit", "registry_generation"):
        s = copy.deepcopy(SNAP)
        s["observed_from"][key] = None
        assert any(f"observed_from.{key}" in e for e in check(None, s)), key


def test_registry_binding_for_unknown_benchmark_is_rejected():
    s = copy.deepcopy(SNAP)
    s["registry_benchmark_bindings"]["S9_NOT_A_BENCHMARK"] = {"task_id": SNAP["registered_task_ids"][0]}
    assert any("unknown benchmark S9_NOT_A_BENCHMARK" in e for e in check(None, s))


def test_stale_snapshot_surfaces_as_failure_not_silent_pass():
    """Dropping a task the projection binds must fail, so snapshot staleness is visible."""
    s = copy.deepcopy(SNAP)
    bound = benchmarks(DATA)["S1_CHATGPT"]["canonical_task_binding"]["task_id"]
    s["registered_task_ids"] = [t for t in s["registered_task_ids"] if t != bound]
    assert any("unregistered" in e for e in check(None, s))


def test_existing_roadmap_validator_still_passes():
    """The binding fields must not break the projection validator that shares this file."""
    spec = importlib.util.spec_from_file_location(
        "roadmap", ROOT / "scripts/check_economic_roadmap_projection.py")
    roadmap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(roadmap)
    assert roadmap.validate(copy.deepcopy(DATA)) == []
