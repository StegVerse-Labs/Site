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

    # The machine-facing trust contract remains authoritative in STATUS.
    # The current primary chat is intentionally ordinary-language-first and may
    # omit the historical internal trust/quota panel. If that legacy panel is
    # present, it must remain complete; otherwise require the current user-first
    # conversational surface rather than forcing governance jargon back into it.
    page_text_normalized = page_text.casefold()
    legacy_panel_present = (
        'id="free-tier-trust"' in page_text
        or "bounded free-tier trust" in page_text_normalized
    )
    if legacy_panel_present:
        for item in REQUIRED_PAGE_TEXT:
            if item.casefold() not in page_text_normalized:
                errors.append("page_missing:" + item)
    else:
        current_user_first = [
            "<h1>How can I help?</h1>",
            "Ask in your own words.",
            'id="chatForm"',
            'id="messageInput"',
        ]
        for item in current_user_first:
            if item not in page_text:
                errors.append("page_missing_current_user_first:" + item)

    for item in REQUIRED_STATUS_TEXT:
        if item not in status_text:
            errors.append("status_missing:" + item)

    if errors:
        print("SITE LLM FREE TIER TRUST: FAIL - " + ", ".join(errors))
        return 1
    print("SITE LLM FREE TIER TRUST: PASS")
    print(f"legacy_public_trust_panel={'true' if legacy_panel_present else 'false'}")
    print("trust_contract_source=docs/LLM_FREE_TIER_TRUST_STATUS.md")
    print("primary_chat_internal_quota_copy_required=false")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
