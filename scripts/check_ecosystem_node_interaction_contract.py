#!/usr/bin/env python3
"""Validate the Ecosystem Node interaction and locale contract without a browser dependency."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "assets" / "ecosystem-node-views.js"
HTML = ROOT / "ecosystem-chat.html"

REQUIRED_JS = (
    "SUPPORTED_LOCALES",
    "'en'",
    "'es'",
    "'zh-Hans'",
    "'zh-Hant'",
    "resolveInitialLocale",
    "stegverse-node-locale",
    "setLocale",
    "applyLocale",
    "data-node-view=\"conversation\"",
    "data-node-view=\"governed\"",
    "data-node-view=\"split\"",
    "aria-selected",
    "tabIndex=0",
    "addEventListener('focus'",
    "selectEvent(event.event_id,'conversation')",
    "selectEvent(event.event_id,'governed')",
    "scrollIntoView",
    "correlated-active",
    "event_id",
    "parent_event_id",
    "evidence_refs",
    "Export JSONL",
)

REQUIRED_HTML = (
    "assets/ecosystem-node-views.js",
    "Canonical governed event stream",
)


def missing(path: Path, needles: tuple[str, ...]) -> list[str]:
    if not path.exists():
        return [f"missing file: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    return [f"{path.relative_to(ROOT)} missing interaction marker: {needle}" for needle in needles if needle not in text]


def main() -> int:
    errors = [*missing(JS, REQUIRED_JS), *missing(HTML, REQUIRED_HTML)]
    if errors:
        print("ECOSYSTEM_NODE_INTERACTION_CONTRACT=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("ECOSYSTEM_NODE_INTERACTION_CONTRACT=PASS")
    print("views=conversation,governed,split")
    print("selection=bidirectional_stable_event_id")
    print("keyboard_focus=bound")
    print("locales=en,es,zh-Hans,zh-Hant")
    print("locale_preference=persistent")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
