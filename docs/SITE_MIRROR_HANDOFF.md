# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: fully functional governed Ecosystem Chat request-response path
Phase: governed-lifecycle-and-final-response-receipt-client-installed
Primary surface: ecosystem-chat.html
Operational projection: governed-transitions.html
Site mode: GOVERNED_GATEWAY_WITH_LOCAL_FALLBACK
Backend implementation: installed in StegVerse-org/LLM-adapter
Backend deployment and health: verification pending
Workflow target: exactly two operational workflows
Result: CROSS_REPOSITORY_IMPLEMENTATION_INSTALLED_LIVE_VALIDATION_PENDING
```

## Canonical workflow progression

```text
Site Bootstrap Validate
-> Site Task Runner
-> acquire governed transition projection and executor state
-> all-local validation
-> commit bounded generated state on main
-> deploy Pages
-> verify public routes
```

Active workflows remain:

```text
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

## Ecosystem Chat governed gateway client

Installed or updated:

```text
data/ecosystem-chat-gateway.json
assets/ecosystem-chat-transition-identity.js
assets/ecosystem-chat-gateway-health.js
assets/ecosystem-chat-hps.js
scripts/check_ecosystem_chat_gateway_activation.py
scripts/check_ecosystem_chat_receipt_envelopes.py
```

Configured service:

```text
POST https://stegverse-ecosystem-chat-gateway.onrender.com/api/ecosystem-chat
GET  https://stegverse-ecosystem-chat-gateway.onrender.com/health
GET  https://stegverse-ecosystem-chat-gateway.onrender.com/api/transitions/{transition_id}
```

## Browser request progression

```text
create canonical SITE_INPUT identity
-> load validated gateway configuration
-> submit text request plus transition identity
-> require transition_id/run_id/event_id/origin_manifest_id equality
-> receive bounded response lifecycle
-> display gateway intake receipt
-> display final response receipt when issued
-> display lifecycle, admissibility, commit-time validity, custody, and reconstruction posture
```

For a normal non-mutating request, the backend may return:

```text
task_status = completed_bounded_response
lifecycle_state = COMPLETED
admissibility_result = ALLOW
commit_time_validity = VALID
final_receipt_id = final-response-receipt:sha256:...
master_record_status = NOT_YET_SUBMITTED
reconstruction_status = PARTIAL
```

For restricted administration or credential-shaped input:

```text
task_status = pending_authority
lifecycle_state = VERIFICATION_REQUIRED
final_receipt_id = null
no execution or mutation
```

On timeout, non-OK response, malformed response, or identity mismatch, the browser fails closed to deterministic local classification. The fallback claims no gateway receipt, final receipt, execution, admissibility, custody, or reconstruction.

## Public health signal

The Ecosystem Chat page now injects a gateway status panel with three explicit states:

```text
LIVE · BOUNDED
LOCAL FALLBACK
UNAVAILABLE
```

The panel verifies `/health` and displays native executor and bounded-pipeline posture. It does not treat health as per-transition authority.

## Deployable backend implementation

Canonical backend repository:

```text
StegVerse-org/LLM-adapter
```

Installed there:

```text
llm_adapter/ecosystem_chat_gateway.py
llm_adapter/governed_chat_pipeline.py
tests/test_ecosystem_chat_gateway.py
tests/test_governed_chat_pipeline.py
render.yaml
pyproject.toml
```

The backend preserves the original transition identity through bounded bridge, delegation, standing, executor, response, and receipt stages. It exposes lifecycle lookup for the same transition.

## Executor and observatory state

The governed transition observatory and receipted executor projection remain installed:

```text
governed-transitions.html
data/governed-transition-index.json
data/governed-transition-index-import-status.json
data/governed-executor-status.json
```

Native executor eligibility and a gateway request are separate boundaries. Executor activation does not grant repository mutation or blanket per-transition authority.

## Non-negotiable boundary

```text
Site does not execute or mutate repositories.
Gateway intake receipt != final response receipt.
Final response receipt covers the bounded response record only.
Final response receipt != repository mutation authority.
Final response receipt != publication authority.
Final response receipt != Master-Records custody.
Native executor activation != blanket per-transition authority.
Projection != source authority.
```

## Validation surface

The existing receipt-envelope validation checks:

```text
gateway configuration and HTTPS endpoints
identity-preserving request/response markers
timeout and local fallback behavior
lifecycle and final receipt display
public gateway health module
health panel load registration
gateway receipt/final response receipt distinction
```

No workflow was added.

## Remaining files/modules and destinations

```text
StegVerse-org/LLM-adapter:
- current-main gateway and pipeline test evidence
- successful Render deployment
- public GET /health verification
- durable Master-Records submission for completed response records

StegVerse-Labs/Site:
- current-main validation evidence
- live browser POST round-trip evidence
- deployed public health indicator verification

Cross-repository runtime:
- replace in-memory lifecycle lookup with durable custody-backed lookup
- return Master-Records custody receipt when independently issued
- add provider-backed generated responses only after provider policy, credentials, quota, and cost boundaries are active
```

## Next task

```text
1. Verify LLM-adapter gateway and governed pipeline tests.
2. Deploy render.yaml and verify /health.
3. Submit one public Ecosystem Chat request and verify COMPLETED lifecycle plus final_receipt_id.
4. Add durable Master-Records submission for completed bounded-response relationships.
5. Replace in-memory transition lookup with custody-backed lookup.
6. Add provider-backed responses after governed provider activation.
```

## Release posture

The browser and deployable backend now support identity-preserving bounded lifecycle completion and final response receipt return. The system must not be called publicly live until service deployment, health verification, and a public POST round trip are observed.

## Archive readiness

This handoff contains the current implementation, lifecycle return contract, deployment boundary, validation rules, and continuation order. Earlier conversation context is not required.
