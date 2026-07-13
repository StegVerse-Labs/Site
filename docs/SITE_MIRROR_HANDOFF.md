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
Result: destination usage endpoint implementation installed; validation, same-origin deployment, custody, and live activation evidence pending
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

Current Site transport posture remains:

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

The former `DESTINATION_HANDOFF_MISSING` blocker is resolved. A current destination handoff now exists at:

```text
StegVerse-org/LLM-adapter/LLM_ADAPTER_MIRROR_HANDOFF.md
```

The destination now contains:

```text
llm_adapter/usage_session_api.py
scripts/verify_usage_session_api.py
tests/test_usage_session_api.py
```

and mounts the route into `llm_adapter.combined_gateway`.

Installed destination routes:

```text
POST /api/usage/sessions
GET  /api/usage/sessions/{session_id}
```

The retrieval implementation matches the prepared Site contract:

```text
same-origin session cookie or matching X-SteGVerse-Session identity
stegverse.usage.session.v1
LIVE_USAGE_API
requested session identity preserved
mandatory retrieval receipt
retrieved_at present
producer_identity present
policy_reference present
authority_granted=false
custody_recorded=false
```

Machine submission is separately authenticated. The Site does not receive, render, store, or configure the submission credential.

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

The implementation is not represented as deployed merely because the route exists in source.

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

Current checkpoint remains:

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

The comparison remains `CONFIGURED_FIXTURE`, uses `external_recursive - stegverse_governed`, and does not claim live measurement, authority, or admissibility. Ecosystem Chat exposes direct navigation to the usage and comparison pages.

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
  -> observe a successful current-main workflow artifact set
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
1. Observe the destination validate workflow containing usage-session verification.
2. Repair the first failing step without removing existing checks.
3. Observe the next current-main Site validation artifact set.
4. Verify all Site artifact hashes and run identities.
5. Deploy only through an authorized same-origin topology.
6. Run the Site endpoint conformance suite against the deployed route.
7. Do not enable live transport until all activation evidence is VERIFIED.
8. Do not claim RECORDED until authenticated Master-Records custody and reconstructability PASS are observed.
```

## Release posture

The authenticated retrieval surface remains `PREPARED_NOT_DEPLOYED`. Destination source implementation is installed, but current-main validation, authorized same-origin deployment, live response conformance, authenticated custody, reconstructability, and public route verification remain activation gates. No deployment, credential configuration, transport activation, release, merge, or tag is authorized by this handoff.

## Archive readiness

This handoff preserves the current provider, gateway, custody, usage, comparison, navigation, endpoint implementation, validation, conformance, activation, authority-boundary, and continuation state. Earlier conversation context is not required.