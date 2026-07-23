#!/usr/bin/env python3
"""Static browser-behavior contract check for the direct governed value panel."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "ecosystem-chat-value-browser-behavior.fixture.json"
INTEGRATION = ROOT / "assets" / "ecosystem-chat-value-integration.js"
HPS = ROOT / "assets" / "ecosystem-chat-hps.js"


def main() -> int:
    errors: list[str] = []
    if not FIXTURE.exists():
        errors.append("missing browser behavior fixture")
    if not INTEGRATION.exists():
        errors.append("missing value integration script")
    if not HPS.exists():
        errors.append("missing Ecosystem Node loader")
    if errors:
        print("ECOSYSTEM_CHAT_VALUE_BROWSER_BEHAVIOR_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    integration = INTEGRATION.read_text(encoding="utf-8")
    loader = HPS.read_text(encoding="utf-8")
    if payload.get("authority_effect") != "NONE":
        errors.append("fixture authority_effect must be NONE")
    if payload.get("surface") != "ecosystem-chat.html":
        errors.append("fixture surface must be ecosystem-chat.html")
    if "assets/ecosystem-chat-value-integration.js" not in loader:
        errors.append("Ecosystem Node loader does not load value integration")

    behaviors = payload.get("behaviors")
    if not isinstance(behaviors, list) or not behaviors:
        errors.append("behaviors must be non-empty")
    else:
        ids: set[str] = set()
        for behavior in behaviors:
            behavior_id = behavior.get("id")
            if not isinstance(behavior_id, str) or not behavior_id:
                errors.append("behavior id required")
                continue
            if behavior_id in ids:
                errors.append(f"duplicate behavior id: {behavior_id}")
            ids.add(behavior_id)
            if behavior.get("required") is not True:
                errors.append(f"{behavior_id}: required must be true")
            markers = behavior.get("markers")
            if not isinstance(markers, list) or not markers:
                errors.append(f"{behavior_id}: markers required")
                continue
            for marker in markers:
                if marker not in integration:
                    errors.append(f"{behavior_id}: integration missing marker {marker}")

    if errors:
        print("ECOSYSTEM_CHAT_VALUE_BROWSER_BEHAVIOR_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"ECOSYSTEM_CHAT_VALUE_BROWSER_BEHAVIOR_CHECK=PASS")
    print(f"behaviors={len(behaviors)}")
    print("surface=ecosystem-chat.html")
    print("browser_execution=NOT_OBSERVED")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
