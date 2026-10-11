#!/usr/bin/env python3
"""Read-only, source-classified subgoal inventory. Never grants roadmap completion."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/economy/public-release-benchmarks.v1.json"
REQUIRED = (
    "master_records_state_RECORDED", "reconstruction_PASS",
    "required_evidence_validation_PASS", "exact_receipt_digest_equality",
    "correct_benchmark_identity", "governed_publication_closure",
)

def project(data: dict) -> dict:
    """Return conservative subgoals, never infer authoritative runtime proof."""
    result = []
    for stage in data["stages"]:
        for benchmark in stage["benchmarks"]:
            binding = benchmark.get("canonical_task_binding")
            task = binding.get("task_id") if isinstance(binding, dict) else None
            predicates = list(dict.fromkeys([*REQUIRED, *benchmark.get("required_proof", [])]))
            result.append({
                "stage_id": stage["id"],
                "benchmark_id": benchmark["id"],
                "title": benchmark["name"],
                "canonical_task_id": task,
                "binding_authority": binding.get("binding_authority") if isinstance(binding, dict) else None,
                "binding_state": "OBSERVED_NOT_AUTHORIZING" if task else "UNRESOLVED",
                "acceptance_predicates": [{
                    "predicate": p,
                    "status": "UNKNOWN_NOT_AUTHENTICALLY_OBSERVED",
                    "evidence_ref": None,
                    "next_action": "Obtain exact authenticated owner evidence and Publisher-governed public-safe projection",
                } for p in predicates],
                "verified_subgoals": 0,
                "outstanding_subgoals": len(predicates),
                "public_benchmark_status": benchmark["status"],
                "completion_authority": "PUBLISHER_GOVERNED_PROJECTION_ONLY",
            })
    return {"schema": "stegverse.economic-roadmap-subgoals-readonly/v1",
            "authority_effect": "NONE", "source_class": "SITE_SOURCE_ONLY",
            "benchmark_count": len(result), "benchmarks": result}

def main() -> None:
    print(json.dumps(project(json.loads(SOURCE.read_text(encoding="utf-8"))), indent=2))

if __name__ == "__main__":
    main()
