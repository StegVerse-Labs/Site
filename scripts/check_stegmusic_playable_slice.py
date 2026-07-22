#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "ecosystem-music.html"
JS = ROOT / "assets" / "ecosystem-music.js"
HANDOFF = ROOT / "docs" / "STEGMUSIC_MIRROR_HANDOFF.md"

required = {
    HTML: [
        "StegMusic / StegDJ",
        'id="musicSearch"',
        'id="playPause"',
        'id="statusPlayback"',
        'data-view="conversation"',
        'data-view="governed"',
        'data-view="split"',
        'data-view="raw"',
        'id="capturedInspection"',
        'id="derivedInspection"',
        'id="projectionInspection"',
        'id="permitStegDJ"',
        'id="permitAggregate"',
        'id="permitWellness"',
        'id="revokeButton"',
        'id="resetButton"',
        'id="profileName"',
        "Generated audio only",
    ],
    JS: [
        "stegdj-night-drive",
        "music_selection",
        "playback_started",
        "preference_refinement",
        "projection_permission_changed",
        "future_reuse_revoked",
        "listening_profile_saved",
        "contribution_eligibility",
        "royalty_state",
        "cross_user_raw_history",
        "inspectEvent",
        "permissionSnapshot",
        "localStorage",
        "exportSession",
    ],
    HANDOFF: [
        "Source of truth",
        "Rights/source classes",
        "Captured versus derived records",
        "Downstream projections",
        "Internal-test viability",
        "Archive readiness",
    ],
}

failures = []
for path, markers in required.items():
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            failures.append(f"{path.relative_to(ROOT)} missing marker: {marker}")

if failures:
    print("STEGMUSIC_PLAYABLE_SLICE_FAIL")
    for failure in failures:
        print(f"- {failure}")
    sys.exit(1)

print("STEGMUSIC_PLAYABLE_SLICE_PASS")
print("authority=none")
print("commercial_catalog_license=not_claimed")
print("prototype_financial_value=non_payable")
print("captured_derived_inspection=present")
print("downstream_permission_controls=present")
print("future_reuse_revocation=present")