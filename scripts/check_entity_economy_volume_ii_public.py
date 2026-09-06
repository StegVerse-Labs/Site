#!/usr/bin/env python3
"""Credential-free deployed-browser verification for bounded paper publication routes.

The observer reuses the Entity Economy Volume II public-browser lane to verify
non-colliding public paper routes and exact artifact identities. It grants no
publication, release, custody, activation, admissibility, credential, or runtime
authority.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

PUBLIC_ROOT = os.environ.get("STEGVERSE_PUBLIC_ROOT", "https://stegverse.org").rstrip("/")
VOLUME_II_ARTIFACT_URL = f"{PUBLIC_ROOT}/papers/stegverse-entity-economy-volume-ii/artifact/"
VOLUME_II_LANDING_URL = f"{PUBLIC_ROOT}/papers/stegverse-entity-economy-volume-ii/"
VOLUME_I_LANDING_URL = f"{PUBLIC_ROOT}/papers/stegverse-entity-economy/"
VOLUME_I_PDF_URL = f"{PUBLIC_ROOT}/papers/stegverse-entity-economy/stegverse-entity-economy.pdf"
COHERENT_PARENT_URL = f"{PUBLIC_ROOT}/papers/coherent-life-and-admissible-existence/"
COHERENT_ARTIFACT_URL = f"{PUBLIC_ROOT}/papers/coherent-life-and-admissible-existence/artifact/"
COHERENT_COMPANION_URL = f"{PUBLIC_ROOT}/papers/coherent-life-companion/"

VOLUME_II_SHA256 = "129accea04dcef0c5b063ae5799d9952e97462859fb36842c93a3ca7776fe95f"
VOLUME_II_BYTES = 132330
VOLUME_II_STATUS = "Verified: canonical seven-page Volume II PDF reconstructed successfully."
VOLUME_I_SHA256 = "9fa7ec36c10ee1c97e71b0ef9245326fab209b3046cc7a83773f4bdf6316e4b0"
VOLUME_I_BYTES = 179582
COHERENT_SHA256 = "6afed983e236b260718df548f40cac2e1a8c12cd9c8f82a28c7a5f757eefe918"
COHERENT_BYTES = 413092
COHERENT_STATUS = "Verified exact approved 36-page PDF: byte length and SHA-256 match."
REPORT = Path(os.environ.get("STEGVERSE_ENTITY_ECONOMY_VOLUME_II_PUBLIC_REPORT", "reports/entity-economy-volume-ii-public.json"))


def observe_loader(page, url: str, expected_status: str, expected_sha: str, expected_bytes: int) -> dict[str, object]:
    response = page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    page.wait_for_function(
        """expected => {
            const el = document.querySelector('#status');
            return el && (el.textContent === expected || el.textContent.startsWith('Artifact unavailable:'));
        }""",
        arg=expected_status,
        timeout=90_000,
    )
    status = page.locator("#status").inner_text()
    sha = page.locator("#sha").inner_text()
    size = page.locator("#size").inner_text()
    open_disabled = page.locator("#open").is_disabled()
    download_aria_disabled = page.locator("#download").get_attribute("aria-disabled")
    download_href = page.locator("#download").get_attribute("href")
    passed = (
        response is not None
        and response.status == 200
        and status == expected_status
        and sha == expected_sha
        and size == str(expected_bytes)
        and open_disabled is False
        and download_aria_disabled is None
        and bool(download_href)
    )
    return {
        "url": url,
        "http_status": response.status if response else None,
        "final_url": page.url,
        "status_text": status,
        "observed_sha256": sha,
        "observed_bytes": int(size) if size.isdigit() else size,
        "open_control_enabled": open_disabled is False,
        "download_control_enabled": download_aria_disabled is None and bool(download_href),
        "passed": passed,
    }


def observe_page(page, url: str, required_text: list[str], required_href_fragments: list[str]) -> dict[str, object]:
    response = page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    body = page.locator("body").inner_text()
    hrefs = page.locator("a").evaluate_all("els => els.map(a => a.getAttribute('href') || '')")
    missing_text = [item for item in required_text if item not in body]
    missing_hrefs = [fragment for fragment in required_href_fragments if not any(fragment in href for href in hrefs)]
    passed = response is not None and response.status == 200 and not missing_text and not missing_hrefs
    return {
        "url": url,
        "http_status": response.status if response else None,
        "final_url": page.url,
        "missing_text": missing_text,
        "missing_href_fragments": missing_hrefs,
        "passed": passed,
    }


def observe_binary(request, url: str, expected_sha: str, expected_bytes: int) -> dict[str, object]:
    response = request.get(url, timeout=60_000, fail_on_status_code=False)
    body = response.body()
    sha = hashlib.sha256(body).hexdigest()
    passed = response.status == 200 and len(body) == expected_bytes and sha == expected_sha and body.startswith(b"%PDF-") and b"%%EOF" in body[-2048:]
    return {
        "url": url,
        "http_status": response.status,
        "observed_bytes": len(body),
        "observed_sha256": sha,
        "pdf_header": body.startswith(b"%PDF-"),
        "pdf_eof": b"%%EOF" in body[-2048:],
        "passed": passed,
    }


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    receipt: dict[str, object] = {
        "schema": "site.current_news_paper_public_observation.v2",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "credential_requirement": "NONE",
        "authority_effect": False,
        "activation_effect": False,
        "publication_authority_granted": False,
        "release_authority_granted": False,
        "expected": {
            "volume_ii_sha256": VOLUME_II_SHA256,
            "volume_ii_bytes": VOLUME_II_BYTES,
            "volume_i_sha256": VOLUME_I_SHA256,
            "volume_i_bytes": VOLUME_I_BYTES,
            "coherent_life_sha256": COHERENT_SHA256,
            "coherent_life_bytes": COHERENT_BYTES,
        },
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 390, "height": 844})
            page = context.new_page()

            checks: dict[str, object] = {}
            checks["volume_ii_artifact"] = observe_loader(page, VOLUME_II_ARTIFACT_URL, VOLUME_II_STATUS, VOLUME_II_SHA256, VOLUME_II_BYTES)
            checks["volume_ii_landing"] = observe_page(
                page,
                VOLUME_II_LANDING_URL,
                ["The StegVerse Entity Economy", "Volume II", "Identity, Agency, Labor, Autonomy, and Legal Standing"],
                ["artifact/"],
            )
            checks["volume_i_landing"] = observe_page(
                page,
                VOLUME_I_LANDING_URL,
                ["The StegVerse Entity Economy", "Volume I"],
                ["stegverse-entity-economy.pdf"],
            )
            checks["volume_i_pdf"] = observe_binary(context.request, VOLUME_I_PDF_URL, VOLUME_I_SHA256, VOLUME_I_BYTES)
            checks["coherent_life_parent"] = observe_page(
                page,
                COHERENT_PARENT_URL,
                ["Coherent Life and Admissible Existence", "Attached companion materials", "Complete paper — 36 pages"],
                ["artifact/", "coherent-life-companion/"],
            )
            checks["coherent_life_companion"] = observe_page(
                page,
                COHERENT_COMPANION_URL,
                ["Coherent Life and Admissible Existence", "Companion Extensions", "Notation Table and Theorem Witnesses", "Unknown-Class Transformation at the Quantum-Gravitational Boundary", "Recoverable Capacity Across Representational Boundaries"],
                [],
            )
            checks["coherent_life_artifact"] = observe_loader(page, COHERENT_ARTIFACT_URL, COHERENT_STATUS, COHERENT_SHA256, COHERENT_BYTES)

            receipt["checks"] = checks
            passed = all(bool(check.get("passed")) for check in checks.values() if isinstance(check, dict))
            receipt["state"] = "VERIFIED_PUBLIC_PAPER_ROUTE_SET" if passed else "PUBLIC_PAPER_ROUTE_SET_MISMATCH"
            receipt["passed"] = passed
            browser.close()
    except PlaywrightTimeoutError as exc:
        receipt.update({"state": "PUBLIC_BROWSER_TIMEOUT", "passed": False, "error": str(exc)})
    except Exception as exc:
        receipt.update({"state": "PUBLIC_BROWSER_ERROR", "passed": False, "error": f"{type(exc).__name__}: {exc}"})

    REPORT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    if receipt.get("passed") is True:
        print("CURRENT_NEWS_PAPER_PUBLIC_OBSERVATION=PASS")
        print(f"ENTITY_ECONOMY_VOLUME_II_PUBLIC_SHA256={VOLUME_II_SHA256}")
        print(f"ENTITY_ECONOMY_VOLUME_I_PUBLIC_SHA256={VOLUME_I_SHA256}")
        print(f"COHERENT_LIFE_PUBLIC_SHA256={COHERENT_SHA256}")
        print("AUTHORITY_EFFECT=NONE")
        return 0
    print("CURRENT_NEWS_PAPER_PUBLIC_OBSERVATION=FAIL")
    print("AUTHORITY_EFFECT=NONE")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
