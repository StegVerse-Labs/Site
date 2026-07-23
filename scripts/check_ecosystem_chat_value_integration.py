#!/usr/bin/env python3
"""Validate direct Ecosystem Node value integration and governed aspect boundaries."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HPS = ROOT / "assets" / "ecosystem-chat-hps.js"
INTEGRATION = ROOT / "assets" / "ecosystem-chat-value-integration.js"
I18N = ROOT / "data" / "ecosystem-chat-value-expectations.i18n.json"
PERMISSIONS = ROOT / "data" / "ecosystem-chat-value-projection-permissions.fixture.json"
BROWSER_BEHAVIOR = ROOT / "data" / "ecosystem-chat-value-browser-behavior.fixture.json"
ASPECT_REGISTRY = ROOT / "data" / "ecosystem-chat-governed-aspects.registry.json"
ASPECT_MODEL = ROOT / "docs" / "ECOSYSTEM_CHAT_GOVERNED_ASPECT_MODEL.md"
CHECKS = (
    ROOT / "scripts" / "check_ecosystem_chat_value_projection_permissions.py",
    ROOT / "scripts" / "check_ecosystem_chat_value_browser_behavior.py",
    ROOT / "scripts" / "check_ecosystem_chat_governed_aspects.py",
)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


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
    errors: list[str] = []
    for path, message in [
        (HPS, "missing assets/ecosystem-chat-hps.js"),
        (INTEGRATION, "missing assets/ecosystem-chat-value-integration.js"),
        (I18N, "missing multilingual value expectation fixture"),
        (PERMISSIONS, "missing captured-derived projection permission fixture"),
        (BROWSER_BEHAVIOR, "missing direct-panel browser behavior fixture"),
        (ASPECT_REGISTRY, "missing governed aspect registry"),
        (ASPECT_MODEL, "missing governed aspect model"),
    ]:
        require(path.exists(), message, errors)
    for check in CHECKS:
        require(check.exists(), f"missing {check.relative_to(ROOT)}", errors)

    if HPS.exists():
        text = HPS.read_text(encoding="utf-8")
        for marker in ["ecosystem-chat-value.html", "assets/ecosystem-chat-value-integration.js"]:
            require(marker in text, f"ecosystem-chat-hps.js missing {marker}", errors)

    if INTEGRATION.exists():
        text = INTEGRATION.read_text(encoding="utf-8")
        for marker in [
            "ecosystemValueClaimPanel",
            "data/ecosystem-chat-value-claims.fixture.json",
            "data/ecosystem-chat-value-claim-history.fixture.json",
            "data/ecosystem-chat-value-projection-permissions.fixture.json",
            "data/ecosystem-chat-value-expectations.i18n.json",
            "submission_event_id",
            "history_event_id",
            "information_class",
            "allowed_destinations",
            "denied_destinations",
            "redaction_required",
            "minimum_disclosure",
            "StegVerseCanonicalEventStream",
            "Export value history",
            "authority_effect:'NONE'",
            "No value, ownership, distribution, projection, payment, custody, or authority claim is inferred",
        ]:
            require(marker in text, f"value integration missing {marker}", errors)

    if I18N.exists():
        payload = json.loads(I18N.read_text(encoding="utf-8"))
        require(payload.get("authority_effect") == "NONE", "i18n fixture authority_effect must be NONE", errors)
        locales = payload.get("locales")
        require(isinstance(locales, dict), "i18n locales must be an object", errors)
        for locale in ["en", "es", "zh-Hans", "zh-Hant"]:
            copy = locales.get(locale) if isinstance(locales, dict) else None
            require(isinstance(copy, dict), f"missing locale {locale}", errors)
            if isinstance(copy, dict):
                for field in ["title", "summary", "preserved", "recognized", "distributable", "privacy", "consent", "button"]:
                    require(isinstance(copy.get(field), str) and bool(copy[field].strip()), f"{locale} missing {field}", errors)

    if errors:
        print("ECOSYSTEM_CHAT_VALUE_INTEGRATION_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    for check in CHECKS:
        returncode, output = run_check(check)
        if returncode != 0:
            print("ECOSYSTEM_CHAT_VALUE_INTEGRATION_CHECK=FAIL")
            print(output)
            return returncode
        print(output)

    print("ECOSYSTEM_CHAT_VALUE_INTEGRATION_CHECK=PASS")
    print("surface=ecosystem-chat.html")
    print("source=claim,history,projection_permission,governed_aspect_registry")
    print("locales=en,es,zh-Hans,zh-Hant")
    print("correlation=claim_id,submission_event_id,history_event_id")
    print("projection_default=DENY")
    print("aspect_default=UNRESOLVED")
    print("browser_behavior=STATIC_CONTRACT_VERIFIED_EXECUTION_NOT_OBSERVED")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
