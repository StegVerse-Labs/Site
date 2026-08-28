#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
ORG = ROOT / "organizational-kv.html"
HANDOFF = ROOT / "docs" / "SITE_HOMEPAGE_CHAT_MIRROR_HANDOFF.md"

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
    'assets/semantic-command-router.js',
    'assets/ecosystem-chat-semantic-commands.js',
    'assets/ecosystem-chat-va-runtime.js',
    'assets/ecosystem-chat-simple.js',
]
FORBIDDEN_INDEX = [
    "transition-grid",
    "Governed transition path",
    "Continue to a governed transition",
    "Current proof status",
    "HeartBeat</a>",
    "StegWallet</a>",
    "Papers</a>",
    "Thought Experiments</a>",
]
REQUIRED_ORG = [
    "Organizational KV",
    "NOT CONNECTED",
    "does not currently claim that an organization KV is installed or connected",
    "grants none of them",
    'href="index.html"',
]

def main() -> int:
    failures = []
    index = INDEX.read_text(encoding="utf-8")
    org = ORG.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")

    for marker in REQUIRED_INDEX:
        if marker not in index:
            failures.append(f"index missing required marker: {marker}")
    for marker in FORBIDDEN_INDEX:
        if marker in index:
            failures.append(f"index retains removed homepage clutter: {marker}")
    for marker in REQUIRED_ORG:
        if marker not in org:
            failures.append(f"organizational-kv missing required marker: {marker}")

    if index.count('data-chat-prompt=') != 3:
        failures.append("homepage must expose exactly three starter prompts")
    if index.count('href="my-kv.html"') != 1:
        failures.append("homepage must expose exactly one My KV navigation link")
    if index.count('href="organizational-kv.html"') != 1:
        failures.append("homepage must expose exactly one Organizational KV navigation link")
    if "Do not modify canonical Ecosystem Chat runtime/provider assets" not in handoff and "does not modify those files" not in handoff:
        failures.append("handoff missing canonical chat-runtime non-ownership boundary")
    if 'type="password"' in index or "STEGVERSE_REPO_SYNC_TOKEN" in index:
        failures.append("homepage contains prohibited credential surface")

    if failures:
        print("SITE_HOMEPAGE_CHAT_FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("SITE_HOMEPAGE_CHAT_PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
