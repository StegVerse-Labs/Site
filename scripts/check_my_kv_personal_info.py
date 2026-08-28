#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "my-kv.html"
JS = ROOT / "assets" / "my-kv-personal-info.js"
HANDOFF = ROOT / "docs" / "MY_KV_MULTI_EMAIL_MIRROR_HANDOFF.md"

required_html = [
    "Personal Information",
    "Email Addresses",
    "Add email",
    "Connect this email",
    "SKAP Vault",
    "assets/my-kv-personal-info.js",
]
required_js = [
    "stegverse.kv.personal-contact-profile/v1",
    "MAPPED_CREDENTIAL_REQUIRED",
    "COMPLETE_SKAP_CREDENTIAL_SETUP",
    "FAIL_CLOSED: canonical KV email mapping bridge unavailable",
    "SKAP_VAULT",
    "authority_effect",
]
forbidden_html = [
    'type="password"',
    'name="password"',
    'name="token"',
    'name="app_password"',
]
forbidden_js_literals = [
    "localStorage.setItem",
    "sessionStorage.setItem",
]

def main() -> int:
    failures = []
    html = HTML.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")

    for marker in required_html:
        if marker not in html:
            failures.append(f"missing HTML marker: {marker}")
    for marker in required_js:
        if marker not in js:
            failures.append(f"missing JS marker: {marker}")
    for marker in forbidden_html:
        if marker in html:
            failures.append(f"secret-bearing HTML input prohibited: {marker}")
    for marker in forbidden_js_literals:
        if marker in js:
            failures.append(f"unbounded browser persistence prohibited: {marker}")

    if "Site does not redefine" not in handoff:
        failures.append("handoff missing upstream-authority boundary")
    if "Live mailbox/provider/SKAP execution remains a separate" not in handoff:
        failures.append("handoff missing live-activation non-claim")

    if failures:
        print("MY_KV_PERSONAL_INFO_FAIL")
        for failure in failures:
            print(failure)
        return 1

    print("MY_KV_PERSONAL_INFO_PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
