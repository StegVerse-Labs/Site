#!/usr/bin/env python3
"""Observe the deployed HIL Site and bounded intake gateway without granting activation."""
from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SITE_URL = "https://stegverse-labs.github.io/Site/humans-as-interoperability-layer.html"
GATEWAY_URL = "https://stegverse-ecosystem-chat-gateway.onrender.com/api/hil/readiness"
EXPECTED_HASH = "52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946"
EXPECTED_TRACE = "HIL-TRACE-0001"


def fetch(url: str) -> tuple[int, bytes, str]:
    request = Request(url, headers={"User-Agent": "StegVerse-HIL-live-readiness/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.status, response.read(), response.headers.get("Content-Type", "")


def main() -> int:
    report = {
        "schema": "stegverse.hil_live_readiness_observation.v1",
        "site_url": SITE_URL,
        "gateway_url": GATEWAY_URL,
        "site_observed": False,
        "site_review_surface_current": False,
        "gateway_observed": False,
        "gateway_state": "UNKNOWN",
        "gateway_primary_hash_matches_review_candidate": False,
        "public_acquisition_authorized": False,
        "publication_authority": False,
        "activation_authority": False,
        "blockers": [],
    }

    try:
        status, body, content_type = fetch(SITE_URL)
        text = body.decode("utf-8", errors="replace")
        report["site_observed"] = status == 200 and "text/html" in content_type
        required = (
            "Prepublication review",
            "Sara Katpar",
            EXPECTED_TRACE,
            "Review permission",
            "final presentation approval",
        )
        report["site_review_surface_current"] = report["site_observed"] and all(item in text for item in required)
        if not report["site_observed"]:
            report["blockers"].append("site_not_observed")
        elif not report["site_review_surface_current"]:
            report["blockers"].append("site_review_surface_stale")
    except (HTTPError, URLError, TimeoutError) as exc:
        report["blockers"].append(f"site_fetch_failed:{type(exc).__name__}")

    try:
        status, body, _content_type = fetch(GATEWAY_URL)
        payload = json.loads(body.decode("utf-8"))
        report["gateway_observed"] = status == 200
        report["gateway_state"] = payload.get("state", "UNKNOWN")
        report["gateway_primary_hash_matches_review_candidate"] = payload.get("primary_sha256") == EXPECTED_HASH
        if not report["gateway_observed"]:
            report["blockers"].append("gateway_not_observed")
        if report["gateway_state"] != "READY":
            report["blockers"].append("gateway_not_ready")
        if not report["gateway_primary_hash_matches_review_candidate"]:
            report["blockers"].append("gateway_primary_hash_not_v0_5_review_candidate")
        if payload.get("publication_authority") is not False:
            report["blockers"].append("gateway_publication_boundary_invalid")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        report["blockers"].append(f"gateway_fetch_failed:{type(exc).__name__}")

    report["review_surface_ready"] = report["site_review_surface_current"]
    report["intake_execution_ready"] = (
        report["gateway_observed"]
        and report["gateway_state"] == "READY"
        and report["gateway_primary_hash_matches_review_candidate"]
    )
    report["state"] = "REVIEW_READY" if report["review_surface_ready"] else "REVIEW_NOT_READY"

    print(json.dumps(report, indent=2, sort_keys=True))
    print("HIL_LIVE_REVIEW_SURFACE=" + ("PASS" if report["review_surface_ready"] else "FAIL"))
    print("HIL_LIVE_INTAKE=" + ("READY" if report["intake_execution_ready"] else "NOT_READY"))
    print("HIL_PUBLIC_ACQUISITION_AUTHORITY=NONE")

    return 0 if report["review_surface_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
