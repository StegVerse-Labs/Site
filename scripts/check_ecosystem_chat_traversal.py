#!/usr/bin/env python3
"""Validate the bounded Ecosystem Chat traversal/user-first projection contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ecosystem-chat.html"
LOADER = ROOT / "assets" / "ecosystem-chat-hps.js"
SCRIPT = ROOT / "assets" / "ecosystem-chat-traversal.js"
UX = ROOT / "docs" / "ECOSYSTEM_CHAT_UX_STATUS.md"


def require(path: Path, phrases: list[str]) -> str:
    if not path.exists():
        raise SystemExit(f"missing {path.relative_to(ROOT)}")
    body = path.read_text(encoding="utf-8")
    missing = [phrase for phrase in phrases if phrase not in body]
    if missing:
        raise SystemExit(f"{path.relative_to(ROOT)} missing: {', '.join(missing)}")
    return body


def main() -> int:
    page = require(PAGE, [
        '<h1>How can I help?</h1>',
        'Ask in your own words.',
        'id="chatForm"',
        'id="messageInput"',
        'assets/semantic-command-router.js',
        'assets/ecosystem-chat-semantic-commands.js',
        'assets/ecosystem-chat-simple.js',
        'assets/ecosystem-node-views.js',
    ])
    require(UX, [
        'single-primary-governed-chat-preview-entry',
        'technical competency assumption: none',
        'no public worker/runtime/receipt jargon unless needed for a user-visible limitation',
    ])

    legacy_present = 'id="ecosystemTraversal"' in page
    if legacy_present:
        require(PAGE, [
            'class="traversal-step active">Request',
            '>Intent<', '>Boundary<', '>Evidence<', '>Destination<', '>Receipt<',
            'not network access or authority-issued proof',
        ])
        require(LOADER, [
            'assets/ecosystem-chat-traversal.js',
            "dataset.previewOnly = 'true'",
        ])
        require(SCRIPT, [
            "const ordered = ['request', 'intent', 'boundary', 'evidence', 'destination', 'receipt']",
            "strip.dataset.authority = 'none'",
            "strip.dataset.execution = 'disabled'",
            "setPhase('receipt', 'not-issued')",
            'fixture-only',
            'local-preview',
        ])
        print("PASS: Ecosystem Chat legacy traversal preview is bounded and non-authorizing")
        return 0

    # Current canonical UI intentionally hides the old internal traversal strip.
    # Fail closed if the removed internal preview is reintroduced only as script
    # execution without its bounded visible contract.
    if 'assets/ecosystem-chat-traversal.js' in page:
        raise SystemExit(
            "ecosystem-chat.html loads legacy traversal execution without the bounded traversal surface"
        )

    router = page.find('<script src="assets/semantic-command-router.js"></script>')
    bridge = page.find('<script src="assets/ecosystem-chat-semantic-commands.js"></script>')
    runtime = page.find('<script src="assets/ecosystem-chat-simple.js"></script>')
    if min(router, bridge, runtime) < 0 or not (router < bridge < runtime):
        raise SystemExit("ecosystem-chat semantic discovery must load before current chat runtime")

    print("PASS: Ecosystem Chat uses the current user-first unified chat projection")
    print("legacy_traversal_public_surface=false")
    print("semantic_discovery_before_chat_runtime=true")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
