from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
REQUIRED = [
    "governed-ecosystem.html",
    "Governed Ecosystem",
    "display mirror",
    "Admissibility Wiki",
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
