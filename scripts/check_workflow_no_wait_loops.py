#!/usr/bin/env python3
"""Ratchet: no Site workflow sleeps while waiting on, polling or retrying another machine.

Owner direction on StegVerse-Labs/.github#3106: no external machine is awaited and every action is
bound to a state transition. A workflow that needs a deployed page runs on the deployment's
completion (``workflow_run`` of ``pages-build-deployment``) and makes one attempt; a refused push
fails closed with the re-run as its retry edge.

PENDING lists workflows that still sleep and are being converted lane by lane. The check fails when
any other workflow sleeps, and when a PENDING workflow no longer sleeps (remove it from the list),
so the list can only shrink.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
SLEEP = re.compile(r"^\s*[^#\s].*\bsleep\s+[\d$]|^\s*sleep\s+[\d$]")

PENDING = {
    "conectrr-live-verification.yml",
    "entity-economy-volume-ii-public-observation.yml",
    "stegmusic-browser-execution.yml",
    "stegmusic-live-verification.yml",
    "stegos-device-root-race-public-observation.yml",
    "stegos-node-public-observation.yml",
    "validate.yml",
}


def sleeping_workflows() -> set[str]:
    found = set()
    for path in sorted(WORKFLOWS.glob("*.y*ml")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.lstrip().startswith("#") and SLEEP.search(line):
                found.add(path.name)
                break
    return found


def main() -> int:
    sleeping = sleeping_workflows()
    failures = [f"{name} sleeps while waiting or retrying; bind it to a state transition" for name in sorted(sleeping - PENDING)]
    failures += [f"{name} no longer sleeps; remove it from PENDING" for name in sorted(PENDING - sleeping)]
    print("WORKFLOW_NO_WAIT_LOOPS=" + ("FAIL" if failures else "PASS") + f" pending={len(PENDING & sleeping)}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
