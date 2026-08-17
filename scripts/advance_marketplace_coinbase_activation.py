#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "marketplace-coinbase-activation-tasks.json"
FORBIDDEN_CREDENTIAL_ENV = (
    "STEGVERSE_CROSS_REPO_READ_TOKEN",
    "MARKETPLACE_COINBASE_EVIDENCE_TOKEN",
    "GITHUB_TOKEN",
    "GH_TOKEN",
    "STEGVERSE_GITHUB_TOKEN",
)

SOURCES = [
    {"task_id": "MC-01-CRYPTO-ACCESSIBILITY", "repository": "StegVerse-Labs/crypto-bot", "issue": "StegVerse-Labs/crypto-bot#7", "evidence_path": "data/first-accessibility-mark-status.json", "complete": lambda v: v.get("status") == "PASS" and v.get("paper_trading_accessible") is True, "stop_condition": "status=PASS and paper_trading_accessible=true", "completion_action": "The canonical crypto-bot owner regenerates the committed first-accessibility receipt."},
    {"task_id": "MC-02-MARKETPLACE-COLLECTION", "repository": "GCAT-BCAT-Engine/Marketplace", "issue": "GCAT-BCAT-Engine/Marketplace#1", "evidence_path": "data/marketplace-coinbase-outbound-collection-status.json", "complete": lambda v: v.get("status") == "COLLECTED", "stop_condition": "status=COLLECTED; acknowledgement ACCEPTED or DUPLICATE; sequence-2 transport present", "completion_action": "The canonical Marketplace owner retains collection, acknowledgement, sequence-2 generation, and durable status."},
    {"task_id": "MC-03-PUBLISHER-VERIFY", "repository": "GCAT-BCAT-Engine/Publisher", "issue": "GCAT-BCAT-Engine/Publisher#19", "evidence_path": "data/marketplace-coinbase-release-evidence-status.json", "complete": lambda v: v.get("status") == "VERIFIED" and v.get("paper_release_verified") is True, "stop_condition": "status=VERIFIED and paper_release_verified=true", "completion_action": "The canonical Publisher owner retains bounded reconstruction, verification, and committed public status."},
    {"task_id": "MC-04-SITE-PROJECTION", "repository": "StegVerse-Labs/Site", "issue": "StegVerse-Labs/Site#131", "evidence_path": "data/marketplace-coinbase-accessibility-status.json", "complete": lambda v: v.get("state") == "PAPER_ACCESSIBLE" and v.get("live_trading_accessible") is False, "stop_condition": "state=PAPER_ACCESSIBLE and live_trading_accessible=false", "completion_action": "The canonical Site projection owner retains regeneration after Publisher verification."},
]


def reject_credentials() -> None:
    present = [name for name in FORBIDDEN_CREDENTIAL_ENV if os.environ.get(name)]
    if present:
        raise RuntimeError("credential-bearing environment is prohibited for Marketplace Coinbase observation: " + ", ".join(sorted(present)))


def repository_roots() -> dict[str, Path]:
    roots: dict[str, Path] = {"StegVerse-Labs/Site": ROOT}
    raw = os.environ.get("STEGVERSE_REPO_ROOTS_JSON", "").strip()
    if not raw:
        return roots
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("STEGVERSE_REPO_ROOTS_JSON must be an object")
    for repository, value in parsed.items():
        if not isinstance(repository, str) or not isinstance(value, str):
            raise ValueError("repository root entries must be strings")
        path = Path(value).expanduser().resolve()
        if path.is_dir():
            roots[repository] = path
    roots["StegVerse-Labs/Site"] = ROOT
    return roots


def fetch_json(repository: str, path: str, roots: dict[str, Path]) -> tuple[str, dict, str | None]:
    repo_root = roots.get(repository)
    if repo_root is None:
        return "LOCAL_REPOSITORY_NOT_MATERIALIZED", {}, repository
    evidence = repo_root / path
    if not evidence.is_file():
        return "LOCAL_EVIDENCE_MISSING", {}, str(evidence)
    try:
        value = json.loads(evidence.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return type(exc).__name__.upper(), {}, str(exc)
    if not isinstance(value, dict):
        return "INVALID_EVIDENCE_SHAPE", {}, str(evidence)
    return "OBSERVED", value, None


def build_payload() -> dict:
    reject_credentials()
    roots = repository_roots()
    tasks = []
    all_complete = True
    for source in SOURCES:
        observation, value, detail = fetch_json(source["repository"], source["evidence_path"], roots)
        complete = observation == "OBSERVED" and source["complete"](value)
        all_complete = all_complete and complete
        if complete:
            state, next_action = "COMPLETE", "none"
        elif observation in {"LOCAL_REPOSITORY_NOT_MATERIALIZED", "LOCAL_EVIDENCE_MISSING"}:
            state = "BLOCKED_DEPENDENCY"
            next_action = "The required local StegVerse repository/evidence is not materialized. The named repository/issue remains the canonical owner; do not repair observation by introducing a GitHub token or remote checkout."
        else:
            state = "RETRY"
            next_action = source["completion_action"] + " StegVerse-owned local observation may retry later."
        tasks.append({"task_id": source["task_id"], "repository": source["repository"], "issue": source["issue"], "evidence_path": source["evidence_path"], "observation": observation, "observation_detail": detail, "state": state, "stop_condition": source["stop_condition"], "observed_status": value.get("status", value.get("state")), "development_halt": False, "completion_action": source["completion_action"], "next_action": next_action})
    return {"schema": "stegverse.site.marketplace_coinbase_activation_tasks.v4", "controller_issue": "StegVerse-Labs/Site#131", "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "state": "COMPLETE" if all_complete else "ACTIVE_STEGVERSE_CONTINUATION", "development_halt": False, "continuation_mode": "STEGVERSE_LOCAL_OBSERVATION_ONLY", "controller_access": {"credential_requirement": "NONE", "github_token_allowed": False, "non_tv_tvc_secret_or_token_allowed": False, "remote_github_observation_allowed": False, "remote_checkout_allowed": False, "local_repository_roots_required_for_cross_repo_observation": True, "access_failure_is_not_task_failure": True, "access_failure_owner": "StegVerse-Labs/Site#131"}, "tasks": tasks, "authority": {"publication": False, "release": False, "execution": False, "live": False, "financial": False}}


def main() -> int:
    payload = build_payload()
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"state": payload["state"], "tasks": len(payload["tasks"])}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
