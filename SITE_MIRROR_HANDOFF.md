# Site Mirror Handoff

## Current source of truth

This file is the active handoff for `StegVerse-Labs/Site` until superseded.

## Active goal

Goal: StegVerse AI Entry Point contract-synced local-ready/live-disabled surface with no-manual-task validation closure.

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
data/ai-entry-release-readiness.json
data/ai-entry-validation-stabilization.json
data/ai-entry-workflow-parity.json
data/ai-entry-automation-closure.json
schemas/ecosystem-chat-backend-response.schema.json
schemas/ecosystem-chat-provider-adapter.schema.json
schemas/ecosystem-chat-sdk-access.schema.json
schemas/ecosystem-chat-receipt-preview.schema.json
schemas/ecosystem-chat-adapter-extension.schema.json
fixtures/ecosystem-chat/backend-response.example.json
fixtures/ecosystem-chat/receipt-preview.example.json
fixtures/ecosystem-chat/adapter-extension.example.json
fixtures/ecosystem-chat/route-precedence-cases.json
docs/STEGVERSE_AI_ENTRYPOINT.md
docs/STEGVERSE_LLM_COMPARISON_CONSOLE.md
docs/ECOSYSTEM_CHAT_BACKEND_ROUTE_MODEL.md
docs/ECOSYSTEM_CHAT_ROUTE_ACTIVATION_STATUS.md
docs/AI_ENTRY_ACTIONS_AUTO_RUN_STATUS.md
docs/AI_ENTRY_ROUTE_PRIORITY_STATUS.md
scripts/check_ecosystem_chat_routes.py
scripts/check_ecosystem_chat_backend.py
scripts/check_ecosystem_chat_api_wrapper.py
scripts/check_ecosystem_chat_provider_adapters.py
scripts/check_ecosystem_chat_sdk_access.py
scripts/check_ecosystem_chat_receipt_preview.py
scripts/check_ecosystem_chat_readiness.py
scripts/check_ecosystem_chat_adapter_extension.py
scripts/check_ecosystem_chat_ui_route_priority.py
scripts/check_ai_entry_no_manual_tasks.py
scripts/check_ai_entry_release_readiness.py
scripts/check_ai_entry_validation_stabilization.py
scripts/check_ai_entry_green_run_readiness.py
scripts/check_ai_entry_workflow_parity.py
scripts/check_ai_entry_workflow_commands.py
scripts/check_ai_entry_automation_closure.py
scripts/check_ecosystem_chat_ai_entry.py
scripts/check_ecosystem_chat_ai_entry_full.py
.github/workflows/validate.yml
iosnoperiod/github/workflows/validate.yml
iosnoperiod.md
```

## Upstream adapter boundary

`StegVerse-org/LLM-adapter` provides the interim adapter-side AI Entry boundary and now runs its full wrapper:

```text
llm_adapter/ai_entry_provider_boundary.py
llm_adapter/ai_entry_backend_service.py
llm_adapter/ai_entry_endpoint.py
llm_adapter/ai_entry_service_wrapper.py
scripts/verify_goal4_full.py
scripts/check_workflow_parity.py
```

`StegVerse-org/StegVerse-SDK` provides the SDK-side receipt/intake/import-path checks:

```text
scripts/verify_goal4.py
scripts/check_sdk_local_import_path.py
scripts/check_pytest_compatibility_surface.py
scripts/check_workflow_parity.py
```

## Canonical validation command

```bash
python scripts/check_ecosystem_chat_ai_entry_full.py
```

Expected terminal output includes:

```text
ECOSYSTEM_CHAT_AI_ENTRY_PASS
AI_ENTRY_GREEN_RUN_READINESS_PASS
AI_ENTRY_WORKFLOW_PARITY_PASS
AI_ENTRY_WORKFLOW_COMMANDS_PASS
AI_ENTRY_AUTOMATION_CLOSURE_PASS
ECOSYSTEM_CHAT_AI_ENTRY_FULL_PASS
```

## Active validation workflow

```text
Canonical: .github/workflows/validate.yml
Mirror: iosnoperiod/github/workflows/validate.yml
```

The canonical workflow and mirror run:

```bash
python scripts/check_ecosystem_chat_ai_entry_full.py
```

The mirror remains only as an iOS-safe restoration copy. The canonical workflow is the active validation surface.

## Required invariant

```text
one_window_entry_surface == true
route_manifest_present == true
route_precedence_fixture_present == true
backend_route_priority_self_verified == true
browser_route_priority_self_verified == true
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
manual_tasks_remaining == []
```

## Remaining files or modules to install

```text
None for Site-side AI Entry no-manual-task validation closure.
```

## Boundary

The current build is contract-synced local-ready/live-disabled. It is not live provider activation, not SDK access, not credential exposure, not authority issuance, not repo mutation, and not real receipt issuance.

## Archive posture

This handoff preserves the AI Entry Site contract-sync and no-manual-task validation closure state so the Complete thread can be archived without additional context. The Site-side validation closure is complete pending workflow-run confirmation or future governed-live activation work.
