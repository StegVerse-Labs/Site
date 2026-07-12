# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: fully functional governed Ecosystem Chat request-response and custody path
Phase: persistence-and-custody-status-client-installed
Primary surface: ecosystem-chat.html
Operational projection: governed-transitions.html
Site mode: GOVERNED_GATEWAY_WITH_LOCAL_FALLBACK
Gateway implementation: installed in StegVerse-org/LLM-adapter
Custody implementation: installed in master-records/orchestration
Public deployments and authenticated round trip: verification pending
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

Configured gateway routes:

```text
POST /api/ecosystem-chat
GET  /health
GET  /api/transitions/{transition_id}
```

## Browser request progression

```text
create canonical SITE_INPUT identity
-> submit text request plus transition identity
-> require transition_id/run_id/event_id/origin_manifest_id equality
-> receive bounded response lifecycle
-> display gateway intake receipt
-> display final response receipt
-> display SQLite persistence posture
-> display restart durability posture
-> display custody queue state
-> display Master-Records status/reference when independently returned
-> display reconstruction posture
```

For a normal non-mutating request, the backend may return:

```text
task_status = completed_bounded_response
lifecycle_state = COMPLETED
admissibility_result = ALLOW
commit_time_validity = VALID
final_receipt_id = final-response-receipt:sha256:...
sqlite_persisted = true
storage_durable_across_restarts = true | false
master_record_status = PENDING | RECORDED
custody_submission.state = PENDING | RETRY | RECORDED
reconstruction_status = PARTIAL | PASS
```

For restricted administration or credential-shaped input:

```text
task_status = pending_authority
lifecycle_state = VERIFICATION_REQUIRED
final_receipt_id = null
custody_submission = null
no execution or mutation
```

On timeout, non-OK response, malformed response, or identity mismatch, the browser fails closed to deterministic local classification.

## Public health signal

The gateway status panel distinguishes:

```text
LIVE · BOUNDED
LOCAL FALLBACK
UNAVAILABLE
```

When healthy it now reports:

```text
native executor posture
bounded response pipeline
SQLite transition store availability
whether storage survives restarts
whether Master-Records submission is configured
```

It explicitly states that local SQLite persistence is not Master-Records custody.

## Gateway implementation

`StegVerse-org/LLM-adapter` now contains:

```text
llm_adapter/ecosystem_chat_gateway.py
llm_adapter/governed_chat_pipeline.py
llm_adapter/transition_store.py
llm_adapter/master_records_client.py
llm_adapter/custody_worker.py
tests/test_ecosystem_chat_gateway.py
tests/test_governed_chat_pipeline.py
tests/test_transition_store_and_custody.py
render.yaml
```

## Master-Records receiving implementation

`master-records/orchestration` now contains:

```text
services/master_records_custody_api.py
tests/test_master_records_custody_api.py
requirements-service.txt
render-custody.yaml
```

The custody service requires authentication, preserves transition/run/final-receipt identity, issues an HMAC-bound custody receipt, and returns `RECORDED` only after its reconstruction checks pass.

## Storage posture

Both supplied free Render blueprints currently use `/tmp` SQLite files and declare restart durability as false. This supports end-to-end contract validation but is not durable retention across redeploys.

Before production custody claims, both services require persistent disks or managed storage.

## Non-negotiable boundary

```text
Site does not execute or mutate repositories.
Gateway intake receipt != final response receipt.
Final response receipt != Master-Records custody.
SQLite persistence != Master-Records custody.
Custody submission != custody admission.
RECORDED requires the authenticated custody service receipt.
Native executor activation != blanket per-transition authority.
Projection != source authority.
```

## Validation surface

The existing Site validation now checks:

```text
gateway configuration and HTTPS endpoints
identity-preserving request/response markers
timeout and local fallback behavior
lifecycle and final receipt display
SQLite persistence and restart-durability markers
custody queue and Master-Records reference display
public gateway health module
non-overclaim authority boundaries
```

No workflow was added.

## Next task

```text
1. Verify LLM-adapter gateway, pipeline, storage, and custody-client tests.
2. Verify orchestration custody API tests.
3. Deploy both Render blueprints and configure shared custody credentials.
4. Verify gateway /health and custody /health.
5. Submit one public Ecosystem Chat request and observe COMPLETED -> PENDING -> RECORDED.
6. Move both SQLite databases to persistent disks or managed storage.
7. Export live custody state into governed-transitions.html.
8. Add provider-backed responses only after provider policy, cost, quota, and credential boundaries are active.
```

## Release posture

The browser, gateway, persistence, custody queue, authenticated receiving service, and lifecycle display are implemented. Public deployment, current-main validation, authenticated end-to-end evidence, and persistent storage remain pending. No release tag is authorized.

## Archive readiness

This handoff contains the current implementation, persistence/custody distinction, deployment boundaries, and continuation order. Earlier conversation context is not required.
