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

The iOS mirror remains `iosnoperiod/github/workflows/validate.yml`. No workflow was added.

## Installed usage and destination surfaces

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

data/llm-adapter-usage-endpoint-handoff.json
scripts/check_llm_adapter_usage_endpoint_handoff.py
data/llm-adapter-usage-endpoint-conformance.json
scripts/check_llm_adapter_usage_endpoint_conformance.py
```

Current Site transport posture:

```text
contract_status: PREPARED_NOT_DEPLOYED
route: GET /api/usage/sessions/{session_id}
authentication: same_origin_session
same-origin browser credentials: allowed
cross-origin browser credentials: prohibited
Site bearer/query/local-storage token configuration: prohibited
live_transport.enabled: false
usage_api_base: null
```

Current destination state:

```text
repository: StegVerse-org/LLM-adapter
handoff: LLM_ADAPTER_MIRROR_HANDOFF.md
state: DESTINATION_IMPLEMENTATION_INSTALLED_VALIDATION_PENDING
blocker: DESTINATION_VALIDATION_AND_DEPLOYMENT_EVIDENCE_PENDING
implementation: llm_adapter/usage_session_api.py
verifier: scripts/verify_usage_session_api.py
test: tests/test_usage_session_api.py
routes:
- POST /api/usage/sessions
- GET /api/usage/sessions/{session_id}
```

The retrieval contract requires same-origin session identity, `stegverse.usage.session.v1`, `LIVE_USAGE_API`, requested session preservation, a mandatory retrieval receipt, producer and policy identity, `authority_granted=false`, and `custody_recorded=false`.

Machine submission is separately authenticated. Site does not receive, render, store, or configure the submission credential.

## Workflow consolidation

Bootstrap enforces:

```text
python scripts/write_site_workflow_inventory.py
python scripts/check_site_workflow_inventory.py
python scripts/check_ecosystem_chat_application.py
```

The operational workflow guard requires exactly:

```text
validate.yml
site-task-runner.yml
```

Triggerless and jobless placeholders remain cleanup items and do not count as operational entry points.

## Current-main validation progression

### Run 29228087741

```text
Commit: 6289a4be10a7aaaa5a0524080b3fb88e3851144a
Result: FAILED
Passing boundaries:
- workflow inventory
- two-operational-workflow guard
- navigation
- authenticated usage contract
- usage ledger
Failed command: scripts/check_llm_adapter_usage_endpoint_handoff.py
Failure: validator required the obsolete AWAITING_DESTINATION_HANDOFF_AUTHORITY state
Artifact: site-application-validation-result
Artifact digest: sha256:58181fedd142fc9a87a5edb00282c03895a98d615b8b7f912e319f08813823a8
```

Bounded repair:

```text
Commit: 7448cbec119023fe447a2560e1680d7b352f830f
File: scripts/check_llm_adapter_usage_endpoint_handoff.py
```

The repaired validator accepts only the two governed handoff states and preserves every route, receipt, evidence, failure, and authority check. For the installed destination state it additionally requires exact implementation paths, route mounting, workflow registration, unpromoted deployment evidence, and the pending validation/deployment blocker.

### Run 29228204514

```text
Commit: 7448cbec119023fe447a2560e1680d7b352f830f
Result: FAILED after substantial validation advancement
Destination handoff validator: PASSED
Endpoint conformance: PASSED
Activation evidence contract: PASSED
Preactivation checkpoint: PASSED
Current-main evidence contract: PASSED
Receipt writer contract: PASSED
Artifact manifest writer contract: PASSED
Artifact bundle verifier contract: PASSED
Comparison and governed-transition checks: PASSED
AI-entry validation chain: PASSED
Failed command: scripts/check_site_media_pipeline_mirror.py
Failure: docs/SITE_MIRROR_HANDOFF.md missing exact compatibility marker
Required marker: Result: Site preparation complete; live activation and external custody evidence pending
Artifact: site-application-validation-result
Artifact digest: sha256:fba09520a8aae503980ceaf010815016de5d3af734920812bcc282f4ca7fc210
```

Bounded repair:

```text
This handoff now preserves the exact required compatibility marker without changing activation posture.
```

No validator was weakened. No deployment, credential configuration, live transport activation, release, merge, tag, custody admission, or authority expansion occurred.

### Run 29249185595

```text
Commit: de68f9c99d4e58f081732dbd9dfadced606891a5
Result: FAILED after all prior readiness repairs passed
Passing boundaries:
- site mirror orchestration
- navigation discovery
- mirror release readiness
- consolidated workflow validation
- mirror readiness
Failed command: scripts/check_site_mirror_task_completion.py
Failure: task-completion checker and status still referenced removed .github/workflows/site-mirror-readiness.yml
```

Bounded repair:

```text
Commits:
- b7c7523d4e6d48480cc3766a78012be3f0c35473
- ce611a66d6da46d11253a1d1d89fa8303728c3e4
Files:
- scripts/check_site_mirror_task_completion.py
- static/status/site-mirror-task-completion-status.json
```

The checker and status now bind validation to `.github/workflows/site-task-runner.yml`, task `mirror-readiness`, `scripts/run_site_task.py`, and `scripts/check_site_mirror_full_readiness.py`. The exactly-two-workflow architecture remains unchanged. Successor current-main verification is pending.

## Activation evidence and checkpoint

```text
data/usage-endpoint-activation-evidence.json
scripts/check_usage_endpoint_activation_evidence.py
data/usage-endpoint-preactivation-checkpoint.json
scripts/check_usage_endpoint_preactivation_checkpoint.py
```

Activation remains blocked until all are verified:

```text
destination current-main tests
same-origin authenticated deployment
sample response conformance
retrieval receipt validation
no browser secret surface
Site current-main validation
Master-Records custody
reconstructability PASS
```

Current checkpoint:

```text
SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED
usage_api_base: null
live_transport_enabled: false
contract_status: PREPARED_NOT_DEPLOYED
```

## Current-main evidence artifacts

The existing validation workflow produces:

```text
site_application_validation.result.json
site_current_main_validation.receipt.json
site_current_main_validation.manifest.json
```

Successful result, receipt, and manifest evidence has not yet been observed on one current-main run.

## Comparison posture

```text
ecosystem-comparison.html
assets/ecosystem-comparison.js
data/llm-route-comparison-fixture.json
assets/ecosystem-chat-hps.js
scripts/check_ecosystem_comparison.py
scripts/check_ecosystem_chat_navigation.py
```

The comparison remains `CONFIGURED_FIXTURE`, uses `external_recursive - stegverse_governed`, and does not claim live measurement, authority, or admissibility.

## Authority boundary

```text
Site display != execution.
Usage retrieval != authority.
Usage display != admissibility.
Prepared client != deployed endpoint.
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
  -> observe the successor current-main validation after commit ce611a66d6da46d11253a1d1d89fa8303728c3e4
  -> repair only the next exact failing command without removing checks
  -> verify one successful result, receipt, and manifest artifact set
  -> bind verified Site evidence into the activation ledger
  -> run conformance only against an authorized same-origin deployment
  -> enable live transport only after every activation prerequisite passes

StegVerse-org/LLM-adapter
  -> observe current-main validation containing usage-session verification
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
1. Observe the successor Site Task Runner/current-main validation after commit ce611a66d6da46d11253a1d1d89fa8303728c3e4.
2. Confirm scripts/check_site_mirror_task_completion.py passes.
3. Repair only the next failing command without removing existing checks.
4. Verify the first successful current-main result, receipt, and manifest artifact set.
5. Observe StegVerse-org/LLM-adapter current-main validation containing usage-session verification.
6. Deploy only through an explicitly authorized same-origin topology.
7. Run Site endpoint conformance against that deployed route.
8. Do not enable live transport until all activation evidence is VERIFIED.
9. Do not claim RECORDED until authenticated Master-Records custody and reconstructability PASS are observed.
```

## Release posture

The authenticated retrieval surface remains `PREPARED_NOT_DEPLOYED`. Destination source implementation is installed, but current-main validation, authorized same-origin deployment, live response conformance, authenticated custody, reconstructability, and public route verification remain activation gates. No deployment, credential configuration, transport activation, release, merge, or tag is authorized by this handoff.

## Archive readiness

This handoff preserves the current provider, gateway, custody, usage, comparison, navigation, endpoint implementation, workflow consolidation, validation, conformance, activation, authority boundary, failure repairs, and continuation state. Earlier conversation context is not required.
