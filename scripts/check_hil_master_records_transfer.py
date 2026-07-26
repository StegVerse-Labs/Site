#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "hil-master-records.json"
TRANSFERS = ROOT / "data" / "hil-master-record-transfers"
HEX64 = re.compile(r"^[a-f0-9]{64}$")
EXPECTED_PRIMARY = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
EXPECTED_PROMPT = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"


def fail(message: str) -> None:
    raise SystemExit(f"HIL MASTER RECORDS TRANSFER: FAIL: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    releases = index.get("releases")
    if not isinstance(releases, list):
        fail("invalid Master Record index")

    if not TRANSFERS.exists():
        print("HIL MASTER RECORDS TRANSFER: PASS (no transfers yet)")
        return 0

    seen: set[str] = set()
    for path in sorted(TRANSFERS.glob("*.json")):
        packet = json.loads(path.read_text(encoding="utf-8"))
        if packet.get("schema_version") != "HIL-MASTER-RECORDS-TRANSFER-v1":
            fail(f"unsupported schema in {path.name}")
        transfer_id = packet.get("transfer_id")
        if not isinstance(transfer_id, str) or transfer_id in seen:
            fail(f"invalid or duplicate transfer_id in {path.name}")
        seen.add(transfer_id)

        site_release = packet.get("site_release") or {}
        if site_release.get("primary_sha256") != EXPECTED_PRIMARY:
            fail(f"Primary mismatch in {path.name}")
        if site_release.get("prompt_sha256") != EXPECTED_PROMPT:
            fail(f"prompt mismatch in {path.name}")
        release_path = ROOT / str(site_release.get("release_path", ""))
        if not release_path.exists():
            fail(f"missing release file for {path.name}")
        if sha256(release_path) != site_release.get("release_sha256"):
            fail(f"release hash mismatch in {path.name}")
        if not any(r.get("release_id") == site_release.get("release_id") for r in releases):
            fail(f"release not indexed for {path.name}")

        chain = packet.get("source_chain")
        if not isinstance(chain, list) or not chain:
            fail(f"missing source chain in {path.name}")
        for item in chain:
            digest = item.get("sha256")
            source_path = item.get("path")
            if not isinstance(digest, str) or not HEX64.fullmatch(digest):
                fail(f"invalid source hash in {path.name}")
            if not isinstance(source_path, str) or source_path.startswith(("/", "http://", "https://")):
                fail(f"source paths must be repository-relative in {path.name}")

        requested = packet.get("requested_operations") or {}
        if requested != {"durable_custody": True, "reconstruction": True, "return_receipt": True}:
            fail(f"invalid requested operations in {path.name}")
        authority = packet.get("authority") or {}
        if any(authority.values()):
            fail(f"transfer packet grants authority in {path.name}")

    print(f"HIL MASTER RECORDS TRANSFER: PASS ({len(seen)} packet(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
