#!/usr/bin/env python3
"""Credential-free deployed-browser verification for Entity Economy Volume II.

This observer executes the already-published artifact loader in Chromium and
requires the browser-visible reconstruction result to match the canonical
Volume II byte count and SHA-256. It grants no publication, release, custody,
activation, admissibility, credential, or runtime authority.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

URL = os.environ.get(
    "STEGVERSE_ENTITY_ECONOMY_VOLUME_II_ARTIFACT_URL",
    "https://stegverse.org/papers/stegverse-entity-economy-volume-ii/artifact/",
)
EXPECTED_SHA256 = "129accea04dcef0c5b063ae5799d9952e97462859fb36842c93a3ca7776fe95f"
EXPECTED_BYTES = "132330"
EXPECTED_STATUS = "Verified: canonical seven-page Volume II PDF reconstructed successfully."
REPORT = Path(os.environ.get("STEGVERSE_ENTITY_ECONOMY_VOLUME_II_PUBLIC_REPORT", "reports/entity-economy-volume-ii-public.json"))


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    receipt: dict[str, object] = {
        "schema": "site.entity_economy_volume_ii_public_observation.v1",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "url": URL,
        "expected_sha256": EXPECTED_SHA256,
        "expected_bytes": int(EXPECTED_BYTES),
        "credential_requirement": "NONE",
        "authority_effect": False,
        "activation_effect": False,
        "publication_authority_granted": False,
        "release_authority_granted": False,
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 390, "height": 844})
            response = page.goto(URL, wait_until="domcontentloaded", timeout=60_000)
            receipt["http_status"] = response.status if response else None
            receipt["final_url"] = page.url
            page.wait_for_function(
                """expected => {
                    const el = document.querySelector('#status');
                    return el && (el.textContent === expected || el.textContent.startsWith('Artifact unavailable:'));
                }""",
                arg=EXPECTED_STATUS,
                timeout=90_000,
            )
            status = page.locator("#status").inner_text()
            sha = page.locator("#sha").inner_text()
            size = page.locator("#size").inner_text()
            open_disabled = page.locator("#open").is_disabled()
            download_aria_disabled = page.locator("#download").get_attribute("aria-disabled")
            download_href = page.locator("#download").get_attribute("href")
            receipt.update(
                {
                    "status_text": status,
                    "observed_sha256": sha,
                    "observed_bytes_text": size,
                    "open_control_disabled": open_disabled,
                    "download_aria_disabled": download_aria_disabled,
                    "download_href_present": bool(download_href),
                }
            )
            passed = (
                response is not None
                and response.status == 200
                and status == EXPECTED_STATUS
                and sha == EXPECTED_SHA256
                and size == EXPECTED_BYTES
                and open_disabled is False
                and download_aria_disabled is None
                and bool(download_href)
            )
            receipt["state"] = "VERIFIED_PUBLIC_BROWSER_EXECUTION" if passed else "PUBLIC_BROWSER_EXECUTION_MISMATCH"
            receipt["passed"] = passed
            browser.close()
    except PlaywrightTimeoutError as exc:
        receipt.update({"state": "PUBLIC_BROWSER_TIMEOUT", "passed": False, "error": str(exc)})
    except Exception as exc:  # fail closed and retain exact observer failure
        receipt.update({"state": "PUBLIC_BROWSER_ERROR", "passed": False, "error": f"{type(exc).__name__}: {exc}"})

    REPORT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    if receipt.get("passed") is True:
        print("ENTITY_ECONOMY_VOLUME_II_PUBLIC_BROWSER_OBSERVATION=PASS")
        print(f"ENTITY_ECONOMY_VOLUME_II_PUBLIC_SHA256={EXPECTED_SHA256}")
        print(f"ENTITY_ECONOMY_VOLUME_II_PUBLIC_BYTES={EXPECTED_BYTES}")
        print("AUTHORITY_EFFECT=NONE")
        return 0
    print("ENTITY_ECONOMY_VOLUME_II_PUBLIC_BROWSER_OBSERVATION=FAIL")
    print("AUTHORITY_EFFECT=NONE")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
