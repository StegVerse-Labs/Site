#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "marketplace-coinbase-accessibility-status.json"
PUBLISHER_REPO = "GCAT-BCAT-Engine/Publisher"
PUBLISHER_RELATIVE_PATH = Path("data/marketplace-coinbase-release-evidence-status.json")
FORBIDDEN_CREDENTIAL_ENV = (
    "GITHUB_TOKEN",
    "GH_TOKEN",
    "GITHUB_PAT",
    "STEGVERSE_GITHUB_TOKEN",
    "STEGVERSE_CROSS_REPO_READ_TOKEN",
    "MARKETPLACE_COINBASE_EVIDENCE_TOKEN",
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def reject_credentials() -> None:
    present = sorted(name for name in FORBIDDEN_CREDENTIAL_ENV if os.environ.get(name))
    if present:
        raise RuntimeError("FORBIDDEN_CREDENTIAL_ENV:" + ",".join(present))


def repo_roots() -> dict[str, Path]:
    raw = os.environ.get("STEGVERSE_REPO_ROOTS_JSON", "").strip()
    if not raw:
        raise ValueError("STEGVERSE_REPO_ROOTS_JSON_REQUIRED")
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("STEGVERSE_REPO_ROOTS_JSON_NOT_OBJECT")
    roots: dict[str, Path] = {}
    for repository, value in parsed.items():
        if isinstance(repository, str) and isinstance(value, str):
            path = Path(value).expanduser().resolve()
            if path.is_dir():
                roots[repository] = path
    return roots


def fetch_source() -> dict[str, Any]:
    reject_credentials()
    publisher_root = repo_roots().get(PUBLISHER_REPO)
    if publisher_root is None:
        raise FileNotFoundError("PUBLISHER_LOCAL_REPOSITORY_NOT_MATERIALIZED")
    source_path = publisher_root / PUBLISHER_RELATIVE_PATH
    if not source_path.is_file():
        raise FileNotFoundError("PUBLISHER_LOCAL_EVIDENCE_NOT_MATERIALIZED")
    value = json.loads(source_path.read_text(encoding="utf-8"))
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
        "source_repository": PUBLISHER_REPO,
        "source_path": str(PUBLISHER_RELATIVE_PATH),
        "source_transport": "LOCAL_MATERIALIZED_REPOSITORY",
        "credential_requirement": "NONE",
        "github_token_allowed": False,
        "remote_source_fetch_allowed": False,
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
        "financial_authority": "NOT_GRANTED",
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
    except RuntimeError as exc:
        write(project("BLOCKED_DEPENDENCY", str(exc)))
        return 3
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        write(project("PENDING_UPSTREAM", f"publisher_local_status_unavailable:{exc}"))
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
