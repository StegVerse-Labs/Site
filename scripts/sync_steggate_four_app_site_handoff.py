#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "steggate-four-app-status.json"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
BEGIN = "<!-- STEGGATE_FOUR_APP_SITE_STATUS_BEGIN -->"
END = "<!-- STEGGATE_FOUR_APP_SITE_STATUS_END -->"


def render(data: dict) -> str:
    a = data["aggregate"]
    o = data.get("orchestration", {})
    return "\n".join([
        BEGIN,
        "## StegGate four-public-application execution status",
        "",
        "Canonical progress handoff: `docs/STEGGATE_FOUR_APP_MIRROR_HANDOFF.md`",
        "Machine status: `data/steggate-four-app-status.json`",
        "Parent goal: `StegVerse-Labs/Site#239`",
        "",
        "```text",
        f"execution_progress: {a['execution_progress_percent']}% ({a['completed_gates']}/{a['total_gates']} verified gates)",
        f"fully_functional_public_apps: {a['fully_functional_public_apps']}/{a['required_fully_functional_public_apps']}",
        f"goal_complete: {str(a['goal_complete']).lower()}",
        f"orchestration_state: {o.get('state', 'UNKNOWN')}",
        f"archive_ready_for_four_app_goal: {str(a['goal_complete']).lower()}",
        f"status_timestamp: {data['updated_at']}",
        "```",
        "",
        "Status checks must read the dedicated four-app handoff and machine status, then current heartbeat/orchestration state, before reporting progress. Product completion is never inferred from orchestration completion.",
        END,
    ])


def desired() -> str:
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    text = HANDOFF.read_text(encoding="utf-8")
    block = render(data)
    if BEGIN in text and END in text:
        prefix, remainder = text.split(BEGIN, 1)
        _, suffix = remainder.split(END, 1)
        return prefix + block + suffix
    anchor = "This file is the current handoff and task source of truth for `StegVerse-Labs/Site`."
    if anchor not in text:
        raise SystemExit("SITE_MIRROR_HANDOFF source-of-truth anchor missing")
    return text.replace(anchor, anchor + "\n\n" + block, 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    current = HANDOFF.read_text(encoding="utf-8")
    expected = desired()
    if args.check:
        if current != expected:
            print("STEGGATE_FOUR_APP_SITE_HANDOFF_SYNC_FAIL")
            return 1
        print("STEGGATE_FOUR_APP_SITE_HANDOFF_SYNC_PASS")
        return 0
    if current != expected:
        HANDOFF.write_text(expected, encoding="utf-8")
        print("STEGGATE_FOUR_APP_SITE_HANDOFF_UPDATED")
    else:
        print("STEGGATE_FOUR_APP_SITE_HANDOFF_ALREADY_CURRENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
