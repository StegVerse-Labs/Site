#!/usr/bin/env python3
"""Static contract check for the Ecosystem Node synchronized dual-view shell."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "ecosystem-chat.html"
JS = ROOT / "assets" / "ecosystem-node-views.js"
CONTRACT = ROOT / "docs" / "ECOSYSTEM_NODE_CANONICAL_EVENT_CONTRACT.md"

REQUIRED_HTML = [
    "assets/ecosystem-node-views.js",
    "Conversation renderer",
    "Governed-record renderer",
    "Split-view correlation layer",
]
REQUIRED_JS = [
    'data-node-view="conversation"',
    'data-node-view="governed"',
    'data-node-view="split"',
    "event_id",
    "parent_event_id",
    "human_projection",
    "governed_projection",
    "policy_refs",
    "evidence_refs",
    "artifact_refs",
    "continuity_refs",
    "Export JSON",
    "Export JSONL",
    "StegVerseCanonicalEventStream",
    "SUPPORTED_LOCALES",
    "zh-Hans",
    "zh-Hant",
    "Español",
    "setLocale",
    "stegverse-node-locale",
]
REQUIRED_CONTRACT = [
    "Neither visible pane is authoritative",
    "correlation never uses text matching",
    "Role-based disclosure and redaction",
    "Production next step",
]


def require(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return [f"missing file: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    return [f"{path.relative_to(ROOT)} missing: {needle}" for needle in needles if needle not in text]


def main() -> int:
    errors = []
    errors.extend(require(HTML, REQUIRED_HTML))
    errors.extend(require(JS, REQUIRED_JS))
    errors.extend(require(CONTRACT, REQUIRED_CONTRACT))
    if errors:
        print("ECOSYSTEM_NODE_DUAL_VIEW_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ECOSYSTEM_NODE_DUAL_VIEW_CHECK=PASS")
    print("modes=conversation,governed,split")
    print("correlation=stable_event_id")
    print("exports=json,jsonl")
    print("locales=en,es,zh-Hans,zh-Hant")
    print("locale_selection=persistent_browser_preference")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
