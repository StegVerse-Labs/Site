#!/usr/bin/env python3
"""Verify the public HIL v1.1 paper, page, client, and manifest as one chain."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "data" / "HIL_Canonical_Paper_v1_1.pdf"
PAGE = ROOT / "humans-as-interoperability-layer.html"
CLIENT = ROOT / "assets" / "hil-experiment-v1.1.js"
MANIFEST = ROOT / "data" / "hil-experiment.json"

EXPECTED_SIZE = 87271
EXPECTED_SHA256 = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
EXPECTED_PROMPT_SHA256 = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
EXPECTED_PATH = "data/HIL_Canonical_Paper_v1_1.pdf"
EXPECTED_PROTOCOL = "HIL-PROTOCOL-v1.1"
EXPECTED_PROMPT = "HIL-PROMPT-v1.1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL v1.1 release verification failed: {message}")


def main() -> None:
    require(PDF.is_file(), f"missing canonical PDF: {PDF.relative_to(ROOT)}")
    payload = PDF.read_bytes()
    require(payload.startswith(b"%PDF-"), "canonical artifact lacks PDF signature")
    require(len(payload) == EXPECTED_SIZE, f"canonical PDF size is {len(payload)}, expected {EXPECTED_SIZE}")
    digest = hashlib.sha256(payload).hexdigest()
    require(digest == EXPECTED_SHA256, f"canonical PDF SHA-256 is {digest}, expected {EXPECTED_SHA256}")

    page = PAGE.read_text(encoding="utf-8")
    client = CLIENT.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    # The public page must expose the human-facing canonical artifact contract.
    for marker in (
        "Canonical experiment input · v1.1",
        "Download Canonical v1.1 Primary PDF",
        "HIL_Canonical_Paper_v1_1.pdf",
        EXPECTED_SHA256,
        EXPECTED_PROMPT_SHA256,
        "assets/hil-experiment-v1.1.js",
    ):
        require(marker in page, f"public page missing marker: {marker}")

    # The client must bind exact bytes, hashes, and upload behavior.
    for marker in (
        EXPECTED_PATH,
        EXPECTED_SHA256,
        EXPECTED_PROMPT_SHA256,
        "bytes.byteLength !== 87271",
        "crypto.subtle.digest('SHA-256'",
        "GATEWAY_CANDIDATES",
        "new FormData()",
    ):
        require(marker in client, f"client missing marker: {marker}")

    # Protocol identifiers are authoritative machine-readable manifest fields;
    # they need not be rendered as visible page text.
    primary = manifest["primary_document"]
    protocol = manifest["protocol"]
    require(manifest["schema_version"] == "HIL-EXPERIMENT-v1.1", "manifest schema mismatch")
    require(primary["version"] == "v1.1", "manifest primary version mismatch")
    require(primary["artifact_path"] == EXPECTED_PATH, "manifest artifact path mismatch")
    require(primary["size_bytes"] == EXPECTED_SIZE, "manifest size mismatch")
    require(primary["sha256"] == EXPECTED_SHA256, "manifest hash mismatch")
    require(protocol["version"] == EXPECTED_PROTOCOL, "manifest protocol version mismatch")
    require(protocol["prompt_version"] == EXPECTED_PROMPT, "manifest prompt version mismatch")
    require(protocol["prompt_sha256"] == EXPECTED_PROMPT_SHA256, "manifest prompt hash mismatch")
    require(all(value is False for value in manifest["authority"].values()), "authority must remain fail-closed")

    print("HIL_V1_1_RELEASE_VERIFICATION=PASS")
    print(f"HIL_V1_1_PDF_SIZE={len(payload)}")
    print(f"HIL_V1_1_PDF_SHA256={digest}")
    print(f"HIL_V1_1_ARTIFACT_PATH={EXPECTED_PATH}")
    print(f"HIL_V1_1_PROTOCOL={EXPECTED_PROTOCOL}")
    print(f"HIL_V1_1_PROMPT={EXPECTED_PROMPT}")
    print("HIL_V1_1_DOWNLOAD_CLIENT=BOUND")
    print("HIL_V1_1_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
