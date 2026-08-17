#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "marketplace-coinbase-activation-tasks.json"

# This observer intentionally requires no credential. GitHub/project/provider tokens are
# rejected rather than consumed so it can execute in a StegVerse-owned lane without
# transferring credential or control-plane authority to GitHub Actions.
FORBIDDEN_CREDENTIAL_ENV = (
    "STEGVERSE_CROSS_REPO_READ_TOKEN",
    "MARKETPLACE_COINBASE_EVIDENCE_TOKEN",
    "GITHUB_TOKEN",
    "GH_TOKEN",
    "STEGVERSE_GITHUB_TOKEN",
)

SOURCES = [
    {
        "task_id": "MC-01-CRYPTO-ACCESSIBILITY",
        "repository": "StegVerse-Labs/crypto-bot",
        "issue": "StegVerse-Labs/crypto-bot#7",
        "workflow": ".github/workflows/first-accessibility-mark.yml",
        "evidence_path": "data/first-accessibility-mark-status.json",
        "complete": lambda v: v.get("status") == "PASS" and v.get("paper_trading_accessible") is True,
        "stop_condition": "status=PASS and paper_trading_accessible=true",
        "completion_action": "The canonical crypto-bot owner regenerates the committed first-accessibility receipt.",
    },
    {
        "task_id": "MC-02-MARKETPLACE-COLLECTION",
        "repository": "GCAT-BCAT-Engine/Marketplace",
        "issue": "GCAT-BCAT-Engine/Marketplace#1",
        "workflow": ".github/workflows/import-marketplace-coinbase-settlements.yml",
        "evidence_path": "data/marketplace-coinbase-outbound-collection-status.json",
        "complete": lambda v: v.get("status") == "COLLECTED",
        "stop_condition": "status=COLLECTED; acknowledgement ACCEPTED or DUPLICATE; sequence-2 transport present",
        "completion_action": "The canonical Marketplace owner retains collection, acknowledgement, sequence-2 generation, and durable status.",
    },
    {
        "task_id": "MC-03-PUBLISHER-VERIFY",
        "repository": "GCAT-BCAT-Engine/Publisher",
        "issue": "GCAT-BCAT-Engine/Publisher#19",
        "workflow": ".github/workflows/collect-marketplace-coinbase-release-evidence.yml",
        "evidence_path": "data/marketplace-coinbase-release-evidence-status.json",
        "complete": lambda v: v.get("status") == "VERIFIED" and v.get("paper_release_verified") is True,
        "stop_condition": "status=VERIFIED and paper_release_verified=true",
        "completion_action": "The canonical Publisher owner retains bounded reconstruction, verification, and committed public status.",
    },
    {
        "task_id": "MC-04-SITE-PROJECTION",
        "repository": "StegVerse-Labs/Site",
        "issue": "StegVerse-Labs/Site#131",
        "workflow": ".github/workflows/import-marketplace-coinbase-accessibility.yml",
        "evidence_path": "data/marketplace-coinbase-accessibility-status.json",
        "complete": lambda v: v.get("state") == "PAPER_ACCESSIBLE" and v.get("live_trading_accessible") is False,
        "stop_condition": "state=PAPER_ACCESSIBLE and live_trading_accessible=false",
        "completion_action": "The canonical Site projection owner retains regeneration after Publisher verification.",
    },
]


def reject_credentials() -> None:
    present = [name for name in FORBIDDEN_CREDENTIAL_ENV if os.environ.get(name)]
    if present:
        raise RuntimeError(
            "credential-bearing environment is prohibited for Marketplace Coinbase observation: "
            + ", ".join(sorted(present))
        )


def api_url(repository: str, path: str) -> str:
    return f"https://api.github.com/repos/{repository}/contents/{path}?ref=main"


def fetch_json(repository: str, path: str) -> tuple[str, dict, str | None]:
    if repository == "StegVerse-Labs/Site":
        local_path = ROOT / path
        if not local_path.exists():
            return "LOCAL_MISSING", {}, None
        try:
            value = json.loads(local_path.read_text(encoding="utf-8"))
            return "OBSERVED", value if isinstance(value, dict) else {}, None
        except (OSError, json.JSONDecodeError) as exc:
            return type(exc).__name__.upper(), {}, str(exc)

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "StegVerse-Marketplace-Coinbase-Observation/3.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    try:
        req = request.Request(api_url(repository, path), headers=headers)
        with request.urlopen(req, timeout=20) as response:
            envelope = json.loads(response.read().decode("utf-8"))
        encoded = envelope.get("content", "").replace("\n", "")
        if not encoded:
            return "EMPTY_CONTENT", {}, None
        import base64

        value = json.loads(base64.b64decode(encoded).decode("utf-8"))
        return "OBSERVED", value if isinstance(value, dict) else {}, None
    except error.HTTPError as exc:
        if exc.code in {401, 403, 404}:
            return "OBSERVATION_PATH_BLOCKED", {}, f"anonymous_github_api_http_{exc.code}"
        return f"HTTP_{exc.code}", {}, str(exc)
    except (error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as exc:
        return type(exc).__name__.upper(), {}, str(exc)


def build_payload() -> dict:
    reject_credentials()
    tasks = []
    all_complete = True
    for source in SOURCES:
        observation, value, detail = fetch_json(source["repository"], source["evidence_path"])
        complete = observation == "OBSERVED" and source["complete"](value)
        all_complete = all_complete and complete

        if complete:
            state = "COMPLETE"
            next_action = "none"
        elif observation == "OBSERVATION_PATH_BLOCKED":
            state = "BLOCKED_DEPENDENCY"
            next_action = (
                "The anonymous observation path cannot see this evidence. The named repository/issue remains the "
                "canonical owner; do not repair observation by introducing a GitHub token."
            )
        else:
            state = "RETRY"
            next_action = source["completion_action"] + " StegVerse-owned observation may retry later."

        tasks.append(
            {
                "task_id": source["task_id"],
                "repository": source["repository"],
                "issue": source["issue"],
                "workflow": source["workflow"],
                "evidence_path": source["evidence_path"],
                "observation": observation,
                "observation_detail": detail,
                "state": state,
                "stop_condition": source["stop_condition"],
                "observed_status": value.get("status", value.get("state")),
                "development_halt": False,
                "completion_action": source["completion_action"],
                "next_action": next_action,
            }
        )

    return {
        "schema": "stegverse.site.marketplace_coinbase_activation_tasks.v3",
        "controller_issue": "StegVerse-Labs/Site#131",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "state": "COMPLETE" if all_complete else "ACTIVE_STEGVERSE_CONTINUATION",
        "development_halt": False,
        "continuation_mode": "STEGVERSE_OWNED_OBSERVATION_ONLY",
        "controller_access": {
            "credential_requirement": "NONE",
            "github_token_allowed": False,
            "non_tv_tvc_secret_or_token_allowed": False,
            "anonymous_public_observation_only": True,
            "access_failure_is_not_task_failure": True,
            "access_failure_owner": "StegVerse-Labs/Site#131",
        },
        "tasks": tasks,
        "authority": {
            "publication": False,
            "release": False,
            "execution": False,
            "live": False,
            "financial": False,
        },
    }


def main() -> int:
    payload = build_payload()
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"state": payload["state"], "tasks": len(payload["tasks"])}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
