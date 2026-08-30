from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sv002_observation_queues_non_authorizing_event_materialization() -> None:
    js = (ROOT / "assets/sv002-observe.js").read_text(encoding="utf-8")
    required = (
        "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION",
        "DURABLE_QUEUE_OR_EVENT_EPHEMERAL_MATERIALIZATION",
        "always_on_receiver_required:false",
        "second_user_device_required:false",
        "request_grants_execution_authority:false",
        "claim_or_fence_minted:false",
        'credential_authority:"TV/TVC"',
        'github_token_runtime_authority:"NONE"',
        'downstream_owner_ref:"StegVerse-Labs/.github#493"',
        "queueIntrMaterializationRequest",
        'e.code==="INTR_RUNTIME_UNAVAILABLE"',
        "MATERIALIZATION QUEUED",
    )
    for token in required:
        assert token in js, token
    assert "observer_direct_relation_to_stegverse_002" not in js


def test_node_continuity_exposes_write_once_generic_intr_outbox() -> None:
    js = (ROOT / "assets/stegverse-node-continuity.js").read_text(encoding="utf-8")
    for token in (
        'var DB_VERSION = 2',
        'var INTR_OUTBOX = "intr_outbox"',
        "queueIntrMaterializationRequest",
        "getIntrOutbox",
        "FAIL_CLOSED: InTr outbox write-once collision",
        'authority_effect: "NONE_LOCAL_CONTINUITY_ONLY"',
    ):
        assert token in js, token


def test_connector_classifies_runtime_unavailable_without_granting_authority() -> None:
    js = (ROOT / "assets/evaluator-intr-connector.js").read_text(encoding="utf-8")
    assert 'e.code="INTR_RUNTIME_UNAVAILABLE"' in js
    assert "credentials:"omit"" in js


def test_sv002_sync_target_is_fail_closed_until_sovereign_ingress_observed() -> None:
    target = json.loads((ROOT / "stegos-node/sv002-intr-sync-target.json").read_text(encoding="utf-8"))
    assert target == {
        "schema": "stegos.site.sv002_intr_sync_target.v1",
        "state": "AWAITING_SOVEREIGN_INTR_INGRESS",
        "ingress_url": None,
        "transport_origin": "STEGOS_NODE_OUTBOX",
        "runtime_ingress_observed": False,
        "configuration_authority": "StegVerse sovereign runtime evidence projection",
        "credential_authority": "TV/TVC",
        "credential_requirement": "NONE",
        "github_token_runtime_authority": "NONE",
        "execution_authority": "NONE",
        "authority_effect": "NONE_DISCOVERY_ONLY",
    }


def test_sv002_page_loads_event_sync_before_observation_client() -> None:
    html = (ROOT / "sv002-observe/index.html").read_text(encoding="utf-8")
    sync = html.index("../stegos-node/sv002-intr-sync.js")
    observe = html.index("../assets/sv002-observe.js")
    assert sync < observe
