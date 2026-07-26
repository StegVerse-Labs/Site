#!/usr/bin/env python3
"""Validate governed Master Records custody/reconstruction return receipts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = ROOT / "data" / "hil-master-records-return-receipts"
EXPECTED_SCHEMA = "HIL-MASTER-RECORDS-RETURN-RECEIPT-v1"
SOURCE_REPOSITORY = "master-records/orchestration"
HEX = set("0123456789abcdef")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def is_hex(value: object, size: int) -> bool:
    return isinstance(value, str) and len(value) == size and set(value) <= HEX


def main() -> int:
    if not IMPORT_DIR.exists():
        print("HIL_MASTER_RECORDS_RETURN_RECEIPTS=PENDING")
        return 0

    files = sorted(IMPORT_DIR.glob("*.json"))
    if not files:
        print("HIL_MASTER_RECORDS_RETURN_RECEIPTS=PENDING")
        return 0

    transfer_ids: set[str] = set()
    source_hashes: set[str] = set()
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        require(payload.get("schema") == EXPECTED_SCHEMA, f"{path}: schema mismatch")
        require(payload.get("source_repository") == SOURCE_REPOSITORY, f"{path}: source repository mismatch")
        require(is_hex(payload.get("source_commit"), 40), f"{path}: invalid source commit")
        require(is_hex(payload.get("source_sha256"), 64), f"{path}: invalid source sha256")
        require(is_hex(payload.get("site_release_sha256"), 64), f"{path}: invalid Site release sha256")
        source_path = payload.get("source_path")
        require(isinstance(source_path, str) and source_path.endswith(".json") and not source_path.startswith("/"), f"{path}: invalid source path")

        transfer_id = payload.get("transfer_id")
        require(isinstance(transfer_id, str) and transfer_id, f"{path}: missing transfer id")
        require(transfer_id not in transfer_ids, f"{path}: duplicate transfer id")
        transfer_ids.add(transfer_id)

        source_sha = payload["source_sha256"]
        require(source_sha not in source_hashes, f"{path}: duplicate source receipt hash")
        source_hashes.add(source_sha)

        for key in ("custody_receipt", "reconstruction_receipt"):
            receipt = payload.get(key)
            require(isinstance(receipt, dict), f"{path}: missing {key}")
            require(isinstance(receipt.get("receipt_id"), str) and receipt["receipt_id"], f"{path}: invalid {key} id")
            require(is_hex(receipt.get("receipt_sha256"), 64), f"{path}: invalid {key} hash")
            require(receipt.get("verified") is True, f"{path}: {key} not verified")
            require(receipt.get("authority_effect") == "NONE", f"{path}: {key} grants authority")

        authority = payload.get("authority")
        require(isinstance(authority, dict), f"{path}: missing authority block")
        require(set(authority) == {"execution", "publication", "release", "custody", "reconstruction"}, f"{path}: authority keys mismatch")
        require(all(value is False for value in authority.values()), f"{path}: authority escalation")

        # Bind the imported JSON bytes to the filename-independent source claim.
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        require(hashlib.sha256(canonical).hexdigest() != "0" * 64, f"{path}: impossible canonical hash")

    print(f"HIL_MASTER_RECORDS_RETURN_RECEIPTS=PASS count={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
