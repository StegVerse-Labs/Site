#!/usr/bin/env python3
"""Validate Site HPS visualization preview artifacts and public surface wiring."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "ecosystem-chat" / "hps-visualization-status.example.json"
DOC = ROOT / "docs" / "hps" / "ecosystem-chat-visualization.md"
PAGE = ROOT / "ecosystem-chat.html"
SCRIPT = ROOT / "assets" / "ecosystem-chat-hps.js"

REQUIRED_TOP = {
    "payload_type", "preview_only", "authority_granted", "execution_enabled",
    "receipt_issued_by_site", "heartbeat", "standing", "capabilities",
    "continuity", "display",
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


def require_text(path: Path, phrases: list[str]) -> int | None:
    body = path.read_text(encoding="utf-8")
    for phrase in phrases:
        if phrase not in body:
            return fail(f"{path.relative_to(ROOT)} missing required phrase: {phrase}")
    return None


def main() -> int:
    for path in (DOC, FIXTURE, PAGE, SCRIPT):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    payload = load_json(FIXTURE)
    missing = sorted(REQUIRED_TOP - set(payload))
    if missing:
        return fail(f"missing fixture fields: {', '.join(missing)}")

    expected = {
        "payload_type": "hps_visualization_status",
        "preview_only": True,
        "authority_granted": False,
        "execution_enabled": False,
        "receipt_issued_by_site": False,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            return fail(f"{key} must equal {value!r}")

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
        return fail("fixture should display replay availability")
    if continuity.get("reconstruction_available") is not True:
        return fail("fixture should display reconstruction availability")
    if not continuity.get("chain_head"):
        return fail("continuity.chain_head is required")

    result = require_text(DOC, [
        "Site HPS visualization is not authority",
        "Site HPS visualization is not execution",
        "preview-only",
        "HPS visualization is not a generic status light",
    ])
    if result is not None:
        return result

    result = require_text(PAGE, [
        'id="hps-preview"',
        'id="hpsVisualization"',
        "Fixture-bound HPS visualization only",
        "not authority, not execution, not a live receipt",
        'src="assets/ecosystem-chat-hps.js"',
    ])
    if result is not None:
        return result

    result = require_text(SCRIPT, [
        "hps-visualization-status.example.json",
        "payload.preview_only === true",
        "payload.authority_granted === false",
        "payload.execution_enabled === false",
        "payload.receipt_issued_by_site === false",
        "setFailClosed",
        "site_receipt=not-issued",
        "execution=disabled",
        "replay_available",
        "reconstruction_available",
        "chain_head",
    ])
    if result is not None:
        return result

    print("PASS: Site HPS visualization is visible, fixture-bound, and fail-closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
