#!/usr/bin/env python3
"""Run full AI Entry validation plus cohesive application surface checks."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]

COMMANDS: tuple[tuple[str, ...], ...] = (
    (sys.executable, "scripts/check_ecosystem_chat_ai_entry_full.py"),
    (sys.executable, "scripts/check_ai_entry_ui_activation_status.py"),
    (sys.executable, "scripts/check_ai_entry_application_page.py"),
    (sys.executable, "scripts/check_ai_entry_application_completion.py"),
    (sys.executable, "scripts/check_ai_entry_backend_activation_boundary.py"),
    (sys.executable, "scripts/check_ai_entry_activation_routes.py"),
    (sys.executable, "scripts/check_ai_entry_backend_activation_fixtures.py"),
    (sys.executable, "scripts/check_ai_entry_ui_activation_routes.py"),
    (sys.executable, "scripts/check_ai_entry_backend_activation_progress.py"),
    (sys.executable, "scripts/check_ai_entry_ci_visibility.py"),
    (sys.executable, "scripts/check_ai_entry_authority_service_boundary.py"),
    (sys.executable, "scripts/check_ai_entry_authority_decision_fixtures.py"),
    (sys.executable, "scripts/check_ai_entry_operator_recoverability_boundary.py"),
    (sys.executable, "scripts/check_ai_entry_recovery_state_fixtures.py"),
    (sys.executable, "scripts/check_ai_entry_recovery_completion.py"),
    (sys.executable, "scripts/check_ai_entry_cross_repo_handoff.py"),
    (sys.executable, "scripts/check_ai_entry_green_run_visibility_consolidation.py"),
    (sys.executable, "scripts/check_ai_entry_release_readiness_lockfile.py"),
    (sys.executable, "scripts/check_ai_entry_tag_gate.py"),
    (sys.executable, "scripts/check_ai_entry_final_handoff_index.py"),
    (sys.executable, "scripts/check_ai_entry_next_path_gate.py"),
)


def run(command: Sequence[str]) -> None:
    completed = subprocess.run(
        list(command),
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print("$ " + " ".join(command))
    print(completed.stdout.rstrip())
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> int:
    for command in COMMANDS:
        run(command)
    print("ECOSYSTEM_CHAT_APPLICATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
