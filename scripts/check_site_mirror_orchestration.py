#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "governance" / "site-mirror-orchestration.md"
STATUS = ROOT / "static" / "status" / "site-mirror-orchestration.json"
HANDOFF = ROOT / "SITE_MIRROR_HANDOFF.md"
PLAN = ROOT / "docs" / "governance" / "repo-standards-site-mirror-plan.md"


def read(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"SITE MIRROR ORCHESTRATION: FAIL - missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    doc = read(DOC)
    handoff = read(HANDOFF)
    plan = read(PLAN)
    data = json.loads(read(STATUS))

    if "SITE_MIRROR_ORCHESTRATION_PREPARED" not in doc:
        raise SystemExit("SITE MIRROR ORCHESTRATION: FAIL - doc status missing")
    if "Goal 3" not in handoff:
        raise SystemExit("SITE MIRROR ORCHESTRATION: FAIL - existing handoff not preserved")
    if "READY_FOR_ACTIVATION_AFTER_UPSTREAM_GATES" not in plan:
        raise SystemExit("SITE MIRROR ORCHESTRATION: FAIL - repo standards plan not ready")
    if data.get("status") != "SITE_MIRROR_ORCHESTRATION_PREPARED":
        raise SystemExit("SITE MIRROR ORCHESTRATION: FAIL - status artifact not prepared")
    if len(data.get("workstreams", [])) < 2:
        raise SystemExit("SITE MIRROR ORCHESTRATION: FAIL - expected at least two workstreams")

    print("SITE MIRROR ORCHESTRATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
