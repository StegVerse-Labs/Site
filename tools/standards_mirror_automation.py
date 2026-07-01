#!/usr/bin/env python3
"""Run site standards mirror validation automation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    [sys.executable, "tools/validate_standards_mirror.py"],
]


def run(command: list[str]) -> int:
    print("$ " + " ".join(command))
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    return result.returncode


def main() -> int:
    failures = []
    for command in COMMANDS:
        code = run(command)
        if code != 0:
            failures.append((command, code))
    if failures:
        print("DENY standards_mirror_automation_failed")
        for command, code in failures:
            print(f"- exit={code} command={' '.join(command)}")
        return 1
    print("ALLOW standards_mirror_automation_passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
