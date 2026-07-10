#!/usr/bin/env python3
"""Validate fixture-bound provider, quota, cost, latency, fallback, and usage display."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "ecosystem-chat" / "provider-status.example.json"
SCRIPT = ROOT / "assets" / "ecosystem-chat-provider.js"
LOADER = ROOT / "assets" / "ecosystem-chat-hps.js"


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    for path in (FIXTURE, SCRIPT, LOADER):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    required = {"payload_type", "preview_only", "live_invocation", "authority_granted", "execution_enabled", "receipt_issued_by_site", "pricing_current", "provider", "quota", "usage", "cost", "latency", "display"}
    missing = sorted(required - set(data))
    if missing:
        return fail("fixture missing: " + ", ".join(missing))

    expected = {
        "payload_type": "provider_status_preview",
        "preview_only": True,
        "live_invocation": False,
        "authority_granted": False,
        "execution_enabled": False,
        "receipt_issued_by_site": False,
        "pricing_current": False,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            return fail(f"{key} must equal {value!r}")

    quota = data.get("quota", {})
    for key in ("limit", "used", "remaining", "trial_total_limit", "trial_total_used"):
        if not isinstance(quota.get(key), int) or quota[key] < 0:
            return fail(f"quota.{key} must be non-negative integer")
    if quota["used"] + quota["remaining"] != quota["limit"]:
        return fail("daily quota arithmetic mismatch")
    if quota["trial_total_used"] > quota["trial_total_limit"]:
        return fail("trial usage exceeds limit")

    usage = data.get("usage", {})
    for key in ("requests", "input_units", "output_units", "billable_units"):
        if not isinstance(usage.get(key), int) or usage[key] < 0:
            return fail(f"usage.{key} must be non-negative integer")
    if usage.get("billable_units") != 0:
        return fail("preview fixture must not claim billable usage")

    cost = data.get("cost", {})
    if cost.get("estimated") != 0.0 or cost.get("billed") != 0.0:
        return fail("preview fixture cost must remain zero")
    if cost.get("pricing_source") != "fixture_only_not_current":
        return fail("pricing source must explicitly remain non-current")

    latency = data.get("latency", {})
    if latency.get("provider_ms") is not None:
        return fail("provider latency must be null when provider was not invoked")

    script = SCRIPT.read_text(encoding="utf-8")
    required_script = [
        "provider-status.example.json",
        "data.live_invocation === false",
        "data.pricing_current === false",
        "No model is invoked",
        "not current pricing",
        "billable_units",
        "provider_ms",
        "receipt=not-issued",
        "authority=none",
        "failClosed",
    ]
    for phrase in required_script:
        if phrase not in script:
            return fail(f"renderer missing: {phrase}")

    loader = LOADER.read_text(encoding="utf-8")
    if "assets/ecosystem-chat-provider.js" not in loader:
        return fail("provider renderer is not loaded by Ecosystem Chat")

    print("PASS: provider status preview is fixture-bound, zero-billable, and non-authorizing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
