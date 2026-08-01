#!/usr/bin/env python3
"""Import the public crypto-bot first-accessibility receipt into a bounded Site projection.

This importer verifies receipt integrity and authority boundaries. It does not grant
publication, release, funded execution, custody, withdrawal, or live Coinbase authority.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "marketplace-coinbase-first-accessibility-status.json"
SOURCE_URL = (
    "https://raw.githubusercontent.com/StegVerse-Labs/crypto-bot/main/"
    "data/first-accessibility-mark-status.json"
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def write(status: str, reason: str, source: dict[str, Any] | None = None, failures: list[str] | None = None) -> None:
    source = source or {}
    body = {
        "schema": "stegverse.site.marketplace_coinbase_first_accessibility.v1",
        "status": status,
        "reason": reason,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_repository": "StegVerse-Labs/crypto-bot",
        "source_path": "data/first-accessibility-mark-status.json",
        "source_commit_sha": source.get("commit_sha"),
        "source_workflow_run_id": source.get("workflow_run_id"),
        "source_receipt_digest": source.get("receipt_digest"),
        "outbound_manifest_digest": source.get("outbound_manifest_digest"),
        "paper_trading_accessible": status == "ACCESSIBLE",
        "failures": sorted(failures or []),
        "projection_only": True,
        "publication_authority": "NOT_GRANTED",
        "release_authority": "NOT_GRANTED",
        "execution_authority": "NOT_GRANTED",
        "live_authority": "NOT_GRANTED",
        "custody_authority": "NOT_GRANTED",
        "withdrawal_authority": "NOT_GRANTED",
        "activation_effect": False,
        "authority_effect": False,
    }
    payload = {**body, "status_digest": digest(body)}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate(source: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    body = {key: value for key, value in source.items() if key != "receipt_digest"}
    if source.get("schema") != "stegverse.crypto_bot.first_accessibility_mark.v1":
        failures.append("unsupported_source_schema")
    if source.get("receipt_digest") != digest(body):
        failures.append("source_receipt_digest_mismatch")
    if source.get("status") != "PASS":
        failures.append("source_status_not_pass")
    if source.get("paper_trading_accessible") is not True:
        failures.append("paper_trading_not_accessible")
    if not isinstance(source.get("commit_sha"), str) or len(source.get("commit_sha", "")) != 40:
        failures.append("invalid_source_commit_sha")
    if not str(source.get("workflow_run_id", "")).isdigit():
        failures.append("invalid_workflow_run_id")
    if not str(source.get("outbound_manifest_digest", "")).startswith("sha256:"):
        failures.append("invalid_outbound_manifest_digest")
    for field in ("publication_authority", "release_authority", "live_authority"):
        if source.get(field) != "NOT_GRANTED":
            failures.append(f"{field}_boundary_invalid")
    if source.get("execution_authority") not in {"PAPER_ONLY", "NOT_GRANTED"}:
        failures.append("execution_authority_boundary_invalid")
    return failures


def main() -> int:
    try:
        req = request.Request(SOURCE_URL, headers={"User-Agent": "StegVerse-Site-Accessibility-Importer/1.0"})
        with request.urlopen(req, timeout=30) as response:
            source = json.loads(response.read().decode("utf-8"))
        if not isinstance(source, dict):
            raise ValueError("source_not_object")
    except (error.HTTPError, error.URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
        write("PENDING_SOURCE", f"source_fetch_failed:{type(exc).__name__}")
        return 0

    failures = validate(source)
    if failures:
        write("REJECTED", "source_validation_failed", source, failures)
        return 1

    write("ACCESSIBLE", "verified_paper_trading_accessibility_projection", source)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
