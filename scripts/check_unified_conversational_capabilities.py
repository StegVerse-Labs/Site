#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "unified-conversational-capabilities.json"
HANDOFF = ROOT / "docs" / "UNIFIED_CONVERSATIONAL_CAPABILITY_MIRROR_HANDOFF.md"
EXPECTED_IDS = ["general_ecosystem", "vacc_va", "mathematics_educator", "hil_experiment"]


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if data.get("schema") != "stegverse.site.unified-conversational-capability.v1":
        fail("schema mismatch")
    if data.get("primary_surface") != "ecosystem-chat.html":
        fail("primary surface must be ecosystem-chat.html")
    if data.get("shared_runtime_owner") != "StegVerse-org/LLM-adapter":
        fail("shared runtime owner mismatch")
    if data.get("authority_effect") != "NONE" or data.get("activation_effect") is not False:
        fail("contract must not grant authority or activation")
    semantics = data.get("completion_semantics") or {}
    for key in ("static_surface_is_complete", "task_assignment_is_complete", "ci_pass_is_runtime", "handoff_is_activation"):
        if semantics.get(key) is not False:
            fail(f"false-completion semantic violated: {key}")
    if semantics.get("product_complete_requires_deployed_execution_evidence") is not True:
        fail("deployed execution evidence must be required")
    capabilities = data.get("capabilities")
    if not isinstance(capabilities, list):
        fail("capabilities must be a list")
    ids = [item.get("id") for item in capabilities if isinstance(item, dict)]
    if ids != EXPECTED_IDS:
        fail(f"capability ids/order mismatch: {ids}")
    for item in capabilities:
        if item.get("consumes_primary_surface") is not True:
            fail(f"{item.get('id')} must consume primary surface")
        if item.get("alternate_primary_chat_allowed") is not False:
            fail(f"{item.get('id')} must not create competing primary chat")
        evidence = item.get("required_completion_evidence")
        if not isinstance(evidence, list) or not evidence:
            fail(f"{item.get('id')} missing completion evidence contract")
    vacc = capabilities[1]
    if vacc.get("source_policy") != "ADMITTED_OFFICIAL_VA_ONLY_FOR_EXTERNAL_FACTUAL_CLAIMS":
        fail("VACC source policy mismatch")
    math = capabilities[2]
    if math.get("image_transcription_must_be_correctable") is not True:
        fail("math image transcription correction boundary missing")
    hil = capabilities[3]
    if hil.get("experiment_specific_surface_allowed") is not True:
        fail("HIL experiment surface exception missing")
    handoff = HANDOFF.read_text(encoding="utf-8")
    for needle in ("TASK-2026-0007", "ecosystem-chat.html", "general_ecosystem", "vacc_va", "mathematics_educator", "hil_experiment"):
        if needle not in handoff:
            fail(f"handoff missing {needle}")
    print("UNIFIED_CONVERSATIONAL_CAPABILITIES_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
