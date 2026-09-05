#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs/GAUI_STEGVERSE_ANALYSIS_MIRROR_HANDOFF.md"
ANALYSIS = ROOT / "research/gaui-stegverse-analysis.md"

REQUIRED_HANDOFF = [
    "StegVerse-Labs/Site#1005",
    "identity continuity != authority continuity != transition admissibility",
    "Authority is represented state/evidence supplied to an admissibility evaluation",
    "This is a research hypothesis, not an implemented integration contract.",
    "GAUI_STEGVERSE_ANALYSIS=PASS",
]

REQUIRED_ANALYSIS = [
    "Persistent Identity Is Not Persistent Permission",
    "https://zenodo.org/records/22301698",
    "identity continuity != authority continuity != transition admissibility",
    "A_t does not imply Adm(T_t)",
    "Authority-as-condition vs authority-as-permission test",
    "It does not establish:",
    "partnership;",
    "runtime integration;",
    "ownership of the governed-execution boundary.",
    "That question must be answered before claiming that StegVerse and BIGMAE meet at the same governed-execution boundary.",
]

PROHIBITED_ANALYSIS = [
    "GAUI and StegVerse are integrated",
    "GAUI is integrated with StegVerse",
    "BIGMAE owns the governed-execution boundary",
    "StegVerse owns the governed-execution boundary",
    "GAUI endorses StegVerse",
    "BIGMAE endorses StegVerse",
]


def require(path: Path, needles: list[str]) -> list[str]:
    failures: list[str] = []
    if not path.is_file():
        return [f"missing file: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            failures.append(f"missing required marker in {path.relative_to(ROOT)}: {needle}")
    return failures


def main() -> int:
    failures = []
    failures.extend(require(HANDOFF, REQUIRED_HANDOFF))
    failures.extend(require(ANALYSIS, REQUIRED_ANALYSIS))

    if ANALYSIS.is_file():
        text = ANALYSIS.read_text(encoding="utf-8")
        for phrase in PROHIBITED_ANALYSIS:
            if phrase in text:
                failures.append(f"unsupported integration/boundary claim: {phrase}")

    if failures:
        print("GAUI_STEGVERSE_ANALYSIS=FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("GAUI_STEGVERSE_ANALYSIS=PASS")
    print("authority_effect=false")
    print("activation_effect=false")
    print("publication_effect=false")
    print("integration_claim=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
