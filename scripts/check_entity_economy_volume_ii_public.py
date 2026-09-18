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
ENTITY_ECONOMY_SERIES_URL = f"{PUBLIC_ROOT}/papers/stegverse-entity-economy-series/"
NEWS_RELEASES_URL = f"{PUBLIC_ROOT}/news-releases.html"

VOLUME_II_SHA256 = "129accea04dcef0c5b063ae5799d9952e97462859fb36842c93a3ca7776fe95f"
VOLUME_II_BYTES = 132330
VOLUME_II_STATUS = "Verified: canonical seven-page Volume II PDF reconstructed successfully."
VOLUME_I_REPOSITORY_PATH = Path("papers/stegverse-entity-economy/stegverse-entity-economy.pdf")
VOLUME_I_REPOSITORY_BYTES = VOLUME_I_REPOSITORY_PATH.read_bytes()
VOLUME_I_SHA256 = hashlib.sha256(VOLUME_I_REPOSITORY_BYTES).hexdigest()
VOLUME_I_BYTES = len(VOLUME_I_REPOSITORY_BYTES)
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


def observe_edition_feed(page, url: str) -> dict[str, object]:
    response = page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    select = page.locator("#edition")
    releases = page.locator(".release[data-published]")
    initial_value = select.input_value()
    initial_visible = page.locator(".release[data-published]:not([hidden])").count()
    option_values = select.locator("option").evaluate_all("els => els.map(o => o.value)")

    select.select_option("2026-09-04")
    visible_0904 = page.locator(".release[data-published]:not([hidden])").all_inner_texts()

    select.select_option("2026-09-03")
    visible_0903 = page.locator(".release[data-published]:not([hidden])").all_inner_texts()

    select.select_option("all")
    visible_all = page.locator(".release[data-published]:not([hidden])").count()

    published = releases.evaluate_all("els => els.map(e => e.dataset.published)")
    sequences = releases.evaluate_all("els => els.map(e => Number(e.dataset.sequence))")
    deterministic_order = sequences == sorted(sequences, reverse=True)

    required_0903 = [
        "The StegVerse Entity Economy — Volume II",
        "The StegVerse Entity Economy — Volume I",
        "AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model.",
    ]
    joined_0903 = "\n".join(visible_0903)
    passed = (
        response is not None
        and response.status == 200
        and initial_value == "2026-09-05"
        and initial_visible == 1
        and option_values == ["2026-09-05", "2026-09-04", "2026-09-03", "all"]
        and any("Coherent Life and Admissible Existence" in item for item in visible_0904)
        and all(item in joined_0903 for item in required_0903)
        and visible_all == len(published) == 5
        and deterministic_order
    )
    return {
        "url": url,
        "http_status": response.status if response else None,
        "final_url": page.url,
        "initial_edition": initial_value,
        "initial_visible_count": initial_visible,
        "edition_options": option_values,
        "visible_2026_09_04": visible_0904,
        "visible_2026_09_03": visible_0903,
        "all_releases_visible_count": visible_all,
        "release_count": len(published),
        "published_dates": published,
        "sequence_values": sequences,
        "deterministic_sequence_preserved": deterministic_order,
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
            "volume_i_repository_path": str(VOLUME_I_REPOSITORY_PATH),
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
            volume_i_passed = bool(checks["volume_i_landing"].get("passed")) and bool(checks["volume_i_pdf"].get("passed"))
            receipt["volume_i_state"] = "VERIFIED_PUBLIC_REPOSITORY_IDENTITY" if volume_i_passed else "VOLUME_I_PUBLIC_REPOSITORY_IDENTITY_MISMATCH"
            receipt["volume_i_repository_identity"] = {
                "path": str(VOLUME_I_REPOSITORY_PATH),
                "bytes": VOLUME_I_BYTES,
                "sha256": VOLUME_I_SHA256,
            }
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
            checks["entity_economy_series"] = observe_page(
                page,
                ENTITY_ECONOMY_SERIES_URL,
                [
                    "The StegVerse Entity Economy",
                    "From scarce professional capability to sovereign, attributable economic participation.",
                    "not a new paper identity",
                    "not an empirical forecast",
                ],
                ["../stegverse-entity-economy/", "../stegverse-entity-economy-volume-ii/", "../coherent-life-and-admissible-existence/"],
            )
            checks["edition_feed"] = observe_edition_feed(page, NEWS_RELEASES_URL)

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
    print(
        "ENTITY_ECONOMY_VOLUME_I_PUBLIC_OBSERVATION="
        + ("PASS" if receipt.get("volume_i_state") == "VERIFIED_PUBLIC_REPOSITORY_IDENTITY" else "FAIL")
    )
    if receipt.get("passed") is True:
        print("CURRENT_NEWS_PAPER_PUBLIC_OBSERVATION=PASS")
        print(f"ENTITY_ECONOMY_VOLUME_II_PUBLIC_SHA256={VOLUME_II_SHA256}")
        print(f"ENTITY_ECONOMY_VOLUME_I_PUBLIC_SHA256={VOLUME_I_SHA256}")
        print(f"COHERENT_LIFE_PUBLIC_SHA256={COHERENT_SHA256}")
        print("ENTITY_ECONOMY_SERIES_PUBLIC_OBSERVATION=PASS")
        print("CURRENT_NEWS_EDITION_FEED_PUBLIC_OBSERVATION=PASS")
        print("AUTHORITY_EFFECT=NONE")
        return 0
    print("CURRENT_NEWS_PAPER_PUBLIC_OBSERVATION=FAIL")
    print("AUTHORITY_EFFECT=NONE")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
