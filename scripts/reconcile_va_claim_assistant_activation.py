#!/usr/bin/env python3
"""Reconcile the bounded VA Claim Assistant public activation from repository and live evidence."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENDPOINT = ROOT / "api/va-claim-assistant/evidence-requirement.json"
SURFACE = ROOT / "va-claim-assistant-source-grounded.html"
GATES = ROOT / "data/va-claim-assistant/activation-gates.json"
RECEIPT = ROOT / "data/va-claim-assistant/source-grounded-activation-receipt.json"
LIVE_BASE = "https://stegverse.org"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def get(url: str) -> tuple[int, bytes]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "stegverse-va-activation-reconciler"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode()


def main() -> int:
    endpoint_raw = ENDPOINT.read_bytes()
    surface_raw = SURFACE.read_bytes()
    endpoint = json.loads(endpoint_raw)
    flags_false = not any(endpoint["authority_flags"].values())
    local_valid = (
        endpoint["capability"] == "SOURCE_GROUNDED_ASSISTANT"
        and endpoint["route"] == "evidence_requirement"
        and len(endpoint["answer"]["propositions"]) >= 1
        and all(p.get("support") for p in endpoint["answer"]["propositions"])
        and flags_false
    )

    page_url = f"{LIVE_BASE}/va-claim-assistant-source-grounded.html"
    api_url = f"{LIVE_BASE}/api/va-claim-assistant/evidence-requirement.json"
    page_status, page_live = get(page_url)
    api_status, api_live = get(api_url)
    deployed = page_status == 200 and api_status == 200
    live_matches = deployed and digest(api_live) == digest(endpoint_raw)

    state = "VERIFIED" if local_valid and deployed and live_matches else "BUILDING"
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    receipt = {
        "schema_version": "1.0.0",
        "receipt_id": "site-va-source-grounded-activation-001",
        "observed_at": now,
        "capability": "SOURCE_GROUNDED_ASSISTANT",
        "state": state,
        "local": {
            "surface_path": str(SURFACE.relative_to(ROOT)),
            "surface_sha256": digest(surface_raw),
            "endpoint_path": str(ENDPOINT.relative_to(ROOT)),
            "endpoint_sha256": digest(endpoint_raw),
            "contract_valid": local_valid,
            "authority_flags_false": flags_false,
        },
        "deployed": {
            "surface_url": page_url,
            "surface_http_status": page_status,
            "endpoint_url": api_url,
            "endpoint_http_status": api_status,
            "endpoint_sha256": digest(api_live) if api_status == 200 else None,
            "matches_repository_endpoint": live_matches,
        },
        "cross_repository_evidence": {
            "llm_adapter_receipt": "StegVerse-org/LLM-adapter@c643d13e7950d3cb14f8850b2b5b791dedc62154:receipts/va-claim-assistant-public-source-fixture.json",
            "tvc_readiness": "StegVerse-Labs/TVC@f5e4b911ce46d0b3d0e10e114b05def064102d43:receipts/va-claim-assistant-governed-retrieval-readiness.json",
            "master_records_custody": "master-records/orchestration@477a8aee2c68fbb47a25f9ba65f3300319f96977:receipts/va-claim-assistant-public-source-custody.json",
        },
        "activation_authorized": state == "VERIFIED",
        "authority_effect": False,
        "next_action": None if state == "VERIFIED" else "Retry live observation after Site deployment; do not halt or require an external task.",
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    gates = json.loads(GATES.read_text(encoding="utf-8"))
    for gate in gates["gates"]:
        if gate["id"] == "VCA-GATE-08":
            gate["state"] = "VERIFIED" if local_valid else "BUILDING"
            gate["evidence"] = ["data/va-claim-assistant/source-grounded-activation-receipt.json"]
            gate["next_action"] = None if local_valid else "Repair the Site-owned activation receipt contract."
        elif gate["id"] == "VCA-GATE-09":
            gate["state"] = "VERIFIED" if state == "VERIFIED" else "BUILDING"
            gate["evidence"] = ["data/va-claim-assistant/source-grounded-activation-receipt.json"]
            gate["next_action"] = None if state == "VERIFIED" else receipt["next_action"]
    required = {"VCA-GATE-01", "VCA-GATE-02", "VCA-GATE-03", "VCA-GATE-04", "VCA-GATE-06", "VCA-GATE-07", "VCA-GATE-08", "VCA-GATE-09"}
    source_ready = all(g["state"] == "VERIFIED" for g in gates["gates"] if g["id"] in required)
    gates["state"] = "SOURCE_GROUNDED_ACTIVE" if source_ready else "BUILDING"
    gates["activation_authorized"] = source_ready
    gates["current_public_capability"] = "SOURCE_GROUNDED_ASSISTANT" if source_ready else "BOUNDED_PROCEDURAL_ASSISTANT"
    GATES.write_text(json.dumps(gates, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"state": state, "source_grounded_activation_authorized": source_ready}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
