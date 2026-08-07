#!/usr/bin/env python3
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "data" / "heartbeat-response-adapter-targets.json"
OUTBOX = ROOT / "data" / "heartbeat-response-outbox" / "bootstrap-2026-08-07.json"
NETWORK = ROOT / "data" / "ecosystem-heartbeat-response-network.json"
RECEIPTS = ROOT / "data" / "heartbeat-response-receipts"
CLASSIFICATION = ROOT / "data" / "heartbeat-response-classification-state.json"
IMPORT_REPORT = ROOT / "data" / "heartbeat-response-import-report.json"
AUTH_KEYS = ("execution", "activation", "publication", "custody", "release")
DETAIL_CLASSES = {"MEMORY", "ACTION", "AWARENESS", "AUTHORITY", "EVIDENCE", "BLOCKER", "CAPABILITY", "CONTEXT"}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def canonical_sha256(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def authority_false(authority):
    return all(authority.get(key) is False for key in AUTH_KEYS)


def fetch_json(url):
    request = Request(url, headers={"User-Agent": "stegverse-heartbeat-response-collector/1.0"})
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def validate_pair(org, exchange_id, message, received, responded):
    expected_message_hash = canonical_sha256(message)
    for receipt, stage in ((received, "RECEIVED"), (responded, "RESPONDED")):
        if receipt.get("stage") != stage:
            raise ValueError(f"{org} {stage} receipt has wrong stage")
        if receipt.get("exchange_id") != exchange_id:
            raise ValueError(f"{org} receipt exchange mismatch")
        if receipt.get("node_org") != org or receipt.get("destination_org") != org:
            raise ValueError(f"{org} receipt destination mismatch")
        if receipt.get("source_org") != message.get("source_org"):
            raise ValueError(f"{org} receipt source mismatch")
        if receipt.get("observed_message_sha256") != expected_message_hash:
            raise ValueError(f"{org} receipt observed-message hash mismatch")
        if receipt.get("detail_class") not in DETAIL_CLASSES:
            raise ValueError(f"{org} receipt detail class invalid")
        if not authority_false(receipt.get("authority", {})):
            raise ValueError(f"{org} receipt attempts authority escalation")
    if responded.get("parent_receipt_sha256") != canonical_sha256(received):
        raise ValueError(f"{org} response parent receipt hash mismatch")


def receipt_paths(exchange_id):
    return (
        RECEIPTS / f"{exchange_id}.received.json",
        RECEIPTS / f"{exchange_id}.responded.json",
        RECEIPTS / f"{exchange_id}.recovered.json",
    )


def make_recovered(org, exchange_id, responded):
    response_hash = canonical_sha256(responded)
    return {
        "schema_version": "1.0.0",
        "message_id": f"{exchange_id}-recovered",
        "exchange_id": exchange_id,
        "node_org": org,
        "source_org": "StegVerse-Labs",
        "destination_org": org,
        "stage": "RECOVERED",
        "detail_class": "EVIDENCE",
        "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "observed_message_sha256": responded.get("observed_message_sha256"),
        "parent_receipt_sha256": response_hash,
        "classification": {
            "primary": "EVIDENCE",
            "recovered_into": "StegVerse-Labs/Site",
            "upstream_response_sha256": response_hash,
            "memory_retention": "PROJECT",
            "action_admitted": False,
            "awareness_updated": True,
        },
        "authority": {key: False for key in AUTH_KEYS},
    }


def pct(n, d):
    return round(100.0 * n / d, 2) if d else 0.0


def collect(apply_changes=True):
    targets_doc = load_json(TARGETS)
    outbox = load_json(OUTBOX)
    network = load_json(NETWORK)
    messages = {item["destination_org"]: item for item in outbox["messages"]}
    known = {item["organization"] for item in targets_doc["targets"]}
    if set(messages) != known:
        raise ValueError("outbox and target inventories differ")

    RECEIPTS.mkdir(parents=True, exist_ok=True)
    report_rows = []
    classification_rows = []
    verified = {}

    for target in targets_doc["targets"]:
        org = target["organization"]
        mode = target.get("receipt_mode")
        exchange_id = target.get("exchange_id")
        row = {"organization": org, "repository": target.get("repository"), "target_state": target["state"], "receipt_mode": mode}
        if target["state"] != "ADAPTER_INSTALLED":
            row["state"] = target["state"]
            row["release_condition"] = target.get("release_condition")
            report_rows.append(row)
            classification_rows.append({
                "organization": org,
                "state": target["state"],
                "memory": "NO_NEW_MEMORY",
                "action": "NO_ACTION_ADMITTED",
                "awareness": "BLOCKER_RETAINED" if target["state"].startswith("BLOCKED") else "UNCHANGED",
                "evidence": [],
                "release_condition": target.get("release_condition"),
            })
            continue

        if not exchange_id:
            raise ValueError(f"installed target {org} lacks exchange_id")
        received_path, responded_path, recovered_path = receipt_paths(exchange_id)
        try:
            if mode == "PUBLIC_RAW":
                base = target["receipt_base"].rstrip("/")
                received = fetch_json(f"{base}/{exchange_id}.received.json")
                responded = fetch_json(f"{base}/{exchange_id}.responded.json")
                validate_pair(org, exchange_id, messages[org], received, responded)
                if apply_changes:
                    dump_json(received_path, received)
                    dump_json(responded_path, responded)
            elif mode == "LOCAL":
                if not received_path.exists() or not responded_path.exists():
                    raise FileNotFoundError("local response receipts not yet present")
                received = load_json(received_path)
                responded = load_json(responded_path)
                validate_pair(org, exchange_id, messages[org], received, responded)
            elif mode == "PRIVATE_RELAY_REQUIRED":
                if not received_path.exists() or not responded_path.exists():
                    row["state"] = "BLOCKED_PRIVATE_RELAY"
                    row["release_condition"] = target.get("release_condition")
                    report_rows.append(row)
                    classification_rows.append({
                        "organization": org,
                        "state": "BLOCKED_PRIVATE_RELAY",
                        "memory": "REMOTE_ONLY_NOT_CANONICALLY_IMPORTED",
                        "action": "NO_ACTION_ADMITTED",
                        "awareness": "PRIVATE_NODE_RESPONSE_NOT_YET_IMPORTED",
                        "evidence": [],
                        "release_condition": target.get("release_condition"),
                    })
                    continue
                received = load_json(received_path)
                responded = load_json(responded_path)
                validate_pair(org, exchange_id, messages[org], received, responded)
            else:
                raise ValueError(f"installed target {org} has unsupported receipt mode {mode}")

            if recovered_path.exists():
                recovered = load_json(recovered_path)
                if recovered.get("stage") != "RECOVERED" or recovered.get("parent_receipt_sha256") != canonical_sha256(responded):
                    raise ValueError(f"{org} recovered receipt continuity mismatch")
                if not authority_false(recovered.get("authority", {})):
                    raise ValueError(f"{org} recovered receipt attempts authority escalation")
            else:
                recovered = make_recovered(org, exchange_id, responded)
                if apply_changes:
                    dump_json(recovered_path, recovered)

            verified[org] = {"received": True, "responded": True, "recovered": True}
            row.update({
                "state": "RECOVERED",
                "received_path": str(received_path.relative_to(ROOT)),
                "responded_path": str(responded_path.relative_to(ROOT)),
                "recovered_path": str(recovered_path.relative_to(ROOT)),
                "response_sha256": canonical_sha256(responded),
                "recovered_sha256": canonical_sha256(recovered),
            })
            report_rows.append(row)
            classification_rows.append({
                "organization": org,
                "state": "RECOVERED",
                "memory": "PROJECT_CONTEXT_RETAINED",
                "action": "NO_ACTION_ADMITTED",
                "awareness": "UPDATED",
                "capability": responded.get("classification", {}).get("node_state", "RESPONSIVE"),
                "detail_classes_observed": sorted({received.get("detail_class"), responded.get("detail_class"), "EVIDENCE"}),
                "evidence": [row["received_path"], row["responded_path"], row["recovered_path"]],
            })
        except (HTTPError, URLError, TimeoutError, FileNotFoundError) as exc:
            row["state"] = "RETRY"
            row["error"] = str(exc)
            row["next_action"] = "retry receipt acquisition on the repository-native schedule"
            report_rows.append(row)
            classification_rows.append({
                "organization": org,
                "state": "RETRY",
                "memory": "NO_NEW_CANONICAL_MEMORY",
                "action": "NO_ACTION_ADMITTED",
                "awareness": "RESPONSE_NOT_YET_OBSERVED",
                "evidence": [],
            })

    org_state = {item["organization"]: item for item in network["organizations"]}
    target_state = {item["organization"]: item for item in targets_doc["targets"]}
    for org, item in org_state.items():
        target = target_state[org]
        item["protocol_state"] = "ADAPTER_INSTALLED" if target["state"] == "ADAPTER_INSTALLED" else target["state"]
        item["receive_state"] = "VERIFIED" if verified.get(org, {}).get("received") else "UNVERIFIED"
        item["respond_state"] = "VERIFIED" if verified.get(org, {}).get("responded") else "UNVERIFIED"
        item["recovery_state"] = "VERIFIED" if verified.get(org, {}).get("recovered") else "UNVERIFIED"
        item["evidence_repository"] = target.get("repository")
        if target.get("release_condition"):
            item["release_condition"] = target["release_condition"]

    total = network["organization_count"]
    installed = sum(item["protocol_state"] == "ADAPTER_INSTALLED" for item in network["organizations"])
    receive = sum(item["receive_state"] == "VERIFIED" for item in network["organizations"])
    respond = sum(item["respond_state"] == "VERIFIED" for item in network["organizations"])
    recovered_count = sum(item["recovery_state"] == "VERIFIED" for item in network["organizations"])
    network["coverage"] = {
        "organizations_registered": total,
        "organizations_protocol_installed": installed,
        "organizations_receive_verified": receive,
        "organizations_respond_verified": respond,
        "organizations_recovery_verified": recovered_count,
        "registered_percent": pct(total, total),
        "protocol_installed_percent": pct(installed, total),
        "receive_verified_percent": pct(receive, total),
        "respond_verified_percent": pct(respond, total),
        "recovery_verified_percent": pct(recovered_count, total),
    }
    network["next_machine_action"] = "retry public receipt acquisition; preserve private-relay and no-repository blockers; emit REPEAT only after a new admitted transition requires another exchange"

    classification_doc = {
        "schema_version": "1.0.0",
        "owner": "StegVerse-Labs/Site issue #234",
        "classification_rule": "transport details are classified into memory/action/awareness/capability/evidence without granting execution authority",
        "action_authority_rule": "ACTION remains candidate work until destination-owned authority and collision checks admit it",
        "organizations": classification_rows,
    }
    report = {
        "schema_version": "1.0.0",
        "owner": "StegVerse-Labs/Site issue #234",
        "state": "COMPLETE_WITH_BLOCKERS" if len(verified) < installed else "COMPLETE",
        "verified_recovered": len(verified),
        "installed_nodes": installed,
        "rows": report_rows,
        "next_executable_task": "continue machine retries and private relay observation; do not emit REPEAT absent a new admitted transition",
    }
    if apply_changes:
        dump_json(NETWORK, network)
        dump_json(CLASSIFICATION, classification_doc)
        dump_json(IMPORT_REPORT, report)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.apply and not args.check:
        parser.error("choose --apply or --check")
    report = collect(apply_changes=args.apply)
    print(f"HB_RESPONSE_COLLECTOR:{report['state']}:recovered={report['verified_recovered']}:installed={report['installed_nodes']}")


if __name__ == "__main__":
    main()
