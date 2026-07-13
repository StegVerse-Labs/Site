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

## Current Site and destination posture

```text
contract_status: PREPARED_NOT_DEPLOYED
route: GET /api/usage/sessions/{session_id}
authentication: same_origin_session
same-origin browser credentials: allowed
cross-origin browser credentials: prohibited
Site bearer/query/local-storage token configuration: prohibited
live_transport.enabled: false
usage_api_base: null

destination repository: StegVerse-org/LLM-adapter
destination handoff: LLM_ADAPTER_MIRROR_HANDOFF.md
destination state: DESTINATION_IMPLEMENTATION_INSTALLED_VALIDATION_PENDING
blocker: DESTINATION_VALIDATION_AND_DEPLOYMENT_EVIDENCE_PENDING
```

The retrieval contract requires same-origin session identity, `stegverse.usage.session.v1`, `LIVE_USAGE_API`, requested-session preservation, a mandatory retrieval receipt, producer and policy identity, `authority_granted=false`, and `custody_recorded=false`.

## Current-main validation progression

### Run 29261718764

```text
Commit: d56f5faa37c63d87f92e271825dcf166773ad7c5
Branch: main
Workflow: Site Task Runner
Job: run-site-task
Result: FAILED after prior public-verification repair passed
Passing boundary: scripts/check_site_governed_ecosystem_public_verification.py
Failed command: scripts/check_site_llm_free_tier_trust.py
Failure class: stale literal-form assertions against the current bounded public display and canonical status surface
```

The public page already contained the bounded free-tier section, quota, receipt inspection, recent-session replay limitation, no-provider-call boundary, and no-execution-authority boundary. The canonical status file already retained `StegVerse-org/LLM-adapter`, `adapter.capabilities.json`, `free_tier_trust`, exact quota values, replay/export limits, and explicit admissibility and upgrade non-claims.

Bounded repair:

```text
Commit: 3fbd3720976ea83439c7641da0b5d6b2aaedb00b
File: scripts/check_site_llm_free_tier_trust.py
```

The checker was rebound to the user-facing page forms while retaining canonical machine-facing destination, policy, quota, replay, export, admissibility, and upgrade assertions in `docs/LLM_FREE_TIER_TRUST_STATUS.md`.

### Run 29265864007

```text
Commit: b5da6e9a4fc87b7957c8a57dbc942d09b6b5be72
Branch: main
Workflow: Site Task Runner
Job: run-site-task
Result: FAILED after governed public verification passed
Passing boundary: scripts/check_site_governed_ecosystem_public_verification.py
Failed command: scripts/check_site_llm_free_tier_trust.py
Failure: page_missing:no provider call
Failure class: case-sensitive validator mismatch against existing public copy "No provider call"
```

The page already contained the required boundary at `ecosystem-chat.html`: `No provider call, proof receipt, shell access, or repo write occurs.` The failure did not identify a missing governance claim, quota, status field, workflow capability, or destination contract.

Bounded repair:

```text
Commit: 343c614049cc3486933cef065f59fd291e4ce9c9
File: scripts/check_site_llm_free_tier_trust.py
```

Public-facing prose checks now use Unicode case normalization while exact machine-facing status assertions remain unchanged. No public copy, claim, quota, workflow, deployment posture, external destination, release authority, or activation boundary changed.

### Run 29270157819

```text
Commit: c2464f8fdb44315babeee18d4c0031b8c2e75961
Branch: main
Workflow: Site Task Runner
Job: run-site-task
Result: FAILED after the free-tier trust validator passed
Passing boundary: scripts/check_site_llm_free_tier_trust.py
Failed command: scripts/check_site_final_activation_pending.py
Failure class: stale activation-pending assertions requiring a removed third workflow and obsolete final-goal helper commands
```

The current handoff still declares exactly two operational workflows and keeps Site in `PREPARED_NOT_DEPLOYED`, `SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED`, and `live_transport_enabled: false` posture. The failed checker required `site-autonomous-continuation.yml` plus obsolete final-goal update/check commands that are not part of the current two-workflow architecture.

Bounded repair:

```text
Commit: a1793b66c30cf16c6154eceac96def652c6df144
File: scripts/check_site_final_activation_pending.py
```

The checker now validates the current two-workflow inventory, prepared-not-deployed checkpoint, disabled live transport, destination validation, Master-Records custody, reconstructability, and no-release boundary while preserving all existing non-claim and forbidden-activation assertions. No workflow, deployment, release, custody, credential, or external-repository state changed.

Successor current-main verification is pending.

## Activation evidence and checkpoint

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

The validation workflow is expected to produce:

```text
site_application_validation.result.json
site_current_main_validation.receipt.json
site_current_main_validation.manifest.json
```

A successful result, receipt, and manifest artifact set has not yet been observed together on one current-main run.

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
  -> observe successor current-main validation after commit a1793b66c30cf16c6154eceac96def652c6df144
  -> confirm scripts/check_site_final_activation_pending.py passes
  -> repair only the next exact failing command without removing checks
  -> verify one successful result, receipt, and manifest artifact set
  -> bind verified Site evidence into the activation ledger
  -> run conformance only against an authorized same-origin deployment
  -> enable live transport only after every activation prerequisite passes

StegVerse-org/LLM-adapter
  -> observe current-main validation containing usage-session verification
  -> integrate automatic provider-owned usage submission
  -> deploy combined gateway with mutation disabled only under explicit destination authority
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
1. Observe the successor Site Task Runner/current-main validation after commit a1793b66c30cf16c6154eceac96def652c6df144.
2. Confirm scripts/check_site_final_activation_pending.py passes.
3. Repair only the next exact failing command without removing existing checks.
4. Verify the first successful current-main result, receipt, and manifest artifact set.
5. Observe StegVerse-org/LLM-adapter current-main validation containing usage-session verification.
6. Deploy only through an explicitly authorized same-origin topology.
7. Run Site endpoint conformance only against that deployed route.
8. Do not enable live transport until all activation evidence is VERIFIED.
9. Do not claim RECORDED until authenticated Master-Records custody and reconstructability PASS are observed.
```

## Release posture

The authenticated retrieval surface remains `PREPARED_NOT_DEPLOYED`. Destination source implementation is installed, but current-main validation, authorized same-origin deployment, live response conformance, authenticated custody, reconstructability, and public-route verification remain activation gates. No deployment, credential configuration, transport activation, release, merge, or tag is authorized by this handoff.

## Archive readiness

This handoff preserves the current provider, gateway, custody, usage, comparison, workflow consolidation, validation, activation, authority boundary, latest bounded repair, and continuation state. Earlier conversation context is not required.
