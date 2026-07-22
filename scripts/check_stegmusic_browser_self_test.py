#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ecosystem-music.html"
RUNTIME = ROOT / "assets" / "ecosystem-music-diagnostics.js"


def fail(message: str) -> int:
    print(f"STEGMUSIC_BROWSER_SELF_TEST_FAIL: {message}")
    return 1


def main() -> int:
    for path in (PAGE, RUNTIME):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    runtime = RUNTIME.read_text(encoding="utf-8")

    page_markers = (
        'id="audioSelfTest"',
        'id="audioSelfTestResult"',
        'Run audio self-test',
        'assets/ecosystem-music-diagnostics.js',
        'confirms browser execution, not audibility',
    )
    runtime_markers = (
        "StegMusicDiagnostics",
        "audio_self_test_passed",
        "audio_self_test_failed",
        "composition_progress_advanced",
        "playback_event_observed",
        "audible_output_confirmed: false",
        "browser_runtime_execution_confirmed: true",
        "window.dispatchEvent(new CustomEvent('stegmusic:emit'",
    )

    for marker in page_markers:
        if marker not in page:
            return fail(f"page missing marker: {marker}")
    for marker in runtime_markers:
        if marker not in runtime:
            return fail(f"runtime missing marker: {marker}")

    if page.index("assets/ecosystem-music-diagnostics.js") < page.index("assets/ecosystem-music.js"):
        return fail("diagnostics runtime must load after the base music runtime")
    if "audible_output_confirmed: true" in runtime:
        return fail("self-test must not claim audible output")

    print("STEGMUSIC_BROWSER_SELF_TEST_PASS")
    print("authority_effect=NONE")
    print("audibility_claim=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
