#!/usr/bin/env python3
"""Validate the provider-neutral Ecosystem Visual Render transport source contract."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST_SCHEMA = ROOT / "schemas" / "ecosystem-visual-render-request.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas" / "ecosystem-visual-render-receipt.schema.json"
TRANSPORT = ROOT / "assets" / "ecosystem-visual-render-transport.js"
TEST = ROOT / "tests" / "ecosystem-visual-render-transport.test.cjs"
HANDOFF = ROOT / "docs" / "ECOSYSTEM_VISUAL_RENDER_TRANSPORT_MIRROR_HANDOFF.md"
PREFLIGHT = ROOT / "docs" / "ECOSYSTEM_VISUAL_RENDER_TRANSPORT_PREFLIGHT.md"
README = ROOT / "README.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ECOSYSTEM_VISUAL_RENDER_TRANSPORT_FAIL: {message}")


def main() -> int:
    for path in (REQUEST_SCHEMA, RECEIPT_SCHEMA, TRANSPORT, TEST, HANDOFF, PREFLIGHT, README):
        require(path.is_file() and path.stat().st_size > 0, f"missing required source: {path.relative_to(ROOT)}")

    request = json.loads(REQUEST_SCHEMA.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    transport = TRANSPORT.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    preflight = PREFLIGHT.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    require(request.get("properties", {}).get("schema", {}).get("const") == "stegverse.ecosystem_visual_render_request/v1", "request schema id mismatch")
    require(receipt.get("properties", {}).get("schema", {}).get("const") == "stegverse.ecosystem_visual_render_receipt/v1", "receipt schema id mismatch")

    for marker in (
        'renderer_role: RENDERER_ROLE',
        'renderer_may_mutate_canonical_events: false',
        'renderer_may_grant_admission: false',
        'renderer_may_invent_evidence: false',
        'renderer_may_authorize_credentials: false',
        'renderer_may_publish_state: false',
        'canonical_event_mutation',
        'admission_granted',
        'custody_authority',
        'execution_authority',
        'projection hash mismatch',
        'receipt request hash mismatch',
        'receipt capability escalation',
    ):
        require(marker in transport, f"transport marker missing: {marker}")

    for prohibited in (
        "CLOUDFLARE_API_TOKEN",
        "GITHUB_TOKEN",
        "GH_TOKEN",
        "RENDER_API_KEY",
        "VERCEL_TOKEN",
        "Authorization: Bearer",
    ):
        require(prohibited not in transport, f"prohibited credential/runtime marker present: {prohibited}")

    require("Decision: `PASS / ADMIT_ON_CURRENT_MAIN_SUCCESSOR_BRANCH`" in preflight, "machine preflight PASS missing")
    require("README_UPDATE_REQUIRED" in preflight, "README completeness decision missing")
    require("README.md" in handoff, "handoff does not bind README completeness")
    require("Ecosystem visual render transport" in readme, "README transport interface documentation missing")
    require("PROJECTION_ONLY" in readme, "README renderer authority boundary missing")

    completed = subprocess.run(
        ["node", str(TEST)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="")
    require(completed.returncode == 0, "Node transport tests failed")

    print("ECOSYSTEM_VISUAL_RENDER_TRANSPORT_PASS")
    print("README_COMPLETENESS=PASS")
    print("CREDENTIAL_REQUIREMENT=NONE")
    print("RENDERER_ROLE=PROJECTION_ONLY")
    print("AUTHORITY_EFFECT=NONE")
    print("ACTIVATION_EFFECT=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
