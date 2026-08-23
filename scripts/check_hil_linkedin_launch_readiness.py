#!/usr/bin/env python3
"""Fail-closed consistency checks for the HIL v1.1 LinkedIn launch boundary."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data" / "hil-linkedin-launch-readiness.json"
PRIMARY = ROOT / "data" / "HIL_Canonical_Paper_v1_1.pdf"
PAGE = ROOT / "humans-as-interoperability-layer.html"
CLIENT = ROOT / "assets" / "hil-experiment-v1.1.js"
CHECKLIST = ROOT / "docs" / "HIL_LINKEDIN_LAUNCH_CHECKLIST.md"

EXPECTED_SIZE = 87271
EXPECTED_PRIMARY_HASH = "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462"
EXPECTED_PROMPT_HASH = "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c"
EXPECTED_PUBLIC_URL = "https://stegverse-labs.github.io/Site/humans-as-interoperability-layer.html"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL LinkedIn launch verification failed: {message}")


def all_claims_true(claims: dict[str, object], required: list[str]) -> bool:
    return all(claims.get(key) is True for key in required)


def main() -> None:
    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")
    client = CLIENT.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    payload = PRIMARY.read_bytes()

    require(payload.startswith(b"%PDF-"), "canonical Primary lacks PDF signature")
    require(len(payload) == EXPECTED_SIZE, f"canonical Primary size mismatch: {len(payload)}")
    actual_hash = hashlib.sha256(payload).hexdigest()
    require(actual_hash == EXPECTED_PRIMARY_HASH, f"canonical Primary hash mismatch: {actual_hash}")

    require(readiness["experiment_version"] == "v1.1", "readiness version mismatch")
    require(readiness["public_url"] == EXPECTED_PUBLIC_URL, "public URL mismatch")
    require(readiness["canonical_primary"]["path"] == "data/HIL_Canonical_Paper_v1_1.pdf", "artifact path mismatch")
    require(readiness["canonical_primary"]["size_bytes"] == EXPECTED_SIZE, "declared size mismatch")
    require(readiness["canonical_primary"]["sha256"] == EXPECTED_PRIMARY_HASH, "declared Primary hash mismatch")
    require(readiness["canonical_prompt"]["sha256"] == EXPECTED_PROMPT_HASH, "declared prompt hash mismatch")

    for marker in ("v1.1", "HIL_Canonical_Paper_v1_1.pdf", EXPECTED_PRIMARY_HASH, EXPECTED_PROMPT_HASH):
        require(marker in page, f"public page missing marker: {marker}")
    for marker in ("data/HIL_Canonical_Paper_v1_1.pdf", EXPECTED_PRIMARY_HASH, EXPECTED_PROMPT_HASH):
        require(marker in client, f"client missing marker: {marker}")
    require(EXPECTED_PUBLIC_URL in checklist, "checklist public URL mismatch")

    claims = readiness["launch_claims"]
    wording = readiness["allowed_linkedin_wording"]
    intake_requirements = readiness["required_before_intake_live_claim"]
    acquisition_requirements = readiness["required_before_public_acquisition_open"]
    intake_ready = all_claims_true(claims, intake_requirements)
    acquisition_ready = all_claims_true(claims, acquisition_requirements)

    require(wording["research_surface_public"] is True, "research surface should be public")
    require(wording["canonical_download_available"] is True, "canonical download claim must be true")
    require(wording["governed_response_intake_live"] is intake_ready, "intake-live wording exceeds or understates evidence")
    require(wording["public_response_acquisition_open"] is acquisition_ready, "public-acquisition wording exceeds or understates evidence")
    require(all(value is False for value in readiness["authority"].values()), "readiness record must grant no authority")

    print("HIL_LINKEDIN_LAUNCH_VERIFICATION=PASS")
    print(f"HIL_PRIMARY_SHA256={actual_hash}")
    print(f"HIL_PUBLIC_URL={EXPECTED_PUBLIC_URL}")
    print("HIL_RESEARCH_SURFACE_PUBLIC=true")
    print(f"HIL_GOVERNED_INTAKE_LIVE={str(wording['governed_response_intake_live']).lower()}")
    print(f"HIL_PUBLIC_ACQUISITION_OPEN={str(wording['public_response_acquisition_open']).lower()}")
    print("HIL_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
