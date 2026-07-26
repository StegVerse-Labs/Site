#!/usr/bin/env python3
"""Fail-closed validation for imported HIL HTTPS receiver probe evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

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
    require(len(data.get("source_commit", "")) == 40, f"{path}: source commit missing")
    require(len(data.get("source_evidence_sha256", "")) == 64, f"{path}: source evidence hash missing")
    require(str(data.get("receiver_origin", "")).startswith("https://"), f"{path}: HTTPS receiver required")
    require(data.get("contract_state") == "CONFORMING_V1_1_READINESS_OBSERVED", f"{path}: receiver not conforming")
    require(data.get("tls_verified") is True and data.get("http_status") == 200, f"{path}: TLS/HTTP readiness not proven")
    require(data.get("primary_sha256") == PRIMARY, f"{path}: Primary mismatch")
    require(data.get("prompt_sha256") == PROMPT, f"{path}: prompt mismatch")
    require(data.get("protocol_version") == "HIL-PROTOCOL-v1.1", f"{path}: protocol mismatch")
    require(data.get("prompt_version") == "HIL-PROMPT-v1.1", f"{path}: prompt version mismatch")
    require(data.get("provenance_manifest_schema") == "HIL-RESPONSE-PROVENANCE-v1.1", f"{path}: provenance mismatch")
    require(data.get("mutation_performed") is False, f"{path}: probe must be non-mutating")
    require(data.get("authority") == FALSE_AUTHORITY, f"{path}: authority escalation")
    require(hashlib.sha256(raw).hexdigest() != data.get("source_evidence_sha256"), f"{path}: import hash incorrectly claims to be source evidence hash")


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
