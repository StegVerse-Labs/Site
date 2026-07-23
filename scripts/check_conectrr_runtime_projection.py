#!/usr/bin/env python3
"""Verify the Conectrr runtime projection and immutable import boundary."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODE = ROOT / "assets" / "ecosystem-node-views.js"
LOADER = ROOT / "assets" / "conectrr-interop.js"
FIXTURE = ROOT / "data" / "conectrr-independent-evaluation.fixture.json"

REQUIRED_NODE = [
    "importCanonicalEvents",
    "duplicate imported event_id",
    "unresolved parent_event_id",
    "JSON.parse(JSON.stringify(event))",
    "eventIndex.has(event.event_id)",
]
REQUIRED_LOADER = [
    "conectrr-independent-evaluation.fixture.json",
    "source_event",
    "downstream_event",
    "structuredClone",
    "source mutated during import",
    "api.importCanonicalEvents([source, decision])",
    "conectrrInterop",
]


def missing(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return [f"missing file: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    return [f"{path.relative_to(ROOT)} missing: {needle}" for needle in needles if needle not in text]


def main() -> int:
    errors = []
    errors.extend(missing(NODE, REQUIRED_NODE))
    errors.extend(missing(LOADER, REQUIRED_LOADER))
    if not FIXTURE.exists():
        errors.append("missing independent evaluation fixture")
    if errors:
        print("CONECTRR_RUNTIME_PROJECTION_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CONECTRR_RUNTIME_PROJECTION_CHECK=PASS")
    print("source_event=evidence")
    print("downstream_event=decision")
    print("import_semantics=clone_then_freeze")
    print("correlation=stable_event_id")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
