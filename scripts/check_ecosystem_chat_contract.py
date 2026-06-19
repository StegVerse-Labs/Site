#!/usr/bin/env python3
"""Validate the text-only Ecosystem Chat activation surface.

This checker is intentionally static. It verifies that the public Site page,
browser-side script, gateway contract, and README continue to preserve the
public-mirror boundary and the gateway handoff contract.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "ecosystem-chat.html": [
        "<script src=\"assets/ecosystem-chat.js\"></script>",
        "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md",
        "POST /api/ecosystem-chat",
        "Site is a public mirror and command surface",
        "receipt_id",
    ],
    "assets/ecosystem-chat.js": [
        "const STEGVERSE_GATEWAY_PATH = '/api/ecosystem-chat';",
        "const STEGVERSE_LOCAL_MODE = true;",
        "Gateway request failed; fail-closed to local classification.",
        "receipt=not-issued",
        "repo: 'StegVerse-Labs/Site'",
    ],
    "docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md": [
        "The browser page must not become proof authority",
        "POST /api/ecosystem-chat",
        "receipt_id",
        "Local transcript hashes are not proof receipts.",
        "Only the appropriate governed backend authority may issue a proof receipt.",
    ],
    "README.md": [
        "[`ecosystem-chat.html`](ecosystem-chat.html)",
        "[`assets/ecosystem-chat.js`](assets/ecosystem-chat.js)",
        "[`docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md`](docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md)",
        "Ecosystem Chat     =  text-only command surface, not proof authority",
    ],
}


def main() -> int:
    failures: list[str] = []

    for relative_path, required_fragments in CHECKS.items():
        path = ROOT / relative_path
        if not path.exists():
            failures.append(f"missing file: {relative_path}")
            continue

        content = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in content:
                failures.append(f"{relative_path}: missing required fragment: {fragment}")

    if failures:
        print("Ecosystem Chat contract check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Ecosystem Chat contract check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
