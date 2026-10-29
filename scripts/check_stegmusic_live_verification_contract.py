#!/usr/bin/env python3
"""Statically validate the StegMusic post-deployment verification contract."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ecosystem-music.html"
CHECKER = ROOT / "scripts" / "check_stegmusic_live_routes.py"
WORKFLOW = ROOT / ".github" / "workflows" / "stegmusic-live-verification.yml"

REQUIRED_PAGE_MARKERS = (
    'id="playPause"',
    'id="adaptiveNext"',
    'id="localAudioFile"',
    'assets/ecosystem-music.js',
    'assets/ecosystem-music-adaptive.js',
    'assets/ecosystem-music-local-source.js',
)
REQUIRED_CHECKER_MARKERS = (
    'stegmusic_live_verification',
    'browser_audio_execution_verified',
    'catalog_license_verified',
    'authority_effect',
    'ecosystem-music.html',
    'ecosystem-chat.html',
)
REQUIRED_WORKFLOW_MARKERS = (
    'name: StegMusic Live Verification',
    'pages-build-deployment',
    "github.event.workflow_run.head_branch == 'main'",
    'python scripts/check_stegmusic_live_routes.py',
    'Upload StegMusic live verification receipt',
    'reports/stegmusic-live-verification.json',
)


def check(path: Path, markers: tuple[str, ...]) -> list[str]:
    if not path.exists():
        return [f"missing file: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    return [f"{path.relative_to(ROOT)} missing marker: {marker}" for marker in markers if marker not in text]


def live_routes() -> dict[str, tuple[str, ...]]:
    spec = importlib.util.spec_from_file_location("check_stegmusic_live_routes", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ROUTES


def check_source_parity(routes: dict[str, tuple[str, ...]]) -> list[str]:
    """Every marker the post-deployment check requires must exist in source.

    Pages publishes this tree, so a marker absent from source can never be
    observed on the deployment; the live check would fail closed on every
    run. Catch that drift here, before merge.
    """
    failures = []
    for route, markers in routes.items():
        failures.extend(
            f"source parity: {failure}" for failure in check(ROOT / route, markers)
        )
    return failures


def main() -> int:
    failures = []
    failures.extend(check_source_parity(live_routes()))
    failures.extend(check(PAGE, REQUIRED_PAGE_MARKERS))
    failures.extend(check(CHECKER, REQUIRED_CHECKER_MARKERS))
    failures.extend(check(WORKFLOW, REQUIRED_WORKFLOW_MARKERS))
    if failures:
        for failure in failures:
            print(f"STEGMUSIC_LIVE_CONTRACT_FAIL: {failure}")
        return 1
    print("STEGMUSIC_LIVE_CONTRACT_PASS")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
