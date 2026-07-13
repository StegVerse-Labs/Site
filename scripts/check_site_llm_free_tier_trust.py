from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ecosystem-chat.html"
STATUS = ROOT / "docs" / "LLM_FREE_TIER_TRUST_STATUS.md"

# The public page uses user-facing copy while the retained status document
# preserves the canonical machine-facing names and destination identity.
REQUIRED_PAGE_TEXT = [
    "Bounded free-tier trust",
    'id="free-tier-trust"',
    "5 per day, 25 trial total",
    "Receipt inspection",
    "Recent-session limited",
    "no provider call",
    "no execution authority",
]

REQUIRED_STATUS_TEXT = [
    "LLM Free Tier Trust Status",
    "StegVerse-org/LLM-adapter",
    "adapter.capabilities.json",
    "free_tier_trust",
    "Governed inquiries per day: 5",
    "Trial governed inquiries total: 25",
    "Receipt exports per day: 1",
    "Replays per day: 1",
    "Quota availability is not admissibility.",
    "Upgrading does not change admissibility requirements.",
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
        print("SITE LLM FREE TIER TRUST: FAIL - " + ", ".join(errors))
        return 1
    print("SITE LLM FREE TIER TRUST: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
