#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/personal-data-control-runtime.json"
TASK = ROOT / "data/tasks/SITE-0001-PERSONAL-DATA-CONTROL.json"
PAGE = ROOT / "personal-data-control.html"
HANDOFF = ROOT / "docs/PERSONAL_DATA_CONTROL_RUNTIME_MIRROR_HANDOFF.md"

REQUIRED_STATES = {
    "NOT_REQUESTED", "RECEIVED", "IDENTITY_VERIFICATION_REQUIRED", "VERIFIED",
    "PROCESSING_RESTRICTED", "INVENTORY_COMPLETE", "DELETION_IN_PROGRESS",
    "PROCESSOR_PROPAGATION_PENDING", "COMPLETED", "PARTIALLY_DENIED",
    "DENIED", "APPEAL_OPEN", "CHANNEL_FAILED",
}
REQUIRED_PAGE_MARKERS = (
    "Controller identity", "Request channel", "Identity verification boundary",
    "Retention boundary", "Processor propagation", "Appeal route",
    "Completion receipt", "no-reply authentication address",
)


def main() -> int:
    failures: list[str] = []
    for path in (CONTRACT, TASK, PAGE, HANDOFF):
        if not path.is_file():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("PERSONAL_DATA_CONTROL_RUNTIME=FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    task = json.loads(TASK.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")

    if contract.get("external_tasks_required") is not False:
        failures.append("external_tasks_required must be false")
    if contract.get("manual_tasks_required") is not False:
        failures.append("manual_tasks_required must be false")
    if contract.get("authority_granted") is not False:
        failures.append("authority_granted must be false")
    missing_states = sorted(REQUIRED_STATES - set(contract.get("request_states", [])))
    if missing_states:
        failures.append(f"missing request states: {', '.join(missing_states)}")
    for marker in REQUIRED_PAGE_MARKERS:
        if marker not in page:
            failures.append(f"public surface missing marker: {marker}")

    if task.get("repository") != "StegVerse-Labs/Site":
        failures.append("task repository mismatch")
    if task.get("external_dependencies") != []:
        failures.append("task external_dependencies must be empty")
    if task.get("auto_admit") is not True:
        failures.append("task must be auto_admit=true")

    if failures:
        print("PERSONAL_DATA_CONTROL_RUNTIME=FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PERSONAL_DATA_CONTROL_RUNTIME=PASS")
    print("EXTERNAL_TASKS_REQUIRED=false")
    print("MANUAL_TASKS_REQUIRED=false")
    print("AUTHORITY_GRANTED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
