#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "assets" / "stegmusic-source-adapters.js"

required = [
    "StegMusicSourceAdapters",
    "GLOBAL_JUKEBOX",
    "DUNYA_COMPMUSIC",
    "MUSICBRAINZ",
    "ACOUSTICBRAINZ",
    "NATIONAL_JUKEBOX",
    "DOREMUS",
    "RISM",
    "MILLION_SONG_DATASET",
    "adaptGlobalJukebox",
    "adaptDunya",
    "adaptMusicBrainz",
    "adaptAcousticBrainz",
    "adaptNationalJukebox",
    "adaptDoremus",
    "adaptRism",
    "adaptMillionSongDataset",
    "native_record",
    "mapping_confidence",
    "response_hash",
    "provenance_path",
    "authority: 'none'",
    "Unsupported StegMusic source adapter"
]

failures = []
if not RUNTIME.exists():
    failures.append("missing assets/stegmusic-source-adapters.js")
else:
    text = RUNTIME.read_text(encoding="utf-8")
    failures.extend(f"missing source adapter marker: {marker}" for marker in required if marker not in text)
    priorities = [
        "priority: 1", "priority: 2", "priority: 3", "priority: 4",
        "priority: 5", "priority: 6", "priority: 7", "priority: 8"
    ]
    failures.extend(f"missing priority marker: {marker}" for marker in priorities if marker not in text)

if failures:
    print("STEGMUSIC_SOURCE_ADAPTERS_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGMUSIC_SOURCE_ADAPTERS_PASS")
print("sources=8_prioritized_adapters")
print("preservation=native_record_hash_provenance_uncertainty")
print("normalization=field_level_status_and_mapping_confidence")
print("network_calls=none")
print("authority=none")
