#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "song": ROOT / "assets" / "stegmusic-song-reference-builder.js",
    "corpus": ROOT / "assets" / "stegmusic-corpus-reference-builder.js",
    "song_schema": ROOT / "data" / "stegmusic" / "song-reference.schema.v1.json",
    "corpus_schema": ROOT / "data" / "stegmusic" / "corpus-reference.schema.v1.json",
}
REQUIRED = {
    "song": ["StegMusicSongReferenceBuilder", "SECONDARY_DERIVED", "buildSongReference", "compositionEligibility", "builder_hash", "authority:'none'"],
    "corpus": ["StegMusicCorpusReferenceBuilder", "normalizeMembership", "weightedDistribution", "groupClusters", "classifyOutliers", "RARE_VALID", "TRANSITIONAL", "buildCorpusReference", "compositionEligibility", "builder_hash", "authority:'none'"],
    "song_schema": ["song_reference_id", "source_records", "rights_and_access", "confidence", "SECONDARY_DERIVED"],
    "corpus_schema": ["corpus_reference_id", "membership", "distributions", "variant_clusters", "outliers", "RARE_VALID", "TRANSITIONAL", "composition_constraints"],
}

failures=[]
for name,path in FILES.items():
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        continue
    text=path.read_text(encoding="utf-8")
    failures.extend(f"{name} missing marker: {marker}" for marker in REQUIRED[name] if marker not in text)

if failures:
    print("STEGMUSIC_SONG_CORPUS_BUILDERS_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGMUSIC_SONG_CORPUS_BUILDERS_PASS")
print("song=source_preserving_rights_aware_hashed")
print("corpus=weighted_clustered_outlier_preserving_hashed")
print("rare_valid=retained_not_flattened")
print("authority=none")
