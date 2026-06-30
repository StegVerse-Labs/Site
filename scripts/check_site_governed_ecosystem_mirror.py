from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "governed-ecosystem.html"
STATUS = ROOT / "docs" / "SITE_GOVERNED_ECOSYSTEM_STATUS.txt"

REQUIRED_PAGE_TEXT = [
    "StegVerse Governed Ecosystem Mirror",
    "StegVerse-Labs/admissibility-wiki",
    "Site is display-only",
    "Governed Ecosystem Index",
    "Ecosystem Capability Status",
    "Capability Lifecycle",
]

REQUIRED_STATUS_TEXT = [
    "SITE_GOVERNED_ECOSYSTEM_MIRROR_PRESENT",
    "DISPLAY_ONLY",
    "governed-ecosystem.html",
    "StegVerse-Labs/admissibility-wiki",
]


def main():
    errors = []
    if not PAGE.exists():
        errors.append("missing_page")
        page_text = ""
    else:
        page_text = PAGE.read_text(encoding="utf-8")
    if not STATUS.exists():
        errors.append("missing_status")
        status_text = ""
    else:
        status_text = STATUS.read_text(encoding="utf-8")
    for item in REQUIRED_PAGE_TEXT:
        if item not in page_text:
            errors.append("page_missing:" + item)
    for item in REQUIRED_STATUS_TEXT:
        if item not in status_text:
            errors.append("status_missing:" + item)
    if errors:
        print("SITE GOVERNED ECOSYSTEM MIRROR: FAIL - " + ", ".join(errors))
        return 1
    print("SITE GOVERNED ECOSYSTEM MIRROR: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
