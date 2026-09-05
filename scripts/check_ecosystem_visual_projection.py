#!/usr/bin/env python3
"""Dependency-light source verifier for the Ecosystem Chat visual projection contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "ecosystem-visual-projection.schema.json"
MODULE = ROOT / "assets" / "ecosystem-visual-projection.js"
TEST = ROOT / "tests" / "ecosystem-visual-projection.test.cjs"
FIXTURE = ROOT / "tests" / "fixtures" / "ecosystem-visual-projection" / "canonical-events.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL_CLOSED: {message}")


def main() -> None:
    for path in (SCHEMA, MODULE, TEST, FIXTURE):
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    module = MODULE.read_text(encoding="utf-8")

    require(schema.get("properties", {}).get("schema", {}).get("const") == "stegverse.ecosystem_visual_projection/v1", "schema identity mismatch")
    require(isinstance(fixture, list) and len(fixture) >= 2, "canonical event fixture is insufficient")
    require(len({event.get("event_id") for event in fixture}) == len(fixture), "fixture event ids must be unique")

    for marker in (
        'renderer_may_mutate_canonical_events: false',
        'renderer_may_grant_admission: false',
        'renderer_may_invent_evidence: false',
        'CAPABILITY_DESCRIPTOR_ONLY',
        'PROJECTION_ONLY',
    ):
        require(marker in module, f"missing authority/capability marker: {marker}")

    result = subprocess.run(
        ["node", str(TEST)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, f"node contract test failed: {result.stdout}{result.stderr}")
    print(result.stdout.strip())
    print("ecosystem visual projection source verification: PASS")


if __name__ == "__main__":
    main()
