#!/usr/bin/env python3
"""Fail-closed validation for imported HIL HTTPS receiver probe evidence."""
from __future__ import annotations

import hashlib
import ipaddress
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = ROOT / "data" / "hil-https-receiver-probes"
PRIMARY = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
PROMPT = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
FALSE_AUTHORITY = {
    "execution": False,
    "activation": False,
    "publication": False,
    "release": False,
    "custody": False,
    "master_record_append": False,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate(path: Path) -> None:
    raw = path.read_bytes()
    data = json.loads(raw)
    require(data.get("schema_version") == "HIL-HTTPS-RECEIVER-PROBE-IMPORT-v1", f"{path}: schema mismatch")
    require(data.get("source_repository") == "StegVerse-org/LLM-adapter", f"{path}: source repository mismatch")
    require(data.get("source_evidence_path") == "reports/hil-https-receiver-probe.json", f"{path}: evidence path mismatch")
    source_commit = data.get("source_commit", "")
    source_hash = data.get("source_evidence_sha256", "")
    require(len(source_commit) == 40 and all(c in "0123456789abcdef" for c in source_commit), f"{path}: source commit invalid")
    require(len(source_hash) == 64 and all(c in "0123456789abcdef" for c in source_hash), f"{path}: source evidence hash invalid")

    origin = str(data.get("receiver_origin", ""))
    parsed = urlparse(origin)
    require(parsed.scheme == "https" and parsed.netloc and parsed.hostname, f"{path}: HTTPS receiver required")
    require(not parsed.username and not parsed.password and not parsed.query and not parsed.fragment, f"{path}: receiver origin invalid")
    require(parsed.path in {"", "/"}, f"{path}: receiver origin must not contain a path")
    require(parsed.hostname.lower() != "localhost", f"{path}: localhost receiver forbidden")

    addresses = data.get("resolved_public_addresses")
    require(isinstance(addresses, list) and addresses, f"{path}: public address evidence missing")
    require(len(addresses) == len(set(addresses)), f"{path}: duplicate resolved addresses")
    for address in addresses:
        try:
            ip = ipaddress.ip_address(address)
        except ValueError as exc:
            raise SystemExit(f"{path}: invalid resolved address {address}: {exc}") from exc
        require(ip.is_global and not ip.is_multicast, f"{path}: non-public resolved address {address}")

    require(data.get("readiness_path") == "/api/hil/readiness", f"{path}: readiness path mismatch")
    require(data.get("contract_state") == "CONFORMING_V1_1_READINESS_OBSERVED", f"{path}: receiver not conforming")
    require(data.get("tls_verified") is True and data.get("http_status") == 200, f"{path}: TLS/HTTP readiness not proven")
    require(data.get("redirects_followed") is False, f"{path}: redirects must be rejected")
    response_size = data.get("response_size_bytes")
    require(isinstance(response_size, int) and 2 <= response_size <= 65536, f"{path}: readiness response size invalid")
    require(data.get("primary_sha256") == PRIMARY, f"{path}: Primary mismatch")
    require(data.get("prompt_sha256") == PROMPT, f"{path}: prompt mismatch")
    require(data.get("protocol_version") == "HIL-PROTOCOL-v1.1", f"{path}: protocol mismatch")
    require(data.get("prompt_version") == "HIL-PROMPT-v1.1", f"{path}: prompt version mismatch")
    require(data.get("provenance_manifest_schema") == "HIL-RESPONSE-PROVENANCE-v1.1", f"{path}: provenance mismatch")
    require(data.get("mutation_performed") is False, f"{path}: probe must be non-mutating")
    require(data.get("authority") == FALSE_AUTHORITY, f"{path}: authority escalation")
    require(hashlib.sha256(raw).hexdigest() != source_hash, f"{path}: import hash incorrectly claims to be source evidence hash")


def main() -> None:
    if not IMPORT_DIR.exists():
        print("HIL_HTTPS_RECEIVER_PROBE_IMPORT=PASS pending_no_imports")
        return
    files = sorted(IMPORT_DIR.glob("*.json"))
    if not files:
        print("HIL_HTTPS_RECEIVER_PROBE_IMPORT=PASS pending_no_imports")
        return
    for path in files:
        validate(path)
    print(f"HIL_HTTPS_RECEIVER_PROBE_IMPORT=PASS imports={len(files)}")


if __name__ == "__main__":
    main()
