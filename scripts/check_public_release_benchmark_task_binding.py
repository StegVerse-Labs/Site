#!/usr/bin/env python3
"""Validate that every public release benchmark binds to a canonical task that actually exists.

`authority_boundary.required_for_complete` on the public roadmap already demands
`correct_benchmark_identity`, but nothing checked it: a benchmark could cite a canonical task
id the Task Registry does not carry, and source validation would still pass. That is how
`STEG-BROWSER-ECOSYSTEM-EPHEMERAL-001` came to sit in two Stage 1 benchmarks while the
registry carried no such task.

This checker is CI-safe and offline. It reads a committed, explicitly non-authorizing
snapshot of the upstream Task Registry rather than reaching across repositories, so the
snapshot going stale is itself visible as a failure rather than as a silent pass. It cannot
create, attest or verify a Master Records receipt, cannot emit a COSV, and observing a
binding here never promotes a benchmark or grants execution authority.

Where a canonical task record names a benchmark in its own registration block, the registry's
statement wins: Site mirrors that binding and may not originate a different one.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/economy/public-release-benchmarks.v1.json"
SNAPSHOT = ROOT / "data/economy/canonical-task-registry-snapshot.v1.json"

BENCHMARK_SCHEMA = "stegverse.public-economic-roadmap/v1"
SNAPSHOT_SCHEMA = "stegverse.site.canonical-task-registry-snapshot/v1"

REGISTRY_ASSERTED = "REGISTRY_ASSERTED"
SITE_ASSERTED = "SITE_ASSERTED_REGISTERED_TASK"
PROVENANCE = {REGISTRY_ASSERTED, SITE_ASSERTED}

# Canonical task ids are upper-case segments ending in a three-digit ordinal. Deliberately
# does not match dated claim ids (…-20260922) or lower-case transport identifiers.
TASK_ID = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{3}\b")


def validate(data: dict, snapshot: dict) -> list[str]:
    errors: list[str] = []

    if data.get("schema") != BENCHMARK_SCHEMA:
        errors.append("wrong benchmark schema")
    if snapshot.get("schema") != SNAPSHOT_SCHEMA:
        errors.append("wrong registry snapshot schema")
    if snapshot.get("authority") != "OBSERVED_NOT_AUTHORIZING":
        errors.append("registry snapshot must remain observed and non-authorizing")

    registered = snapshot.get("registered_task_ids")
    if not isinstance(registered, list) or not registered:
        errors.append("registry snapshot carries no registered task ids")
        return errors
    registered_set = set(registered)

    observed = snapshot.get("observed_from") or {}
    for key in ("repository", "commit", "registry_generation"):
        if not observed.get(key):
            errors.append(f"registry snapshot is missing observed_from.{key}")

    registry_bindings = snapshot.get("registry_benchmark_bindings")
    if not isinstance(registry_bindings, dict):
        errors.append("registry snapshot is missing registry_benchmark_bindings")
        registry_bindings = {}

    contract = data.get("canonical_task_binding_contract") or {}
    for key in ("every_benchmark_declares_binding", "cited_task_must_exist_in_snapshot",
                "registry_assertion_wins_over_site"):
        if contract.get(key) is not True:
            errors.append(f"binding contract must assert {key}")
    for key in ("binding_grants_completion", "binding_emits_cosv"):
        if contract.get(key) is not False:
            errors.append(f"binding contract must deny {key}")
    if contract.get("registry_snapshot_ref") != "data/economy/canonical-task-registry-snapshot.v1.json":
        errors.append("binding contract must reference the committed registry snapshot")

    stages = data.get("stages")
    if not isinstance(stages, list):
        errors.append("stages missing")
        return errors

    bound_by_task: dict[str, list[str]] = {}
    seen: set[str] = set()

    for stage in stages:
        for b in stage.get("benchmarks", []):
            bid = b.get("id")
            seen.add(bid)

            # Any canonical-task-shaped id named in free prose must also be registered,
            # so prose cannot smuggle in a task the registry does not carry.
            for token in TASK_ID.findall(b.get("source") or ""):
                if token not in registered_set:
                    errors.append(f"{bid}: source cites unregistered canonical task {token}")

            if "canonical_task_binding" not in b:
                errors.append(f"{bid}: does not declare canonical_task_binding")
                continue
            binding = b["canonical_task_binding"]
            status = b.get("status")

            if binding is None:
                reason = b.get("canonical_task_binding_pending_reason")
                if not isinstance(reason, str) or not reason.strip():
                    errors.append(f"{bid}: unbound without a stated pending reason")
                if status == "VERIFIED_COMPLETE":
                    errors.append(f"{bid}: complete without an identified canonical task")
                if bid in registry_bindings:
                    errors.append(
                        f"{bid}: the registry names {registry_bindings[bid].get('task_id')} "
                        "for this benchmark but Site records no binding")
                continue

            if not isinstance(binding, dict):
                errors.append(f"{bid}: canonical_task_binding must be an object or null")
                continue

            task_id = binding.get("task_id")
            if not isinstance(task_id, str) or not task_id.strip():
                errors.append(f"{bid}: binding has no task_id")
                continue
            if task_id not in registered_set:
                errors.append(f"{bid}: binds unregistered canonical task {task_id}")
            bound_by_task.setdefault(task_id, []).append(bid)

            provenance = binding.get("provenance")
            if provenance not in PROVENANCE:
                errors.append(f"{bid}: invalid binding provenance {provenance!r}")

            if binding.get("binding_authority") != "OBSERVED_NOT_AUTHORIZING":
                errors.append(f"{bid}: binding must stay observed and non-authorizing")
            if binding.get("grants_completion") is not False:
                errors.append(f"{bid}: a binding may never grant completion")
            if binding.get("cosv_status") != "NOT_YET_EMITTED":
                errors.append(f"{bid}: binding may not claim an emitted COSV")

            asserted = registry_bindings.get(bid)
            if asserted:
                if task_id != asserted.get("task_id"):
                    errors.append(
                        f"{bid}: the registry asserts {asserted.get('task_id')} but Site binds {task_id}")
                if provenance != REGISTRY_ASSERTED:
                    errors.append(f"{bid}: registry asserts this binding, so provenance must be "
                                  f"{REGISTRY_ASSERTED}")
            elif provenance == REGISTRY_ASSERTED:
                errors.append(f"{bid}: claims {REGISTRY_ASSERTED} but no canonical task record in the "
                              "snapshot names this benchmark")

    # A registry-asserted binding for a benchmark this projection does not carry is drift too.
    for bid in registry_bindings:
        if bid not in seen:
            errors.append(f"registry asserts a binding for unknown benchmark {bid}")

    for task_id, bids in sorted(bound_by_task.items()):
        if len(bids) > 1:
            errors.append(f"{task_id} is bound to multiple benchmarks: {sorted(bids)}")

    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    snapshot_path = Path(sys.argv[2]) if len(sys.argv) > 2 else SNAPSHOT
    errors = validate(
        json.loads(path.read_text(encoding="utf-8")),
        json.loads(snapshot_path.read_text(encoding="utf-8")),
    )
    print(json.dumps({
        "path": str(path),
        "snapshot": str(snapshot_path),
        "valid": not errors,
        "errors": errors,
        "authority_effect": "NONE_SOURCE_VALIDATION_ONLY",
    }, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
