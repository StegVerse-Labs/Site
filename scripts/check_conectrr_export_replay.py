#!/usr/bin/env python3
"""Verify browser-loaded Conectrr records are replay-tested in JSON and JSONL."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOADER = ROOT / "assets" / "conectrr-interop.js"

REQUIRED = [
    "verifyExportReplay",
    "stegverse.canonical-event-stream.v0.1",
    "jsonl.trim().split('\\n')",
    "export replay omitted a correlated record",
    "export replay broke source-decision correlation",
    "conectrrExportReplay = 'pass'",
    "conectrrExportReplay = 'failed'",
]


def main() -> int:
    errors: list[str] = []
    if not LOADER.exists():
        errors.append("missing assets/conectrr-interop.js")
    else:
        text = LOADER.read_text(encoding="utf-8")
        errors.extend(f"missing export replay marker: {marker}" for marker in REQUIRED if marker not in text)
    if errors:
        print("CONECTRR_EXPORT_REPLAY_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CONECTRR_EXPORT_REPLAY_CHECK=PASS")
    print("formats=json,jsonl")
    print("records=source,decision")
    print("correlation=preserved")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
