#!/usr/bin/env python3
"""Validate the local Ecosystem Chat preview gateway module."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GATEWAY_PATH = ROOT / "backend" / "ecosystem_chat_gateway_preview.py"
INTERACTION_BANDS = ["intra", "inter", "research", "provider", "solver", "receipt"]


def load_gateway() -> Any:
    if not GATEWAY_PATH.exists():
        raise AssertionError("backend/ecosystem_chat_gateway_preview.py is missing")
    spec = importlib.util.spec_from_file_location("ecosystem_chat_gateway_preview", GATEWAY_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load preview gateway module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require_profile(result: dict[str, Any]) -> None:
    if result.get("interaction_bands") != INTERACTION_BANDS:
        raise AssertionError("gateway result must preserve canonical interaction_bands order")
    profile = result.get("interaction_profile")
    if not isinstance(profile, dict):
        raise AssertionError("gateway result must include interaction_profile object")
    for band in INTERACTION_BANDS:
        value = profile.get(band)
        if not isinstance(value, int) or not 0 <= value <= 100:
            raise AssertionError(f"interaction_profile.{band} must be integer 0..100")
    if result.get("math_solver_supported") is not True:
        raise AssertionError("gateway result must declare math_solver_supported=true")


def main() -> int:
    gateway = load_gateway()
    cases = [
        ("summarize Site state and receipt status", "Site", "preview_only"),
        ("solve 2x + 3 = 11", "Solver", "preview_only"),
        ("search current public sources for provider latency", "Unknown", "preview_only"),
        ("rotate credential", "Restricted admin", "pending_authority"),
    ]
    checked = []
    for message, expected_route, expected_status in cases:
        result = gateway.handle_preview_request({"message": message, "session_id": "check"})
        if result.get("routed_module") != expected_route:
            raise AssertionError(f"expected route {expected_route!r} for {message!r}, got {result.get('routed_module')!r}")
        if result.get("task_status") != expected_status:
            raise AssertionError(f"expected status {expected_status!r} for {message!r}, got {result.get('task_status')!r}")
        if result.get("receipt_id") is not None:
            raise AssertionError("preview gateway must not issue authority receipt_id")
        require_profile(result)
        checked.append({"message": message, "route": result.get("routed_module"), "status": result.get("task_status")})
    print(json.dumps({"ok": True, "checked": checked, "interaction_bands": INTERACTION_BANDS}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
