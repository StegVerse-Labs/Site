#!/usr/bin/env python3
"""Validate the current public Ecosystem Chat product contract.

The public page is intentionally simple. Technical governance, route, receipt,
and runtime details remain in repository records and are not user-facing UI.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    p = ROOT / path
    if not p.is_file():
        raise AssertionError(f"missing required file: {path}")
    return p.read_text(encoding="utf-8")


def load(path: str) -> dict:
    value = json.loads(read(path))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain an object")
    return value


def main() -> int:
    page = read("ecosystem-chat.html")
    va = read("assets/ecosystem-chat-va-runtime.js")
    simple = read("assets/ecosystem-chat-simple.js")
    projection = load("api/va-claim-assistant/runtime-projection.json")
    registry = load("data/va-claim-assistant/source-registry.json")

    for token in (
        "How can I help?",
        "Ask in your own words.",
        'id="chatForm"',
        'id="messageInput"',
        'id="chatLog"',
        "VA home loan",
        "Disability claim",
        "Community Care",
        "VA health care",
        "assets/ecosystem-chat-va-runtime.js",
        "assets/ecosystem-chat-simple.js",
    ):
        if token not in page:
            raise AssertionError(f"ecosystem-chat.html missing {token!r}")

    for token in (
        "raw_shell_allowed",
        "Ecosystem LLM routing bands",
        "SDK manifest preview",
        "Heartbeat / standing visualization",
        "Restricted admin",
        "mode=local-simulation",
        "receipt=not-issued",
        "Current capability:",
        "SOURCE-GROUNDED",
    ):
        if token.lower() in page.lower():
            raise AssertionError(f"ecosystem-chat.html exposes internal term {token!r}")

    for token in (
        "validProjection",
        "COORDINATED_VA_RESOURCES_LLM",
        "ADMITTED_OFFICIAL_VA_ONLY",
        "custody_state==='RECORDED'",
        "reconstruction_state==='PASS'",
        "private_document_context:false",
        "filing_requested:false",
        "authority_escalation_rejected",
    ):
        if token not in va:
            raise AssertionError(f"VA bridge missing {token!r}")

    if "data-chat-prompt" not in simple:
        raise AssertionError("simple chat behavior missing starter-prompt support")
    if 'type="file"' in page.lower():
        raise AssertionError("private upload control exposed before activation")

    if projection.get("private_document_upload_active") is not False:
        raise AssertionError("private document upload must remain inactive")
    if projection.get("filing_active") is not False:
        raise AssertionError("filing must remain inactive")

    source_ids = {item.get("source_id") for item in registry.get("sources", []) if isinstance(item, dict) and item.get("admitted") is True}
    required_sources = {"VA-HOME-LOANS", "VA-EDUCATION", "VA-HEALTH-CARE", "VA-COMMUNITY-CARE", "VA-VRE", "VA-FAMILY-CAREGIVER", "VA-BURIAL-MEMORIAL"}
    missing = sorted(required_sources - source_ids)
    if missing:
        raise AssertionError("source registry missing admitted VA routes: " + ", ".join(missing))

    print("Ecosystem Chat product contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
