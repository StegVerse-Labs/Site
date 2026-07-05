# Ecosystem Chat Route Activation Status

## Current goal

Move the StegVerse AI entry point from static UI text toward a testable route-aware backend surface.

## Installed route artifacts

```text
data/ecosystem-chat-routes.json
api/ecosystem_chat_backend.py
api/ecosystem_chat_api_wrapper.py
assets/ecosystem-ai-entry-adapter.js
schemas/ecosystem-chat-backend-response.schema.json
schemas/ecosystem-chat-provider-adapter.schema.json
schemas/ecosystem-chat-sdk-access.schema.json
schemas/ecosystem-chat-receipt-preview.schema.json
fixtures/ecosystem-chat/backend-response.example.json
fixtures/ecosystem-chat/receipt-preview.example.json
scripts/check_ecosystem_chat_routes.py
scripts/check_ecosystem_chat_backend.py
scripts/check_ecosystem_chat_api_wrapper.py
scripts/check_ecosystem_chat_provider_adapters.py
scripts/check_ecosystem_chat_sdk_access.py
scripts/check_ecosystem_chat_receipt_preview.py
scripts/check_ecosystem_chat_readiness.py
scripts/check_ecosystem_chat_ai_entry.py
docs/ECOSYSTEM_CHAT_BACKEND_ROUTE_MODEL.md
docs/STEGVERSE_AI_ENTRYPOINT.md
stegverse-llm-console.html
.github/workflows/validate.yml
iosnoperiod/github/workflows/validate.yml
```

## Current capability

```text
one user input window
-> local route classification
-> deterministic backend scaffold
-> browser adapter response shape
-> route guidance
-> SDK guidance
-> external comparison placeholders
-> non-authoritative governance metadata
-> active Site validation workflow
```

## Upstream adapter boundary now available

`StegVerse-org/LLM-adapter` now provides the interim adapter-side AI Entry boundary:

```text
llm_adapter/ai_entry_provider_boundary.py
llm_adapter/ai_entry_backend_service.py
llm_adapter/ai_entry_endpoint.py
llm_adapter/ai_entry_service_wrapper.py
scripts/verify_goal4.py
```

The Site should treat that adapter boundary as the current interim backend source for provider comparison behavior while preserving the Site-local fixture-first contract.

## Canonical validation command

```bash
python scripts/check_ecosystem_chat_ai_entry.py
```

Expected output:

```text
ECOSYSTEM_CHAT_ROUTES_PASS
ECOSYSTEM_CHAT_BACKEND_PASS
ECOSYSTEM_CHAT_API_WRAPPER_PASS
ECOSYSTEM_CHAT_PROVIDER_ADAPTERS_PASS
ECOSYSTEM_CHAT_SDK_ACCESS_PASS
ECOSYSTEM_CHAT_RECEIPT_PREVIEW_PASS
ECOSYSTEM_CHAT_READINESS_PASS
ECOSYSTEM_CHAT_AI_ENTRY_PASS
```

## Backend activation checkpoint

The Site remains local-ready/live-disabled. The next Site-side sync target is to align the Site backend response schema and fixture with the `LLM-adapter` endpoint/service-wrapper response shape.

## Boundary

The route-aware page and backend scaffold are still fixture-first and local. They do not call live providers, execute tasks, mutate repositories, grant SDK access, issue proof receipts, or replace governed authority checks.

## Next build target

Sync the Site response fixture/schema with the `LLM-adapter` endpoint-shaped response while keeping live calls disabled by default.
