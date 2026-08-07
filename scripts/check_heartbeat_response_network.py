#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "ecosystem-heartbeat-response-network.json"
TARGETS = ROOT / "data" / "heartbeat-response-adapter-targets.json"
OUTBOX = ROOT / "data" / "heartbeat-response-outbox" / "bootstrap-2026-08-07.json"
RECEIPTS = ROOT / "data" / "heartbeat-response-receipts"

LIFECYCLE = ["SENT", "RECEIVED", "RESPONDED", "RECOVERED", "REPEAT"]
FAILURE = {"BLOCKED", "FAILED", "REVIEW_REQUIRED"}
DETAIL_CLASSES = {"MEMORY", "ACTION", "AWARENESS", "AUTHORITY", "EVIDENCE", "BLOCKER", "CAPABILITY", "CONTEXT"}
INSTALLED_STATES = {"INSTALLED_EXISTING_HB", "ADAPTER_INSTALLED"}


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def pct(n, d):
    return round((100.0 * n / d), 2) if d else 0.0


def authority_is_transport_only(authority):
    return all(authority.get(k) is False for k in ("execution", "activation", "publication", "custody", "release"))


def validate_receipt(receipt, known_orgs):
    required = {"message_id", "exchange_id", "node_org", "source_org", "destination_org", "stage", "detail_class", "authority"}
    missing = required - receipt.keys()
    if missing:
        raise ValueError(f"receipt missing fields: {sorted(missing)}")
    if receipt["node_org"] not in known_orgs or receipt["source_org"] not in known_orgs or receipt["destination_org"] not in known_orgs:
        raise ValueError("receipt references unregistered organization")
    if receipt["node_org"] != receipt["destination_org"]:
        raise ValueError("status receipt node_org must equal original destination_org")
    if receipt["stage"] not in (set(LIFECYCLE) - {"SENT"}) | FAILURE:
        raise ValueError("invalid receipt lifecycle stage")
    if receipt["detail_class"] not in DETAIL_CLASSES:
        raise ValueError("invalid detail class")
    if not authority_is_transport_only(receipt["authority"]):
        raise ValueError("transport receipt attempts to grant authority")
    return hashlib.sha256(json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_outbox(outbox, known_orgs):
    messages = outbox.get("messages", [])
    if outbox.get("message_count") != len(messages) or len(messages) != len(known_orgs):
        raise ValueError("bootstrap outbox must contain exactly one message per organization")
    destinations = []
    for message in messages:
        required = {"message_id", "exchange_id", "source_org", "destination_org", "stage", "detail_class", "authority", "payload"}
        missing = required - message.keys()
        if missing:
            raise ValueError(f"outbox message missing fields: {sorted(missing)}")
        if message["stage"] != "SENT":
            raise ValueError("bootstrap outbox contains non-SENT message")
        if message["source_org"] not in known_orgs or message["destination_org"] not in known_orgs:
            raise ValueError("outbox references unregistered organization")
        if message["detail_class"] not in DETAIL_CLASSES:
            raise ValueError("outbox message has invalid detail class")
        if not authority_is_transport_only(message["authority"]):
            raise ValueError("outbox transport attempts to grant authority")
        destinations.append(message["destination_org"])
    if set(destinations) != known_orgs or len(destinations) != len(set(destinations)):
        raise ValueError("bootstrap outbox destination coverage mismatch")


def main():
    state = load_json(STATE)
    orgs = state["organizations"]
    names = [item["organization"] for item in orgs]
    known_orgs = set(names)
    if len(names) != state["organization_count"] or len(known_orgs) != len(names):
        raise SystemExit("HB_RESPONSE_NETWORK_FAIL: organization inventory count/uniqueness mismatch")
    if state["lifecycle"] != LIFECYCLE:
        raise SystemExit("HB_RESPONSE_NETWORK_FAIL: lifecycle order mismatch")
    if set(state["detail_classes"]) != DETAIL_CLASSES:
        raise SystemExit("HB_RESPONSE_NETWORK_FAIL: detail-class contract mismatch")
    if state["heartbeat_model"] != "TRANSITION_DRIVEN" or state["time_role"] != "WATCHDOG_AND_RETRY_ONLY":
        raise SystemExit("HB_RESPONSE_NETWORK_FAIL: heartbeat/time authority semantics changed")

    targets = load_json(TARGETS)
    target_orgs = [item["organization"] for item in targets["targets"]]
    if targets.get("organization_count") != len(names) or set(target_orgs) != known_orgs or len(target_orgs) != len(set(target_orgs)):
        raise SystemExit("HB_RESPONSE_NETWORK_FAIL: adapter-target inventory mismatch")
    blocked = [item for item in targets["targets"] if item["state"] == "BLOCKED_NO_REPOSITORY"]
    for item in blocked:
        if item.get("repository") is not None or not item.get("release_condition"):
            raise SystemExit("HB_RESPONSE_NETWORK_FAIL: blocked target lacks precise no-repository boundary")

    try:
        validate_outbox(load_json(OUTBOX), known_orgs)
    except ValueError as exc:
        raise SystemExit(f"HB_RESPONSE_NETWORK_FAIL: {exc}") from exc

    seen_stage = {name: set() for name in names}
    receipt_count = 0
    if RECEIPTS.exists():
        for path in sorted(RECEIPTS.glob("*.json")):
            receipt = load_json(path)
            validate_receipt(receipt, known_orgs)
            seen_stage[receipt["node_org"]].add(receipt["stage"])
            receipt_count += 1

    receive_verified = sum("RECEIVED" in stages or "RESPONDED" in stages or "RECOVERED" in stages for stages in seen_stage.values())
    respond_verified = sum("RESPONDED" in stages or "RECOVERED" in stages for stages in seen_stage.values())
    recovery_verified = sum("RECOVERED" in stages for stages in seen_stage.values())
    installed = sum(item["protocol_state"] in INSTALLED_STATES for item in orgs)
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
    print(f"HB_RESPONSE_NETWORK_PASS:orgs={len(names)}:installed={installed}:blocked_no_repo={len(blocked)}:receipts={receipt_count}:receive={receive_verified}:respond={respond_verified}:recovered={recovery_verified}")


if __name__ == "__main__":
    main()
