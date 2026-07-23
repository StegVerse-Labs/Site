#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "docs" / "STEGMUSIC_SOURCE_STUDY_PRIORITY.md"
ALGORITHM = ROOT / "docs" / "STEGMUSIC_COMPOSITION_EVIDENCE_ALGORITHM.md"
REGISTRY = ROOT / "data" / "stegmusic" / "source-study-priority.v1.json"

required_study = [
    "Global Jukebox",
    "Dunya / CompMusic",
    "MusicBrainz",
    "AcousticBrainz",
    "Library of Congress National Jukebox",
    "DOREMUS",
    "RISM",
    "Million Song Dataset",
    "SECONDARY_DERIVED",
    "freeze the result if it influences composition",
]
required_algorithm = [
    "AVAILABLE",
    "ABSENT",
    "UNKNOWN",
    "RESTRICTED",
    "CONFLICTED",
    "Evidence freezing",
    "Song-level mathematical mapping",
    "Corpus derivation",
    "Store versus query decision",
    "FREEZE_AFTER_QUERY",
    "Composition receipt",
    "Site fixture != production activation",
]

failures = []
for path in (STUDY, ALGORITHM, REGISTRY):
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")

if not failures:
    study = STUDY.read_text(encoding="utf-8")
    algorithm = ALGORITHM.read_text(encoding="utf-8")
    failures.extend(f"missing study marker: {marker}" for marker in required_study if marker not in study)
    failures.extend(f"missing algorithm marker: {marker}" for marker in required_algorithm if marker not in algorithm)

    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    sources = payload.get("sources", [])
    priorities = [source.get("priority") for source in sources]
    names = [source.get("name") for source in sources]
    if priorities != list(range(1, 9)):
        failures.append(f"source priorities must be ordered 1..8, got {priorities}")
    if len(set(names)) != 8:
        failures.append("source registry must contain eight unique sources")
    if payload.get("authority") != "none":
        failures.append("registry authority must be none")
    if set(payload.get("availability_states", [])) != {"AVAILABLE", "ABSENT", "UNKNOWN", "RESTRICTED", "CONFLICTED"}:
        failures.append("availability state set is incomplete")
    if set(payload.get("storage_postures", [])) != {"STORE", "QUERY", "FREEZE_AFTER_QUERY"}:
        failures.append("storage posture set is incomplete")
    for source in sources:
        if not source.get("distinct_gaps"):
            failures.append(f"source missing distinct gaps: {source.get('name')}")
        if not source.get("secondary_sources"):
            failures.append(f"source missing secondary sources: {source.get('name')}")

if failures:
    print("STEGMUSIC_SOURCE_STUDY_ALGORITHM_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGMUSIC_SOURCE_STUDY_ALGORITHM_PASS")
print("sources=8_ordered")
print("gap_resolution=primary_preserved_secondary_derived")
print("storage=store_query_freeze_after_query")
print("composition=external_evidence_frozen_before_influence")
print("authority=none")
