#!/usr/bin/env python3
"""Run green-data packet validation."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    completed = subprocess.run(
        [sys.executable, "scripts/check_ai_entry_activation_proposal.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout.rstrip())
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    print("AI_ENTRY_GREEN_DATA_PACKET_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
