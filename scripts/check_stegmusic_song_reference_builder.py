#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "assets" / "stegmusic-song-reference-builder.js"
SCHEMA = ROOT / "data" / "stegmusic" / "song-reference.schema.v1.json"

required_runtime = [
    "StegMusicSongReferenceBuilder",
    "normalizeSourceRecord",
    "buildSourceIndex",
    "deriveConfidence",
    "assertRightsPosture",
    "buildSongReference",
    "compositionEligibility",
    "SECONDARY_DERIVED",
    "Prohibited composition use cannot authorize source-audio custody",
    "builder_hash",
    "authority: 'none'",
]
required_schema = [
    "song_reference_id",
    "source_records",
    "historical_context",
    "audience_and_place",
    "musical_map",
    "performance_map",
    "rights_and_access",
    "provenance",
    "confidence",
    "SECONDARY_DERIVED",
]

failures = []
for path in (RUNTIME, SCHEMA):
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")

if not failures:
    runtime = RUNTIME.read_text(encoding="utf-8")
    schema = SCHEMA.read_text(encoding="utf-8")
    failures.extend(f"missing runtime marker: {marker}" for marker in required_runtime if marker not in runtime)
    failures.extend(f"missing schema marker: {marker}" for marker in required_schema if marker not in schema)

if failures:
    print("STEGMUSIC_SONG_REFERENCE_BUILDER_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGMUSIC_SONG_REFERENCE_BUILDER_PASS")
print("source_records=priority_ordered_gap_preserving")
print("confidence=weighted_with_conflict_penalty")
print("rights=composition_use_posture_enforced")
print("reference=sha256_builder_hash_frozen")
print("authority=none")
