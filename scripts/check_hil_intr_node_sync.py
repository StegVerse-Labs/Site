#!/usr/bin/env python3
"""Validate the non-authorizing StegOS Node -> HIL materialization ingress source contract."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


class HILInTrNodeSyncError(ValueError):
    pass


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise HILInTrNodeSyncError(reason)


def validate_target_projection(value: dict[str, Any]) -> None:
    expected = {
        "schema": "stegos.site.hil_intr_sync_target.v1",
        "state": "AWAITING_SOVEREIGN_INTR_INGRESS",
        "transport_origin": "STEGOS_NODE_OUTBOX",
        "ingress_url": None,
        "runtime_ingress_observed": False,
        "credential_authority": "TV/TVC",
        "credential_requirement": "NONE",
        "github_token_runtime_authority": "NONE",
        "execution_authority": "NONE",
        "authority_effect": "NONE_DISCOVERY_ONLY",
    }
    for key, expected_value in expected.items():
        _require(value.get(key) == expected_value, f"target_{key}_mismatch")


def validate(root: Path = ROOT) -> list[str]:
    target = json.loads((root / "stegos-node/hil-intr-sync-target.json").read_text(encoding="utf-8"))
    validate_target_projection(target)

    sync = (root / "stegos-node/hil-intr-sync.js").read_text(encoding="utf-8")
    node = (root / "stegos-node/stegos-node.js").read_text(encoding="utf-8")
    index = (root / "stegos-node/index.html").read_text(encoding="utf-8")
    worker = (root / "stegos-node/service-worker.js").read_text(encoding="utf-8")

    required_sync = (
        'TRIGGER_SCHEMA = "stegos.node_intr_materialization_trigger.v1"',
        'transport_origin: "STEGOS_NODE_OUTBOX"',
        '"X-StegVerse-Transport-Origin": "STEGOS_NODE_OUTBOX"',
        '"X-StegVerse-Payload-SHA256": payloadSha256',
        'credentials: "omit"',
        'entry.network_delivery_observed !== false',
        'entry.runtime_materialization_observed !== false',
        'entry.receiver_receipt_observed !== false',
        'entry.tvc_receipt_observed !== false',
        'runtime_materialization_observed: false',
        'receiver_receipt_observed: false',
        'tvc_receipt_observed: false',
        'authority_effect: "NONE_TRIGGER_ONLY"',
        'INGRESS_RECEIPT_SCHEMA = "stegverse.hil-intr-materialization-ingress/v1"',
        'response.status !== 202',
        'target.state !== "CONFORMING_SOVEREIGN_INTR_INGRESS"',
    )
    for needle in required_sync:
        _require(needle in sync, f"sync_contract_missing:{needle}")

    forbidden_sync = (
        "X-StegVerse-Authorization-Id",
        "Authorization",
        'credentials: "include"',
        "GITHUB_TOKEN",
        "GH_TOKEN",
    )
    for needle in forbidden_sync:
        _require(needle not in sync, f"sync_forbidden_runtime_authority:{needle}")

    _require('schema: "stegos.node_intr_outbox_entry.v1"' in node, "node_outbox_schema_missing")
    _require('state: "LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY"' in node, "node_outbox_pending_state_missing")
    _require('network_delivery_observed: false' in node, "node_outbox_network_nonclaim_missing")
    _require('<script src="./stegos-node.js"></script>' in index, "node_script_missing")
    _require('<script src="./hil-intr-sync.js"></script>' in index, "sync_script_missing")
    _require(index.index('stegos-node.js') < index.index('hil-intr-sync.js'), "sync_must_load_after_node_projection")
    _require('"./hil-intr-sync.js"' in worker, "sync_not_cached")
    _require('"./hil-intr-sync-target.json"' in worker, "target_not_cached")
    _require("stegos-node-shell-v6-hil-intr-node-sync" in worker, "service_worker_cache_version_not_advanced")

    return [
        "STEGOS_NODE_HIL_INTR_SYNC_SOURCE_PASS",
        "STEGOS_NODE_HIL_INTR_SYNC_TARGET_FAIL_CLOSED_PASS",
        "STEGOS_NODE_HIL_INTR_SYNC_NO_EXECUTION_AUTHORITY_PASS",
        "STEGOS_NODE_HIL_INTR_SYNC_NO_PDF_TRANSPORT_CLAIM_PASS",
    ]


def main() -> int:
    for marker in validate():
        print(marker)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
