#!/usr/bin/env python3
"""Import crypto-bot first-accessibility evidence into a bounded Site projection.

The importer first attempts the canonical upstream record. When cross-repository raw
access is unavailable, it verifies the repository-retained immutable observation that
is bound to the exact observed workflow, job, artifacts, source commit, and receipt.
Neither path grants publication, release, funded execution, custody, withdrawal, or
live Coinbase authority.
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
OBSERVATION = ROOT / "data" / "marketplace-coinbase-first-accessibility-source-observation.json"
SOURCE_URL = (
    "https://raw.githubusercontent.com/StegVerse-Labs/crypto-bot/main/"
    "data/first-accessibility-mark-status.json"
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def write(
    status: str,
    reason: str,
    source: dict[str, Any] | None = None,
    failures: list[str] | None = None,
    observation: dict[str, Any] | None = None,
) -> None:
    source = source or {}
    observation = observation or {}
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
        "source_observation_path": (
            "data/marketplace-coinbase-first-accessibility-source-observation.json"
            if observation
            else None
        ),
        "source_observation_workflow_job_id": observation.get("workflow_job_id"),
        "source_observation_outbound_artifact_id": observation.get("outbound_artifact_id"),
        "source_observation_outbound_artifact_digest": observation.get("outbound_artifact_digest"),
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


def validate_observation(observation: dict[str, Any], source: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if observation.get("schema") != "stegverse.site.marketplace_coinbase_first_accessibility_source_observation.v1":
        failures.append("unsupported_observation_schema")
    if observation.get("observed_source") != source:
        failures.append("observation_source_binding_mismatch")
    if observation.get("workflow_job_conclusion") != "success":
        failures.append("observed_workflow_job_not_success")
    if not isinstance(observation.get("workflow_job_id"), int):
        failures.append("invalid_observed_workflow_job_id")
    for field in ("accessibility_artifact_digest", "outbound_artifact_digest"):
        if not str(observation.get(field, "")).startswith("sha256:"):
            failures.append(f"invalid_{field}")
    if not isinstance(observation.get("outbound_artifact_id"), int):
        failures.append("invalid_outbound_artifact_id")
    if observation.get("observation_is_authority") is not False:
        failures.append("observation_asserted_authority")
    for field in (
        "publication_authority",
        "release_authority",
        "execution_authority",
        "live_authority",
        "custody_authority",
        "withdrawal_authority",
    ):
        if observation.get(field) != "NOT_GRANTED":
            failures.append(f"observation_{field}_boundary_invalid")
    return failures


def load_observation() -> tuple[dict[str, Any], dict[str, Any]]:
    observation = json.loads(OBSERVATION.read_text(encoding="utf-8"))
    if not isinstance(observation, dict):
        raise ValueError("observation_not_object")
    source = observation.get("observed_source")
    if not isinstance(source, dict):
        raise ValueError("observed_source_not_object")
    return observation, source


def main() -> int:
    observation: dict[str, Any] | None = None
    source: dict[str, Any] | None = None
    source_reason = "verified_direct_source"
    try:
        req = request.Request(SOURCE_URL, headers={"User-Agent": "StegVerse-Site-Accessibility-Importer/1.1"})
        with request.urlopen(req, timeout=30) as response:
            value = json.loads(response.read().decode("utf-8"))
        if not isinstance(value, dict):
            raise ValueError("source_not_object")
        source = value
    except (error.HTTPError, error.URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError):
        try:
            observation, source = load_observation()
            source_reason = "verified_immutable_source_observation"
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            write("PENDING_SOURCE", f"source_and_observation_unavailable:{type(exc).__name__}")
            return 1

    assert source is not None
    failures = validate(source)
    if observation is not None:
        failures.extend(validate_observation(observation, source))
    if failures:
        write("REJECTED", "source_validation_failed", source, failures, observation)
        return 1

    write("ACCESSIBLE", source_reason, source, observation=observation)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
