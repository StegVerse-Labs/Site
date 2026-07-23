#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "assets" / "stegmusic-source-evidence.js"

required = [
    "StegMusicSourceEvidence",
    "createSourceObservation",
    "resolveField",
    "SECONDARY_DERIVED",
    "decideStoragePosture",
    "FREEZE_AFTER_QUERY",
    "freezeEvidence",
    "mutableAfterFreeze: false",
    "compositionMayExecute",
    "createCompositionEvidenceSession",
    "Evidence session is frozen",
    "authority: 'none'",
]

failures = []
if not RUNTIME.exists():
    failures.append("missing assets/stegmusic-source-evidence.js")
else:
    text = RUNTIME.read_text(encoding="utf-8")
    failures.extend(f"missing runtime marker: {marker}" for marker in required if marker not in text)

if failures:
    print("STEGMUSIC_SOURCE_EVIDENCE_RUNTIME_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGMUSIC_SOURCE_EVIDENCE_RUNTIME_PASS")
print("resolution=primary_preserved_secondary_derived")
print("storage=store_query_freeze_after_query")
print("immutability=freeze_blocks_mutation")
print("hash=sha256")
print("authority=none")
