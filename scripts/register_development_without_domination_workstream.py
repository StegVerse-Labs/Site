#!/usr/bin/env python3
"""Register the paper publication workstream in Site orchestration state.

Idempotent and repository-local. This removes the false condition where a
real branch/issue/PR exists but validation halts because orchestration has not
admitted the workload.
"""
from __future__ import annotations

import json
from pathlib import Path

STATE = Path("data/site-orchestration-state.json")
TASK_ID = "SITE-0001-DEVELOPMENT-WITHOUT-DOMINATION-PUBLICATION"


def main() -> int:
    data = json.loads(STATE.read_text(encoding="utf-8"))
    active = data.setdefault("active_sequence", {}).setdefault("parallel_safe_tasks", [])
    if TASK_ID not in active:
        active.append(TASK_ID)

    data.setdefault("ownership", {})["development_without_domination_publication"] = {
        "task_id": TASK_ID,
        "owner": "issue/128",
        "branch": "publication/development-without-domination-v1",
        "pull_request": "pull/129",
        "handoff": "papers/development-without-domination/DEVELOPMENT_WITHOUT_DOMINATION_SITE_MIRROR_HANDOFF.md",
        "execution_class": "PARALLEL_SAFE",
        "observer": "scripts/observe_development_without_domination_publication.py",
        "workflow": ".github/workflows/development-without-domination-publication.yml",
    }

    STATE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"REGISTERED {TASK_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
