# Site Mirror Handoff

## Current source of truth

This file is the active handoff for `StegVerse-Labs/Site` until superseded.

## Active goal

Goal: StegVerse AI Entry Point contract-synced local-ready/live-disabled surface.

The Site presents one StegVerse AI entry window that routes user input into chat, comparison, SDK guidance, governance review, runtime status, documentation, or restricted-admin paths without forcing the user to choose repo-specific pages first.

## Installed AI entry artifacts

```text
stegverse-llm-console.html
assets/ecosystem-ai-entry-adapter.js
api/ecosystem_chat_backend.py
api/ecosystem_chat_api_wrapper.py
data/ecosystem-chat-routes.json
data/ecosystem-chat-provider-adapters.json
data/ecosystem-chat-sdk-access.json
data/ecosystem-chat-ai-entry-readiness.json
schemas/ecosystem-chat-backend-response.schema.json
schemas/ecosystem-chat-provider-adapter.schema.json
schemas/ecosystem-chat-sdk-access.schema.json
schemas/ecosystem-chat-receipt-preview.schema.json
schemas/ecosystem-chat-adapter-extension.schema.json
fixtures/ecosystem-chat/backend-response.example.json
fixtures/ecosystem-chat/receipt-preview.example.json
fixtures/ecosystem-chat/adapter-extension.example.json
docs/STEGVERSE_AI_ENTRYPOINT.md
docs/STEGVERSE_LLM_COMPARISON_CONSOLE.md
docs/ECOSYSTEM_CHAT_BACKEND_ROUTE_MODEL.md
docs/ECOSYSTEM_CHAT_ROUTE_ACTIVATION_STATUS.md
scripts/check_ecosystem_chat_routes.py
scripts/check_ecosystem_chat_backend.py
scripts/check_ecosystem_chat_api_wrapper.py
scripts/check_ecosystem_chat_provider_adapters.py
scripts/check_ecosystem_chat_sdk_access.py
scripts/check_ecosystem_chat_receipt_preview.py
scripts/check_ecosystem_chat_readiness.py
scripts/check_ecosystem_chat_adapter_extension.py
scripts/check_ecosystem_chat_ai_entry.py
.github/workflows/validate.yml
iosnoperiod/github/workflows/validate.yml
iosnoperiod.md
```

## Upstream adapter boundary

`StegVerse-org/LLM-adapter` now provides the interim adapter-side AI Entry boundary:

```text
llm_adapter/ai_entry_provider_boundary.py
llm_adapter/ai_entry_backend_service.py
llm_adapter/ai_entry_endpoint.py
llm_adapter/ai_entry_service_wrapper.py
```

The Site browser adapter now emits `adapter_extension` markers that align with that interim boundary:

```text
adapter_status
preview_marker
endpoint_marker
service_marker
```

## Canonical validation command

```bash
python scripts/check_ecosystem_chat_ai_entry.py
```

Expected terminal output includes:

```text
ECOSYSTEM_CHAT_ROUTES_PASS
ECOSYSTEM_CHAT_BACKEND_PASS
ECOSYSTEM_CHAT_API_WRAPPER_PASS
ECOSYSTEM_CHAT_PROVIDER_ADAPTERS_PASS
ECOSYSTEM_CHAT_SDK_ACCESS_PASS
ECOSYSTEM_CHAT_RECEIPT_PREVIEW_PASS
ECOSYSTEM_CHAT_READINESS_PASS
ECOSYSTEM_CHAT_ADAPTER_EXTENSION_PASS
ECOSYSTEM_CHAT_AI_ENTRY_PASS
```

## Active validation workflow

```text
Canonical: .github/workflows/validate.yml
Mirror: iosnoperiod/github/workflows/validate.yml
```

The canonical workflow and mirror run:

```bash
python scripts/check_ecosystem_chat_ai_entry.py
```

The mirror remains only as an iOS-safe restoration copy. The canonical workflow is the active validation surface.

## Required invariant

```text
one_window_entry_surface == true
route_manifest_present == true
browser_adapter_present == true
adapter_extension_present == true
adapter_extension_validated == true
deterministic_backend_scaffold_present == true
api_wrapper_present == true
provider_calls_enabled == false
sdk_calls_enabled == false
credential_surface_enabled == false
execution_authority_issued == false
real_receipt_issued == false
external_provider_outputs_authority == false
workflow_count_exceeds_two == false
```

## Remaining files or modules to install

```text
None for Site-side AI Entry contract sync.
```

## Boundary

The current build is contract-synced local-ready/live-disabled. It is not live provider activation, not SDK access, not credential exposure, not authority issuance, not repo mutation, and not real receipt issuance.

## Archive posture

This handoff preserves the AI Entry Site contract-sync state so the complete thread can be archived without additional context. The Site-side contract sync is complete pending workflow-run confirmation or future governed-live activation work.
