#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "governance" / "site-mirror-orchestration.md"
STATUS = ROOT / "static" / "status" / "site-mirror-orchestration.json"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
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
    if "This file is the current handoff and task source of truth for `StegVerse-Labs/Site`." not in handoff:
        raise SystemExit("SITE MIRROR ORCHESTRATION: FAIL - current handoff source marker missing")
    current_goal_markers = (
        "## Current goal",
        "Goal: fully functional governed Ecosystem Chat / Ecosystem Node request-response",
        "provider",
        "persistence",
        "custody",
        "reconstruction",
        "immutable receipt",
        "Site activation",
        "downstream propagation",
        "Primary surface: ecosystem-chat.html",
        "Manual user action required for routine repository work: false",
    )
    missing_goal_markers = [marker for marker in current_goal_markers if marker not in handoff]
    if missing_goal_markers:
        raise SystemExit(
            "SITE MIRROR ORCHESTRATION: FAIL - current handoff goal markers missing: "
            + ", ".join(missing_goal_markers)
        )
    if "READY_FOR_ACTIVATION_AFTER_UPSTREAM_GATES" not in plan:
        raise SystemExit("SITE MIRROR ORCHESTRATION: FAIL - repo standards plan not ready")
    if data.get("status") != "SITE_MIRROR_ORCHESTRATION_PREPARED":
        raise SystemExit("SITE MIRROR ORCHESTRATION: FAIL - status artifact not prepared")
    if len(data.get("workstreams", [])) < 2:
        raise SystemExit("SITE MIRROR ORCHESTRATION: FAIL - expected at least two workstreams")

    print("SITE MIRROR ORCHESTRATION: PASS")
    print("current_goal_contract=CANONICAL_MARKER_SET")
    print("mirror_authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
