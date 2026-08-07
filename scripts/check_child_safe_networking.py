#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "children-safe-networking.html"
TASK = ROOT / "data/tasks/SITE-0001-CHILD-SAFE-NETWORKING.json"
HANDOFF = ROOT / "docs/CHILD_SAFE_NETWORKING_MIRROR_HANDOFF.md"

REQUIRED_PAGE_MARKERS = (
    "Data harvesting is optional",
    "Data minimization",
    "Purpose limitation",
    "Location hidden by default",
    "No advertising profile by default",
    "Safe networking without isolation",
    "Governed permissions",
    "Parent and child visibility",
    "30-second video transcript",
    "CONNECT WITHOUT SURRENDERING PRIVACY.",
    "Governance boundary",
)

REQUIRED_HANDOFF_MARKERS = (
    "SITE-0001-CHILD-SAFE-NETWORKING",
    "SITE-0001-PERSONAL-DATA-CONTROL",
    "MERGED INTO:",
    "PUBLIC_CONTENT_ONLY",
    "CHILD_SAFE_NETWORKING=PASS",
)


def main() -> int:
    failures: list[str] = []
    for path in (PAGE, TASK, HANDOFF):
        if not path.is_file():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        print("CHILD_SAFE_NETWORKING=FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    page = PAGE.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    task = json.loads(TASK.read_text(encoding="utf-8"))

    for marker in REQUIRED_PAGE_MARKERS:
        if marker not in page:
            failures.append(f"public surface missing marker: {marker}")

    for marker in REQUIRED_HANDOFF_MARKERS:
        if marker not in handoff:
            failures.append(f"handoff missing marker: {marker}")

    if task.get("task_id") != "SITE-0001-CHILD-SAFE-NETWORKING":
        failures.append("task_id mismatch")
    if task.get("repository") != "StegVerse-Labs/Site":
        failures.append("task repository mismatch")
    if task.get("state") != "READY_FOR_MACHINE_COMPLETION_CHECK":
        failures.append("task state must be READY_FOR_MACHINE_COMPLETION_CHECK before controller observation")
    if task.get("auto_admit") is not True:
        failures.append("task must be auto_admit=true")
    if task.get("external_dependencies") != []:
        failures.append("task external_dependencies must be empty")
    if task.get("authority_effect") is not False:
        failures.append("authority_effect must be false")
    if task.get("activation_effect") != "PUBLIC_CONTENT_ONLY":
        failures.append("activation_effect mismatch")

    if failures:
        print("CHILD_SAFE_NETWORKING=FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CHILD_SAFE_NETWORKING=PASS")
    print("DATA_HARVESTING_DEFAULT=OPTIONAL")
    print("CHILD_NETWORKING_POSTURE=PRIVACY_FIRST")
    print("AUTHORITY_GRANTED=false")
    print("ACTIVATION_EFFECT=PUBLIC_CONTENT_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
