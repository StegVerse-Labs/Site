from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PATHS = ROOT / "docs" / "SITE_PUBLIC_PATHS.md"

REQUIRED = [
    "/governed-ecosystem.html",
    "/ecosystem-chat.html",
    "/external-chat.html",
    "/external-review.html",
    "/governed-transitions.html",
    "StegVerse-Labs/admissibility-wiki",
    "docs/SITE_GOVERNED_ECOSYSTEM_STATUS.txt",
    "scripts/check_site_governed_ecosystem_mirror.py",
    "scripts/check_external_chat_compatibility.py",
    "scripts/check_external_review_console.py",
    "external-chat-submission-contract.md",
    "data/external-framework-catalog.json",
    "data/external-framework-catalog.receipt.json",
]


def main():
    errors = []
    if not PUBLIC_PATHS.exists():
        errors.append("missing_public_paths")
        text = ""
    else:
        text = PUBLIC_PATHS.read_text(encoding="utf-8")
    for item in REQUIRED:
        if item not in text:
            errors.append("missing:" + item)
    for path in [
        ROOT / "external-chat.html",
        ROOT / "external-review.html",
        ROOT / "assets" / "external-chat.js",
        ROOT / "assets" / "external-review.js",
        ROOT / "scripts" / "check_external_chat_compatibility.py",
        ROOT / "scripts" / "check_external_review_console.py",
        ROOT / "data" / "external-framework-catalog.json",
        ROOT / "data" / "external-framework-catalog.receipt.json",
    ]:
        if not path.exists():
            errors.append("missing_file:" + str(path.relative_to(ROOT)))
    if errors:
        print("SITE PUBLIC PATHS: FAIL - " + ", ".join(errors))
        return 1
    print("SITE PUBLIC PATHS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
