#!/usr/bin/env python3
"""Consolidated task runner for StegVerse-Labs/Site."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC_PATH = ROOT / "reports" / "site-task-diagnostic.json"
CURRENT_TASK = "unknown"
COMPLETED_VALIDATORS: list[str] = []
DIAGNOSTIC_WRITTEN = False


def write_diagnostic(
    *,
    status: str,
    failed_validator: str | None = None,
    exit_code: int = 0,
    failure_class: str | None = None,
    detail: str | None = None,
) -> None:
    global DIAGNOSTIC_WRITTEN
    payload = {
        "schema_version": "1.0.0",
        "receipt_type": "site_task_diagnostic",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task": CURRENT_TASK,
        "status": status,
        "failed_validator": failed_validator,
        "validator_index": (
            len(COMPLETED_VALIDATORS) + 1 if failed_validator is not None else None
        ),
        "exit_code": exit_code,
        "completed_validators": COMPLETED_VALIDATORS,
        "failure_class": failure_class,
        "detail": detail,
        "authority_effect": "NONE",
        "site_mode": "PREVIEW_ONLY",
        "state_change_authorized": False,
    }
    DIAGNOSTIC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DIAGNOSTIC_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    DIAGNOSTIC_WRITTEN = True
    print(f"SITE TASK DIAGNOSTIC: {DIAGNOSTIC_PATH.relative_to(ROOT)}")


def run(command: Iterable[str], *, cwd: Path = ROOT, optional: bool = False) -> None:
    command = list(command)
    label = " ".join(command)
    print(f"::group::{label}")
    output_lines: list[str] = []
    try:
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        assert process.stdout is not None
        for line in process.stdout:
            output_lines.append(line)
            print(line, end="")
        returncode = process.wait()
    finally:
        print("::endgroup::")

    if returncode != 0 and not optional:
        detail = "".join(output_lines)[-4000:].strip() or "validator returned nonzero"
        write_diagnostic(
            status="FAILED",
            failed_validator=label,
            exit_code=returncode,
            failure_class="VALIDATION_FAILURE",
            detail=detail,
        )
        print(f"::error title=Site validator failed::{label} exited with {returncode}")
        raise SystemExit(returncode)
    if returncode != 0:
        print(f"optional command failed and was skipped: {label}")
        return
    COMPLETED_VALIDATORS.append(label)


def run_if_present(script: str, *, optional: bool = False) -> None:
    path = ROOT / script
    if not path.exists():
        if optional:
            print(f"optional script missing: {script}")
            return
        write_diagnostic(
            status="FAILED",
            failed_validator=script,
            exit_code=1,
            failure_class="MISSING_REQUIRED_VALIDATOR",
            detail=f"required script missing: {script}",
        )
        print(f"::error file={script},title=Required Site validator missing::{script}")
        raise SystemExit(1)
    run([sys.executable, script], optional=optional)


def validate() -> None:
    run_if_present("scripts/check_ecosystem_chat_application.py")
    run_if_present("scripts/check_ecosystem_chat_boundary.py")
    run_if_present("scripts/check_ecosystem_chat_traversal.py")
    run_if_present("scripts/check_ecosystem_chat_provider_status.py")
    run_if_present("scripts/check_ecosystem_chat_solver_response.py")
    run_if_present("scripts/check_ecosystem_chat_authority_handshake.py")
    run_if_present("scripts/check_ecosystem_chat_positive_authority.py")
    run_if_present("scripts/check_ecosystem_chat_execution_transition.py")
    run_if_present("scripts/check_ecosystem_chat_receipt_envelopes.py")
    run_if_present("scripts/check_site_hps_visualization.py")
    run_if_present("scripts/check_site_unified_governed_experience.py")
    run_if_present("scripts/check_documentation_mesh_status.py")
    run_if_present("scripts/check_governed_transition_observatory.py")
    run_if_present("scripts/check_governed_transition_index_import.py")
    run_if_present("scripts/check_site_task_diagnostic_contract.py")
    run_if_present("scripts/check_repo_operations_repair_queue.py")
    run_if_present("scripts/check_site_workflow_inventory.py")
    test_readiness()


def test_readiness() -> None:
    failures: list[str] = []
    if not any((ROOT / name).exists() for name in ("README.md", "README.MD")):
        failures.append("missing README.md")
    workflows = ROOT / ".github" / "workflows"
    if workflows.exists():
        bad = sorted(p.name for p in workflows.glob("*.ym"))
        if bad:
            failures.append("workflow files must end in .yml or .yaml: " + ", ".join(bad))
    for path in sorted(ROOT.rglob("*.json")):
        if any(part in {".git", "node_modules", ".venv", "venv"} for part in path.parts):
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")
    if failures:
        print("TEST READINESS FAILED")
        for failure in failures:
            print(f"- {failure}")
        write_diagnostic(
            status="FAILED",
            failed_validator="test-readiness",
            exit_code=1,
            failure_class="TEST_READINESS_FAILURE",
            detail="; ".join(failures),
        )
        print("::error title=Site test readiness failed::" + "; ".join(failures))
        raise SystemExit(1)
    print("TEST READINESS PASSED")
    COMPLETED_VALIDATORS.append("test-readiness")


def mirror_readiness() -> None:
    run_if_present("scripts/check_site_mirror_full_readiness.py")


def public_guard() -> None:
    for script in (
        "scripts/check_site_non_activation_mirror_status.py",
        "scripts/check_site_homepage_governed_ecosystem.py",
        "scripts/check_site_public_paths.py",
        "scripts/check_site_governed_ecosystem_public_verification.py",
        "scripts/check_site_llm_free_tier_trust.py",
        "scripts/check_site_hps_visualization.py",
        "scripts/check_ecosystem_chat_traversal.py",
        "scripts/check_ecosystem_chat_provider_status.py",
        "scripts/check_ecosystem_chat_solver_response.py",
        "scripts/check_ecosystem_chat_authority_handshake.py",
        "scripts/check_ecosystem_chat_positive_authority.py",
        "scripts/check_ecosystem_chat_execution_transition.py",
        "scripts/check_ecosystem_chat_receipt_envelopes.py",
        "scripts/check_documentation_mesh_status.py",
        "scripts/check_governed_transition_observatory.py",
        "scripts/check_governed_transition_index_import.py",
        "scripts/check_site_task_diagnostic_contract.py",
        "scripts/check_repo_operations_repair_queue.py",
        "scripts/check_site_workflow_inventory.py",
        "scripts/check_site_final_activation_pending.py",
        "scripts/check_site_governed_ecosystem_mirror.py",
        "scripts/check_site_mirror_handoff_final_pending.py",
    ):
        run_if_present(script)


def live_url() -> None:
    run_if_present("scripts/check_site_governed_ecosystem_live_url.py")
    run_if_present("scripts/check_governed_transition_live_urls.py")


def tt_status() -> None:
    run_if_present("scripts/render_tt_code_representation_status.py")
    run_if_present("scripts/check_site_tt_code_representation_mirror.py")


def external_evidence() -> None:
    run_if_present("scripts/write_site_external_evidence_state.py")


def task_elimination_guard() -> None:
    run_if_present("scripts/check_site_manual_task_elimination.py")
    run_if_present("scripts/check_site_ecosystem_management_handoff.py")


def local_completion_receipt() -> None:
    run_if_present("scripts/write_site_local_completion_receipt.py")
    run_if_present("scripts/check_site_local_completion_receipt.py")


def autonomous_continuation() -> None:
    tt_status()
    run_if_present("scripts/check_site_governance_observatory_status.py")
    external_evidence()
    run_if_present("scripts/update_site_final_goal_status.py")
    run_if_present("scripts/check_site_final_goal_status.py")
    run_if_present("scripts/check_site_final_activation_pending.py")
    task_elimination_guard()
    local_completion_receipt()


def universal_ingest() -> None:
    if not (ROOT / "ingestion" / "ingest_runner.py").exists():
        print("universal ingest skipped: ingestion/ingest_runner.py is not present")
        return
    run([sys.executable, "ingestion/ingest_runner.py"])


def import_governed_transition_index() -> None:
    run_if_present("scripts/acquire_governed_transition_index.py")
    run_if_present("scripts/check_governed_transition_index_import.py")
    run_if_present("scripts/check_governed_transition_observatory.py")


def all_local() -> None:
    validate()
    mirror_readiness()
    public_guard()
    live_url()
    autonomous_continuation()
    universal_ingest()


TASKS = {
    "validate": validate,
    "test-readiness": test_readiness,
    "mirror-readiness": mirror_readiness,
    "public-guard": public_guard,
    "live-url": live_url,
    "tt-status": tt_status,
    "external-evidence": external_evidence,
    "task-elimination-guard": task_elimination_guard,
    "local-completion-receipt": local_completion_receipt,
    "autonomous-continuation": autonomous_continuation,
    "universal-ingest": universal_ingest,
    "import-governed-transition-index": import_governed_transition_index,
    "all-local": all_local,
}


def main() -> None:
    global CURRENT_TASK
    parser = argparse.ArgumentParser(description="Run declared Site repository task.")
    parser.add_argument("task", choices=sorted(TASKS), help="Declared task to run")
    args = parser.parse_args()
    CURRENT_TASK = args.task
    os.chdir(ROOT)
    if DIAGNOSTIC_PATH.exists():
        DIAGNOSTIC_PATH.unlink()
    try:
        TASKS[args.task]()
    except SystemExit:
        if not DIAGNOSTIC_WRITTEN:
            write_diagnostic(
                status="FAILED",
                failed_validator="unresolved-task-boundary",
                exit_code=1,
                failure_class="UNRESOLVED_TASK_FAILURE",
                detail="task exited before a validator-specific diagnostic was written",
            )
        raise
    except Exception as exc:
        write_diagnostic(
            status="ERROR",
            failed_validator="unhandled-exception",
            exit_code=1,
            failure_class=type(exc).__name__,
            detail=str(exc),
        )
        print(f"::error title=Unhandled Site task exception::{type(exc).__name__}: {exc}")
        raise
    write_diagnostic(status="PASSED")


if __name__ == "__main__":
    main()
