#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "STEGMUSIC_CULTURAL_PERFORMANCE_MODEL.md"

required = [
    "lyrics-free Appalachian circle performance",
    "musical role != instrument != performer",
    "Universal string-component dependency",
    "uncertain exact failure time",
    "ensemble recovery behavior",
    "instrument_handoff_started",
    "string_failure_occurred",
    "blind_origin_classification_recorded",
    "provenance_disclosed",
    "chance-level origin classification",
    "blind sensory exposure",
    "cultural profile != cultural ownership",
    "Site fixture != production activation",
]

if not DOC.exists():
    print("STEGMUSIC_CULTURAL_PERFORMANCE_MODEL_FAIL")
    print("- missing docs/STEGMUSIC_CULTURAL_PERFORMANCE_MODEL.md")
    raise SystemExit(1)

text = DOC.read_text(encoding="utf-8")
failures = [f"missing marker: {marker}" for marker in required if marker not in text]

if failures:
    print("STEGMUSIC_CULTURAL_PERFORMANCE_MODEL_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGMUSIC_CULTURAL_PERFORMANCE_MODEL_PASS")
print("primary_scope=lyrics_free_instrumental")
print("first_domain=appalachian_circle_performance")
print("string_state=universal_component_standard")
print("failure_timing=stochastic_not_fixed_bar")
print("continuity=recoverable_role_substitution")
print("benchmark=blind_sensory_fidelity_with_post_test_disclosure")
print("authority=none")
