#!/usr/bin/env python3
"""Read-only, evidence-classified subgoal projection for the 16 economic roadmap benchmarks.

The projection never grants roadmap completion. Supplied evidence is classified per
acceptance predicate; only Master Records-verified evidence arriving through the
Publisher-governed public-safe projection, with exact benchmark identity, RECORDED
state, reconstruction PASS, required-evidence PASS and receipt digest equality, can
satisfy a predicate. Source, CI, merge, issue-closure, runtime-observed and synthetic
evidence stay outstanding. Even a fully satisfied benchmark is only ELIGIBLE for the
Publisher's governed review; this script never emits VERIFIED_COMPLETE.

The ``source`` string inside an evidence document is self-declared and proves nothing
about provenance. Unless the caller injects a ``provenance_verifier`` bound to
authenticated Publisher custody and organization receipts, otherwise-valid evidence
stays OBSERVED_UNAUTHENTICATED_PROVENANCE and cannot satisfy any predicate. The CLI
has no verifier, so it can never mark a benchmark eligible.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/economy/public-release-benchmarks.v1.json"
REQUIRED = (
    "master_records_state_RECORDED", "reconstruction_PASS",
    "required_evidence_validation_PASS", "exact_receipt_digest_equality",
    "correct_benchmark_identity", "governed_publication_closure",
)
EVIDENCE_SCHEMA = "stegverse.economic-roadmap-evidence/v1"
GOVERNED_EVIDENCE_SOURCE = "PUBLISHER_GOVERNED_PROJECTION"
AUTHORITATIVE_CLASS = "MASTER_RECORDS_VERIFIED"
NON_AUTHORITATIVE_CLASSES = {
    "SOURCE_VALIDATED", "CI_VALIDATED", "PR_MERGED", "ISSUE_CLOSED",
    "SYNTHETIC_FIXTURE", "RUNTIME_OBSERVED",
}
NON_ALLOW = {"DENY", "FAIL", "FAIL_CLOSED"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _authoritative_failure(benchmark_id: str, entry: dict, evidence_source: str | None) -> str | None:
    """Return the first failed closure predicate for MASTER_RECORDS_VERIFIED evidence."""
    if evidence_source != GOVERNED_EVIDENCE_SOURCE:
        return "evidence_not_from_publisher_governed_projection"
    if entry.get("synthetic") is not False:
        return "evidence_not_declared_non_synthetic"
    if entry.get("benchmark_id") != benchmark_id:
        return "correct_benchmark_identity"
    if entry.get("master_records_state") != "RECORDED":
        return "master_records_state_RECORDED"
    if entry.get("reconstruction_status") != "PASS":
        return "reconstruction_PASS"
    if entry.get("required_evidence_validation_status") != "PASS":
        return "required_evidence_validation_PASS"
    receipt = entry.get("receipt_sha256")
    if not isinstance(receipt, str) or not SHA256.match(receipt) or receipt != entry.get("reconstructed_receipt_sha256"):
        return "exact_receipt_digest_equality"
    if not isinstance(entry.get("evidence_ref"), str) or not entry["evidence_ref"].strip():
        return "evidence_ref_missing"
    return None


def classify(benchmark_id: str, predicate: str, entry, evidence_source: str | None,
             provenance: str = "SELF_DECLARED_UNAUTHENTICATED") -> dict:
    row = {"predicate": predicate, "status": "UNKNOWN_NOT_AUTHENTICALLY_OBSERVED",
           "evidence_class": None, "evidence_ref": None, "failed_predicate": None}
    if entry is None:
        return row
    if not isinstance(entry, dict):
        return {**row, "status": "FAILED", "failed_predicate": "malformed_evidence_entry"}
    row["evidence_class"] = entry.get("evidence_class")
    row["evidence_ref"] = entry.get("evidence_ref")
    if entry.get("disposition") in NON_ALLOW:
        return {**row, "status": "FAILED", "failed_predicate": entry.get("failed_predicate") or predicate}
    if row["evidence_class"] in NON_AUTHORITATIVE_CLASSES:
        return {**row, "status": "OBSERVED_NOT_AUTHORITATIVE"}
    if row["evidence_class"] != AUTHORITATIVE_CLASS:
        return {**row, "status": "FAILED", "failed_predicate": "unknown_evidence_class"}
    failure = _authoritative_failure(benchmark_id, entry, evidence_source)
    if failure:
        return {**row, "status": "FAILED", "failed_predicate": failure}
    if provenance == "VERIFIER_REJECTED":
        return {**row, "status": "FAILED", "failed_predicate": "publisher_provenance_unauthenticated"}
    if provenance != "AUTHENTICATED_BY_INJECTED_VERIFIER":
        return {**row, "status": "OBSERVED_UNAUTHENTICATED_PROVENANCE"}
    return {**row, "status": "SATISFIED"}


def _next_repair(benchmark_id: str, task: str | None, failed: list[dict], outstanding: list[str]) -> str:
    if failed:
        first = failed[0]
        return f"Repair failed predicate {first['predicate']} ({first['failed_predicate']}) at its canonical owner"
    if task is None:
        return f"Register a canonical Task Registry binding for {benchmark_id}; the Site cannot originate it"
    if outstanding:
        return (f"Obtain {outstanding[0]} through canonical owner {task} and the "
                "Publisher-governed public-safe projection")
    return "Submit exact receipt digests for Publisher governed review; Site display cannot award completion"


def project(data: dict, evidence: dict | None = None,
            provenance_verifier: Callable[[dict], bool] | None = None) -> dict:
    """Return a conservative, evidence-classified projection; never infer runtime proof."""
    boundary = data.get("authority_boundary") or {}
    declared = boundary.get("required_for_complete") or []
    missing = [p for p in REQUIRED if p not in declared]
    if missing:
        raise ValueError(f"roadmap source drops completion invariants: {missing}")
    if evidence is not None and not isinstance(evidence, dict):
        raise ValueError("malformed evidence document")
    evidence = evidence or {}
    if evidence and evidence.get("schema") != EVIDENCE_SCHEMA:
        raise ValueError("unsupported evidence schema")
    evidence_source = evidence.get("source")
    if not evidence:
        provenance = None
    elif provenance_verifier is None:
        provenance = "SELF_DECLARED_UNAUTHENTICATED"
    else:
        try:
            authenticated = provenance_verifier(evidence) is True
        except Exception:
            authenticated = False
        provenance = "AUTHENTICATED_BY_INJECTED_VERIFIER" if authenticated else "VERIFIER_REJECTED"
    supplied = evidence.get("benchmarks") or {}
    if not isinstance(supplied, dict):
        raise ValueError("malformed benchmark evidence map")

    result, seen = [], set()
    for stage in data["stages"]:
        for benchmark in stage["benchmarks"]:
            bid = benchmark["id"]
            if bid in seen:
                raise ValueError(f"duplicate benchmark id: {bid}")
            seen.add(bid)
            binding = benchmark.get("canonical_task_binding")
            binding = binding if isinstance(binding, dict) else {}
            task = binding.get("task_id")
            predicates = list(dict.fromkeys([*declared, *benchmark.get("required_proof", [])]))
            entries = supplied.get(bid) or {}
            if not isinstance(entries, dict):
                raise ValueError(f"malformed predicate evidence map: {bid}")
            rows = [classify(bid, p, entries.get(p), evidence_source, provenance) for p in predicates]
            satisfied = [r["predicate"] for r in rows if r["status"] == "SATISFIED"]
            outstanding = [r["predicate"] for r in rows if r["status"] != "SATISFIED"]
            failed = [r for r in rows if r["status"] == "FAILED"]
            status = benchmark["status"]
            if status == "VERIFIED_COMPLETE" and (outstanding or task is None):
                disposition, failed_predicate = "FAIL_CLOSED", "public_status_without_governed_proof"
            elif failed:
                disposition, failed_predicate = "FAIL_CLOSED", failed[0]["failed_predicate"]
            elif outstanding or task is None:
                disposition, failed_predicate = "NOT_ELIGIBLE", None
            else:
                disposition, failed_predicate = "ELIGIBLE_FOR_PUBLISHER_GOVERNED_REVIEW", None
            result.append({
                "stage_id": stage["id"],
                "stage_name": stage.get("name"),
                "benchmark_id": bid,
                "title": benchmark["name"],
                "criterion": benchmark.get("criterion"),
                "canonical_task_id": task,
                "binding_provenance": binding.get("provenance"),
                "binding_authority": binding.get("binding_authority"),
                "binding_state": "OBSERVED_NOT_AUTHORIZING" if task else "UNRESOLVED",
                "acceptance_predicates": rows,
                "completed_subgoals": satisfied,
                "outstanding_subgoals_list": outstanding,
                "failed_predicates": [r["predicate"] for r in failed],
                "unknown_predicates": [r["predicate"] for r in rows if r["status"] == "UNKNOWN_NOT_AUTHENTICALLY_OBSERVED"],
                "verified_subgoals": len(satisfied),
                "outstanding_subgoals": len(outstanding),
                "next_executable_repair": _next_repair(bid, task, failed, outstanding),
                "governed_completion_disposition": disposition,
                "failed_predicate": failed_predicate,
                "public_benchmark_status": status,
                "completion_authority": "PUBLISHER_GOVERNED_PROJECTION_ONLY",
            })
    unknown_ids = sorted(set(supplied) - seen)
    if unknown_ids:
        raise ValueError(f"evidence names benchmarks outside the roadmap: {unknown_ids}")
    return {"schema": "stegverse.economic-roadmap-subgoals-readonly/v1",
            "authority_effect": "NONE", "source_class": "SITE_SOURCE_ONLY",
            "evidence_source": evidence_source,
            "evidence_provenance": provenance,
            "benchmark_count": len(result), "benchmarks": result}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--evidence", type=Path, help="Publisher-governed evidence projection JSON")
    args = parser.parse_args()
    evidence = json.loads(args.evidence.read_text(encoding="utf-8")) if args.evidence else None
    print(json.dumps(project(json.loads(SOURCE.read_text(encoding="utf-8")), evidence), indent=2))


if __name__ == "__main__":
    main()
