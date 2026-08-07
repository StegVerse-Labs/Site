#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "ecosystem-heartbeat-response-network.json"
RECEIPTS = ROOT / "data" / "heartbeat-response-receipts"

LIFECYCLE = ["SENT", "RECEIVED", "RESPONDED", "RECOVERED", "REPEAT"]
FAILURE = {"BLOCKED", "FAILED", "REVIEW_REQUIRED"}
DETAIL_CLASSES = {"MEMORY", "ACTION", "AWARENESS", "AUTHORITY", "EVIDENCE", "BLOCKER", "CAPABILITY", "CONTEXT"}


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def pct(n, d):
    return round((100.0 * n / d), 2) if d else 0.0


def validate_receipt(receipt, known_orgs):
    required = {"message_id", "exchange_id", "source_org", "destination_org", "stage", "detail_class", "authority"}
    missing = required - receipt.keys()
    if missing:
        raise ValueError(f"receipt missing fields: {sorted(missing)}")
    if receipt["source_org"] not in known_orgs or receipt["destination_org"] not in known_orgs:
        raise ValueError("receipt references unregistered organization")
    if receipt["stage"] not in set(LIFECYCLE) | FAILURE:
        raise ValueError("invalid lifecycle stage")
    if receipt["detail_class"] not in DETAIL_CLASSES:
        raise ValueError("invalid detail class")
    authority = receipt["authority"]
    if any(authority.get(k) is not False for k in ("execution", "activation", "publication", "custody", "release")):
        raise ValueError("transport receipt attempts to grant authority")
    return hashlib.sha256(json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main():
    state = load_json(STATE)
    orgs = state["organizations"]
    names = [item["organization"] for item in orgs]
    if len(names) != state["organization_count"] or len(set(names)) != len(names):
        raise SystemExit("HB_RESPONSE_NETWORK_FAIL: organization inventory count/uniqueness mismatch")
    if state["lifecycle"] != LIFECYCLE:
        raise SystemExit("HB_RESPONSE_NETWORK_FAIL: lifecycle order mismatch")
    if set(state["detail_classes"]) != DETAIL_CLASSES:
        raise SystemExit("HB_RESPONSE_NETWORK_FAIL: detail-class contract mismatch")
    if state["heartbeat_model"] != "TRANSITION_DRIVEN" or state["time_role"] != "WATCHDOG_AND_RETRY_ONLY":
        raise SystemExit("HB_RESPONSE_NETWORK_FAIL: heartbeat/time authority semantics changed")

    seen_stage = {name: set() for name in names}
    receipt_count = 0
    if RECEIPTS.exists():
        for path in sorted(RECEIPTS.glob("*.json")):
            receipt = load_json(path)
            validate_receipt(receipt, set(names))
            seen_stage[receipt["destination_org"]].add(receipt["stage"])
            receipt_count += 1

    receive_verified = sum("RECEIVED" in stages or "RESPONDED" in stages or "RECOVERED" in stages for stages in seen_stage.values())
    respond_verified = sum("RESPONDED" in stages or "RECOVERED" in stages for stages in seen_stage.values())
    recovery_verified = sum("RECOVERED" in stages for stages in seen_stage.values())
    installed = sum(item["protocol_state"] == "INSTALLED_EXISTING_HB" for item in orgs)
    expected = {
        "organizations_registered": len(names),
        "organizations_protocol_installed": installed,
        "organizations_receive_verified": receive_verified,
        "organizations_respond_verified": respond_verified,
        "organizations_recovery_verified": recovery_verified,
        "registered_percent": pct(len(names), len(names)),
        "protocol_installed_percent": pct(installed, len(names)),
        "receive_verified_percent": pct(receive_verified, len(names)),
        "respond_verified_percent": pct(respond_verified, len(names)),
        "recovery_verified_percent": pct(recovery_verified, len(names))
    }
    if state["coverage"] != expected:
        raise SystemExit(f"HB_RESPONSE_NETWORK_FAIL: coverage drift expected={expected} actual={state['coverage']}")
    print(f"HB_RESPONSE_NETWORK_PASS:orgs={len(names)}:installed={installed}:receipts={receipt_count}:receive={receive_verified}:respond={respond_verified}:recovered={recovery_verified}")


if __name__ == "__main__":
    main()
