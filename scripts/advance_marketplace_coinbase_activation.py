#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "marketplace-coinbase-activation-tasks.json"

SOURCES = [
    {
        "task_id": "MC-01-CRYPTO-ACCESSIBILITY",
        "repository": "StegVerse-Labs/crypto-bot",
        "issue": "StegVerse-Labs/crypto-bot#7",
        "workflow": ".github/workflows/first-accessibility-mark.yml",
        "evidence_path": "data/first-accessibility-mark-status.json",
        "url": "https://raw.githubusercontent.com/StegVerse-Labs/crypto-bot/main/data/first-accessibility-mark-status.json",
        "complete": lambda v: v.get("status") == "PASS" and v.get("paper_trading_accessible") is True,
        "stop_condition": "status=PASS and paper_trading_accessible=true",
    },
    {
        "task_id": "MC-02-MARKETPLACE-COLLECTION",
        "repository": "GCAT-BCAT-Engine/Marketplace",
        "issue": "GCAT-BCAT-Engine/Marketplace#1",
        "workflow": ".github/workflows/import-marketplace-coinbase-settlements.yml",
        "evidence_path": "data/marketplace-coinbase-outbound-collection-status.json",
        "url": "https://raw.githubusercontent.com/GCAT-BCAT-Engine/Marketplace/main/data/marketplace-coinbase-outbound-collection-status.json",
        "complete": lambda v: v.get("status") == "COLLECTED",
        "stop_condition": "status=COLLECTED; downstream acknowledgement and sequence-2 evidence then become observable",
    },
    {
        "task_id": "MC-03-PUBLISHER-VERIFY",
        "repository": "GCAT-BCAT-Engine/Publisher",
        "issue": "GCAT-BCAT-Engine/Publisher#19",
        "workflow": ".github/workflows/collect-marketplace-coinbase-release-evidence.yml",
        "evidence_path": "data/marketplace-coinbase-release-evidence-status.json",
        "url": "https://raw.githubusercontent.com/GCAT-BCAT-Engine/Publisher/main/data/marketplace-coinbase-release-evidence-status.json",
        "complete": lambda v: v.get("status") == "VERIFIED" and v.get("paper_release_verified") is True,
        "stop_condition": "status=VERIFIED and paper_release_verified=true",
    },
    {
        "task_id": "MC-04-SITE-PROJECTION",
        "repository": "StegVerse-Labs/Site",
        "issue": "StegVerse-Labs/Site#131",
        "workflow": ".github/workflows/import-marketplace-coinbase-accessibility.yml",
        "evidence_path": "data/marketplace-coinbase-accessibility-status.json",
        "url": "https://raw.githubusercontent.com/StegVerse-Labs/Site/main/data/marketplace-coinbase-accessibility-status.json",
        "complete": lambda v: v.get("state") == "PAPER_ACCESSIBLE" and v.get("live_trading_accessible") is False,
        "stop_condition": "state=PAPER_ACCESSIBLE and live_trading_accessible=false",
    },
]


def fetch_json(url: str) -> tuple[str, dict]:
    try:
        req = request.Request(url, headers={"User-Agent": "StegVerse-Marketplace-Coinbase-Activation-Controller/1.0"})
        with request.urlopen(req, timeout=20) as response:
            value = json.loads(response.read().decode("utf-8"))
        return "OBSERVED", value if isinstance(value, dict) else {}
    except error.HTTPError as exc:
        return f"HTTP_{exc.code}", {}
    except (error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        return type(exc).__name__.upper(), {}


def main() -> int:
    tasks = []
    all_complete = True
    for source in SOURCES:
        observation, value = fetch_json(source["url"])
        complete = observation == "OBSERVED" and source["complete"](value)
        all_complete = all_complete and complete
        tasks.append({
            "task_id": source["task_id"],
            "repository": source["repository"],
            "issue": source["issue"],
            "workflow": source["workflow"],
            "evidence_path": source["evidence_path"],
            "observation": observation,
            "state": "COMPLETE" if complete else "ACTIVE_RETRY",
            "stop_condition": source["stop_condition"],
            "observed_status": value.get("status", value.get("state")),
            "development_halt": False,
            "next_action": "observe scheduled repository workflow and continue adjacent work" if not complete else "none",
        })

    payload = {
        "schema": "stegverse.site.marketplace_coinbase_activation_tasks.v1",
        "controller_issue": "StegVerse-Labs/Site#131",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "state": "COMPLETE" if all_complete else "ACTIVE_AUTONOMOUS_CONTINUATION",
        "development_halt": False,
        "continuation_mode": "ADJACENT_WORK_AND_RETRY",
        "tasks": tasks,
        "authority": {"publication": False, "release": False, "execution": False, "live": False},
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"state": payload["state"], "tasks": len(tasks)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
