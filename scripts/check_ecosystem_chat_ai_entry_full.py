#!/usr/bin/env python3
"""Run the standard AI Entry aggregate plus final readiness checks."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]

COMMANDS: tuple[tuple[str, ...], ...] = (
    (sys.executable, "scripts/check_ecosystem_chat_ai_entry.py"),
    (sys.executable, "scripts/check_ai_entry_green_run_readiness.py"),
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
    print("ECOSYSTEM_CHAT_AI_ENTRY_FULL_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
