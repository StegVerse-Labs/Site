#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "song": ROOT / "data" / "stegmusic" / "song-reference.schema.v1.json",
    "corpus": ROOT / "data" / "stegmusic" / "corpus-reference.schema.v1.json",
    "frozen": ROOT / "data" / "stegmusic" / "frozen-composition-evidence.schema.v1.json",
}

required_markers = {
    "song": [
        "song_reference_id",
        "source_records",
        "historical_context",
        "audience_and_place",
        "musical_map",
        "performance_map",
        "rights_and_access",
        "SECONDARY_DERIVED",
        "authority",
    ],
    "corpus": [
        "corpus_reference_id",
        "membership",
        "distributions",
        "variant_clusters",
        "outliers",
        "historical_period_models",
        "regional_models",
        "composition_constraints",
        "RARE_VALID",
        "authority",
    ],
    "frozen": [
        "evidence_packet_id",
        "composition_request_id",
        "retrievals",
        "adopted_values",
        "source_gaps",
        "conflicts",
        "FREEZE_AFTER_QUERY",
        "mutable_after_freeze",
        "composition_may_execute",
        "authority",
    ],
}

failures = []
for name, path in FILES.items():
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        continue
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"invalid json {path.relative_to(ROOT)}: {exc}")
        continue
    if payload.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        failures.append(f"{name} schema draft mismatch")
    text = path.read_text(encoding="utf-8")
    for marker in required_markers[name]:
        if marker not in text:
            failures.append(f"{name} missing marker: {marker}")
    authority = payload.get("properties", {}).get("authority", {}).get("const")
    if authority != "none":
        failures.append(f"{name} authority must be none")

if failures:
    print("STEGMUSIC_REFERENCE_SCHEMAS_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGMUSIC_REFERENCE_SCHEMAS_PASS")
print("song=song_level_identity_history_audience_music_performance_rights_provenance")
print("corpus=distributions_clusters_outliers_period_region_constraints")
print("frozen=primary_gaps_secondary_derivation_conflicts_hashes_immutable_freeze")
print("authority=none")
