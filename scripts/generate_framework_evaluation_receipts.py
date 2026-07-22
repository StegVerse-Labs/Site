#!/usr/bin/env python3
"""Generate deterministic SHA-256 receipts for reciprocal evaluation artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/framework-evaluations"
OUT = BASE / "receipts/index.json"

ARTIFACTS = (
    "index.json",
    "stegverse.json",
    "ta-14.json",
    "stegverse-live-baseline-readiness.json",
    "stegverse-live-baseline-execution-request.json",
    "stegverse-live-baseline-handoff-status.json",
    "evidence/index.json",
    "test-cases/index.json",
    "test-cases/reciprocal-boundary-reconstruction-v1.json",
    "test-cases/stegverse-public-baseline-v1.json",
    "runs/run-stegverse-public-baseline-v1.jsonl",
    "runs/run-ta14-public-reconstruction-v1.jsonl",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    records = []
    for relative in ARTIFACTS:
        path = BASE / relative
        if not path.is_file():
            raise SystemExit(f"missing receipt artifact: {path.relative_to(ROOT)}")
        records.append({
            "artifact_path": str(path.relative_to(ROOT)),
            "sha256": digest(path),
            "size_bytes": path.stat().st_size,
        })

    chain_material = "\n".join(f"{item['artifact_path']}:{item['sha256']}" for item in records).encode("utf-8")
    payload = {
        "schema_version": "1.0.0",
        "receipt_type": "reciprocal_framework_evaluation_artifact_set",
        "hash_algorithm": "sha256",
        "canonicalization": "raw repository bytes; ordered by generator ARTIFACTS tuple",
        "artifacts": records,
        "artifact_set_hash": hashlib.sha256(chain_material).hexdigest(),
        "authority": {
            "comparison": False,
            "admissibility": False,
            "certification": False,
            "execution": False,
            "custody": False,
            "parentage": False,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"RECIPROCAL FRAMEWORK RECEIPTS GENERATED: {len(records)} artifacts")
    print(f"artifact_set_hash: {payload['artifact_set_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
