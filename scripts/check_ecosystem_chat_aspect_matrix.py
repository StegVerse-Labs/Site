#!/usr/bin/env python3
"""Static validation for the Ecosystem Chat governed aspect matrix."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HPS = ROOT / "assets" / "ecosystem-chat-hps.js"
MATRIX = ROOT / "assets" / "ecosystem-chat-aspect-matrix.js"
REGISTRY = ROOT / "data" / "ecosystem-chat-governed-aspects.registry.json"
EVENTS = ROOT / "data" / "ecosystem-chat-governed-aspect-events.fixture.json"

REQUIRED_MATRIX = [
    "ecosystemAspectMatrix",
    'data-aspect-view="human"',
    'data-aspect-view="governed"',
    'data-aspect-view="split"',
    "ecosystemAspectRole",
    "public",
    "contributor",
    "reviewer",
    "custodian",
    "data-event-id",
    "data-claim-id",
    "data-artifact-id",
    "data-execution-id",
    "UNRESOLVED",
    "Raw JSONL",
    "Export aspects",
    "StegVerseAspectMatrix",
    "authority_effect: 'NONE'",
    "No aspect silently grants ownership, consent, authority, admissibility, value, payment, custody, publication, or settlement",
]


def main() -> int:
    errors: list[str] = []
    for path in [HPS, MATRIX, REGISTRY, EVENTS]:
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")

    if HPS.exists() and "assets/ecosystem-chat-aspect-matrix.js" not in HPS.read_text(encoding="utf-8"):
        errors.append("assets/ecosystem-chat-hps.js does not load aspect matrix")

    if MATRIX.exists():
        text = MATRIX.read_text(encoding="utf-8")
        for marker in REQUIRED_MATRIX:
            if marker not in text:
                errors.append(f"assets/ecosystem-chat-aspect-matrix.js missing: {marker}")

    if errors:
        print("ECOSYSTEM_CHAT_ASPECT_MATRIX_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("ECOSYSTEM_CHAT_ASPECT_MATRIX_CHECK=PASS")
    print("views=human,governed,split")
    print("roles=public,contributor,reviewer,custodian")
    print("correlation=event_id,claim_id,artifact_id,execution_id")
    print("missing_evidence=UNRESOLVED")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
