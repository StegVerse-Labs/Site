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
APP_BEGIN = "<!-- STEGGATE_FOUR_APP_APPLICATION_STATE_BEGIN -->"
APP_END = "<!-- STEGGATE_FOUR_APP_APPLICATION_STATE_END -->"
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


def _gate_label(name: str) -> str:
    return name.replace("_", " ")


def render_application_state(data: dict) -> str:
    lines = [APP_BEGIN, "## Application state", ""]
    for key in ("ecosystem_chat", "vacc", "math_solver", "hil"):
        app = data["applications"][key]
        issue = app.get("issue")
        lines.extend(
            [
                f"### {LABELS[key]} — {app['progress_percent']}% execution-gate progress",
                "",
                f"Issue: `StegVerse-Labs/Site#{issue}`.",
                f"Surface: `{app.get('surface')}`.",
                f"Machine state: `{app.get('state')}`.",
                "",
                "Verified gates:",
                "",
            ]
        )
        verified = [name for name, value in app["gates"].items() if value]
        remaining = [name for name, value in app["gates"].items() if not value]
        if verified:
            lines.extend(f"- `{name}` — VERIFIED" for name in verified)
        else:
            lines.append("- none")
        lines.extend(["", "Remaining gates:", ""])
        if remaining:
            lines.extend(f"- `{name}` — NOT VERIFIED" for name in remaining)
        else:
            lines.append("- none")
        lines.extend(["", "Current blockers:", ""])
        blockers = app.get("blockers") or []
        if blockers:
            lines.extend(f"- {blocker}" for blocker in blockers)
        else:
            lines.append("- none")
        if key == "math_solver":
            observation = app.get("latest_runtime_observation") or {}
            if observation:
                lines.extend(
                    [
                        "",
                        "Latest public-runtime observation:",
                        "",
                        f"- state: `{observation.get('state')}`",
                        f"- reason: `{observation.get('reason')}`",
                        f"- workflow run/job: `{observation.get('workflow_run')}` / `{observation.get('workflow_job')}`",
                        f"- receipt: `{observation.get('receipt')}`",
                    ]
                )
        if key == "hil":
            claim = app.get("active_claim") or {}
            queued = app.get("queued_live_task") or {}
            if claim:
                lines.extend(
                    [
                        "",
                        "Active collision boundary:",
                        "",
                        f"- task: `{claim.get('task_id')}`",
                        f"- owner: `{claim.get('owner')}`",
                        f"- state: `{claim.get('state')}`",
                        f"- policy: {claim.get('collision_policy')}",
                    ]
                )
            if queued:
                lines.extend(
                    [
                        "",
                        "Queued live task:",
                        "",
                        f"- task: `{queued.get('task_id')}`",
                        f"- state: `{queued.get('state')}`",
                        f"- owner: `{queued.get('owner')}`",
                        f"- release condition: {queued.get('blocked_until')}",
                        f"- dependency: {queued.get('external_blocker')}",
                    ]
                )
        lines.append("")
    lines.append(APP_END)
    return "\n".join(lines)


def _replace_block(text: str, begin: str, end: str, rendered: str) -> str:
    if begin in text and end in text:
        prefix, remainder = text.split(begin, 1)
        _, suffix = remainder.split(end, 1)
        return prefix + rendered + suffix
    raise SystemExit(f"handoff block markers missing: {begin} / {end}")


def synchronized_text() -> str:
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    text = HANDOFF.read_text(encoding="utf-8")
    text = _replace_block(text, BEGIN, END, render(data))
    if APP_BEGIN not in text or APP_END not in text:
        section_begin = "## Application state"
        section_end = "## Execution order"
        if section_begin not in text or section_end not in text:
            raise SystemExit("handoff application-state section missing")
        prefix, remainder = text.split(section_begin, 1)
        _, suffix = remainder.split(section_end, 1)
        text = prefix + render_application_state(data) + "\n\n## Execution order" + suffix
    else:
        text = _replace_block(text, APP_BEGIN, APP_END, render_application_state(data))
    return text


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
