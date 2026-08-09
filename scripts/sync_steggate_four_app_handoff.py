#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "steggate-four-app-status.json"
HANDOFF = ROOT / "docs" / "STEGGATE_FOUR_APP_MIRROR_HANDOFF.md"
BEGIN = "<!-- STEGGATE_FOUR_APP_PROGRESS_BEGIN -->"
END = "<!-- STEGGATE_FOUR_APP_PROGRESS_END -->"
LABELS = {
    "ecosystem_chat": "Ecosystem Chat",
    "vacc": "VACC / VA Claims Chat",
    "math_solver": "Math Solver",
    "hil": "HIL experiment",
}


def render(data: dict) -> str:
    aggregate = data["aggregate"]
    lines = [
        BEGIN,
        "## Current execution progress",
        "",
        "Machine-derived gate count at handoff update:",
        "",
        "```text",
        f"Verified execution gates: {aggregate['completed_gates']} / {aggregate['total_gates']}",
        f"Aggregate execution progress: {aggregate['execution_progress_percent']}%",
        f"Fully functional public applications: {aggregate['fully_functional_public_apps']} / {aggregate['required_fully_functional_public_apps']}",
        f"Goal complete: {str(aggregate['goal_complete']).lower()}",
        f"Archive ready: {str(aggregate['goal_complete']).lower()}",
        "```",
        "",
        "Application execution-gate progress:",
        "",
        "```text",
    ]
    for key in ("ecosystem_chat", "vacc", "math_solver", "hil"):
        app = data["applications"][key]
        lines.append(
            f"{LABELS[key]}: {app['progress_percent']}% "
            f"({app['completed_gates']}/{app['total_gates']})"
        )
    lines.extend(
        [
            "```",
            "",
            f"Last machine status timestamp: `{data['updated_at']}`",
            END,
        ]
    )
    return "\n".join(lines)


def synchronized_text() -> str:
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    text = HANDOFF.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        raise SystemExit("handoff progress markers missing")
    prefix, remainder = text.split(BEGIN, 1)
    _, suffix = remainder.split(END, 1)
    return prefix + render(data) + suffix


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = synchronized_text()
    current = HANDOFF.read_text(encoding="utf-8")
    if args.check:
        if current != expected:
            print("STEGGATE_FOUR_APP_HANDOFF_SYNC_FAIL")
            return 1
        print("STEGGATE_FOUR_APP_HANDOFF_SYNC_PASS")
        return 0
    if current != expected:
        HANDOFF.write_text(expected, encoding="utf-8")
        print("STEGGATE_FOUR_APP_HANDOFF_UPDATED")
    else:
        print("STEGGATE_FOUR_APP_HANDOFF_ALREADY_CURRENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
