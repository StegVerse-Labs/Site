#!/usr/bin/env python3
"""Validate the Site workflow-consolidation inventory.

The check distinguishes repository workflow files from operational workflow
entry points. Triggerless, jobless placeholders are recorded but do not count
as active execution surfaces. The only permitted operational workflows are the
canonical bootstrap and declared-task runner.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITER = ROOT / "scripts" / "write_site_workflow_inventory.py"
INVENTORY = ROOT / "data" / "site-workflow-inventory.json"
COMPANY_TESTBED_VALIDATOR = ROOT / "scripts" / "check_site_company_testbed_artifacts.py"
COMPANY_TESTBED_TESTS = ROOT / "scripts" / "test_site_company_testbed_artifacts.py"
ACTIVATION_LEDGER_VALIDATOR = ROOT / "scripts" / "check_site_activation_ledger.py"
ACTIVATION_LEDGER_TESTS = ROOT / "scripts" / "test_site_activation_ledger.py"
ACTIVATION_LEDGER_HANDOFF_VALIDATOR = (
    ROOT / "scripts" / "check_site_activation_ledger_handoff.py"
)
CANONICAL = {"validate.yml", "site-task-runner.yml"}


def main() -> int:
    failures: list[str] = []
    if not WRITER.exists():
        print("SITE WORKFLOW INVENTORY CHECK: FAIL")
        print("- missing scripts/write_site_workflow_inventory.py")
        return 1
    for validator in (
        COMPANY_TESTBED_VALIDATOR,
        COMPANY_TESTBED_TESTS,
        ACTIVATION_LEDGER_VALIDATOR,
        ACTIVATION_LEDGER_TESTS,
        ACTIVATION_LEDGER_HANDOFF_VALIDATOR,
    ):
        if not validator.exists():
            print("SITE WORKFLOW INVENTORY CHECK: FAIL")
            print(f"- missing {validator.relative_to(ROOT)}")
            return 1

    completed = subprocess.run([sys.executable, str(WRITER)], cwd=ROOT, check=False)
    if completed.returncode != 0:
        print("SITE WORKFLOW INVENTORY CHECK: FAIL")
        print(f"- inventory writer exited with {completed.returncode}")
        return completed.returncode

    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    records = data.get("workflows", [])
    operational: list[str] = []
    placeholders: list[str] = []

    for record in records:
        name = record.get("file")
        triggers = record.get("triggers") or []
        capabilities = record.get("capabilities") or {}
        has_jobs = bool(record.get("has_jobs", False))
        if triggers or has_jobs:
            operational.append(name)
        else:
            placeholders.append(name)
        if name not in CANONICAL and capabilities.get("creates_release_or_tag"):
            failures.append(f"noncanonical workflow retains release/tag capability: {name}")
        if name not in CANONICAL and capabilities.get("deploys_pages"):
            failures.append(f"noncanonical workflow retains Pages deployment capability: {name}")

    if set(operational) != CANONICAL:
        failures.append(
            "operational workflow set mismatch: "
            + ", ".join(sorted(operational))
            + " (expected validate.yml, site-task-runner.yml)"
        )

    if data.get("canonical_count") != 2:
        failures.append("canonical_count must equal 2")

    if not failures:
        for label, validator in (
            ("company-testbed artifact", COMPANY_TESTBED_VALIDATOR),
            ("company-testbed adversarial tests", COMPANY_TESTBED_TESTS),
            ("activation-ledger", ACTIVATION_LEDGER_VALIDATOR),
            ("activation-ledger adversarial tests", ACTIVATION_LEDGER_TESTS),
            ("activation-ledger handoff", ACTIVATION_LEDGER_HANDOFF_VALIDATOR),
        ):
            completed_validator = subprocess.run(
                [sys.executable, str(validator)],
                cwd=ROOT,
                check=False,
            )
            if completed_validator.returncode != 0:
                failures.append(
                    f"{label} validator exited with {completed_validator.returncode}"
                )
                break

    print("SITE WORKFLOW INVENTORY CHECK:", "FAIL" if failures else "PASS")
    print("Operational workflows:", ", ".join(sorted(operational)) or "none")
    print("Triggerless/jobless placeholders:", ", ".join(sorted(placeholders)) or "none")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
