#!/usr/bin/env python3
"""Fail closed when reciprocal evaluation receipts do not match repository artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data/framework-evaluations/receipts/index.json"
EXPECTED_AUTHORITY = {
    "comparison": False,
    "admissibility": False,
    "certification": False,
    "execution": False,
    "custody": False,
    "parentage": False,
}


def require(value: object, message: str) -> None:
    if not value:
        raise AssertionError(message)


def main() -> int:
    require(RECEIPT.is_file(), "missing framework evaluation receipt index")
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    require(payload.get("schema_version") == "1.0.0", "unsupported receipt schema")
    require(payload.get("hash_algorithm") == "sha256", "unsupported hash algorithm")
    require(payload.get("authority") == EXPECTED_AUTHORITY, "receipt authority boundary changed")

    records = payload.get("artifacts") or []
    require(records, "receipt contains no artifacts")
    seen: set[str] = set()
    chain_lines: list[str] = []
    for item in records:
        artifact_path = item.get("artifact_path")
        expected_hash = item.get("sha256")
        require(artifact_path and expected_hash, "receipt artifact missing path or hash")
        require(artifact_path not in seen, f"duplicate receipt artifact: {artifact_path}")
        seen.add(artifact_path)
        path = ROOT / artifact_path
        require(path.is_file(), f"missing receipted artifact: {artifact_path}")
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual_hash == expected_hash, f"hash mismatch: {artifact_path}")
        require(path.stat().st_size == item.get("size_bytes"), f"size mismatch: {artifact_path}")
        chain_lines.append(f"{artifact_path}:{actual_hash}")

    artifact_set_hash = hashlib.sha256("\n".join(chain_lines).encode("utf-8")).hexdigest()
    require(artifact_set_hash == payload.get("artifact_set_hash"), "artifact set hash mismatch")
    print("RECIPROCAL FRAMEWORK EVALUATION RECEIPTS: PASS")
    print(f"artifact_set_hash: {artifact_set_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
