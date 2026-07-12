#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "external-review.html"
CLIENT = ROOT / "assets" / "external-review.js"


def fail(message: str) -> int:
    print(f"EXTERNAL REVIEW CONSOLE: FAIL - {message}")
    return 1


def main() -> int:
    for path in (PAGE, CLIENT):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")
    page = PAGE.read_text(encoding="utf-8")
    client = CLIENT.read_text(encoding="utf-8")
    for marker in [
        "Delegated reviewer console",
        "does not grant certification",
        "Reviewer token",
        "Issue delegated correction",
        "assets/external-review.js",
    ]:
        if marker not in page:
            return fail(f"page missing marker: {marker}")
    for marker in [
        "/api/external-review/reviewer/packages/",
        "/api/external-review/corrections",
        "reviewer_identity_verified",
        "reviewer_delegation_verified",
        "review_scope_verified",
        "publication_authorized !== false",
        "reviewer-token').value = ''",
    ]:
        if marker not in client:
            return fail(f"client missing marker: {marker}")
    print("EXTERNAL REVIEW CONSOLE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
