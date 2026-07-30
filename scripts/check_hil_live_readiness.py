#!/usr/bin/env python3
"""Observe the canonical deployed HIL surface and receiver without granting authority."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SITE_URL = "https://stegverse.org/hil/upload/"
READINESS_URL = "https://stegverse.org/api/hil/readiness"
EXPECTED = {
    "schema_version": "HIL-RECEIVER-READINESS-v2",
    "state": "READY",
    "receiver_mode": "FULL_CUSTODY",
    "primary_version": "v1.1",
    "primary_sha256": "a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462",
    "protocol_version": "HIL-PROTOCOL-v1.1",
    "prompt_version": "HIL-PROMPT-v1.1",
    "prompt_sha256": "cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c",
    "provenance_manifest_required": True,
    "provenance_manifest_schema": "HIL-RESPONSE-PROVENANCE-v1.1",
    "participant_metadata_required": False,
    "custody_backend": "portable-sqlite-chunks-v1",
    "registry_backend": "sqlite-compatible-registry",
}
SITE_MARKERS = (
    "Submit the single Response PDF",
    "Choose the unchanged response PDF",
    "Upload unavailable",
)


def fetch(url: str) -> tuple[int, bytes, str]:
    request = Request(
        url,
        headers={
            "Accept": "text/html,application/json",
            "User-Agent": "StegVerse-HIL-live-readiness/3.0",
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.status, response.read(65537), response.headers.get("Content-Type", "")


def add_once(report: dict, blocker: str) -> None:
    if blocker not in report["blockers"]:
        report["blockers"].append(blocker)


def observe() -> dict:
    report: dict[str, object] = {
        "schema_version": "HIL-LIVE-READINESS-OBSERVATION-v3",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "site_url": SITE_URL,
        "readiness_url": READINESS_URL,
        "site_observed": False,
        "site_current": False,
        "readiness_observed": False,
        "readiness_http_status": None,
        "readiness_state": "NOT_OBSERVED",
        "readiness_contract_matches": False,
        "readiness_mismatches": {},
        "controlled_cycle_ready": False,
        "public_acquisition_authorized": False,
        "publication_authority": False,
        "activation_authority": False,
        "master_record_append_authority": False,
        "blockers": [],
    }

    try:
        status, body, content_type = fetch(SITE_URL)
        if len(body) > 65536:
            add_once(report, "site_response_too_large")
            body = body[:65536]
        text = body.decode("utf-8", errors="replace")
        report["site_observed"] = status == 200 and "text/html" in content_type.lower()
        report["site_current"] = bool(report["site_observed"]) and all(
            marker in text for marker in SITE_MARKERS
        )
        if not report["site_observed"]:
            add_once(report, "site_not_observed")
        elif not report["site_current"]:
            add_once(report, "site_canonical_surface_stale")
    except (HTTPError, URLError, TimeoutError) as exc:
        add_once(report, f"site_fetch_failed:{type(exc).__name__}")

    try:
        status, body, content_type = fetch(READINESS_URL)
        if len(body) > 65536:
            add_once(report, "readiness_response_too_large")
            body = body[:65536]
        report["readiness_http_status"] = status
        report["readiness_observed"] = "application/json" in content_type.lower()
        payload = json.loads(body.decode("utf-8"))
        report["readiness_state"] = payload.get("state", "UNKNOWN")
        mismatches = {
            key: {"expected": expected, "actual": payload.get(key)}
            for key, expected in EXPECTED.items()
            if payload.get(key) != expected
        }
        report["readiness_mismatches"] = mismatches
        report["readiness_contract_matches"] = status == 200 and not mismatches
        if not report["readiness_observed"]:
            add_once(report, "readiness_not_observed")
        if status != 200:
            add_once(report, f"readiness_http_status:{status}")
        if payload.get("state") != "READY":
            add_once(report, f"receiver_state:{payload.get('state', 'UNKNOWN')}")
        for key in mismatches:
            add_once(report, f"readiness_mismatch:{key}")
    except HTTPError as exc:
        report["readiness_http_status"] = exc.code
        try:
            payload = json.loads(exc.read(65536).decode("utf-8"))
            report["readiness_observed"] = True
            report["readiness_state"] = payload.get("state", "UNKNOWN")
            report["readiness_mismatches"] = {
                key: {"expected": expected, "actual": payload.get(key)}
                for key, expected in EXPECTED.items()
                if payload.get(key) != expected
            }
        except Exception:
            pass
        add_once(report, f"readiness_http_error:{exc.code}")
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        add_once(report, f"readiness_fetch_failed:{type(exc).__name__}")

    report["controlled_cycle_ready"] = bool(
        report["site_current"] and report["readiness_contract_matches"]
    )
    if report["controlled_cycle_ready"]:
        report["state"] = "CONTROLLED_CYCLE_READY"
    elif report["site_current"]:
        report["state"] = "CANONICAL_SURFACE_OBSERVED_RECEIVER_NOT_READY"
    else:
        report["state"] = "BLOCKED"
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
    print("HIL_LIVE_SITE_SURFACE=" + ("PASS" if report["site_current"] else "FAIL"))
    print("HIL_RECEIVER_READINESS=" + str(report["readiness_state"]))
    print("HIL_CONTROLLED_CYCLE=" + ("READY" if report["controlled_cycle_ready"] else "BLOCKED"))
    print("HIL_PUBLIC_ACQUISITION_AUTHORITY=NONE")
    return 0 if report["site_current"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
