#!/usr/bin/env python3
"""Check transition-table public display copy for extraction-safe wording.

The public page may be consumed by text extractors that concatenate adjacent
nodes. This checker prevents known misleading concatenations from being shipped
while allowing the visual page to keep badge text and explanatory copy separate.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = REPO_ROOT / "transition-table-visual.html"

DISALLOWED_SOURCE_FRAGMENTS = [
    "structurally rigorous structure",
    "structurally rigorousstructure",
]

DISALLOWED_PUBLIC_TEXT_FRAGMENTS = [
    "structurally rigorous structure",
    "structurally rigorousstructure",
]

REQUIRED_BOUNDARY_FRAGMENTS = [
    "Site is a public mirror, not proof authority.",
    "formalism-tests produces receipts. Site publishes receipts.",
]


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip_depth and data.strip():
            self.parts.append(data.strip())


def fail(message: str) -> int:
    print(f"transition table public copy check failed: {message}")
    return 1


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def visible_text(source: str) -> str:
    parser = VisibleTextParser()
    parser.feed(source)
    return " ".join(parser.parts)


def main() -> int:
    if not PAGE_PATH.exists():
        return fail("missing transition-table-visual.html")

    source = PAGE_PATH.read_text(encoding="utf-8")
    source_norm = normalized(source)
    public_norm = normalized(visible_text(source))

    for fragment in DISALLOWED_SOURCE_FRAGMENTS:
        if fragment in source_norm:
            return fail(f"disallowed source fragment present: {fragment}")

    for fragment in DISALLOWED_PUBLIC_TEXT_FRAGMENTS:
        if fragment in public_norm:
            return fail(f"disallowed public text fragment present: {fragment}")

    for fragment in REQUIRED_BOUNDARY_FRAGMENTS:
        if normalized(fragment) not in public_norm:
            return fail(f"missing boundary fragment: {fragment}")

    print("valid: Transition Table public copy extraction-safe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
