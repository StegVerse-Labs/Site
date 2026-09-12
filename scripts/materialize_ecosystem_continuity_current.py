#!/usr/bin/env python3
"""Materialize one exact retained Site-safe ECE projection into a served Site root.

This is a copy/verification boundary only. It never calculates continuity and it
must not write into the Site source repository. Authentic publication/live page
observation remains separate runtime evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

CYCLE_SCHEMA = "stegverse.healer-ecosystem-continuity-cycle/v1"
PROJECTION_SCHEMA = "stegverse.site-ecosystem-continuity-projection.v1"
PROJECTION_AUTHORITY = "NONE_READ_ONLY_PROJECTION"
CONTINUITY_STATES = {"CONTINUOUS", "CONTINUOUS_WITH_DEGRADATION", "AT_RISK", "INTERRUPTED", "INDETERMINATE"}
OBSERVATION_STATES = {"PASS", "FAIL", "DEGRADED", "UNKNOWN", "NOT_OBSERVED", "STALE", "UNREACHABLE", "PROBE_REQUIRED"}
SAFE_FINDING_KEYS = {"finding_id", "component_id", "predicate_id", "observation_state", "severity", "continuity_critical", "evidence_age_seconds", "authority_owner", "remediation_state"}


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label}_INVALID_JSON:{type(exc).__name__}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label}_NOT_OBJECT")
    return value


def _validate_projection(value: dict[str, Any]) -> None:
    if value.get("schema") != PROJECTION_SCHEMA:
        raise ValueError("PROJECTION_SCHEMA_INVALID")
    if value.get("authority_effect") != PROJECTION_AUTHORITY:
        raise ValueError("PROJECTION_AUTHORITY_INVALID")
    if value.get("source_available") is not True or value.get("projection_error") is not None:
        raise ValueError("PROJECTION_SOURCE_NOT_AUTHENTIC")
    source_id = value.get("source_evaluation_id")
    if not isinstance(source_id, str) or not source_id.startswith("ece_"):
        raise ValueError("PROJECTION_EVALUATION_ID_INVALID")
    if value.get("continuity_state") not in CONTINUITY_STATES:
        raise ValueError("PROJECTION_CONTINUITY_STATE_INVALID")
    findings = value.get("findings")
    if not isinstance(findings, list):
        raise ValueError("PROJECTION_FINDINGS_INVALID")
    for row in findings:
        if not isinstance(row, dict) or set(row) - SAFE_FINDING_KEYS:
            raise ValueError("PROJECTION_FINDING_UNSAFE")
        if row.get("observation_state") not in OBSERVATION_STATES:
            raise ValueError("PROJECTION_FINDING_STATE_INVALID")


def materialize(*, cycle_receipt: Path, projection: Path, served_site_root: Path, source_site_root: Path | None = None) -> dict[str, Any]:
    cycle_receipt = cycle_receipt.expanduser().resolve()
    projection = projection.expanduser().resolve()
    served_site_root = served_site_root.expanduser().resolve()
    source_site_root = source_site_root.expanduser().resolve() if source_site_root else None

    if source_site_root is not None and (served_site_root == source_site_root or source_site_root in served_site_root.parents):
        raise ValueError("SOURCE_REPOSITORY_WRITEBACK_FORBIDDEN")
    if not cycle_receipt.is_file():
        raise ValueError("CYCLE_RECEIPT_NOT_FOUND")
    if not projection.is_file():
        raise ValueError("PROJECTION_NOT_FOUND")

    cycle = _load_json(cycle_receipt.read_bytes(), "CYCLE_RECEIPT")
    if cycle.get("schema") != CYCLE_SCHEMA or cycle.get("state") != "COMPLETE":
        raise ValueError("CYCLE_NOT_COMPLETE")
    expected_ref = cycle.get("site_projection_ref")
    if not isinstance(expected_ref, str) or Path(expected_ref).expanduser().resolve() != projection:
        raise ValueError("CYCLE_PROJECTION_REF_MISMATCH")

    raw = projection.read_bytes()
    digest = _sha256_bytes(raw)
    if cycle.get("site_projection_sha256") != digest:
        raise ValueError("CYCLE_PROJECTION_SHA256_MISMATCH")
    projected = _load_json(raw, "PROJECTION")
    _validate_projection(projected)

    target = served_site_root / "data" / "ecosystem-continuity" / "current.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".current.", suffix=".tmp", delete=False) as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
        temp_name = handle.name
    os.replace(temp_name, target)
    if target.read_bytes() != raw:
        raise RuntimeError("MATERIALIZED_BYTES_MISMATCH")

    return {
        "schema": "stegverse.site-ecosystem-continuity-materialization-receipt.v1",
        "state": "COMPLETE",
        "source_evaluation_id": projected["source_evaluation_id"],
        "projection_sha256": digest,
        "source_projection_ref": str(projection),
        "target_ref": str(target),
        "exact_bytes_preserved": True,
        "continuity_recalculated": False,
        "source_repository_writeback": False,
        "live_publication_observed": False,
        "recovery_verified": False,
        "authority_effect": "NONE_COPY_ONLY"
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycle-receipt", required=True)
    parser.add_argument("--projection", required=True)
    parser.add_argument("--served-site-root", required=True)
    parser.add_argument("--source-site-root")
    parser.add_argument("--receipt-output")
    args = parser.parse_args()
    try:
        result = materialize(
            cycle_receipt=Path(args.cycle_receipt),
            projection=Path(args.projection),
            served_site_root=Path(args.served_site_root),
            source_site_root=Path(args.source_site_root) if args.source_site_root else None,
        )
    except (ValueError, RuntimeError, OSError) as exc:
        result = {"state": "BLOCKED", "outcome": str(exc), "authority_effect": "NONE_COPY_ONLY"}
        print(json.dumps(result, sort_keys=True))
        return 3
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.receipt_output:
        output = Path(args.receipt_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
