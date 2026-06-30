from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PATHS = ROOT / "docs" / "SITE_PUBLIC_PATHS.md"

REQUIRED = [
    "/governed-ecosystem.html",
    "StegVerse-Labs/admissibility-wiki",
    "docs/SITE_GOVERNED_ECOSYSTEM_STATUS.txt",
    "scripts/check_site_governed_ecosystem_mirror.py",
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
    if errors:
        print("SITE PUBLIC PATHS: FAIL - " + ", ".join(errors))
        return 1
    print("SITE PUBLIC PATHS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
