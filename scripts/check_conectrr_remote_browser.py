#!/usr/bin/env python3
"""Execute the deployed Conectrr fixture in a real headless browser.

This verifies browser execution of the published fixture and its projection
markers. It does not claim genuine external Conectrr interoperability, custody,
certification, admissibility, or authority.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "conectrr-remote-browser-verification.json"
BASE_URL = os.environ.get(
    "STEGVERSE_PAGES_BASE_URL", "https://stegverse-labs.github.io/Site"
).rstrip("/")
URL = f"{BASE_URL}/ecosystem-chat.html"
SOURCE_ID = "event:conectrr:handoff:001"
DECISION_ID = "event:stegverse:evaluation:001"


def write_report(payload: dict) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    payload: dict = {
        "schema": "stegverse.conectrr.remote-browser-verification.v1",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "url": URL,
        "passed": False,
        "markers": {},
        "records": {},
        "correlation": {},
        "authority_effect": "none",
        "claims_not_created": [
            "live_external_interoperability",
            "custody",
            "certification",
            "authorization_to_operate",
            "admissibility",
            "execution_authority",
        ],
    }
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL, wait_until="networkidle", timeout=60_000)
            page.wait_for_function(
                """() => document.documentElement.dataset.conectrrInterop === 'loaded' &&
                document.documentElement.dataset.conectrrBrowserTest === 'pass' &&
                document.documentElement.dataset.conectrrExportReplay === 'pass'""",
                timeout=45_000,
            )
            markers = page.evaluate(
                """() => ({
                  interop: document.documentElement.dataset.conectrrInterop,
                  browser_test: document.documentElement.dataset.conectrrBrowserTest,
                  export_replay: document.documentElement.dataset.conectrrExportReplay
                })"""
            )
            source = page.locator(f'[data-event-id="{SOURCE_ID}"]')
            decision = page.locator(f'[data-event-id="{DECISION_ID}"]')
            source_count = source.count()
            decision_count = decision.count()

            page.evaluate(
                """(id) => window.StegVerseCanonicalEventStream.selectEvent(id, 'governed')""",
                SOURCE_ID,
            )
            source_to_decision = page.locator(
                f'[data-event-id="{DECISION_ID}"].correlated-active'
            ).count() > 0

            page.evaluate(
                """(id) => window.StegVerseCanonicalEventStream.selectEvent(id, 'governed')""",
                DECISION_ID,
            )
            decision_to_source = page.locator(
                f'[data-event-id="{SOURCE_ID}"].correlated-active'
            ).count() > 0

            events = page.evaluate(
                """() => window.StegVerseCanonicalEventStream.getEvents()
                  .filter(e => e.event_id === 'event:conectrr:handoff:001' ||
                               e.event_id === 'event:stegverse:evaluation:001')"""
            )
            browser.close()

        passed = (
            markers == {
                "interop": "loaded",
                "browser_test": "pass",
                "export_replay": "pass",
            }
            and source_count >= 1
            and decision_count >= 1
            and source_to_decision
            and decision_to_source
            and len(events) == 2
            and events[1].get("parent_event_id") == SOURCE_ID
            and SOURCE_ID in events[1].get("evidence_refs", [])
        )
        payload.update(
            {
                "passed": passed,
                "markers": markers,
                "records": {
                    "source_render_count": source_count,
                    "decision_render_count": decision_count,
                    "canonical_event_count": len(events),
                },
                "correlation": {
                    "source_to_decision": source_to_decision,
                    "decision_to_source": decision_to_source,
                    "parent_reference_resolved": len(events) == 2
                    and events[1].get("parent_event_id") == SOURCE_ID,
                    "evidence_reference_resolved": len(events) == 2
                    and SOURCE_ID in events[1].get("evidence_refs", []),
                },
            }
        )
    except (PlaywrightTimeoutError, Exception) as error:
        payload["error"] = repr(error)

    write_report(payload)
    print("CONECTRR_REMOTE_BROWSER_CHECK=PASS" if payload["passed"] else "CONECTRR_REMOTE_BROWSER_CHECK=FAIL")
    print(f"url={URL}")
    print("authority_effect=none")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
