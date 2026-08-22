#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "unified-conversational-capabilities.json"
HANDOFF = ROOT / "docs" / "UNIFIED_CONVERSATIONAL_CAPABILITY_MIRROR_HANDOFF.md"
FOUR_APP_STATUS = ROOT / "data" / "steggate-four-app-status.json"
TWO_ENTRY_STATUS = ROOT / "data" / "two-entry-points-execution-state.json"
EXPECTED_IDS = ["general_ecosystem", "vacc_va", "mathematics_educator", "hil_experiment"]


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if data.get("schema") != "stegverse.site.unified-conversational-capability.v1": fail("schema mismatch")
    if data.get("primary_surface") != "ecosystem-chat.html": fail("primary surface must be ecosystem-chat.html")
    if data.get("shared_runtime_owner") != "StegVerse-org/LLM-adapter": fail("shared runtime owner mismatch")
    if data.get("authority_effect") != "NONE" or data.get("activation_effect") is not False: fail("contract must not grant authority or activation")
    semantics = data.get("completion_semantics") or {}
    for key in ("static_surface_is_complete", "task_assignment_is_complete", "ci_pass_is_runtime", "handoff_is_activation"):
        if semantics.get(key) is not False: fail(f"false-completion semantic violated: {key}")
    if semantics.get("product_complete_requires_deployed_execution_evidence") is not True: fail("deployed execution evidence must be required")
    capabilities = data.get("capabilities")
    if not isinstance(capabilities, list): fail("capabilities must be a list")
    ids = [item.get("id") for item in capabilities if isinstance(item, dict)]
    if ids != EXPECTED_IDS: fail(f"capability ids/order mismatch: {ids}")
    for item in capabilities:
        if item.get("consumes_primary_surface") is not True: fail(f"{item.get('id')} must consume primary surface")
        if item.get("alternate_primary_chat_allowed") is not False: fail(f"{item.get('id')} must not create competing primary chat")
        evidence = item.get("required_completion_evidence")
        if not isinstance(evidence, list) or not evidence: fail(f"{item.get('id')} missing completion evidence contract")
    by_id = {item["id"]: item for item in capabilities}
    if by_id["vacc_va"].get("source_policy") != "ADMITTED_OFFICIAL_VA_ONLY_FOR_EXTERNAL_FACTUAL_CLAIMS": fail("VACC source policy mismatch")
    if by_id["vacc_va"].get("specialty_destination") != "va-claims-chat.html": fail("VACC specialty destination mismatch")
    if by_id["mathematics_educator"].get("image_transcription_must_be_correctable") is not True: fail("math image transcription correction boundary missing")
    if by_id["mathematics_educator"].get("specialty_destination") != "math-solver/index.html": fail("mathematics specialty destination mismatch")
    if by_id["hil_experiment"].get("experiment_specific_surface_allowed") is not True: fail("HIL experiment surface exception missing")
    if by_id["hil_experiment"].get("specialty_destination") != "humans-as-interoperability-layer.html": fail("HIL specialty destination mismatch")
    four_app = json.loads(FOUR_APP_STATUS.read_text(encoding="utf-8"))
    four_topology = four_app.get("topology_semantics") or {}
    if four_topology.get("legacy_four_app_name_is_accounting_only") is not True: fail("legacy four-app status not reconciled")
    if four_topology.get("competing_primary_chat_applications") is not False: fail("legacy four-app status still permits competing primary chats")
    if four_topology.get("primary_public_conversational_surface") != data["primary_surface"]: fail("legacy four-app status primary surface mismatch")
    two_entry = json.loads(TWO_ENTRY_STATUS.read_text(encoding="utf-8"))
    two_topology = two_entry.get("topology_semantics") or {}
    if two_topology.get("legacy_two_entry_name_is_historical_accounting_only") is not True: fail("legacy two-entry status not reconciled")
    if two_topology.get("vacc_is_specialty_capability") is not True: fail("legacy two-entry status does not classify VACC as specialty")
    if two_topology.get("va_claims_chat_is_alternate_primary_chat") is not False: fail("legacy two-entry status still permits VA Claims Chat as alternate primary chat")
    if two_topology.get("primary_public_conversational_surface") != data["primary_surface"]: fail("legacy two-entry status primary surface mismatch")
    handoff = HANDOFF.read_text(encoding="utf-8")
    for needle in ("TASK-2026-0007","ecosystem-chat.html","general_ecosystem","vacc_va","mathematics_educator","hil_experiment"):
        if needle not in handoff: fail(f"handoff missing {needle}")
    print("UNIFIED_CONVERSATIONAL_CAPABILITIES_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
