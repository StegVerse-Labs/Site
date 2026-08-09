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
INTEGRATION_BEGIN = "<!-- STEGGATE_FOUR_APP_INTEGRATION_BEGIN -->"
INTEGRATION_END = "<!-- STEGGATE_FOUR_APP_INTEGRATION_END -->"
APP_BEGIN = "<!-- STEGGATE_FOUR_APP_APPLICATION_STATE_BEGIN -->"
APP_END = "<!-- STEGGATE_FOUR_APP_APPLICATION_STATE_END -->"
ORDER_BEGIN = "<!-- STEGGATE_FOUR_APP_EXECUTION_ORDER_BEGIN -->"
ORDER_END = "<!-- STEGGATE_FOUR_APP_EXECUTION_ORDER_END -->"
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
        lines.append(f"{LABELS[key]}: {app['progress_percent']}% ({app['completed_gates']}/{app['total_gates']})")
    lines.extend(["```", "", f"Last machine status timestamp: `{data['updated_at']}`", END])
    return "\n".join(lines)


def render_integration(data: dict) -> str:
    binding = data.get("common_runtime_binding") or {}
    app_bindings = binding.get("application_bindings") or {}
    core_validation = binding.get("core_validation") or {}
    math_validation = binding.get("math_solver_ci_validation") or {}
    lines = [
        INTEGRATION_BEGIN,
        "## Common runtime identity integration",
        "",
        f"Issue: `{binding.get('issue')}`.",
        f"State: `{binding.get('state')}`.",
        f"Contract version: `{binding.get('contract_version')}`.",
        f"Runtime identity: `{binding.get('runtime_identity')}`.",
        f"Canonical owner: `{binding.get('canonical_owner')}`.",
        f"Canonical admissibility runtime: `{binding.get('canonical_admissibility_runtime')}`.",
        f"Transport identity authoritative: `{str(binding.get('transport_identity_authoritative')).lower()}`.",
        f"Core contract: `{binding.get('core_contract')}`.",
        "",
        "Application binding state:",
        "",
    ]
    for key in ("ecosystem_chat", "vacc", "math_solver", "hil"):
        lines.append(f"- {LABELS[key]}: `{app_bindings.get(key, 'UNRECORDED')}`")
    lines.extend(["", f"Public direct bindings: {binding.get('public_direct_bindings', 0)} / {binding.get('required_public_direct_bindings', 4)}."])
    if core_validation:
        lines.extend([
            "", "Core identity validation:", "",
            f"- run/job: `{core_validation.get('run_id')}` / `{core_validation.get('job_id')}`",
            f"- artifact: `{core_validation.get('artifact_id')}`",
            f"- digest: `{core_validation.get('artifact_digest')}`",
        ])
    if math_validation:
        lines.extend([
            "", "Math Solver identity-binding validation:", "",
            f"- run/job: `{math_validation.get('run_id')}` / `{math_validation.get('job_id')}`",
            f"- artifact: `{math_validation.get('artifact_id')}`",
            f"- digest: `{math_validation.get('artifact_digest')}`",
            f"- public deployment proven: `{str(math_validation.get('public_deployment_proven')).lower()}`",
        ])
    lines.extend([
        "",
        "This integration state has no product-activation effect until direct public application evidence satisfies the corresponding execution gates.",
        INTEGRATION_END,
    ])
    return "\n".join(lines)


def render_application_state(data: dict) -> str:
    lines = [APP_BEGIN, "## Application state", ""]
    for key in ("ecosystem_chat", "vacc", "math_solver", "hil"):
        app = data["applications"][key]
        lines.extend([
            f"### {LABELS[key]} — {app['progress_percent']}% execution-gate progress", "",
            f"Issue: `StegVerse-Labs/Site#{app.get('issue')}`.",
            f"Surface: `{app.get('surface')}`.",
            f"Machine state: `{app.get('state')}`.", "", "Verified gates:", "",
        ])
        verified = [name for name, value in app["gates"].items() if value]
        remaining = [name for name, value in app["gates"].items() if not value]
        lines.extend(f"- `{name}` — VERIFIED" for name in verified) if verified else lines.append("- none")
        lines.extend(["", "Remaining gates:", ""])
        lines.extend(f"- `{name}` — NOT VERIFIED" for name in remaining) if remaining else lines.append("- none")
        lines.extend(["", "Current blockers:", ""])
        blockers = app.get("blockers") or []
        lines.extend(f"- {blocker}" for blocker in blockers) if blockers else lines.append("- none")
        if key == "math_solver":
            observation = app.get("latest_runtime_observation") or {}
            if observation:
                lines.extend([
                    "", "Latest public-runtime observation:", "",
                    f"- state: `{observation.get('state')}`",
                    f"- reason: `{observation.get('reason')}`",
                    f"- workflow run/job: `{observation.get('workflow_run')}` / `{observation.get('workflow_job')}`",
                    f"- receipt: `{observation.get('receipt')}`",
                ])
        if key == "hil":
            claim = app.get("active_claim") or {}
            queued = app.get("queued_live_task") or {}
            if claim:
                lines.extend([
                    "", "Active collision boundary:", "",
                    f"- task: `{claim.get('task_id')}`",
                    f"- owner: `{claim.get('owner')}`",
                    f"- state: `{claim.get('state')}`",
                    f"- policy: {claim.get('collision_policy')}",
                ])
            if queued:
                lines.extend([
                    "", "Queued live task:", "",
                    f"- task: `{queued.get('task_id')}`",
                    f"- state: `{queued.get('state')}`",
                    f"- owner: `{queued.get('owner')}`",
                    f"- release condition: {queued.get('blocked_until')}",
                    f"- dependency: {queued.get('external_blocker')}",
                ])
        lines.append("")
    lines.append(APP_END)
    return "\n".join(lines)


def render_execution_order(data: dict) -> str:
    lines = [ORDER_BEGIN, "## Execution order", "", "Current dependency-aware route:", ""]
    for index, task in enumerate(data.get("next_execution_order") or [], start=1):
        lines.append(f"{index}. {task}")
    lines.extend(["", "Nonconflicting application work may run in parallel. No application may manufacture a substitute StegGate authority.", ORDER_END])
    return "\n".join(lines)


def _replace_block(text: str, begin: str, end: str, rendered: str) -> str:
    if begin not in text or end not in text:
        raise SystemExit(f"handoff block markers missing: {begin} / {end}")
    prefix, remainder = text.split(begin, 1)
    _, suffix = remainder.split(end, 1)
    return prefix + rendered + suffix


def _replace_section(text: str, section_begin: str, section_end: str, rendered: str) -> str:
    if section_begin not in text or section_end not in text:
        raise SystemExit(f"handoff section missing: {section_begin} / {section_end}")
    prefix, remainder = text.split(section_begin, 1)
    _, suffix = remainder.split(section_end, 1)
    return prefix + rendered + "\n\n" + section_end + suffix


def synchronized_text() -> str:
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    text = HANDOFF.read_text(encoding="utf-8")
    text = _replace_block(text, BEGIN, END, render(data))
    if INTEGRATION_BEGIN in text and INTEGRATION_END in text:
        text = _replace_block(text, INTEGRATION_BEGIN, INTEGRATION_END, render_integration(data))
    else:
        marker = "## Application state"
        if marker not in text:
            raise SystemExit("handoff application-state section missing")
        text = text.replace(marker, render_integration(data) + "\n\n" + marker, 1)
    if APP_BEGIN in text and APP_END in text:
        text = _replace_block(text, APP_BEGIN, APP_END, render_application_state(data))
    else:
        text = _replace_section(text, "## Application state", "## Execution order", render_application_state(data))
    if ORDER_BEGIN in text and ORDER_END in text:
        text = _replace_block(text, ORDER_BEGIN, ORDER_END, render_execution_order(data))
    else:
        text = _replace_section(text, "## Execution order", "## Heartbeat / worker / task assignment integration", render_execution_order(data))
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
