#!/usr/bin/env python3
"""Watch adapter activation-monitor execution from Site's operational scheduler."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/ecosystem-chat-adapter-monitor-watch.json"
MONITOR_URL = "https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/reports/ecosystem-chat-live-activation-monitor.json"
SCHEDULER_URL = "https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/reports/ecosystem-chat-activation-scheduler-status.json"


def fetch(url: str) -> dict:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "StegVerse-Site-Adapter-Monitor-Watch/1.0"})
    with urlopen(request, timeout=30) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("source_not_object")
    return value


def digest(value: dict, field: str) -> str:
    material = dict(value)
    material.pop(field, None)
    return hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    blockers: list[str] = []
    monitor: dict = {}
    scheduler: dict = {}
    try:
        monitor = fetch(MONITOR_URL)
        if monitor.get("schema") != "stegverse.ecosystem_chat.live_activation_monitor.v1":
            blockers.append("adapter_monitor_schema_invalid")
        elif digest(monitor, "monitor_sha256") != monitor.get("monitor_sha256"):
            blockers.append("adapter_monitor_hash_invalid")
        if monitor.get("workflow_run_id") is None:
            blockers.append("adapter_monitor_execution_not_observed")
        if monitor.get("observation_present") is not True:
            blockers.append("adapter_live_observation_not_present")
    except Exception as exc:
        blockers.append(f"adapter_monitor_source_unavailable:{type(exc).__name__}")
    try:
        scheduler = fetch(SCHEDULER_URL)
        if scheduler.get("manual_user_action_required") is not False:
            blockers.append("adapter_scheduler_manual_action_escalation")
    except Exception as exc:
        blockers.append(f"adapter_scheduler_status_unavailable:{type(exc).__name__}")

    payload = {
        "schema": "stegverse.ecosystem_chat.adapter_monitor_watch.v1",
        "repository": "StegVerse-Labs/Site",
        "source_repository": "StegVerse-org/LLM-adapter",
        "generated_at": now,
        "state": "OBSERVED" if not blockers else "BLOCKED",
        "blockers": sorted(set(blockers)),
        "adapter_monitor_run_id": monitor.get("workflow_run_id"),
        "adapter_monitor_generated_at": monitor.get("generated_at"),
        "adapter_observation_present": monitor.get("observation_present", False),
        "adapter_scheduler_state": scheduler.get("state"),
        "next_machine_action": "continue_activation_import" if not blockers else "continue_site_watch_and_adapter_schedule",
        "manual_user_action_required": False,
        "authority_boundary": {
            "watch_is_activation_authority": False,
            "watch_is_deployment_authority": False,
            "watch_is_execution_authority": False,
            "watch_is_release_authority": False
        }
    }
    payload["watch_sha256"] = digest(payload, "watch_sha256")
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"ADAPTER MONITOR WATCH: {payload['state']} blockers={len(payload['blockers'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
