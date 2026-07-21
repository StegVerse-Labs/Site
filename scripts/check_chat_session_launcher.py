#!/usr/bin/env python3
"""Validate the browser-local ChatGPT session launcher contract."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "chat-session-launcher.html"
DOC = ROOT / "docs" / "CHATGPT_SESSION_LAUNCHER.md"

REQUIRED_PAGE_SNIPPETS = (
    "stegverse.chatgpt.session-launcher.v1",
    "window.localStorage",
    "parsed.protocol !== 'https:'",
    "parsed.hostname !== 'chatgpt.com'",
    "parsed.hostname !== 'www.chatgpt.com'",
    "!/^\\/c\\/[A-Za-z0-9_-]+\\/?$/.test(parsed.pathname)",
    "parsed.search = ''",
    "parsed.hash = ''",
    "window.open(current.url, '_blank', 'noopener,noreferrer')",
    "No prompt was injected or submitted.",
    "/c/[private-session-id]",
)

FORBIDDEN_PAGE_SNIPPETS = (
    "fetch(current.url",
    "fetch(configuration.url",
    "XMLHttpRequest",
    "navigator.sendBeacon",
    "document.cookie",
    "Authorization:",
    "Bearer ",
    "api.openai.com",
    "chatgpt.com/backend-api",
)

REQUIRED_DOC_SNIPPETS = (
    "browser localStorage only",
    "prompt injection = false",
    "Site execution authority = false",
    "Master-Records custody = none",
    "does not replace the governed Ecosystem Chat gateway",
)


def fail(message: str) -> int:
    print(f"CHAT_SESSION_LAUNCHER_FAIL: {message}")
    return 1


def main() -> int:
    if not PAGE.is_file():
        return fail(f"missing {PAGE.relative_to(ROOT)}")
    if not DOC.is_file():
        return fail(f"missing {DOC.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")

    for snippet in REQUIRED_PAGE_SNIPPETS:
        if snippet not in page:
            return fail(f"launcher page missing required invariant: {snippet}")

    for snippet in FORBIDDEN_PAGE_SNIPPETS:
        if snippet in page:
            return fail(f"launcher page contains forbidden network or credential behavior: {snippet}")

    for snippet in REQUIRED_DOC_SNIPPETS:
        if snippet not in doc:
            return fail(f"launcher contract missing required boundary: {snippet}")

    if "https://chatgpt.com/c/YOUR-" in page or "https://chatgpt.com/c/000" in page:
        return fail("launcher page appears to contain a committed conversation identifier")

    print("CHAT_SESSION_LAUNCHER_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
