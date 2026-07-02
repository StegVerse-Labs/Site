#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    [sys.executable, "scripts/check_site_mirror_orchestration.py"],
    [sys.executable, "scripts/check_site_navigation_discovery.py"],
]


def main() -> int:
    for command in COMMANDS:
        result = subprocess.run(command, cwd=ROOT, text=True)
        if result.returncode != 0:
            print("SITE MIRROR READINESS: FAIL")
            return result.returncode
    print("SITE MIRROR READINESS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
