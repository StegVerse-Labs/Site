#!/usr/bin/env python3
"""Verify the deployed StegMusic surface and required browser runtimes.

This is a publication check only. It verifies that the public Site serves the
playable prototype files and expected boundary markers; it does not assert that
a browser successfully rendered audio, that a catalog license exists, or that
any governance/custody activation gate has passed.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "stegmusic-live-verification.json"
BASE_URL = os.environ.get(
    "STEGVERSE_PAGES_BASE_URL",
    "https://stegverse-labs.github.io/Site",
).rstrip("/")

ROUTES: dict[str, tuple[str, ...]] = {
    "ecosystem-music.html": (
        "StegMusic / StegDJ",
        "StegDJ surprise me",
        'id="playPause"',
        'id="adaptiveNext"',
        "assets/ecosystem-music.js",
        "assets/ecosystem-music-adaptive.js",
        "assets/ecosystem-music-local-source.js",
        "assets/ecosystem-music-diagnostics.js",
        "Generated and user-owned local audio",
    ),
    "assets/ecosystem-music.js": (
        "AudioContext",
        "playback_started",
        "preference_refinement",
        "compositionPhase",
    ),
    "assets/ecosystem-music-adaptive.js": (
        "adaptive_selection_decision",
        "transition",
        "stegmusic.trait-model.v1",
    ),
    "assets/ecosystem-music-local-source.js": (
        "URL.createObjectURL",
        "local_source_loaded",
        "local_playback_started",
        "URL.revokeObjectURL",
    ),
    "assets/ecosystem-music-diagnostics.js": (
        "assets/ecosystem-music-media-transport.js",
        "StegMusicMediaTransport",
        "audio_self_test_passed",
        "audible_output_confirmed: false",
    ),
    "assets/ecosystem-music-media-transport.js": (
        "OfflineAudioContext",
        "encodeWav",
        "generated_media_playback_started",
        "navigator.mediaSession",
        "human_audibility_confirmed",
        "screen_lock_continuity_confirmed",
    ),
    "ecosystem-chat.html": (
        "Ecosystem Node",
        "ecosystem-music.html",
    ),
}


def fetch(route: str) -> tuple[int, str, str]:
    url = f"{BASE_URL}/{route}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "StegVerse-Site-Live-Verification/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8", errors="replace")
        return response.status, response.headers.get("content-type", ""), body


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
            results.append(
                {
                    "route": route,
                    "url": url,
                    "status": status,
                    "content_type": content_type,
                    "required_markers": list(markers),
                    "missing_markers": missing,
                    "passed": route_passed,
                }
            )
            if route_passed:
                print(f"STEGMUSIC_LIVE_ROUTE_PASS: {url}")
            else:
                passed = False
                print(f"STEGMUSIC_LIVE_ROUTE_FAIL: {url} missing={missing}")
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            passed = False
            results.append(
                {
                    "route": route,
                    "url": url,
                    "status": None,
                    "content_type": None,
                    "required_markers": list(markers),
                    "missing_markers": list(markers),
                    "passed": False,
                    "error": repr(error),
                }
            )
            print(f"STEGMUSIC_LIVE_ROUTE_FAIL: {url} error={error!r}")

    payload = {
        "schema_version": "1.1.0",
        "status_type": "stegmusic_live_verification",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "base_url": BASE_URL,
        "passed": passed,
        "routes": results,
        "authority_effect": "NONE",
        "claims": {
            "public_files_present": passed,
            "generated_media_transport_published": passed,
            "browser_audio_execution_verified": False,
            "human_audibility_verified": False,
            "iphone_safari_compatibility_verified": False,
            "screen_lock_continuity_verified": False,
            "catalog_license_verified": False,
            "custody_verified_by_this_check": False,
            "activation_authority_granted": False,
        },
    }
    write_report(payload)
    if passed:
        print("STEGMUSIC_LIVE_VERIFICATION_PASS")
        return 0
    print("STEGMUSIC_LIVE_VERIFICATION_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
