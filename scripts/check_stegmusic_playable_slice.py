#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "ecosystem-music.html"
CHAT = ROOT / "ecosystem-chat.html"
JS = ROOT / "assets" / "ecosystem-music.js"
LOCAL = ROOT / "assets" / "ecosystem-music-local-source.js"
HANDOFF = ROOT / "docs" / "STEGMUSIC_MIRROR_HANDOFF.md"

required = {
    HTML: [
        "StegMusic / StegDJ", 'id="musicSearch"', 'id="playPause"', 'id="audioNotice"',
        'id="volume"', 'id="sessionIntent"', 'id="compositionPhase"', 'id="statusAudio"',
        'id="statusComposition"', 'id="localAudioFile"', 'id="ownershipAffirmation"',
        'id="loadLocalAudio"', 'id="localAudioPlayer"', 'assets/ecosystem-music-local-source.js',
        'data-view="conversation"', 'data-view="governed"', 'data-view="split"', 'data-view="raw"',
        'id="capturedInspection"', 'id="derivedInspection"', 'id="projectionInspection"',
        'id="permitStegDJ"', 'id="permitAggregate"', 'id="permitWellness"',
        'id="revokeButton"', 'id="resetButton"', 'id="profileName"',
        "Generated and user-owned local audio",
    ],
    CHAT: ['id="service-launcher"', 'id="stegMusicServiceLauncher"', 'href="ecosystem-music.html"', "Listen and fine-tune"],
    JS: [
        "stegdj-night-drive", "music_selection", "playback_started", "playback_refused",
        "preference_refinement", "projection_permissions_changed", "future_reuse_revoked",
        "profile_saved", "contribution_eligibility", "royalty_state", "cross_user_raw_history",
        "inspectEvent", "permissionSnapshot", "AudioContext", "composition_form",
        "INTRO", "BUILD", "LIFT", "RESOLVE", "localStorage", "exportSession",
        "window.StegMusicRuntime", "stegmusic:emit", "stegmusic:stop-generated",
    ],
    LOCAL: [
        "user_owned_or_purchased_local", "authorization_not_asserted", "uploaded:false",
        "source_audio_upload", "source_audio_retention", "URL.createObjectURL",
        "URL.revokeObjectURL", "local_source_loaded", "local_playback_started",
        "local_playback_completed", "local_playback_refused",
    ],
    HANDOFF: ["Source of truth", "Rights/source classes", "Internal-test viability", "Archive readiness"],
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

html = HTML.read_text(encoding="utf-8") if HTML.exists() else ""
ids = re.findall(r'\bid="([^"]+)"', html)
duplicates = sorted({item for item in ids if ids.count(item) > 1})
if duplicates:
    failures.append(f"ecosystem-music.html duplicate ids: {', '.join(duplicates)}")

if failures:
    print("STEGMUSIC_PLAYABLE_SLICE_FAIL")
    for failure in failures:
        print(f"- {failure}")
    sys.exit(1)

print("STEGMUSIC_PLAYABLE_SLICE_PASS")
print("authority=none")
print("commercial_catalog_license=not_claimed")
print("user_owned_file_upload=false")
print("duplicate_dom_ids=none")
print("prototype_financial_value=non_payable")
print("captured_derived_inspection=present")
print("downstream_permission_controls=present")
print("future_reuse_revocation=present")
print("ecosystem_chat_launcher=present")
print("browser_audio_failure_visibility=present")
print("structured_composition_phases=present")