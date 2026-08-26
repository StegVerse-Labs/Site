#!/usr/bin/env python3
"""Compatibility validator for the canonical HIL v1.1 participant surface.

Historical v0.5 review evidence is preserved as provenance, but the active public
page is governed by the v1.1 release/upload contracts. This validator therefore
consumes the canonical validators instead of requiring superseded presentation
copy on the live page.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_STATE = ROOT / "data" / "hil-review-state.json"
TRACE = ROOT / "data" / "hil-traces" / "HIL-TRACE-0001.json"
CANONICAL_VALIDATORS = (
    ROOT / "scripts" / "check_hil_v1_1_release.py",
    ROOT / "scripts" / "check_hil_v1_upload_surface.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"HIL experiment compatibility verification failed: {message}")


def run_validator(path: Path) -> None:
    require(path.is_file(), f"missing canonical validator: {path.relative_to(ROOT)}")
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    require(result.returncode == 0, f"canonical validator failed: {path.name}")


def main() -> None:
    for validator in CANONICAL_VALIDATORS:
        run_validator(validator)

    require(REVIEW_STATE.is_file(), "missing preserved v0.5 review state")
    require(TRACE.is_file(), "missing preserved HIL-TRACE-0001")
    review = json.loads(REVIEW_STATE.read_text(encoding="utf-8"))
    trace = json.loads(TRACE.read_text(encoding="utf-8"))

    candidate = review.get("review_candidate") or {}
    authority = review.get("authority") or {}
    require(review.get("schema_version") == "HIL-REVIEW-STATE-v1", "legacy review state schema mismatch")
    require(candidate.get("version") == "v0.5", "historical review candidate identity missing")
    require(candidate.get("sha256") == "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946", "historical review candidate hash mismatch")
    require(review.get("final_presentation_approval") == "APPROVED", "historical participant approval missing")
    require(all(value == "APPROVED" for value in (review.get("requested_review") or {}).values()), "historical requested review decisions incomplete")
    require(authority.get("review_candidate_is_canonical") is False, "v0.5 review candidate must remain non-canonical")
    require(authority.get("site_preview_is_publication_authority") is False, "historical Site preview must not grant publication authority")
    require(authority.get("response_intake_authorized") is False, "historical review state must not grant current intake authority")
    require(trace.get("trace_id") == "HIL-TRACE-0001", "historical trace identity mismatch")
    require((trace.get("review") or {}).get("state") == "PARTICIPANT_REVIEW_APPROVED", "historical trace review state mismatch")
    require((trace.get("authority") or {}).get("technical_activation_approved") is False, "historical review must not imply technical activation")

    print("HIL_EXPERIMENT_STATIC_VERIFICATION=PASS")
    print("HIL_CANONICAL_PUBLIC_VERSION=v1.1")
    print("HIL_V0_5_REVIEW_EVIDENCE=PRESERVED_NONCANONICAL")
    print("HIL_PUBLIC_PAGE_LEGACY_PRESENTATION_REQUIRED=false")
    print("HIL_AUTHORITY=NONE")


if __name__ == "__main__":
    main()
