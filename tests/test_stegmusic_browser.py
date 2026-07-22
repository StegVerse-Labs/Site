#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "stegmusic-browser-execution.json"
BASE_URL = os.environ.get("STEGMUSIC_TEST_BASE_URL", "http://127.0.0.1:8000")


def event_types(page) -> list[str]:
    raw = page.locator("#rawEvents").text_content() or ""
    types: list[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        event_type = payload.get("event_type")
        if isinstance(event_type, str):
            types.append(event_type)
    return types


def snapshot(page, stage: str) -> dict:
    raw = page.locator("#rawEvents").text_content() or ""
    return {
        "stage": stage,
        "audio_notice": page.locator("#audioNotice").text_content() or "",
        "play_button": page.locator("#playPause").text_content() or "",
        "progress": float(page.locator("#progress").input_value()),
        "composition_phase": page.locator("#compositionPhase").text_content() or "",
        "event_types": event_types(page),
        "raw_events_excerpt": raw[-4000:],
        "runtime_loaded": page.evaluate("typeof window.StegMusicRuntime === 'object'"),
        "diagnostics_loaded": page.evaluate("typeof window.StegMusicDiagnostics === 'object'"),
    }


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
        "stages": [],
        "console": [],
        "page_errors": [],
    }

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                args=[
                    "--autoplay-policy=no-user-gesture-required",
                    "--use-fake-ui-for-media-stream",
                ],
            )
            page = browser.new_page()
            page.on("console", lambda message: result["console"].append({"type": message.type, "text": message.text}))
            page.on("pageerror", lambda error: result["page_errors"].append(str(error)))
            page.goto(result["page"], wait_until="networkidle")
            result["stages"].append(snapshot(page, "loaded"))

            page.locator("#resetButton").click()
            page.locator("#playPause").click()
            page.wait_for_timeout(3500)
            playing = snapshot(page, "after_play")
            result["stages"].append(playing)

            page.locator("#adaptiveNext").click()
            page.wait_for_timeout(2500)
            adaptive = snapshot(page, "after_adaptive_next")
            result["stages"].append(adaptive)

            if page.locator("#playPause").text_content().strip().lower() == "pause":
                page.locator("#playPause").click()
                page.wait_for_timeout(500)
            paused = snapshot(page, "after_pause")
            result["stages"].append(paused)

            observed_types = set(paused["event_types"])
            checks = {
                "page_loaded": page.locator("#playPause").count() == 1,
                "base_runtime_loaded": playing["runtime_loaded"],
                "diagnostic_runtime_loaded": playing["diagnostics_loaded"],
                "audio_context_running_marker": "running locally" in playing["audio_notice"].lower(),
                "composition_advanced": playing["progress"] > 0,
                "playback_started_event": "playback_started" in observed_types,
                "adaptive_decision_event": "adaptive_selection_decision" in observed_types,
                "playback_paused_event": "playback_paused" in observed_types,
                "pause_returned_control": paused["play_button"].strip().lower() == "play",
                "no_page_errors": not result["page_errors"],
            }
            result["checks"] = checks
            result["observed_event_types"] = sorted(observed_types)
            result["passed"] = all(checks.values())
            result["browser_audio_execution_verified"] = result["passed"]
            browser.close()
    except Exception as error:
        result["error"] = str(error)

    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
