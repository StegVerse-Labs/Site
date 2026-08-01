#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "marketplace-coinbase-accessibility-status.json"
SOURCE_URL = "https://raw.githubusercontent.com/GCAT-BCAT-Engine/Publisher/main/data/marketplace-coinbase-release-evidence-status.json"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def fetch_source() -> dict[str, Any]:
    req = request.Request(SOURCE_URL, headers={"User-Agent": "StegVerse-Site-Marketplace-Coinbase-Accessibility/1.0"})
    with request.urlopen(req, timeout=30) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("publisher_status_not_object")
    return value


def project(state: str, reason: str, source: dict[str, Any] | None = None, findings: list[str] | None = None) -> dict[str, Any]:
    source = source or {}
    body = {
        "schema": "stegverse.site.marketplace_coinbase_accessibility.v1",
        "state": state,
        "reason": reason,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_repository": "GCAT-BCAT-Engine/Publisher",
        "source_path": "data/marketplace-coinbase-release-evidence-status.json",
        "publisher_status": source.get("status"),
        "publisher_status_digest": source.get("status_digest"),
        "publisher_sources": source.get("sources") or {},
        "evidence_bindings": source.get("evidence_bindings") or {},
        "paper_trading_accessible": state == "PAPER_ACCESSIBLE",
        "live_trading_accessible": False,
        "findings": sorted(findings or []),
        "publication_authority": "NOT_GRANTED",
        "release_authority": "NOT_GRANTED",
        "execution_authority": "NOT_GRANTED",
        "live_authority": "NOT_GRANTED",
    }
    return {**body, "projection_digest": digest(body)}


def validate(source: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    body = {key: value for key, value in source.items() if key != "status_digest"}
    if source.get("schema") != "stegverse.publisher.marketplace_coinbase_release_evidence.v2":
        findings.append("unsupported_publisher_schema")
    if source.get("status_digest") != digest(body):
        findings.append("publisher_status_digest_mismatch")
    if source.get("status") != "VERIFIED":
        findings.append("publisher_status_not_verified")
    if source.get("paper_release_verified") is not True:
        findings.append("publisher_paper_release_not_verified")
    for field in ("publication_authorized", "release_authorized", "execution_authorized", "live_authority_granted"):
        if source.get(field) is not False:
            findings.append(f"publisher_{field}_boundary_invalid")
    if not isinstance(source.get("sources"), dict) or not source.get("sources"):
        findings.append("publisher_source_identities_missing")
    if not isinstance(source.get("evidence_bindings"), dict) or not source.get("evidence_bindings"):
        findings.append("publisher_evidence_bindings_missing")
    return findings


def write(payload: dict[str, Any]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    try:
        source = fetch_source()
    except (error.HTTPError, error.URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
        write(project("PENDING_UPSTREAM", f"publisher_status_unavailable:{type(exc).__name__}"))
        return 0

    if source.get("status") in {"PENDING_CREDENTIAL", "PENDING_SOURCE"}:
        write(project("PENDING_UPSTREAM", f"publisher_{str(source.get('status')).lower()}", source))
        return 0

    findings = validate(source)
    if findings:
        state = "PENDING_UPSTREAM" if findings == ["publisher_status_not_verified"] else "REJECTED_UPSTREAM"
        write(project(state, "publisher_status_not_acceptable", source, findings))
        return 1 if state == "REJECTED_UPSTREAM" else 0

    write(project("PAPER_ACCESSIBLE", "publisher_verified_paper_accessibility_chain", source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
