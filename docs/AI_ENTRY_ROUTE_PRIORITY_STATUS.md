# AI Entry Route Priority Status

## Current status

The Site AI Entry route classifier no longer relies on route manifest order alone.

## Installed route-priority files

```text
api/ecosystem_chat_backend.py
assets/ecosystem-ai-entry-adapter.js
fixtures/ecosystem-chat/route-precedence-cases.json
scripts/check_ecosystem_chat_backend.py
scripts/check_ecosystem_chat_ui_route_priority.py
scripts/check_ecosystem_chat_ai_entry.py
```

## Current behavior

The backend and browser adapter both use deterministic route priority scoring for overlapping route keywords.

This prevents generic route keywords from swallowing more specific requests, including:

```text
How do I access the SDK? -> sdk_access_guidance
Explain runtime adapter status -> runtime_status
Compare StegVerse with ChatGPT and Claude -> llm_comparison
Review governance evidence reconstruction -> governance_review
Show docs for proof runbook -> documentation_route
What is StegVerse? -> ecosystem_explanation
```

## Validation

The aggregate validator now includes:

```bash
python scripts/check_ecosystem_chat_backend.py
python scripts/check_ecosystem_chat_ui_route_priority.py
```

Expected output includes:

```text
ECOSYSTEM_CHAT_BACKEND_PASS
ECOSYSTEM_CHAT_UI_ROUTE_PRIORITY_PASS
```

## Manual task elimination

Route-precedence review no longer requires manual screenshot inspection or ad hoc route checks. New route regression cases can be added to:

```text
fixtures/ecosystem-chat/route-precedence-cases.json
```
