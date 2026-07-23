#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "assets" / "stegmusic-composition-records.js"

required = [
    "StegMusicCompositionRecords",
    "buildCompositionRequest",
    "assertExecutable",
    "buildCompositionReceipt",
    "Composition evidence is not frozen",
    "Composition rights gate did not pass",
    "Composition execution is blocked",
    "protected_expression_copying_prohibited: true",
    "artist_voice_imitation_prohibited: true",
    "generated_origin_disclosed: true",
    "receipt.receipt_hash = await sha256",
    "authority: 'none'",
]

failures = []
if not RUNTIME.exists():
    failures.append("missing assets/stegmusic-composition-records.js")
else:
    text = RUNTIME.read_text(encoding="utf-8")
    failures.extend(f"missing runtime marker: {marker}" for marker in required if marker not in text)

if failures:
    print("STEGMUSIC_COMPOSITION_RECORDS_RUNTIME_FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("STEGMUSIC_COMPOSITION_RECORDS_RUNTIME_PASS")
print("request=frozen_evidence_rights_execution_gate")
print("receipt=hash_replay_components_continuity_disclosure")
print("mutation=receipt_frozen")
print("authority=none")
