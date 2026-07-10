#!/usr/bin/env python3
"""Validate the fixture-bound governed math-solver response preview."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "ecosystem-chat" / "solver-response.example.json"
SCRIPT = ROOT / "assets" / "ecosystem-chat-solver.js"
LOADER = ROOT / "assets" / "ecosystem-chat-hps.js"


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    for path in (FIXTURE, SCRIPT, LOADER):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    required = {
        "payload_type", "preview_only", "live_solver_execution",
        "authority_granted", "execution_enabled", "receipt_issued_by_site",
        "request", "result", "proof_steps", "verification", "limits", "display",
    }
    missing = sorted(required - set(data))
    if missing:
        return fail("fixture missing: " + ", ".join(missing))

    expected = {
        "payload_type": "solver_response_preview",
        "preview_only": True,
        "live_solver_execution": False,
        "authority_granted": False,
        "execution_enabled": False,
        "receipt_issued_by_site": False,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            return fail(f"{key} must equal {value!r}")

    proof_steps = data.get("proof_steps")
    if not isinstance(proof_steps, list) or not proof_steps:
        return fail("proof_steps must be a non-empty list")
    indexes = [step.get("index") for step in proof_steps if isinstance(step, dict)]
    if indexes != list(range(1, len(proof_steps) + 1)):
        return fail("proof step indexes must be sequential from 1")
    for step in proof_steps:
        for key in ("statement", "operation", "result"):
            if not isinstance(step.get(key), str) or not step[key].strip():
                return fail(f"proof step missing {key}")

    verification = data.get("verification", {})
    if verification.get("passed") is not True:
        return fail("fixture verification must pass")
    if verification.get("left_value") != verification.get("right_value"):
        return fail("verification values must match")
    if verification.get("independent_engine") is not False:
        return fail("fixture must not claim independent engine verification")

    limits = data.get("limits", {})
    if limits.get("operation_allowlisted") is not True:
        return fail("operation must be allowlisted")
    if limits.get("resource_limit_applied") is not True:
        return fail("resource limit must be applied")
    if not isinstance(limits.get("max_steps"), int) or limits["max_steps"] <= 0:
        return fail("max_steps must be positive integer")
    if limits.get("steps_used") != len(proof_steps):
        return fail("steps_used must equal proof step count")
    if limits["steps_used"] > limits["max_steps"]:
        return fail("fixture exceeds max_steps")

    script = SCRIPT.read_text(encoding="utf-8")
    required_script = [
        "solver-response.example.json",
        "data.live_solver_execution === false",
        "data.authority_granted === false",
        "data.execution_enabled === false",
        "data.receipt_issued_by_site === false",
        "Fixture exceeded declared resource limits",
        "Fixture verification did not pass",
        "independent engine",
        "live_solver_execution=false",
        "receipt=not-issued",
        "authority=none",
        "failClosed",
    ]
    for phrase in required_script:
        if phrase not in script:
            return fail(f"renderer missing: {phrase}")

    loader = LOADER.read_text(encoding="utf-8")
    if "assets/ecosystem-chat-solver.js" not in loader:
        return fail("solver renderer is not loaded by Ecosystem Chat")

    print("PASS: solver response preview is verified, resource-bounded, and non-authorizing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
