#!/usr/bin/env python3
"""Verify deployed Conectrr interoperability assets and browser-test contract.

This check confirms that the public Site serves the runtime loader, fixture, and
required observation markers. It does not claim that a remote browser executed
the JavaScript unless a separate browser runner supplies observed dataset state.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "conectrr-live-verification.json"
BASE_URL = os.environ.get(
    "STEGVERSE_PAGES_BASE_URL",
    "https://stegverse-labs.github.io/Site",
).rstrip("/")

ROUTES: dict[str, tuple[str, ...]] = {
    "ecosystem-chat.html": (
        "assets/ecosystem-node-views.js",
        "Ecosystem Node",
    ),
    "assets/ecosystem-node-views.js": (
        "assets/conectrr-interop.js",
        "importCanonicalEvents",
        "version:'0.4'",
    ),
    "assets/conectrr-interop.js": (
        "conectrrInterop",
        "conectrrBrowserTest",
        "conectrrExportReplay",
        "source-to-decision selection correlation failed",
        "decision-to-source selection correlation failed",
        "export replay broke source-decision correlation",
    ),
    "data/conectrr-independent-evaluation.fixture.json": (
        '"event_id": "event:conectrr:handoff:001"',
        '"event_id": "event:stegverse:evaluation:001"',
        '"agreement_with_source": false',
        '"authority_effect": "none"',
    ),
}


def fetch(route: str) -> tuple[int, str, str]:
    request = urllib.request.Request(
        f"{BASE_URL}/{route}",
        headers={"User-Agent": "StegVerse-Conectrr-Live-Verification/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return (
            response.status,
            response.headers.get("content-type", ""),
            response.read().decode("utf-8", errors="replace"),
        )


def write_report(payload: dict) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    results: list[dict] = []
    passed = True
    for route, markers in ROUTES.items():
        url = f"{BASE_URL}/{route}"
        try:
            status, content_type, body = fetch(route)
            missing = [marker for marker in markers if marker not in body]
            route_passed = status == 200 and not missing
            passed = passed and route_passed
            results.append({
                "route": route,
                "url": url,
                "status": status,
                "content_type": content_type,
                "required_markers": list(markers),
                "missing_markers": missing,
                "passed": route_passed,
            })
            print(f"CONECTRR_LIVE_ROUTE_{'PASS' if route_passed else 'FAIL'}: {url}")
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            passed = False
            results.append({
                "route": route,
                "url": url,
                "status": None,
                "passed": False,
                "error": repr(error),
            })
            print(f"CONECTRR_LIVE_ROUTE_FAIL: {url} error={error!r}")

    payload = {
        "schema_version": "1.0.0",
        "status_type": "conectrr_live_publication_verification",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "base_url": BASE_URL,
        "passed": passed,
        "routes": results,
        "expected_runtime_dataset": {
            "data-conectrr-interop": "loaded",
            "data-conectrr-browser-test": "pass",
            "data-conectrr-export-replay": "pass",
        },
        "claims": {
            "public_assets_present": passed,
            "runtime_observation_contract_published": passed,
            "remote_browser_execution_observed": False,
            "live_external_conectrr_output_verified": False,
            "custody_verified": False,
            "authority_effect": "NONE",
        },
    }
    write_report(payload)
    print("CONECTRR_LIVE_PUBLICATION_CHECK=" + ("PASS" if passed else "FAIL"))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
