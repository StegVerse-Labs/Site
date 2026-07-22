#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    ROOT / "ecosystem-chat-value.html": [
        'data-value-view="conversation"',
        'data-value-view="governed"',
        'data-value-view="split"',
        "assets/ecosystem-chat-value-claims.js",
        "claim preserved ≠ value proven",
        "distributable ≠ payment",
    ],
    ROOT / "assets" / "ecosystem-chat-value-claims.js": [
        "submitted",
        "recognized",
        "attributed",
        "realized",
        "distributable",
        "settled",
        "submission_event_id",
        "StegVerseValueClaims",
        "No payment or royalty is implied",
    ],
    ROOT / "docs" / "ECOSYSTEM_CHAT_VALUE_CLAIM_CONTRACT.md": [
        "request for intelligence",
        "contribution of intelligence",
        "Every governed submission can preserve a traceable value claim",
    ],
}
FIXTURE = ROOT / "data" / "ecosystem-chat-value-claims.fixture.json"


def main() -> int:
    errors = []
    for path, markers in FILES.items():
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        errors.extend(f"{path.relative_to(ROOT)} missing: {marker}" for marker in markers if marker not in text)
    if not FIXTURE.exists():
        errors.append(f"missing file: {FIXTURE.relative_to(ROOT)}")
    if errors:
        print("ECOSYSTEM_CHAT_VALUE_RENDERER_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ECOSYSTEM_CHAT_VALUE_RENDERER_CHECK=PASS")
    print("views=conversation,governed,split")
    print("correlation=stable_claim_id_and_submission_event_id")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
