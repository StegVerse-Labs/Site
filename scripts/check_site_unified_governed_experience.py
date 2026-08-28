#!/usr/bin/env python3
"""Validate the current Site unified governed experience contract."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
STATUS = ROOT / "docs" / "SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md"

REQUIRED_INDEX = [
    "How can I help?",
    "How do I use this chat?",
    "What is StegVerse?",
    "What is My KV?",
    'href="my-kv.html"',
    'href="organizational-kv.html"',
    'id="chatForm"',
    'id="messageInput"',
    'id="chatLog"',
    'id="node-llm-status"',
    "assets/stegverse-node-continuity.js",
    "assets/semantic-command-router.js",
    "assets/ecosystem-chat-semantic-commands.js",
    "assets/ecosystem-chat-va-runtime.js",
    "assets/ecosystem-chat-simple.js",
]

FORBIDDEN_RETIRED_HOMEPAGE = [
    "Start with Ecosystem Chat.",
    "Everything else is a governed transition.",
    "Open Ecosystem Chat",
    'href="#transition-menu"',
    'id="transition-menu"',
    "Continue to a governed transition",
    "Explain admissibility",
    "Demonstrate governance",
    "Evaluate a runtime",
    "View governed ecosystem model",
    "Inspect transition table",
    "Use math-solver adapter",
    "Read the research",
    "Current proof status",
    "transition-grid",
]

REQUIRED_STATUS = [
    "Goal: unified-governed-experience",
    "Primary public operating surface: index.html conversational shell",
    "Homepage posture: conversation first; My KV and Organizational KV are the only primary navigation destinations",
    "Shared capability contract: data/unified-conversational-capabilities.json",
    "Capability handoff: docs/UNIFIED_CONVERSATIONAL_CAPABILITY_MIRROR_HANDOFF.md",
    "technical competency assumption: none",
    "ordinary-language conversation: primary",
    "internal architecture: hidden by default",
    "false authority: prohibited",
    "Execution authority from Site: none",
    "Receipt authority from Site: none",
]


def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    index = read(INDEX)
    status = read(STATUS)

    missing = [marker for marker in REQUIRED_INDEX if marker not in index]
    if missing:
        raise AssertionError("index.html missing current unified-experience marker(s): " + ", ".join(missing))

    retired = [marker for marker in FORBIDDEN_RETIRED_HOMEPAGE if marker in index]
    if retired:
        raise AssertionError("index.html restored retired transition-directory UI: " + ", ".join(retired))

    missing_status = [marker for marker in REQUIRED_STATUS if marker not in status]
    if missing_status:
        raise AssertionError("SITE_UNIFIED_GOVERNED_EXPERIENCE_STATUS.md missing current contract text: " + ", ".join(missing_status))

    if index.count('data-chat-prompt=') != 3:
        raise AssertionError("homepage must expose exactly three starter prompts")
    if index.count('href="my-kv.html"') != 1:
        raise AssertionError("homepage must expose exactly one My KV primary navigation link")
    if index.count('href="organizational-kv.html"') != 1:
        raise AssertionError("homepage must expose exactly one Organizational KV primary navigation link")
    if 'type="password"' in index or 'name="password"' in index:
        raise AssertionError("homepage must not expose credential input")

    print("SITE UNIFIED GOVERNED EXPERIENCE: PASS")
    print("SITE_PRIMARY_PUBLIC_SURFACE=index.html")
    print("SITE_CONVERSATIONAL_RUNTIME=canonical_existing_ecosystem_chat_assets")
    print("SITE_PRIMARY_NAVIGATION=my-kv.html,organizational-kv.html")
    print("SITE_STARTER_PROMPTS=3")
    print("SITE_INTERNAL_ARCHITECTURE=HIDDEN_BY_DEFAULT")
    print("SITE_EXECUTION_AUTHORITY=NONE")
    print("SITE_RECEIPT_AUTHORITY=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
