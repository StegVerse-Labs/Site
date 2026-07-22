#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "stegmusic-browser-execution.json"
BASE_URL = os.environ.get("STEGMUSIC_TEST_BASE_URL", "http://127.0.0.1:8000")


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "schema_version": "1.0.0",
        "status_type": "stegmusic_browser_execution",
        "page": f"{BASE_URL}/ecosystem-music.html",
        "passed": False,
        "browser_audio_execution_verified": False,
        "audible_output_confirmed": False,
        "catalog_license_verified": False,
        "custody_verified_by_this_check": False,
        "activation_authority_granted": False,
        "checks": {},
    }

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                args=["--autoplay-policy=no-user-gesture-required"],
            )
            page = browser.new_page()
            page.goto(result["page"], wait_until="networkidle")

            page.locator("#resetButton").click()
            page.locator("#playPause").click()
            page.wait_for_function(
                "document.querySelector('#audioNotice').textContent.includes('running locally')",
                timeout=10_000,
            )
            page.wait_for_function(
                "Number(document.querySelector('#progress').value) > 0",
                timeout=10_000,
            )

            raw_before = page.locator("#rawEvents").text_content() or ""
            page.locator("#adaptiveNext").click()
            page.wait_for_function(
                "document.querySelector('#rawEvents').textContent.includes('adaptive_selection_decision')",
                timeout=10_000,
            )
            page.locator("#playPause").click()
            page.wait_for_function(
                "document.querySelector('#audioNotice').textContent.includes('paused')",
                timeout=10_000,
            )

            raw_after = page.locator("#rawEvents").text_content() or ""
            checks = {
                "page_loaded": page.locator("#playPause").count() == 1,
                "audio_context_running_marker": "running locally" in (page.locator("#audioNotice").text_content() or "" ) or "paused" in (page.locator("#audioNotice").text_content() or ""),
                "composition_advanced": float(page.locator("#progress").input_value()) > 0,
                "playback_started_event": "playback_started" in raw_before or "playback_started" in raw_after,
                "adaptive_decision_event": "adaptive_selection_decision" in raw_after,
                "playback_paused_event": "playback_paused" in raw_after,
                "diagnostic_runtime_loaded": page.evaluate("typeof window.StegMusicRuntime === 'object'"),
            }
            result["checks"] = checks
            result["passed"] = all(checks.values())
            result["browser_audio_execution_verified"] = result["passed"]
            result["event_stream_excerpt"] = raw_after[-4000:]
            browser.close()
    except Exception as error:
        result["error"] = str(error)

    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
