# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: fully functional governed Ecosystem Chat request-response, provider, custody, comparison, and cross-entry usage path
Primary surface: ecosystem-chat.html
Usage and role surface: ecosystem-usage.html
Comparison surface: ecosystem-comparison.html
Operational projection: governed-transitions.html
Workflow target: exactly two operational workflows
Result: destination usage endpoint implementation installed; Site validation is advancing; same-origin deployment, custody, and live activation evidence remain pending
```

## Active workflows

```text
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

The iOS mirror remains `iosnoperiod/github/workflows/validate.yml`. No workflow was added.

## Installed usage surface

```text
ecosystem-usage.html
assets/ecosystem-usage-auth-client.js
assets/ecosystem-usage-ledger.js
data/entry-point-roles.json
data/usage-session-fixture.json
data/ecosystem-usage-config.json
data/ecosystem-usage-live-contract.json
scripts/check_ecosystem_usage_auth_contract.py
scripts/check_ecosystem_usage_ledger.py
```

The surface preserves session identity across entry points, deduplicates by `metric_owner + measurement_id`, preserves evidence classes, prepends usage before transitions, supports session lookup, JSON export, and receipt navigation.

Current transport posture:

```text
contract status: PREPARED_NOT_DEPLOYED
route template: /api/usage/sessions/{session_id}
authentication mode: same_origin_session
same-origin browser credentials: allowed
cross-origin browser credentials: prohibited
Site-configured bearer/query/local-storage tokens: prohibited
live_transport.enabled: false
usage_api_base: null
activation prerequisite: AUTHORIZED_DEPLOYED_ENDPOINT
```

Integrity failures remain fail-closed. Network unavailability alone may use bounded local or configured-fixture fallback.

## Destination endpoint handoff

```text
data/llm-adapter-usage-endpoint-handoff.json
scripts/check_llm_adapter_usage_endpoint_handoff.py
data/llm-adapter-usage-endpoint-conformance.json
scripts/check_llm_adapter_usage_endpoint_conformance.py
```

Current destination state:

```text
state: DESTINATION_IMPLEMENTATION_INSTALLED_VALIDATION_PENDING
blocker: DESTINATION_VALIDATION_AND_DEPLOYMENT_EVIDENCE_PENDING
```

The current destination handoff exists at:

```text
StegVerse-org/LLM-adapter/LLM_ADAPTER_MIRROR_HANDOFF.md
```

Installed destination components:

```text
llm_adapter/usage_session_api.py
scripts/verify_usage_session_api.py
tests/test_usage_session_api.py
```

Installed routes:

```text
POST /api/usage/sessions
GET  /api/usage/sessions/{session_id}
```

The retrieval contract requires same-origin session identity, `stegverse.usage.session.v1`, `LIVE_USAGE_API`, requested session preservation, a retrieval receipt, producer and policy identity, `authority_granted=false`, and `custody_recorded=false`.

Machine submission is separately authenticated. Site does not receive, render, store, or configure the submission credential.

## Latest Site validation handling

```text
Workflow: Site Bootstrap Validate
Run: 29228087741
Branch: main
Commit: 6289a4be10a7aaaa5a0524080b3fb88e3851144a
Job: bootstrap-validate
Failure class: destination handoff validator state drift
Passing steps:
- workflow inventory
- two-operational-workflow guard
- navigation validation
- authenticated usage contract
- usage ledger validation
Failed command:
python scripts/check_llm_adapter_usage_endpoint_handoff.py
Artifact: site-application-validation-result
Artifact digest: sha256:58181fedd142fc9a87a5edb00282c03895a98d615b8b7f912e319f08813823a8
Failure output: LLM_ADAPTER_USAGE_HANDOFF_FAIL: handoff must remain blocked until destination authority exists
```

The data packet had correctly advanced from `AWAITING_DESTINATION_HANDOFF_AUTHORITY` to `DESTINATION_IMPLEMENTATION_INSTALLED_VALIDATION_PENDING`, but the validator still required only the former state.

Bounded repair:

```text
File: scripts/check_llm_adapter_usage_endpoint_handoff.py
Commit: 7448cbec119023fe447a2560e1680d7b352f830f
```

The validator now:

```text
accepts only the two explicitly governed handoff states
preserves all route, receipt, failure, evidence, and authority checks
requires exact destination implementation, verifier, test, and handoff paths
requires the combined gateway route and workflow registration to be true
requires unobserved validation, deployment, and conformance evidence to remain false
requires DESTINATION_VALIDATION_AND_DEPLOYMENT_EVIDENCE_PENDING while those proofs are absent
```

No check was removed. No deployment, credential configuration, transport activation, release, merge, or tag occurred.

## Destination validation posture

```text
destination handoff: observed
destination endpoint implementation: observed
destination verifier and tests: installed
destination workflow registration: installed
current-main green validation: not observed
same-origin authenticated deployment: not observed
Site conformance against deployed endpoint: not observed
Master-Records custody: not observed
reconstructability PASS: not observed
```

Source implementation is not represented as deployed.

## Activation evidence and preactivation checkpoint

```text
data/usage-endpoint-activation-evidence.json
scripts/check_usage_endpoint_activation_evidence.py
data/usage-endpoint-preactivation-checkpoint.json
scripts/check_usage_endpoint_preactivation_checkpoint.py
```

Activation remains blocked until all required evidence is verified:

```text
destination handoff authority
destination endpoint tests
same-origin authenticated deployment
sample response conformance
retrieval receipt validation
no browser secret surface
Site current-main validation
Master-Records custody
reconstructability
```

Current checkpoint:

```text
SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED
usage_api_base: null
live_transport_enabled: false
contract_status: PREPARED_NOT_DEPLOYED
```

## Current-main validation evidence path

```text
data/site-current-main-validation-evidence.json
scripts/check_site_current_main_validation_evidence.py
scripts/write_site_current_main_validation_receipt.py
scripts/check_site_current_main_validation_receipt_writer.py
scripts/write_site_validation_artifact_manifest.py
scripts/check_site_validation_artifact_manifest_writer.py
```

The existing validation workflow produces:

```text
site_application_validation.result.json
site_current_main_validation.receipt.json
site_current_main_validation.manifest.json
```

Successful current-main artifact evidence has not yet been observed.

## Comparison and navigation

```text
ecosystem-comparison.html
assets/ecosystem-comparison.js
data/llm-route-comparison-fixture.json
assets/ecosystem-chat-hps.js
scripts/check_ecosystem_comparison.py
scripts/check_ecosystem_chat_navigation.py
```

The comparison remains `CONFIGURED_FIXTURE`, uses `external_recursive - stegverse_governed`, and does not claim live measurement, authority, or admissibility.

## Canonical validation surface

```text
python scripts/check_ecosystem_chat_application.py
  -> navigation
  -> authenticated usage contract
  -> usage ledger
  -> LLM-adapter destination handoff
  -> endpoint conformance
  -> activation evidence
  -> preactivation checkpoint
  -> current-main evidence record
  -> validation receipt writer contract
  -> validation artifact manifest writer contract
  -> comparison
  -> governed transition and remaining Site checks
```

## Authority boundary

```text
Site display != execution.
Usage retrieval != authority.
Usage display != admissibility.
Prepared or loaded client != deployed endpoint.
Destination handoff packet != destination authority.
Source implementation != live deployment.
Conformance fixture pass != deployment authority.
Validation receipt != deployment evidence.
Workflow artifact != Master-Records custody.
Configured fixture != live measurement.
Retrieval receipt != Master-Records custody.
RECORDED requires authenticated custody evidence and reconstructability PASS.
Site does not execute or mutate external repositories.
No release tag is authorized.
```

## Remaining work

```text
StegVerse-Labs/Site
  -> observe the successor current-main validation artifact set after commit 7448cbec119023fe447a2560e1680d7b352f830f
  -> repair only the next exact failing command without removing checks
  -> verify result, receipt, and manifest hashes
  -> bind verified Site evidence into the activation ledger
  -> run conformance against an authorized same-origin deployment
  -> enable live transport only after every activation prerequisite passes
  -> replace CONFIGURED_FIXTURE only after live paired results are observed

StegVerse-org/LLM-adapter
  -> observe current-main validation containing usage-session checks
  -> integrate automatic provider-owned usage submission
  -> deploy combined gateway with mutation disabled
  -> establish authorized same-origin gateway/proxy
  -> emit retrieval and provider usage receipts

master-records/orchestration
  -> custody usage and comparison events
  -> provide authenticated custody receipt
  -> provide reconstructability PASS evidence

StegVerse-org/core-node-runtime-demo
  -> automatic runtime usage emission
  -> live governed route result submission
```

## Next task

```text
1. Observe the successor Site Bootstrap Validate run after commit 7448cbec119023fe447a2560e1680d7b352f830f.
2. Confirm the destination handoff validator passes.
3. Repair only the next failing command without removing existing checks.
4. Verify the first successful current-main Site result, receipt, and manifest artifact set.
5. Observe the destination validate workflow containing usage-session verification.
6. Deploy only through an authorized same-origin topology.
7. Run the Site endpoint conformance suite against the deployed route.
8. Do not enable live transport until all activation evidence is VERIFIED.
9. Do not claim RECORDED until authenticated Master-Records custody and reconstructability PASS are observed.
```

## Release posture

The authenticated retrieval surface remains `PREPARED_NOT_DEPLOYED`. Destination source implementation is installed, but current-main validation, authorized same-origin deployment, live response conformance, authenticated custody, reconstructability, and public route verification remain activation gates. No deployment, credential configuration, transport activation, release, merge, or tag is authorized by this handoff.

## Archive readiness

This handoff preserves the current provider, gateway, custody, usage, comparison, navigation, endpoint implementation, validation, conformance, activation, authority-boundary, failure repair, and continuation state. Earlier conversation context is not required.
