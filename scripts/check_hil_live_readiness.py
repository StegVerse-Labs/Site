#!/usr/bin/env python3
"""Observe deployed HIL surfaces and emit non-authorizing readiness evidence."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SITE_URL = "https://stegverse-labs.github.io/Site/humans-as-interoperability-layer.html"
PRIMARY_URL = "https://stegverse-labs.github.io/Site/data/hil-primary-v0.5-review.pdf.b64"
GATEWAY_BASE = "https://stegverse-ecosystem-chat-gateway.onrender.com/api/hil"
EXPECTED_PRIMARY_HASH = "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"
EXPECTED_PROMPT_HASH = "0ebe215318b4eeeb8ed6422e0954372c314fadc8fac9254e452bc7670a1b9922"
EXPECTED_TRACE = "HIL-TRACE-0001"


def fetch(url: str) -> tuple[int, bytes, str]:
    request = Request(url, headers={"User-Agent": "StegVerse-HIL-live-readiness/2.0"})
    with urlopen(request, timeout=30) as response:
        return response.status, response.read(), response.headers.get("Content-Type", "")


def add_once(report: dict, blocker: str) -> None:
    if blocker not in report["blockers"]:
        report["blockers"].append(blocker)


def observe() -> dict:
    report = {
        "schema_version": "HIL-LIVE-READINESS-OBSERVATION-v2",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "site_url": SITE_URL,
        "primary_url": PRIMARY_URL,
        "gateway_readiness_url": f"{GATEWAY_BASE}/readiness",
        "publication_readiness_url": f"{GATEWAY_BASE}/publication-readiness",
        "site_observed": False,
        "site_approved_surface_current": False,
        "primary_artifact_observed": False,
        "primary_artifact_sha256": None,
        "primary_artifact_hash_matches": False,
        "gateway_observed": False,
        "gateway_state": "UNKNOWN",
        "gateway_primary_hash_matches": False,
        "gateway_prompt_hash_matches": False,
        "gateway_provenance_required": False,
        "gateway_private_review_configured": False,
        "publication_readiness_observed": False,
        "publication_state": "UNKNOWN",
        "publication_append_only": False,
        "controlled_cycle_ready": False,
        "public_acquisition_authorized": False,
        "publication_authority": False,
        "activation_authority": False,
        "master_record_append_authority": False,
        "blockers": [],
    }

    try:
        status, body, content_type = fetch(SITE_URL)
        text = body.decode("utf-8", errors="replace")
        report["site_observed"] = status == 200 and "text/html" in content_type
        required = (
            "Approved presentation",
            "Sara Katpar",
            EXPECTED_TRACE,
            "Submit response artifact",
            "Prompt SHA-256",
        )
        report["site_approved_surface_current"] = report["site_observed"] and all(
            marker in text for marker in required
        )
        if not report["site_observed"]:
            add_once(report, "site_not_observed")
        elif not report["site_approved_surface_current"]:
            add_once(report, "site_approved_surface_stale")
    except (HTTPError, URLError, TimeoutError) as exc:
        add_once(report, f"site_fetch_failed:{type(exc).__name__}")

    try:
        status, body, _content_type = fetch(PRIMARY_URL)
        encoded = b"".join(body.split())
        payload = base64.b64decode(encoded, validate=True)
        digest = hashlib.sha256(payload).hexdigest()
        report["primary_artifact_observed"] = status == 200 and payload.startswith(b"%PDF-")
        report["primary_artifact_sha256"] = digest
        report["primary_artifact_hash_matches"] = digest == EXPECTED_PRIMARY_HASH
        if not report["primary_artifact_observed"]:
            add_once(report, "primary_artifact_not_observed")
        if not report["primary_artifact_hash_matches"]:
            add_once(report, "primary_artifact_hash_mismatch")
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        add_once(report, f"primary_artifact_fetch_failed:{type(exc).__name__}")

    try:
        status, body, _content_type = fetch(f"{GATEWAY_BASE}/readiness")
        payload = json.loads(body.decode("utf-8"))
        report["gateway_observed"] = status == 200
        report["gateway_state"] = payload.get("state", "UNKNOWN")
        report["gateway_primary_hash_matches"] = payload.get("primary_sha256") == EXPECTED_PRIMARY_HASH
        report["gateway_prompt_hash_matches"] = payload.get("prompt_sha256") == EXPECTED_PROMPT_HASH
        report["gateway_provenance_required"] = payload.get("provenance_manifest_required") is True
        report["gateway_private_review_configured"] = payload.get("private_review_configured") is True
        if not report["gateway_observed"]:
            add_once(report, "gateway_not_observed")
        if report["gateway_state"] != "READY":
            add_once(report, "gateway_not_ready")
        if not report["gateway_primary_hash_matches"]:
            add_once(report, "gateway_primary_hash_mismatch")
        if not report["gateway_prompt_hash_matches"]:
            add_once(report, "gateway_prompt_hash_mismatch")
        if not report["gateway_provenance_required"]:
            add_once(report, "gateway_provenance_requirement_missing")
        if not report["gateway_private_review_configured"]:
            add_once(report, "gateway_private_review_not_configured")
        if payload.get("publication_authority") is not False:
            add_once(report, "gateway_publication_boundary_invalid")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        add_once(report, f"gateway_fetch_failed:{type(exc).__name__}")

    try:
        status, body, _content_type = fetch(f"{GATEWAY_BASE}/publication-readiness")
        payload = json.loads(body.decode("utf-8"))
        report["publication_readiness_observed"] = status == 200
        report["publication_state"] = payload.get("state", "UNKNOWN")
        report["publication_append_only"] = payload.get("append_only") is True
        if not report["publication_readiness_observed"]:
            add_once(report, "publication_readiness_not_observed")
        if report["publication_state"] != "READY":
            add_once(report, "publication_not_ready")
        if not report["publication_append_only"]:
            add_once(report, "publication_append_only_boundary_missing")
        if payload.get("execution_authority") is not False:
            add_once(report, "publication_execution_boundary_invalid")
        if payload.get("master_record_append_authority") is not False:
            add_once(report, "publication_master_record_boundary_invalid")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        add_once(report, f"publication_readiness_fetch_failed:{type(exc).__name__}")

    report["controlled_cycle_ready"] = all(
        (
            report["site_approved_surface_current"],
            report["primary_artifact_hash_matches"],
            report["gateway_state"] == "READY",
            report["gateway_primary_hash_matches"],
            report["gateway_prompt_hash_matches"],
            report["gateway_provenance_required"],
            report["gateway_private_review_configured"],
            report["publication_state"] == "READY",
            report["publication_append_only"],
        )
    )
    report["state"] = "CONTROLLED_CYCLE_READY" if report["controlled_cycle_ready"] else "BLOCKED"
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="write the JSON observation to this path")
    args = parser.parse_args()
    report = observe()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    print("HIL_LIVE_APPROVED_SURFACE=" + ("PASS" if report["site_approved_surface_current"] else "FAIL"))
    print("HIL_PRIMARY_ARTIFACT=" + ("VERIFIED" if report["primary_artifact_hash_matches"] else "NOT_VERIFIED"))
    print("HIL_CONTROLLED_CYCLE=" + ("READY" if report["controlled_cycle_ready"] else "BLOCKED"))
    print("HIL_PUBLIC_ACQUISITION_AUTHORITY=NONE")
    return 0 if report["site_approved_surface_current"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
