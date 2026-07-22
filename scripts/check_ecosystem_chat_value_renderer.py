#!/usr/bin/env python3
import subprocess
import sys
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
HISTORY_FIXTURE = ROOT / "data" / "ecosystem-chat-value-claim-history.fixture.json"
CHECKS = (
    ROOT / "scripts" / "check_ecosystem_chat_value_claim_history.py",
    ROOT / "scripts" / "check_ecosystem_chat_value_integration.py",
)


def run_check(path: Path) -> tuple[int, str]:
    completed = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout.rstrip()


def main() -> int:
    errors = []
    for path, markers in FILES.items():
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        errors.extend(f"{path.relative_to(ROOT)} missing: {marker}" for marker in markers if marker not in text)
    for fixture in (FIXTURE, HISTORY_FIXTURE):
        if not fixture.exists():
            errors.append(f"missing file: {fixture.relative_to(ROOT)}")
    for check in CHECKS:
        if not check.exists():
            errors.append(f"missing file: {check.relative_to(ROOT)}")
    if errors:
        print("ECOSYSTEM_CHAT_VALUE_RENDERER_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    for check in CHECKS:
        returncode, output = run_check(check)
        if returncode != 0:
            print("ECOSYSTEM_CHAT_VALUE_RENDERER_CHECK=FAIL")
            print(output)
            return returncode
        print(output)

    print("ECOSYSTEM_CHAT_VALUE_RENDERER_CHECK=PASS")
    print("views=conversation,governed,split")
    print("integration=ecosystem-chat.html")
    print("locales=en,es,zh-Hans,zh-Hant")
    print("correlation=stable_claim_id,submission_event_id,history_event_id")
    print("stage_history=reconstructed")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
