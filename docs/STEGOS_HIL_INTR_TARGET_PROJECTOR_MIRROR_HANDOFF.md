# StegOS HIL InTr Runtime Target Projector Mirror Handoff

Updated: 2026-08-29
Repository: `StegVerse-Labs/Site`
Issue: #640
Upstream profile source: `StegVerse-Labs/.github` HIL InTr profiled ingress
Parent HIL activation owner: `StegVerse-Labs/.github#246`

```text
goal_id: SITE-HIL-INTR-INGRESS-TARGET-PROJECTOR-640
state: IMPLEMENTED_ON_BRANCH_VALIDATION_PENDING
credential_authority: TV/TVC
github_token_runtime_authority: NONE
authority_effect: NONE_DISCOVERY_ONLY
runtime_ingress_observed: false
runtime_target_projected: false
```

## Purpose

Provide the missing deterministic evidence gate between an authentic observed sovereign ingress profile and Site's browser runtime target projection.

The merged default `stegos-node/hil-intr-sync-target.json` stays fail-closed:

```text
state: AWAITING_SOVEREIGN_INTR_INGRESS
ingress_url: null
runtime_ingress_observed: false
```

Running source/CI is intentionally insufficient to change that file. The projector consumes a separately captured runtime observation packet only.

## Observation requirements

Input schema:

```text
stegverse.hil-intr-ingress-observation/v1
```

Required authentic predicates include:

```text
observation_state = OBSERVED_HTTPS_PROFILE
observed_profile_url = exact credentialless https://.../intr/profile
https_observed = true
http_status = 200
credential_used = false
profile_sha256 = exact canonical observed profile hash
evidence_ref = durable runtime-observation reference
github_token_runtime_authority = NONE
execution_authority = NONE
authority_effect = NONE_OBSERVATION_ONLY
```

The embedded profile must independently satisfy the sovereign ingress profile contract:

```text
state = ACTIVE_SOVEREIGN_INTR_INGRESS
protocol = InTr
profile_path = /intr/profile
materialization_path = /intr/materialization
supported_origins includes STEGOS_NODE_OUTBOX and TVC_RELAY_EGRESS
direct_node_credential_requirement = NONE
direct_node_tvc_authorization_required = false
relay_tvc_authorization_required = true
event_triggered = true
always_on_receiver_required = false
second_user_device_required = false
exact_request_validation_required = true
write_once_queue_admission = true
tls_enabled = true
runtime_execution_attempted = false
hil_receiver_readiness_claimed = false
hil_custody_claimed = false
g18_required = false
credential_authority = TV/TVC
github_token_runtime_authority = NONE
execution_authority = NONE
authority_effect = NONE_DISCOVERY_EVIDENCE_ONLY
```

## Projection

Only after every observation/profile predicate passes may `project_hil_intr_sync_target.py` emit:

```text
state: CONFORMING_SOVEREIGN_INTR_INGRESS
ingress_url: https://<observed-origin>/intr/materialization
runtime_ingress_observed: true
transport_origin: STEGOS_NODE_OUTBOX
credential_requirement: NONE
execution_authority: NONE
```

The output also carries the source profile URL/hash, observation timestamp and evidence reference. It explicitly preserves:

```text
hil_execution_observed = false
hil_receiver_readiness_observed = false
hil_custody_observed = false
g18_completion_required = false
```

Therefore profile observation is not HIL activation and does not grant WorkerCoordinator, TVC lifecycle, custody, review or publication authority.

## Validation boundary

Before merge:

```text
python -m unittest -v tests.test_hil_intr_sync_target_projector
python -m json.tool data/schemas/hil-intr-ingress-observation.schema.json
source default target still null/unobserved
Site credential-clean validation gates PASS
```

Actual target promotion remains runtime evidence work after source merge. No synthetic test fixture may be committed as a live observation packet or used to update the merged default target.


## R2 stale-PR recovery — 2026-09-02

Original implementation PR #641 remained open and diverged from current `main`. Its bounded projector/source files were not present on current `main`, while the claim remained active. This successor lane recovers the same non-authorizing source work without changing the runtime evidence contract.

```text
successor branch: repair/hil-intr-ingress-target-projector-640-r2
recovered from: PR #641
state: RECOVERED_STALE_PR_FOR_INTEGRATION
second user device required: false
authority effect: NONE_DISCOVERY_ONLY
```

The successor must pass the current Site validation gates before merge. After successful merge, PR #641 must close as superseded and the claim must terminalize to RELEASED. Runtime target promotion remains separate and can only consume an authentic HTTPS profile observation.


## Release reconciliation — 2026-09-02

Successor PR #933 merged as `a493bca460d2fd1b45ac3c5b0e97864cd2489520`. Stale PR #641 was closed as superseded after its implementation was recovered onto current main.

Validated successor head `1960a4c1da8e334df552b9c71acd88652e587f15`:

- Site Handoff Orchestrator `33699325944` — SUCCESS
- Ecosystem Heartbeat Orchestration `33699325945` — SUCCESS
- Site Bootstrap Validate `33699326031` — SUCCESS

Source goal state: RELEASED.

The checked-in HIL target remains fail-closed and null until an authentic HTTPS profile observation is supplied. That remaining runtime promotion is consumption of external runtime state, not missing projector implementation, and it does not require a second user-operated device.


## Same-device profile relationship — 2026-09-02

Site PR #941 / `20b7603be8e88dd714fa4cef3337552704f9e4e8` introduced a bounded `HIL:Ingress` profile into the existing registered-iPhone root Universal InTr service worker.

This does not invalidate this projector. It narrows its role:

- the current-device authenticated `/intr/profile` is preferred for same-device HIL admission;
- this projector remains the canonical source for promoting a **separate external** HTTPS HIL ingress from authentic observation;
- the checked-in target remains fail-closed when no such external ingress is observed.

Therefore missing external-ingress observation is no longer a blocker to same-device HIL request admission on the registered iPhone.
