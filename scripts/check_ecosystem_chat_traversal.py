#!/usr/bin/env python3
"""Validate the local, non-authorizing Ecosystem Chat traversal preview."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ecosystem-chat.html"
LOADER = ROOT / "assets" / "ecosystem-chat-hps.js"
SCRIPT = ROOT / "assets" / "ecosystem-chat-traversal.js"


def require(path: Path, phrases: list[str]) -> None:
    if not path.exists():
        raise SystemExit(f"missing {path.relative_to(ROOT)}")
    body = path.read_text(encoding="utf-8")
    missing = [phrase for phrase in phrases if phrase not in body]
    if missing:
        raise SystemExit(f"{path.relative_to(ROOT)} missing: {', '.join(missing)}")


def main() -> int:
    require(PAGE, [
        'id="ecosystemTraversal"',
        'class="traversal-step active">Request',
        '>Intent<', '>Boundary<', '>Evidence<', '>Destination<', '>Receipt<',
        "not network access or authority-issued proof",
    ])
    require(LOADER, [
        "assets/ecosystem-chat-traversal.js",
        "dataset.previewOnly = 'true'",
    ])
    require(SCRIPT, [
        "const ordered = ['request', 'intent', 'boundary', 'evidence', 'destination', 'receipt']",
        "strip.dataset.authority = 'none'",
        "strip.dataset.execution = 'disabled'",
        "setPhase('receipt', 'not-issued')",
        "fixture-only",
        "local-preview",
    ])
    print("PASS: Ecosystem Chat traversal preview is bounded and non-authorizing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
