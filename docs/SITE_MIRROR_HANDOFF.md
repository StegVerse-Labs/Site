# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: fully functional governed Ecosystem Chat request-response, provider, and custody path
Phase: governed-provider-status-client-installed
Primary surface: ecosystem-chat.html
Operational projection: governed-transitions.html
Site mode: GOVERNED_GATEWAY_WITH_LOCAL_FALLBACK
Gateway implementation: installed in StegVerse-org/LLM-adapter
Custody implementation: installed in master-records/orchestration
Public deployments and authenticated round trip: verification pending
Workflow target: exactly two operational workflows
Result: CROSS_REPOSITORY_IMPLEMENTATION_INSTALLED_LIVE_VALIDATION_PENDING
```

## Active workflows

```text
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

No workflow was added.

## Ecosystem Chat governed request path

```text
create canonical SITE_INPUT identity
-> submit to governed gateway
-> validate identity-preserving response
-> display governed provider posture or deterministic fallback
-> display final response receipt
-> display SQLite persistence and restart durability
-> display custody queue and Master-Records state
-> inspect the same transition in governed-transitions.html
```

## Governed provider display

Updated:

```text
assets/ecosystem-chat-transition-identity.js
assets/ecosystem-chat-gateway-health.js
scripts/check_ecosystem_chat_gateway_activation.py
```

For every gateway response, the Site displays:

```text
response source = GOVERNED_PROVIDER_USED | DETERMINISTIC_FALLBACK
provider status
provider name
provider model
provider response receipt
estimated provider cost
provider output authority = false
```

The Site rejects any response claiming `provider_output_is_authority != false`.

The health panel displays whether the provider broker is enabled under bounded policy or disabled with deterministic fallback. It also requires `provider_failure_falls_back = true`.

Provider credentials are never sent to or rendered by Site.

## Provider fail-closed posture

The gateway may fall back deterministically when the provider is:

```text
disabled
misconfigured
outside the hostname allowlist
over quota
over request or daily cost boundary
over input/output size boundary
unavailable
contract-invalid
identity-mismatched
```

Fallback does not claim a provider receipt and does not change transition authority.

## Live custody observatory

Installed:

```text
assets/governed-transitions-live-custody.js
governed-transitions.html
scripts/check_governed_transition_observatory.py
```

The observatory resolves `?transition_id=<canonical-transition-id>` or the latest successful browser transition and displays lifecycle, final receipt, custody queue, custody receipt, Master-Records reference, and reconstruction posture.

A `RECORDED` result is rejected unless `master_record_ref` exists and `reconstruction_status = PASS`.

## Current backend surfaces

`StegVerse-org/LLM-adapter`:

```text
llm_adapter/ecosystem_chat_gateway.py
llm_adapter/governed_provider.py
llm_adapter/governed_chat_pipeline.py
llm_adapter/transition_store.py
llm_adapter/master_records_client.py
llm_adapter/custody_worker.py
render.yaml
render-production.yaml
```

`master-records/orchestration`:

```text
services/master_records_custody_api.py
render-custody.yaml
render-custody-production.yaml
tools/verify_live_ecosystem_chat_custody_roundtrip.py
```

## Non-negotiable boundary

```text
Site does not execute or mutate repositories.
Provider output != authority.
Provider receipt != final response receipt.
Provider response != admissibility.
Gateway intake receipt != final response receipt.
Final response receipt != Master-Records custody.
SQLite persistence != Master-Records custody.
RECORDED requires the authenticated custody service receipt.
Live projection != source authority.
```

## Validation surface

The existing Site validation checks:

```text
gateway and health HTTPS endpoints
identity-preserving request/response markers
provider status, receipt, cost, and deterministic fallback markers
provider authority and credential-isolation boundaries
lifecycle and final receipt display
SQLite persistence and custody display
live observatory lookup and RECORDED consistency
```

## Observed validation failures and bounded repairs

```text
Workflow: Site Bootstrap Validate
Run: 29179673207
Commit: c19e0015c24ba2f5ccd39eda6c97477d78e2a92a
First failing step: Validate application
Failing command: python scripts/check_site_media_pipeline_mirror.py
Failure class: stale preview-only handoff assertion
Repair commit: 181668077ecd3e8d686374758de051f7ba76c07f
Artifact: site-application-validation-result
Artifact ID: 8256003741
Artifact digest: sha256:1bf661d6438c63a016c868ac383ceeb61a03b80d8ba966cb21b5edd0d4885852

Workflow: Site Task Runner
Run: 29191451576
Commit: 1d64d9c16b91cea0b9fbb56874193caf491d30ff
First failing step: Run declared Site task
Failing validator: python scripts/check_ecosystem_chat_boundary.py
Failure class: deterministic substring-count bug in hero button validation
Repair commit: 62d6c88df9e126978b477ac14913a9ef4dc375c0
Artifact: site-task-diagnostic-29191451576-1
Artifact ID: 8259633062
Artifact digest: sha256:8dd3daca1a24e0f534fd7279b97c85573c59b1fb4af0bb087a8891c37794009a

Workflow: Site Task Runner
Run: 29192461329
Commit: 82d485c224ba9590aa05c53ff4b008b26978095f
First failing step: Run declared Site task
Failing validator: python scripts/check_ecosystem_chat_boundary.py
Failure class: stale continuation-panel identifier assertion (`destinationHref`)
Observed implementation: `item.destination` assigned through `link.href`
Repair commit: ba8e68d4906654698a736c02475077d5bef40921
Artifact: site-task-diagnostic-29192461329-1
Artifact ID: 8259922135
Artifact digest: sha256:f3e3daa6beedf5da6895c55739ddaa8297b01464f1afdd757e47b20b95f624ad
Authority effect: NONE
State change authorized by repair: false
```

The boundary checker now counts the two `sv-btn-primary` elements for the hero entry and chat submit, independently verifies the two hero links, and validates the continuation implementation against its current `item.destination` and `link.href` behavior rather than a removed local identifier.

Verification remains pending on commit `ba8e68d4906654698a736c02475077d5bef40921` or a documented successor.

## Next task

```text
1. Verify current-main Site and LLM-adapter tests, including Site Task Runner and Site Bootstrap Validate on commit ba8e68d4906654698a736c02475077d5bef40921 or later.
2. Preserve the passing Site validation receipt before deployment work.
3. Deploy gateway and custody production blueprints only with required deployment authority.
4. Configure shared custody credentials only through authorized secret-management paths.
5. Optionally configure the provider broker with endpoint, hostname allowlist, token, model, quota, and cost ceilings.
6. Verify one public response reports provider USED or explicit deterministic fallback.
7. Verify the same transition reaches RECORDED custody.
8. Run the orchestration live round-trip verifier before public activation claims.
```

## Release posture

Provider policy and display, deterministic fallback, persistent storage profiles, custody admission, and live observability are implemented. Public deployment, secrets, green current-main evidence, and an observed identity-preserving RECORDED transition remain pending. No release tag is authorized.

## Archive readiness

This handoff contains the current provider, gateway, custody, Site display, latest bounded validation repairs, preserved authority boundaries, and continuation state. Earlier conversation context is not required.
