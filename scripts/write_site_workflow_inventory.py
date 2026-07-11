#!/usr/bin/env python3
"""Write a machine-readable inventory of Site workflow entry points.

This tool is read-only with respect to workflow files. It does not disable,
delete, rename, dispatch, or authorize any workflow. It records the current
migration boundary so consolidation can proceed without losing triggers,
permissions, artifacts, secrets, or receipts.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
OUTPUT = ROOT / "data" / "site-workflow-inventory.json"
CANONICAL = {"validate.yml", "site-task-runner.yml"}


def scalar_name(text: str, fallback: str) -> str:
    match = re.search(r"(?m)^name:\s*(.+?)\s*$", text)
    return match.group(1).strip(" '\"") if match else fallback


def trigger_names(text: str) -> list[str]:
    lines = text.splitlines()
    triggers: list[str] = []
    in_on = False
    on_indent = 0
    for line in lines:
        if not in_on:
            match = re.match(r"^(\s*)on:\s*$", line)
            if match:
                in_on = True
                on_indent = len(match.group(1))
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= on_indent:
            break
        match = re.match(r"^\s{2,}([A-Za-z_][A-Za-z0-9_-]*):", line)
        if match and match.group(1) not in triggers:
            triggers.append(match.group(1))
    return triggers


def mentions(text: str, token: str) -> bool:
    return token in text


def has_jobs(text: str) -> bool:
    return re.search(r"(?m)^jobs:\s*$", text) is not None


def main() -> int:
    records = []
    for path in sorted(WORKFLOWS.glob("*.y*ml")):
        text = path.read_text(encoding="utf-8")
        triggers = trigger_names(text)
        jobs_present = has_jobs(text)
        operational = bool(triggers or jobs_present)
        records.append(
            {
                "file": path.name,
                "name": scalar_name(text, path.name),
                "classification": "CANONICAL" if path.name in CANONICAL else "MIGRATION_REQUIRED",
                "triggers": triggers,
                "has_jobs": jobs_present,
                "operational": operational,
                "capabilities": {
                    "contents_write": mentions(text, "contents: write"),
                    "pages_write": mentions(text, "pages: write"),
                    "id_token_write": mentions(text, "id-token: write"),
                    "uses_secrets": mentions(text, "secrets."),
                    "uploads_artifact": mentions(text, "actions/upload-artifact"),
                    "deploys_pages": mentions(text, "actions/deploy-pages"),
                    "pushes_git": bool(re.search(r"(?m)^\s*git push\s*$", text)),
                    "creates_release_or_tag": any(
                        token in text for token in ("gh release", "git tag", "create-release")
                    ),
                },
                "migration_status": (
                    "RETAIN"
                    if path.name in CANONICAL
                    else (
                        "TRIGGERLESS_JOBLESS_PLACEHOLDER"
                        if not operational
                        else "INVENTORY_ONLY_NOT_AUTHORIZED_TO_RETIRE"
                    )
                ),
            }
        )

    operational_records = [record for record in records if record["operational"]]
    operational_noncanonical = [
        record for record in operational_records if record["file"] not in CANONICAL
    ]
    payload = {
        "schema_version": "1.1.0",
        "inventory_type": "site_workflow_consolidation_inventory",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/Site",
        "canonical_workflows": sorted(CANONICAL),
        "workflow_file_count": len(records),
        "operational_workflow_count": len(operational_records),
        "canonical_count": sum(r["classification"] == "CANONICAL" for r in records),
        "migration_required_file_count": sum(
            r["classification"] == "MIGRATION_REQUIRED" for r in records
        ),
        "migration_required_operational_count": len(operational_noncanonical),
        "placeholder_count": sum(not r["operational"] for r in records),
        "consolidation_complete": (
            {record["file"] for record in operational_records} == CANONICAL
            and len(operational_noncanonical) == 0
        ),
        "authority_boundary": {
            "inventory_disables_workflows": False,
            "inventory_deletes_workflows": False,
            "inventory_grants_release_authority": False,
            "inventory_grants_deployment_authority": False,
            "retirement_requires_preserved_contract_and_explicit_handoff_authority": True,
        },
        "workflows": records,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"SITE WORKFLOW INVENTORY: {len(records)} workflow file(s)")
    print(f"OPERATIONAL: {payload['operational_workflow_count']}")
    print(f"CANONICAL: {payload['canonical_count']}")
    print(f"MIGRATION REQUIRED OPERATIONAL: {payload['migration_required_operational_count']}")
    print(f"PLACEHOLDERS: {payload['placeholder_count']}")
    print(f"CONSOLIDATION COMPLETE: {payload['consolidation_complete']}")
    print(f"OUTPUT: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
