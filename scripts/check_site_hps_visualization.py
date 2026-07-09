#!/usr/bin/env python3
"""Validate Site HPS visualization preview artifacts.

The checker enforces that Site HPS visualization remains preview-only and does
not claim authority, execution, or Site-issued receipts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "ecosystem-chat" / "hps-visualization-status.example.json"
DOC = ROOT / "docs" / "hps" / "ecosystem-chat-visualization.md"

REQUIRED_TOP = {
    "payload_type",
    "preview_only",
    "authority_granted",
    "execution_enabled",
    "receipt_issued_by_site",
    "heartbeat",
    "standing",
    "capabilities",
    "continuity",
    "display",
}


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("fixture root must be an object")
    return data


def main() -> int:
    if not DOC.exists():
        return fail("missing docs/hps/ecosystem-chat-visualization.md")
    if not FIXTURE.exists():
        return fail("missing fixtures/ecosystem-chat/hps-visualization-status.example.json")

    payload = load_json(FIXTURE)
    missing = sorted(REQUIRED_TOP - set(payload.keys()))
    if missing:
        return fail(f"missing fixture fields: {', '.join(missing)}")

    if payload.get("payload_type") != "hps_visualization_status":
        return fail("payload_type must be hps_visualization_status")
    if payload.get("preview_only") is not True:
        return fail("preview_only must be true")
    if payload.get("authority_granted") is not False:
        return fail("authority_granted must be false")
    if payload.get("execution_enabled") is not False:
        return fail("execution_enabled must be false")
    if payload.get("receipt_issued_by_site") is not False:
        return fail("receipt_issued_by_site must be false")

    standing = payload.get("standing", {})
    if standing.get("class") not in {"RESTORED", "DEGRADED", "FAILED"}:
        return fail("standing.class must be RESTORED, DEGRADED, or FAILED")
    if not isinstance(standing.get("score"), (int, float)):
        return fail("standing.score must be numeric")

    caps = payload.get("capabilities", {})
    for key in ("open", "closed", "expired"):
        if not isinstance(caps.get(key), list):
            return fail(f"capabilities.{key} must be a list")

    continuity = payload.get("continuity", {})
    if continuity.get("replay_available") is not True:
        return fail("fixture should show replay availability as a displayed field")
    if continuity.get("reconstruction_available") is not True:
        return fail("fixture should show reconstruction availability as a displayed field")
    if not continuity.get("chain_head"):
        return fail("continuity.chain_head is required")

    doc_text = DOC.read_text(encoding="utf-8")
    required_phrases = [
        "Site HPS visualization is not authority",
        "Site HPS visualization is not execution",
        "preview-only",
        "HPS visualization is not a generic status light",
    ]
    for phrase in required_phrases:
        if phrase not in doc_text:
            return fail(f"missing doc phrase: {phrase}")

    print("PASS: Site HPS visualization preview artifacts are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
