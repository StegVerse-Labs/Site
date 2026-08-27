from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
REQUIRED = [
    "governed-ecosystem.html",
    "Governed Ecosystem",
    "Admissibility Wiki",
    "StegVerse public mirror status",
    "Site is a public mirror and transition router preview, not proof source.",
]


def main():
    errors = []
    if not INDEX.exists():
        errors.append("missing_index")
        text = ""
    else:
        text = INDEX.read_text(encoding="utf-8")
    for item in REQUIRED:
        if item not in text:
            errors.append("missing:" + item)
    if errors:
        print("SITE HOMEPAGE GOVERNED ECOSYSTEM: FAIL - " + ", ".join(errors))
        return 1
    print("SITE HOMEPAGE GOVERNED ECOSYSTEM: PASS")
    print("homepage_mirror_contract=CURRENT_USER_FIRST_NONAUTHORITY")
    print("homepage_requires_legacy_display_mirror_phrase=false")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
