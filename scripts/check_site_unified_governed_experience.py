#!/usr/bin/env python3
"""Validate the Site unified governed experience surface."""

from __future__ import annotations

import re
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

# Validate stable semantic milestones instead of binding CI to one transient phase label.
REQUIRED_STATUS_TEXT = [
    "Goal: unified-governed-experience",
    "Primary operating surface: ecosystem-chat.html",
    "Homepage posture: one primary conversational entry plus contextual governed destinations",
    "Shared capability contract: data/unified-conversational-capabilities.json",
    "Capability handoff: docs/UNIFIED_CONVERSATIONAL_CAPABILITY_MIRROR_HANDOFF.md",
    "technical competency assumption: none",
    "ordinary-language conversation: primary",
    "internal architecture: hidden by default",
    "false authority: prohibited",
    "Execution authority from Site: none",
    "Receipt authority from Site: none",
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
    # The semantic boundary is the next single-entry note, not an exact
    # whitespace/newline serialization. Keep validation robust to formatting
    # changes while still refusing an absent or reordered note.
    match = re.search(r'<div\s+class=["\']single-entry-note["\']', page[start:])
    if match is None:
        raise AssertionError("homepage missing single-entry note after hero")
    end = start + match.start()
    if end <= start:
        raise AssertionError("homepage single-entry note does not follow hero")
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
    hero_anchors = re.findall(
        r'<a\b[^>]*class="([^"]*\bsv-btn\b[^"]*)"[^>]*href="([^"]+)"[^>]*>',
        hero,
    )
    primary = [(classes, href) for classes, href in hero_anchors if "sv-btn-primary" in classes.split()]
    if len(primary) != 1 or primary[0][1] != "ecosystem-chat.html":
        raise AssertionError("homepage hero must expose exactly one primary Ecosystem Chat action")
    secondaries = [href for classes, href in hero_anchors if "sv-btn-secondary" in classes.split()]
    allowed_secondary = {"ecosystem-version.html", "#transition-menu"}
    if set(secondaries) != allowed_secondary or len(secondaries) != len(allowed_secondary):
        raise AssertionError("homepage hero secondary actions must be Version & Status and the transition menu only")
    forbidden = [item for item in FORBIDDEN_HERO_TEXT if item in hero]
    if forbidden:
        raise AssertionError("homepage hero restored competing entry text: " + ", ".join(forbidden))

    print("SITE UNIFIED GOVERNED EXPERIENCE: PASS")
    print("SITE_PRIMARY_CONVERSATIONAL_ENTRY=ecosystem-chat.html")
    print("SITE_HERO_CONTEXTUAL_DESTINATIONS=ecosystem-version.html,#transition-menu")
    print("SITE_EXECUTION_AUTHORITY=NONE")
    print("SITE_RECEIPT_AUTHORITY=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
