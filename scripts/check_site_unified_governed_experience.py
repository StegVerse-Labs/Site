#!/usr/bin/env python3
"""Validate the Site unified governed experience surface."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
STATUS = ROOT / "docs" / "SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md"

REQUIRED_INDEX_TEXT = [
    "Start with Ecosystem Chat.",
    "Everything else is a governed transition.",
    "Open Ecosystem Chat",
    "href=\"ecosystem-chat.html\"",
    "View transition menu",
    "href=\"#transition-menu\"",
    "id=\"transition-menu\"",
    "Continue to a governed transition",
    "Explain admissibility",
    "Demonstrate governance",
    "Evaluate a runtime",
    "View governed ecosystem model",
    "Inspect transition table",
    "Use math-solver adapter",
    "Read the research",
    "Ecosystem Chat   =  primary operating surface preview, not proof source",
]

REQUIRED_STATUS_TEXT = [
    "Goal: unified-governed-experience",
    "Status: phase-1-installed",
    "Primary operating surface: ecosystem-chat.html",
    "Primary hero action: Open Ecosystem Chat -> ecosystem-chat.html",
    "Secondary hero action: View transition menu -> #transition-menu",
    "Phase 2: intent engine",
]

FORBIDDEN_HERO_TEXT = [
    "Run governance filter",
    "Run execution demo",
    "Math-solver adapter",
    "Stage 1–31 proof",
    "Transition Table</a>",
    "Admissibility Wiki</a>",
]


def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def hero_region(page: str) -> str:
    start = page.find('<div class="sv-hero">')
    if start < 0:
        raise AssertionError("homepage missing sv-hero")
    end = page.find('</div>\n\n  <div class="single-entry-note">', start)
    if end < 0:
        raise AssertionError("homepage missing single-entry note after hero")
    return page[start:end]


def main() -> int:
    index = read(INDEX)
    status = read(STATUS)

    missing_index = [item for item in REQUIRED_INDEX_TEXT if item not in index]
    if missing_index:
        raise AssertionError("index.html missing unified experience text: " + ", ".join(missing_index))

    missing_status = [item for item in REQUIRED_STATUS_TEXT if item not in status]
    if missing_status:
        raise AssertionError("SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md missing text: " + ", ".join(missing_status))

    hero = hero_region(index)
    if hero.count('sv-btn') != 2:
        raise AssertionError("homepage hero must expose exactly one primary chat action and one secondary transition-menu action")
    forbidden = [item for item in FORBIDDEN_HERO_TEXT if item in hero]
    if forbidden:
        raise AssertionError("homepage hero restored competing entry text: " + ", ".join(forbidden))

    print("SITE UNIFIED GOVERNED EXPERIENCE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
