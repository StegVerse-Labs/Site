from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
GOVERNED = ROOT / "governed-ecosystem.html"
ADMISSIBILITY = ROOT / "admissibility-wiki.html"

REQUIRED_INDEX = [
    "How can I help?",
    'href="my-kv.html"',
    'href="organizational-kv.html"',
    "How do I use this chat?",
    "What is StegVerse?",
    "What is My KV?",
]

FORBIDDEN_PRIMARY_SPECIALTY_LINKS = [
    'href="governed-ecosystem.html"',
    'href="admissibility-wiki.html"',
    "StegVerse public mirror status",
    "Site is a public mirror and transition router preview, not proof source.",
]

REQUIRED_GOVERNED = [
    "StegVerse Governed Ecosystem Mirror",
    "StegVerse-Labs/admissibility-wiki",
    "Site is display-only",
    "Governed Ecosystem Index",
    "Capability Lifecycle",
]

REQUIRED_ADMISSIBILITY = [
    "Admissibility Wiki",
    "StegVerse-Labs/admissibility-wiki",
    "Site is a public bridge and display surface.",
    "It does not accept proposals, issue receipts, approve terminology, or activate proof authority.",
]


def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main():
    errors = []
    index = read(INDEX)
    governed = read(GOVERNED)
    admissibility = read(ADMISSIBILITY)

    for item in REQUIRED_INDEX:
        if item not in index:
            errors.append("index_missing:" + item)

    for item in FORBIDDEN_PRIMARY_SPECIALTY_LINKS:
        if item in index:
            errors.append("retired_primary_homepage_specialty_link:" + item)

    for item in REQUIRED_GOVERNED:
        if item not in governed:
            errors.append("governed_surface_missing:" + item)

    for item in REQUIRED_ADMISSIBILITY:
        if item not in admissibility:
            errors.append("admissibility_surface_missing:" + item)

    if index.count('data-chat-prompt=') != 3:
        errors.append("homepage_starter_prompt_count")

    if errors:
        print("SITE HOMEPAGE GOVERNED ECOSYSTEM: FAIL - " + ", ".join(errors))
        return 1

    print("SITE HOMEPAGE GOVERNED ECOSYSTEM: PASS")
    print("homepage_contract=SIMPLIFIED_CONVERSATIONAL_SHELL")
    print("homepage_specialty_navigation_required=false")
    print("governed_ecosystem_destination=DEDICATED_DIRECT_CONTEXTUAL")
    print("admissibility_wiki_destination=DEDICATED_DIRECT_CONTEXTUAL")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
