# HIL Browser ESRL LEASE_OPEN Mirror Handoff

Updated: 2026-09-11
Repository: `StegVerse-Labs/Site`
Issue: `#1156`
Parent goal: `SHWP-HIL-SOVEREIGN-RECEIVER-001`
Canonical continuation: `StegVerse-Labs/.github/docs/HIL_RESIDENT_SESSION_MANIFOLD_ACTIVATION_MIRROR_HANDOFF.md`
Current parent COSV: `50000000103000`

## Purpose

Carry the already-accepted current-iPhone G25 HIL browser state into the next independent ESRL `LEASE_OPEN` observation without minting another claim/fence or resetting the retained standalone-Safari context.

## Accepted upstream physical state

```text
HIL_BROWSER_EVIDENCE_V16
-> BROWSER_HIL_LOCAL_READY_OBSERVED
-> current-iPhone standalone Safari
-> context ctx_d151139d2db1eeecb6512f5844058246
-> node stegnode-web-f24e3bfb7f5343cb37323187a88e51f3
-> retained G25 claim/fence
-> journal replay PASS
-> canonical .github request-consumption receipt SATISFIED
```

Route: `/stegos-bootstrap/portable-workercoordinator/hil-esrl-v1`  
Protocol: `HIL_BROWSER_ESRL_V1`

## Completed source repairs

Site PR `#1165`, merged at `7a72c94b3e4fc246424975d97729c4f2220fbef0`, repaired the historical G25 activation envelope compatibility so a missing checkout receipt hash may be recovered only from the exact retained WorkerCoordinator checkout after lineage validation while preserving the authentic raw execution-entry digest.

Site PR `#1169`, merged at `9751d100250c5a3905a363e08c9d9bed47d54ff7`, made `hil-esrl-activate.html` automatically continue from exact retained G25 state and persist only an exact same-context `LEASE_OPEN` result.

Site PR `#1173`, merged at `61865d7649fc39669caa39008568764f8b7c45b4`, repaired stale standalone-Safari page/service-worker convergence while preserving the admitted `stegos-web-bootstrap-v16` / `HIL_BROWSER_EVIDENCE_V16` contract, retained storage, and G25 lineage. Exact-head and post-merge validation passed as previously recorded.

## Authentic physical ESRL success now observed

The retained standalone-Safari current-iPhone context has now physically loaded the current auto-resume page and reached the component-produced ESRL success result.

Observed result fields include:

```text
schema = stegverse.hil-browser-esrl-lease-open/v1
state = LEASE_OPEN
lease_state = LEASE_OPEN
lease_id = HIL-BROWSER-ESRL-7bafde4a280e847758da157e
hil_esrl_protocol = HIL_BROWSER_ESRL_V1
source_browser_protocol = HIL_BROWSER_EVIDENCE_V16
task_id = SHWP-HIL-SOVEREIGN-RECEIVER-001
resident_request_id = RESIDENT-EXEC-HIL-SOVEREIGN-RECEIVER-002
browser_context_id = ctx_d151139d2db1eeecb6512f5844058246
node_id = stegnode-web-f24e3bfb7f5343cb37323187a88e51f3
claim_id = SHWP-SHWP-HIL-SOVEREIGN-RECEIVER-001-G25
fencing_token = 25
source_execution_entry_sha256 = 8ddd8c6fc08038ce4111b349f47a5f44bd48a7bfbc551fae1bfb59a1a384da69
state_machine = REQUESTED -> ADMITTED -> PROVISIONING -> LOCAL_READY -> LEASE_OPEN
runtime_class = EVENT_EPHEMERAL
lease_profile = INTAKE
runtime_materialized = true
local_identity_verified = true
local_ready_source_observed = true
journal_replay_state = PASS
same_device_execution_required = true
execution_surface = CURRENT_USER_IPHONE
requires_other_machine = false
second_claim_minted = false
request_consumption_claimed = false
custody_observed = false
post_restart_exact_byte_proof_observed = false
tvc_lifecycle_receipt_observed = false
broader_hil_lifecycle_complete = false
credential_authority = TV/TVC
github_token_runtime_authority = NONE
heartbeat_granted_authority = false
authority_effect = NONE_RUNTIME_OBSERVATION_ONLY
```

The current page showed enabled `Copy evidence JSON` and `Download evidence JSON`, so the automatic path progressed beyond opening state to an exportable component artifact.

## Stale-navigation repair claim released

The separate Site repair claim `SITE-HIL-ESRL-STALE-NAVIGATION-1156-20260909` is now `RELEASED` because its explicit expiry condition has been met: the repair was merged and validated, current public bytes were physically observed in the retained standalone-Safari context, automatic continuation ran, and `LEASE_OPEN` appeared without the stale button being required as the worker/page convergence mechanism.

This claim release does **not** remove the parent ESRL evidence blocker.

## Exact-byte canonical intake boundary

The parent blocker remains until the exact exported file bytes are accepted by canonical `.github/scripts/intake_hil_browser_esrl_evidence.py`.

Screenshots prove the physical runtime observation but are not the byte-exact component artifact. Do not reconstruct, retype, normalize, or regenerate JSON from screenshots. The exact unedited `hil-esrl-lease-open-*.json` download must be preserved and supplied to canonical intake.

Therefore the current distinction is:

```text
physical component LEASE_OPEN = OBSERVED
public current-page convergence = OBSERVED
exact exported artifact bytes accepted by .github intake = PENDING
parent COSV = 50000000103000
```

When the exact file is accepted, the already-merged canonical reconciliation path may remove only the ESRL blocker and propose the two-blocker vector `50000000102000`; post-restart exact-byte proof and TVC lifecycle handoff remain independent.

## Explicit non-claims

Physical ESRL success alone does not prove:

```text
custody_observed
post_restart_exact_byte_proof_observed
tvc_lifecycle_receipt_observed
broader_hil_lifecycle_complete
```

No second WorkerCoordinator, replacement G25 claim/fence, Safari reset, second machine, GitHub runtime authority, or new credential path is introduced.

## README maintenance

`README.md` was re-reviewed after the physical success observation. Existing statements about the v16 propagation generation and HIL browser protocol remain accurate. No README prose change is required.

## Remaining parent blockers

Until exact-byte intake occurs, canonical parent state still carries all three blockers:

1. `AUTHENTIC_ESRL_HIL_LEASE_OPEN_NOT_YET_OBSERVED`
2. `POST_RESTART_EXACT_BYTE_PROOF_NOT_YET_PRESERVED`
3. `TVC_HIL_LIFECYCLE_HANDOFF_NOT_YET_PROVEN`

The first is now physically observed but intentionally remains canonical until exact artifact bytes are accepted and state is reconciled.
