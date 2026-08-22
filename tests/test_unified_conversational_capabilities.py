from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "unified-conversational-capabilities.json"


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_one_primary_surface_and_no_competing_chat_stacks() -> None:
    data = load_contract()
    assert data["primary_surface"] == "ecosystem-chat.html"
    assert data["shared_runtime_owner"] == "StegVerse-org/LLM-adapter"
    assert [c["id"] for c in data["capabilities"]] == [
        "general_ecosystem",
        "vacc_va",
        "mathematics_educator",
        "hil_experiment",
    ]
    assert all(c["consumes_primary_surface"] is True for c in data["capabilities"])
    assert all(c["alternate_primary_chat_allowed"] is False for c in data["capabilities"])


def test_specialty_contracts_preserve_required_boundaries() -> None:
    data = load_contract()
    by_id = {item["id"]: item for item in data["capabilities"]}
    assert by_id["vacc_va"]["source_policy"] == "ADMITTED_OFFICIAL_VA_ONLY_FOR_EXTERNAL_FACTUAL_CLAIMS"
    assert by_id["vacc_va"]["runtime_owner"] == "StegVerse-org/LLM-adapter"
    assert by_id["mathematics_educator"]["image_transcription_must_be_correctable"] is True
    assert by_id["hil_experiment"]["experiment_specific_surface_allowed"] is True
    assert data["authority_effect"] == "NONE"
    assert data["activation_effect"] is False


def test_false_completion_is_explicitly_rejected() -> None:
    semantics = load_contract()["completion_semantics"]
    assert semantics["static_surface_is_complete"] is False
    assert semantics["task_assignment_is_complete"] is False
    assert semantics["ci_pass_is_runtime"] is False
    assert semantics["handoff_is_activation"] is False
    assert semantics["product_complete_requires_deployed_execution_evidence"] is True
