#!/usr/bin/env python3
"""Capture and validate the public HIL receiver readiness response.

This probe preserves the raw response body, response metadata, and a validation
result. It grants no execution, custody, review, publication, or Master Record
authority.
"""
from __future__ import annotations

import hashlib
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RECEIVER_URL = os.environ.get(
    "HIL_READINESS_URL",
    "https://receiver.stegverse.com/api/hil/readiness",
)
OUT = Path(os.environ.get("HIL_EVIDENCE_DIR", "artifacts/hil-readiness-live"))
EXPECTED = {
    "state": "READY",
    "primary_version": "v1.1",
    "primary_sha256": "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462",
    "protocol_version": "HIL-PROTOCOL-v1.1",
    "prompt_version": "HIL-PROMPT-v1.1",
    "prompt_sha256": "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c",
    "provenance_manifest_required": True,
    "provenance_manifest_schema": "HIL-RESPONSE-PROVENANCE-v1.1",
    "participant_metadata_required": False,
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    observed_at = now()
    evidence: dict[str, object] = {
        "schema_version": "HIL-LIVE-READINESS-EVIDENCE-v1",
        "observed_at": observed_at,
        "url": RECEIVER_URL,
        "authority_effect": False,
        "ready_validated": False,
    }

    request = urllib.request.Request(
        RECEIVER_URL,
        headers={"Accept": "application/json", "User-Agent": "StegVerse-HIL-readiness-probe/1.0"},
        method="GET",
    )

    try:
        context = ssl.create_default_context()
        with urllib.request.urlopen(request, timeout=30, context=context) as response:
            raw = response.read()
            evidence["http_status"] = response.status
            evidence["content_type"] = response.headers.get("Content-Type")
            evidence["response_sha256"] = hashlib.sha256(raw).hexdigest()
            (OUT / "response.raw").write_bytes(raw)
            payload = json.loads(raw.decode("utf-8"))
            (OUT / "response.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            mismatches = {
                key: {"expected": expected, "actual": payload.get(key)}
                for key, expected in EXPECTED.items()
                if payload.get(key) != expected
            }
            evidence["mismatches"] = mismatches
            evidence["ready_validated"] = response.status == 200 and not mismatches
            evidence["canonical_response_sha256"] = hashlib.sha256(canonical_json(payload)).hexdigest()
    except urllib.error.HTTPError as error:
        raw = error.read()
        evidence.update({
            "http_status": error.code,
            "failure_class": "HTTP_ERROR",
            "failure": str(error),
            "response_sha256": hashlib.sha256(raw).hexdigest(),
        })
        (OUT / "response.raw").write_bytes(raw)
    except Exception as error:  # fail-closed evidence, including DNS/TLS/JSON errors
        evidence.update({"failure_class": type(error).__name__, "failure": str(error)})

    evidence_bytes = canonical_json(evidence)
    evidence["evidence_sha256"] = hashlib.sha256(evidence_bytes).hexdigest()
    (OUT / "evidence.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if evidence.get("ready_validated") is True else 1


if __name__ == "__main__":
    sys.exit(main())
