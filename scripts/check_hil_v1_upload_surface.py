#!/usr/bin/env python3
"""Fail-closed verification for the canonical HIL v1 upload surface."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "humans-as-interoperability-layer.html"
SCRIPT = ROOT / "assets" / "hil-experiment-v1.js"
MANIFEST = ROOT / "data" / "hil-experiment.json"
GATEWAY_CONFIG = ROOT / "data" / "hil-gateway-config.json"
PRIMARY = ROOT / "data" / "hil-primary-v1.0.pdf.b64"

PRIMARY_HASH = "e7a86cf05323d8352cfa188e0bff1c35fdb15f9fac6af91ca62b6a126ac4e68f"
PROMPT_HASH = "bbb2db652a10ef404d565e561bb0a2f7b078bbe95105400faec14be9a6d5642a"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL v1 upload verification failed: {message}")


def read(path: Path) -> str:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    page = read(PAGE)
    script = read(SCRIPT)
    manifest = json.loads(read(MANIFEST))
    gateway = json.loads(read(GATEWAY_CONFIG))
    require(PRIMARY.is_file(), "canonical v1 Primary base64 artifact missing")

    require(manifest["primary_document"]["version"] == "v1.0", "manifest is not v1.0")
    require(manifest["primary_document"]["sha256"] == PRIMARY_HASH, "manifest Primary hash mismatch")
    require(manifest["protocol"]["prompt_sha256"] == PROMPT_HASH, "manifest prompt hash mismatch")
    require(manifest["submission"]["provenance_manifest_required"] is True, "provenance must remain required")
    require(all(value is False for value in manifest["authority"].values()), "manifest authority must remain false")

    for marker in (
        PRIMARY_HASH,
        PROMPT_HASH,
        "Drop the response PDF here or select it below",
        "Submit once",
        "Download provenance JSON",
        "Download receiver receipt",
        "aria-live=\"polite\"",
    ):
        require(marker in page, f"page missing marker: {marker}")

    for marker in (
        "data/hil-gateway-config.json",
        "first_exact_ready_chain",
        "fetchWithTimeout",
        "new FormData()",
        "crypto.subtle.digest('SHA-256'",
        "response_pdf",
        "provenance_manifest",
        "participant_consent_authority_acknowledged",
        "No successful submission is being claimed",
    ):
        require(marker in script or marker in read(GATEWAY_CONFIG), f"client/config missing marker: {marker}")

    candidates = gateway.get("gateway_candidates")
    require(isinstance(candidates, list) and len(candidates) >= 1, "gateway candidates missing")
    require(candidates[0]["id"] == "same-origin", "same-origin must be first gateway candidate")
    require(gateway.get("selection_policy") == "first_exact_ready_chain", "gateway selection policy mismatch")
    require(gateway.get("fail_closed") is True, "gateway discovery must fail closed")
    require(all(value is False for value in gateway["authority"].values()), "gateway config must not grant authority")

    print("HIL_V1_UPLOAD_SURFACE=PASS")
    print(f"HIL_PRIMARY_SHA256={PRIMARY_HASH}")
    print(f"HIL_PROMPT_SHA256={PROMPT_HASH}")
    print("HIL_GATEWAY_DISCOVERY=SAME_ORIGIN_THEN_COMPATIBILITY_FALLBACK")
    print("HIL_UPLOAD_FLOW=ONE_ACTION_HASH_PROVENANCE_UPLOAD_RECEIPT")
    print("HIL_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
