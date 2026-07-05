# Site Mirror Handoff

## Current source of truth

This file is the active handoff for `StegVerse-Labs/Site` until superseded.

## Active goal

Goal: Governed Live Authority Service Boundary, preview-only/live-disabled, extending the completed cohesive StegVerse AI Entry Application and governed backend activation preview path.

The Site presents one StegVerse AI entry window that routes user input into chat, comparison, SDK guidance, governance review, runtime status, documentation, restricted-admin paths, governed-live activation status, backend activation guidance, and authority decision previews without forcing the user to choose repo-specific pages first.

## Installed AI entry application, activation-path, and authority-boundary artifacts

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
data/ai-entry-governed-live-activation-plan.json
data/ai-entry-governed-live-readiness.json
data/ai-entry-application-completion.json
data/ai-entry-backend-activation-boundary.json
data/ai-entry-activation-routes.json
data/ai-entry-backend-activation-progress.json
data/ai-entry-ci-visibility.json
data/ai-entry-authority-service-boundary.json
schemas/ecosystem-chat-backend-response.schema.json
schemas/ecosystem-chat-provider-adapter.schema.json
schemas/ecosystem-chat-sdk-access.schema.json
schemas/ecosystem-chat-receipt-preview.schema.json
schemas/ecosystem-chat-adapter-extension.schema.json
schemas/ai-entry-governed-live-activation-request.schema.json
fixtures/ecosystem-chat/backend-response.example.json
fixtures/ecosystem-chat/receipt-preview.example.json
fixtures/ecosystem-chat/adapter-extension.example.json
fixtures/ecosystem-chat/route-precedence-cases.json
fixtures/ecosystem-chat/governed-live-activation-request.example.json
fixtures/ecosystem-chat/backend-activation-request.example.json
fixtures/ecosystem-chat/backend-activation-response.example.json
fixtures/ecosystem-chat/authority-decision-request.example.json
fixtures/ecosystem-chat/authority-decision-response.example.json
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
scripts/check_ai_entry_governed_live_activation_plan.py
scripts/check_ai_entry_governed_live_activation_request.py
scripts/check_ai_entry_governed_live_readiness.py
scripts/check_ai_entry_ui_activation_status.py
scripts/check_ai_entry_application_page.py
scripts/check_ai_entry_application_completion.py
scripts/check_ai_entry_backend_activation_boundary.py
scripts/check_ai_entry_activation_routes.py
scripts/check_ai_entry_backend_activation_fixtures.py
scripts/check_ai_entry_ui_activation_routes.py
scripts/check_ai_entry_backend_activation_progress.py
scripts/check_ai_entry_ci_visibility.py
scripts/check_ai_entry_authority_service_boundary.py
scripts/check_ai_entry_authority_decision_fixtures.py
scripts/check_ecosystem_chat_ai_entry.py
scripts/check_ecosystem_chat_ai_entry_full.py
scripts/check_ecosystem_chat_application.py
.github/workflows/validate.yml
iosnoperiod/github/workflows/validate.yml
iosnoperiod.md
```

## Cohesive application surface

The current UI surface includes:

```text
One StegVerse AI window
StegVerse AI response
Route / ecosystem essentials
SDK / access guidance
Governed-live activation status
ChatGPT comparison
Claude comparison
Other LLM comparison
Activation guidance
Activation request preview
Activation boundary review
```

The browser adapter exposes `activation_status` and remains fail-closed:

```text
current_mode=local_ready_live_disabled
readiness_state=not_ready_fail_closed
live_provider_calls_enabled=false
live_sdk_calls_enabled=false
credential_surface_enabled=false
execution_authority_issued=false
real_receipt_issued=false
repo_mutation_from_chat_enabled=false
```

## Backend activation path status

Completed preview components:

```text
activation_boundary_contract=true
activation_route_model=true
backend_activation_request_fixture=true
backend_activation_response_fixture=true
ui_activation_guidance_routes=true
ci_visibility_state_recorded=true
authority_service_boundary=true
authority_decision_request_fixture=true
authority_decision_response_fixture=true
adapter_authority_boundary_mirror=true
```

Remaining governed-live components:

```text
true_green_run_confirmation=true
receipt_issuer_boundary=true
provider_capture_boundary=true
sdk_access_decision_boundary=true
operator_recoverability_boundary=true
```

The activation and authority paths are still non-executing:

```text
authority_decision=DENY
authority_issued=false
activation_request_executes=false
provider_call=false
sdk_call=false
credential_lookup=false
receipt_issue=false
execution_authority_issue=false
repo_mutation=false
```

## CI visibility status

Connector checks for recent Site commits returned no visible combined statuses and no visible workflow runs. This is recorded as:

```text
ci_visibility_state=not_visible_through_connector
green_run_confirmed=false
manual_screenshot_required=false
treat_ci_as_green=false
local_validator_command=python scripts/check_ecosystem_chat_application.py
```

Green is not claimed until connector-visible or workflow-visible data confirms it.

## Upstream adapter boundary

`StegVerse-org/LLM-adapter` provides the interim adapter-side AI Entry boundary and runs its full wrapper:

```text
llm_adapter/ai_entry_provider_boundary.py
llm_adapter/ai_entry_backend_service.py
llm_adapter/ai_entry_endpoint.py
llm_adapter/ai_entry_service_wrapper.py
llm_adapter/ai_entry_authority_boundary.py
scripts/check_ai_entry_authority_boundary.py
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
python scripts/check_ecosystem_chat_application.py
```

Expected terminal output includes:

```text
ECOSYSTEM_CHAT_AI_ENTRY_PASS
AI_ENTRY_GREEN_RUN_READINESS_PASS
AI_ENTRY_WORKFLOW_PARITY_PASS
AI_ENTRY_WORKFLOW_COMMANDS_PASS
AI_ENTRY_AUTOMATION_CLOSURE_PASS
AI_ENTRY_GOVERNED_LIVE_ACTIVATION_PLAN_PASS
AI_ENTRY_GOVERNED_LIVE_ACTIVATION_REQUEST_PASS
AI_ENTRY_GOVERNED_LIVE_READINESS_PASS
ECOSYSTEM_CHAT_AI_ENTRY_FULL_PASS
AI_ENTRY_UI_ACTIVATION_STATUS_PASS
AI_ENTRY_APPLICATION_PAGE_PASS
AI_ENTRY_APPLICATION_COMPLETION_PASS
AI_ENTRY_BACKEND_ACTIVATION_BOUNDARY_PASS
AI_ENTRY_ACTIVATION_ROUTES_PASS
AI_ENTRY_BACKEND_ACTIVATION_FIXTURES_PASS
AI_ENTRY_UI_ACTIVATION_ROUTES_PASS
AI_ENTRY_BACKEND_ACTIVATION_PROGRESS_PASS
AI_ENTRY_CI_VISIBILITY_PASS
AI_ENTRY_AUTHORITY_SERVICE_BOUNDARY_PASS
AI_ENTRY_AUTHORITY_DECISION_FIXTURES_PASS
ECOSYSTEM_CHAT_APPLICATION_PASS
```

## Active validation workflow

```text
Canonical: .github/workflows/validate.yml
Mirror: iosnoperiod/github/workflows/validate.yml
```

The canonical workflow and mirror run:

```bash
python scripts/check_ecosystem_chat_application.py
```

The mirror remains only as an iOS-safe restoration copy. The canonical workflow is the active validation surface.

## Required invariant

```text
one_window_entry_surface == true
cohesive_application_surface == true
backend_activation_preview_path == true
authority_service_boundary_present == true
authority_decision_fixtures_present == true
adapter_authority_boundary_mirror_present == true
route_manifest_present == true
route_precedence_fixture_present == true
backend_route_priority_self_verified == true
browser_route_priority_self_verified == true
browser_adapter_present == true
adapter_extension_present == true
adapter_extension_validated == true
activation_status_surface_present == true
activation_status_fail_closed == true
activation_routes_present == true
activation_request_response_fixtures_present == true
ci_visibility_state_recorded == true
green_run_confirmed == false until visible data confirms green
deterministic_backend_scaffold_present == true
api_wrapper_present == true
provider_calls_enabled == false
sdk_calls_enabled == false
credential_surface_enabled == false
execution_authority_issued == false
real_receipt_issued == false
repo_mutation_from_chat_enabled == false
activation_request_executes == false
external_provider_outputs_authority == false
workflow_count_exceeds_two == false
manual_tasks_remaining == []
```

## Remaining files or modules to install

```text
Receipt issuer boundary -> StegVerse-org/StegVerse-SDK and/or StegVerse-org/LLM-adapter
Provider capture boundary -> StegVerse-org/LLM-adapter
SDK access decision boundary -> StegVerse-org/StegVerse-SDK
Operator recoverability boundary -> StegVerse-Labs/Site / StegVerse-org/LLM-adapter
```

## Boundary

The current build is cohesive, preview-only, and live-disabled. It is not live provider activation, not SDK access, not credential exposure, not authority issuance, not repo mutation, and not real receipt issuance. CI green is also not claimed while connector-visible run data is absent.

## Archive posture

This handoff preserves the cohesive AI Entry application, governed backend activation preview path, authority service boundary, adapter authority mirror, and CI visibility state so the Complete thread can be archived without additional context. The authority boundary is complete pending true green-run confirmation or future receipt/provider/SDK/recoverability boundary work.
