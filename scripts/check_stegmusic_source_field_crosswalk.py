#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "STEGMUSIC_SOURCE_FIELD_CROSSWALK.md"
DATA = ROOT / "data" / "stegmusic" / "source-field-crosswalk.v1.json"

EXPECTED_SOURCES = {
    "Global Jukebox",
    "Dunya / CompMusic",
    "MusicBrainz",
    "AcousticBrainz",
    "Library of Congress National Jukebox",
    "DOREMUS",
    "RISM",
    "Million Song Dataset",
}
EXPECTED_FIELDS = {
    "work_identity",
    "recording_identity",
    "release_or_source_identity",
    "performer_identity",
    "instrument_identity",
    "place",
    "date_or_period",
    "audience",
    "social_function",
    "musical_structure",
    "pitch_and_tuning",
    "rhythm_and_microtiming",
    "timbre_and_acoustics",
    "ensemble_and_role_grammar",
    "historical_lineage",
    "physical_component_state",
    "rights_and_access",
}
DOC_MARKERS = [
    "Global Jukebox",
    "Dunya / CompMusic",
    "MusicBrainz",
    "AcousticBrainz",
    "Library of Congress National Jukebox",
    "DOREMUS",
    "RISM",
    "Million Song Dataset",
    "SECONDARY_DERIVED",
    "field-name similarity != semantic equivalence",
    "Site fixture != production activation",
]

failures = []
for path in (DOC, DATA):
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")

if not failures:
    doc = DOC.read_text(encoding="utf-8")
    failures.extend(f"missing doc marker: {marker}" for marker in DOC_MARKERS if marker not in doc)

    payload = json.loads(DATA.read_text(encoding="utf-8"))
    if payload.get("authority") != "none":
        failures.append("crosswalk authority must be none")
    fields = set(payload.get("canonical_fields", []))
    if fields != EXPECTED_FIELDS:
        failures.append(f"canonical fields mismatch: missing={sorted(EXPECTED_FIELDS-fields)} extra={sorted(fields-EXPECTED_FIELDS)}")
    sources = payload.get("sources", {})
    if set(sources) != EXPECTED_SOURCES:
        failures.append("source set must contain the eight prioritized compendiums")
    priorities = sorted(entry.get("priority") for entry in sources.values())
    if priorities != list(range(1, 9)):
        failures.append(f"source priorities must be 1..8, got {priorities}")
    for name, entry in sources.items():
        covered = set(entry.get("direct", [])) | set(entry.get("partial", []))
        gaps = set(entry.get("absent_or_insufficient", []))
        if not covered:
            failures.append(f"{name} has no direct or partial mappings")
        if not gaps:
            failures.append(f"{name} has no preserved gaps")
        if not entry.get("secondary_by_field"):
            failures.append(f"{name} has no secondary field substitutions")
        unknown = (covered | gaps) - EXPECTED_FIELDS
        if unknown:
            failures.append(f"{name} has unknown canonical fields: {sorted(unknown)}")
    rules = " ".join(payload.get("normalization_rule", []))
    for marker in ("SECONDARY_DERIVED", "freeze every composition-affecting adopted value"):
        if marker not in rules:
            failures.append(f"normalization rule missing: {marker}")

if failures:
    print("STEGMUSIC_SOURCE_FIELD_CROSSWALK_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGMUSIC_SOURCE_FIELD_CROSSWALK_PASS")
print("sources=8")
print("canonical_fields=17")
print("gap_posture=preserved")
print("secondary_values=SECONDARY_DERIVED")
print("authority=none")
