# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: fully functional governed Ecosystem Chat request-response path
Phase: live-gateway-client-integration-installed
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

## Ecosystem Chat live gateway client

Installed or updated:

```text
data/ecosystem-chat-gateway.json
assets/ecosystem-chat-transition-identity.js
scripts/check_ecosystem_chat_gateway_activation.py
scripts/check_ecosystem_chat_receipt_envelopes.py
```

Configured service:

```text
POST https://stegverse-ecosystem-chat-gateway.onrender.com/api/ecosystem-chat
GET  https://stegverse-ecosystem-chat-gateway.onrender.com/health
```

Browser behavior:

```text
create canonical SITE_INPUT identity
-> load validated gateway configuration
-> submit text request plus transition identity
-> require transition_id/run_id/event_id/origin_manifest_id round-trip equality
-> display bounded gateway response and GATEWAY_INTAKE_RECEIPT
-> on timeout, non-OK response, malformed response, or identity mismatch: fail closed to local classification
```

The fallback does not claim a gateway receipt, final receipt, execution, admissibility, custody, or reconstruction.

## Deployable gateway implementation

Canonical backend repository:

```text
StegVerse-org/LLM-adapter
```

Installed there:

```text
llm_adapter/ecosystem_chat_gateway.py
tests/test_ecosystem_chat_gateway.py
render.yaml
pyproject.toml
```

The service provides validation, CORS, rate limiting, restricted-request handling, canonical identity preservation, bounded response generation, gateway intake receipts, and `/health`.

## Executor and observatory state

The governed transition observatory and receipted executor projection remain installed:

```text
governed-transitions.html
data/governed-transition-index.json
data/governed-transition-index-import-status.json
data/governed-executor-status.json
```

Native executor eligibility and a gateway request are separate boundaries. Executor activation does not grant per-transition execution authority.

## Non-negotiable boundary

```text
Site does not execute or mutate repositories.
Gateway intake receipt != final transition receipt.
Gateway response != admissibility.
Gateway routing != execution authority.
Native executor activation != per-transition authority.
Final receipt != Master-Records custody.
Projection != source authority.
```

## Validation surface

The existing receipt-envelope validation now also checks:

```text
gateway config schema and HTTPS endpoints
authority boundary flags
identity-preserving client markers
timeout and local fallback behavior
gateway receipt/final receipt distinction
```

No workflow was added.

## Remaining files/modules and destinations

```text
StegVerse-org/LLM-adapter:
- current-main gateway test evidence
- successful Render deployment
- GET /health public verification

StegVerse-Labs/Site:
- current-main validation evidence
- live browser POST round-trip evidence
- public status indicator for gateway health

Cross-repository runtime:
- transport accepted gateway candidate into hybrid-collab-bridge
- return delegation/SPE/orchestration lifecycle updates to the same chat transition
- return final receipt and Master-Records state when independently issued

Downstream after validation:
- StegVerse-Labs/admissibility-wiki
- GCAT-BCAT-Engine/Publisher
- StegVerse-002/stegguardian-wiki
- StegVerse-Labs/Sit
```

## Next task

```text
1. Verify LLM-adapter tests including the FastAPI gateway suite.
2. Deploy render.yaml and verify /health.
3. Submit one public Ecosystem Chat request and verify identity-preserving response.
4. Install gateway-to-hybrid-collab-bridge transport.
5. Stream lifecycle and final receipt updates back to the same transition.
```

## Release posture

The browser and deployable backend implementations are connected by contract. The system must not be called fully live until service deployment, health verification, public POST round-trip, and downstream bridge transport are observed.

## Archive readiness

This handoff contains the current implementation, deployment boundary, validation rules, and continuation order. Earlier conversation context is not required.
