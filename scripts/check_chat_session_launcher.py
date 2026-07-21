#!/usr/bin/env python3
"""Validate the browser-local ChatGPT session launcher contract."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "chat-session-launcher.html"
DOC = ROOT / "docs" / "CHATGPT_SESSION_LAUNCHER.md"
NAVIGATION = ROOT / "assets" / "ecosystem-chat-hps.js"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

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


def contains_any(text: str, alternatives: tuple[str, ...]) -> bool:
    return any(value in text for value in alternatives)


def main() -> int:
    for path in (PAGE, DOC, NAVIGATION, HANDOFF):
        if not path.is_file():
            return fail(f"missing {path.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")
    navigation = NAVIGATION.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")

    for snippet in REQUIRED_PAGE_SNIPPETS:
        if snippet not in page:
            return fail(f"launcher page missing required invariant: {snippet}")

    for snippet in FORBIDDEN_PAGE_SNIPPETS:
        if snippet in page:
            return fail(f"launcher page contains forbidden network or credential behavior: {snippet}")

    for snippet in REQUIRED_DOC_SNIPPETS:
        if snippet not in doc:
            return fail(f"launcher contract missing required boundary: {snippet}")

    if "['chat-session-launcher.html', 'Session Launcher']" not in navigation:
        return fail("Ecosystem Chat primary navigation does not expose the launcher")

    handoff_requirements = (
        ("browser-local continuation heading", ("## Browser-local ChatGPT session continuation",)),
        (
            "prompt injection or submission is false",
            ("prompt injection or submission = false", "does not inject prompts"),
        ),
        (
            "activation evidence is absent",
            ("activation evidence = none", "produce activation evidence"),
        ),
    )
    for label, alternatives in handoff_requirements:
        if not contains_any(handoff, alternatives):
            return fail(f"Site handoff missing launcher continuation boundary: {label}")

    if "https://chatgpt.com/c/YOUR-" in page or "https://chatgpt.com/c/000" in page:
        return fail("launcher page appears to contain a committed conversation identifier")

    print("CHAT_SESSION_LAUNCHER_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
