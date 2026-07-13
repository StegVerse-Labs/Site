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
Result: Site preparation complete; live activation and external custody evidence pending
```

## Active workflows

```text
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

The iOS no-leading-dot mirror remains:

```text
iosnoperiod/github/workflows/validate.yml
```

No workflow was added.

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

The surface preserves one session identity across entry points, deduplicates by `metric_owner + measurement_id`, preserves evidence classes, prepends usage before each transition, supports session lookup, JSON export, and receipt navigation.

Current transport posture:

```text
contract status: PREPARED_NOT_DEPLOYED
route template: /api/usage/sessions/{session_id}
authentication mode: same_origin_session
same-origin browser credentials: allowed
cross-origin browser credentials: prohibited
Site-configured bearer/query/local-storage tokens: prohibited
request timeout: 10 seconds
cache posture: no-store
live_transport.enabled: false
usage_api_base: null
activation prerequisite: AUTHORIZED_DEPLOYED_ENDPOINT
```

Failure classes remain separated:

```text
network unavailable -> bounded local or configured-fixture fallback may occur
400 / 401 / 403 / 409 / 422 -> fail closed
session identity mismatch -> fail closed
missing retrieval receipt -> fail closed
contract-invalid output -> fail closed
```

## Destination handoff and conformance

```text
data/llm-adapter-usage-endpoint-handoff.json
scripts/check_llm_adapter_usage_endpoint_handoff.py
data/llm-adapter-usage-endpoint-conformance.json
scripts/check_llm_adapter_usage_endpoint_conformance.py
```

Required destination capability:

```text
GET /api/usage/sessions/{session_id}
same-origin session authentication
stegverse.usage.session.v1
LIVE_USAGE_API
mandatory retrieval receipt
authority_granted=false
custody_recorded=false
```

Conformance cases:

```text
valid_live_usage_response -> ALLOW
session_identity_drift -> DENY:IDENTITY_MISMATCH
missing_retrieval_receipt -> DENY:RECEIPT_MISSING
authority_overreach -> DENY:AUTHORITY_OVERREACH
custody_overreach -> DENY:CUSTODY_OVERREACH
invalid_evidence_class -> DENY:EVIDENCE_CLASS_INVALID
unavailable_value_violation -> DENY:UNAVAILABLE_VALUE_INVALID
```

Current destination state:

```text
state: AWAITING_DESTINATION_HANDOFF_AUTHORITY
blocker: DESTINATION_HANDOFF_MISSING
reason: no current *_MIRROR_HANDOFF.md is present in StegVerse-org/LLM-adapter
```

Site does not mutate the destination repository, configure credentials, enable transport, or claim endpoint availability while this blocker remains.

## Activation evidence and preactivation checkpoint

```text
data/usage-endpoint-activation-evidence.json
scripts/check_usage_endpoint_activation_evidence.py
data/usage-endpoint-preactivation-checkpoint.json
scripts/check_usage_endpoint_preactivation_checkpoint.py
```

Activation evidence remains `BLOCKED` until every requirement is `VERIFIED`:

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

The existing validation workflow now produces and uploads one verifiable artifact set:

```text
site_application_validation.result.json
site_current_main_validation.receipt.json
site_current_main_validation.manifest.json
```

The receipt binds the canonical result to repository, commit SHA, ref, event, workflow, job, run ID, run attempt, timestamp, result hash, and passed-command count.

The manifest binds the result and receipt by SHA-256 and declares a deterministic verification order. Artifact integrity does not grant deployment, endpoint-live, release, custody, admissibility, or RECORDED authority.

Current evidence posture:

```text
receipt generation: installed
artifact manifest generation: installed
canonical workflow: updated
iOS workflow mirror: synchronized
workflow permissions: contents read
successful current-main artifact set: not yet observed
```

## Validation repair completed

The media mirror validator no longer depends on the obsolete transient marker:

```text
Site mode: GOVERNED_GATEWAY_WITH_LOCAL_FALLBACK
```

It now validates stable handoff obligations:

```text
current governed Ecosystem Chat goal
implementation installed / live validation pending
exactly two operational workflows
non-execution authority boundary
```

Repair commit:

```text
6b8c0b0f887bdb34b3e4f49a8dd1b99f58de3796
```

This repair is bounded to validator compatibility and does not change deployment or release state.

## Comparison and navigation

```text
ecosystem-comparison.html
assets/ecosystem-comparison.js
data/llm-route-comparison-fixture.json
assets/ecosystem-chat-hps.js
scripts/check_ecosystem_comparison.py
scripts/check_ecosystem_chat_navigation.py
```

The comparison remains `CONFIGURED_FIXTURE`, uses the canonical delta `external_recursive - stegverse_governed`, and does not claim live measurement, authority, or admissibility.

Ecosystem Chat exposes direct navigation to:

```text
ecosystem-usage.html
 ecosystem-comparison.html
```

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

Predeployment validation remains separate from postdeployment public-route observation.

## Authority boundary

```text
Site display != execution.
Usage retrieval != authority.
Usage display != admissibility.
Prepared or loaded client != deployed endpoint.
Destination handoff packet != destination authority.
Conformance fixture pass != deployment authority.
Validation receipt != deployment evidence.
Validation manifest != release authority.
Workflow artifact != Master-Records custody.
Configured fixture != live measurement.
Provider receipt != final response receipt.
Final response receipt != Master-Records custody.
RECORDED requires authenticated custody evidence and reconstructability PASS.
Site does not execute or mutate external repositories.
No release tag is authorized.
```

## Latest bounded task completion

```text
Task: make successful Site validation artifacts independently verifiable
Manifest writer commit: 01abfb031faf2dfcf91eea5377776a96950cba15
Writer validator commit: 281fb2f9bb66d61c10d91051adb025ef31a38a84
Canonical integration commit: 729e9b757c4c83d64ea9213884bc72410141c736
Workflow commit: ce83bd594c0f61c9f616683d1fd926476addcb98
Workflow mirror commit: b4a5adb0cc7f0a3cf391a7f211273b458ab24ce0
State: ARTIFACT_MANIFEST_READY; current-main run observation pending
```

## Remaining work

```text
StegVerse-Labs/Site
  -> observe a successful current-main workflow artifact set
  -> verify result, receipt, and manifest hashes
  -> bind verified Site evidence into the activation ledger
  -> configure an authorized deployed endpoint only after all external prerequisites pass
  -> replace CONFIGURED_FIXTURE only after live paired results are observed

StegVerse-org/LLM-adapter
  -> establish or identify current *_MIRROR_HANDOFF.md
  -> authorize authenticated session-usage endpoint work
  -> implement and test endpoint against Site conformance suite
  -> deploy same-origin authentication path
  -> emit provider usage and retrieval receipts

StegVerse-org/core-node-runtime-demo
  -> automatic runtime usage emission
  -> live governed route endpoint

master-records
  -> custody usage and comparison events
  -> deduplication and reconstruction indexes
  -> authenticated custody receipt
  -> reconstructability PASS evidence
```

## Next task

```text
1. Observe the next current-main Site validation run.
2. Download or inspect site-application-validation-result.
3. Verify all three artifact hashes and run identities.
4. Advance site_current_main_validation to VERIFIED only with concrete evidence.
5. Recheck StegVerse-org/LLM-adapter for a current mirror handoff.
6. Do not mutate the destination until that handoff explicitly authorizes endpoint work.
7. Do not enable live transport until every activation-ledger requirement is VERIFIED.
8. Do not claim RECORDED until authenticated Master-Records custody and reconstructability PASS are observed.
```

## Release posture

The authenticated retrieval surface remains `PREPARED_NOT_DEPLOYED`, `CLIENT_LOADED_TRANSPORT_DISABLED`, `AWAITING_DESTINATION_HANDOFF_AUTHORITY`, and `CONFORMANCE_READY_AWAITING_DESTINATION_AUTHORITY`. Site validation receipt and manifest generation are installed, but no successful current-main artifact set has yet been observed. Live endpoint transport, live paired results, authenticated custody, reconstructability, public endpoint verification, and an identity-preserving RECORDED transition remain activation gates. No deployment, release, merge, credential configuration, destination mutation, or tag is authorized by this handoff.

## Archive readiness

This handoff preserves the current provider, gateway, custody, usage, comparison, navigation, conformance, activation, validation-receipt, artifact-manifest, authority-boundary, and continuation state. Earlier conversation context is not required.
