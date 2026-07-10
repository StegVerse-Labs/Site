#!/usr/bin/env python3
"""Consolidated task runner for StegVerse-Labs/Site."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]


def run(command: Iterable[str], *, cwd: Path = ROOT, optional: bool = False) -> None:
    command = list(command)
    label = " ".join(command)
    print(f"::group::{label}")
    try:
        completed = subprocess.run(command, cwd=str(cwd), check=False)
    finally:
        print("::endgroup::")
    if completed.returncode != 0 and not optional:
        raise SystemExit(completed.returncode)
    if completed.returncode != 0:
        print(f"optional command failed and was skipped: {label}")


def run_if_present(script: str, *, optional: bool = False) -> None:
    path = ROOT / script
    if not path.exists():
        if optional:
            print(f"optional script missing: {script}")
            return
        raise SystemExit(f"required script missing: {script}")
    run([sys.executable, script], optional=optional)


def validate() -> None:
    run_if_present("scripts/check_ecosystem_chat_application.py")
    run_if_present("scripts/check_ecosystem_chat_boundary.py")
    run_if_present("scripts/check_ecosystem_chat_traversal.py")
    run_if_present("scripts/check_ecosystem_chat_provider_status.py")
    run_if_present("scripts/check_ecosystem_chat_solver_response.py")
    run_if_present("scripts/check_site_hps_visualization.py")
    run_if_present("scripts/check_site_unified_governed_experience.py")
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
    import json
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
        raise SystemExit(1)
    print("TEST READINESS PASSED")


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
        "scripts/check_site_final_activation_pending.py",
        "scripts/check_site_governed_ecosystem_mirror.py",
        "scripts/check_site_mirror_handoff_final_pending.py",
    ):
        run_if_present(script)


def live_url() -> None:
    run_if_present("scripts/check_site_governed_ecosystem_live_url.py")


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
    "all-local": all_local,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run declared Site repository task.")
    parser.add_argument("task", choices=sorted(TASKS), help="Declared task to run")
    args = parser.parse_args()
    os.chdir(ROOT)
    TASKS[args.task]()


if __name__ == "__main__":
    main()
