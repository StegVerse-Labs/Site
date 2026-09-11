# MyKV Service Federation Implementation Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Goal Task ID: `STEGOS-DEVICE-KV-SKAP-ROUNDTRIP-001`
Parent Goal Task ID: `KV-CONNECTION-REVALIDATION-WORKER-001` (root lineage only)
Canonical child handoff: `StegVerse-Labs/.github/docs/DEVICE_KV_SKAP_ROUNDTRIP_MIRROR_HANDOFF.md`
COSV: `50000000102000`
Parent handoff: `docs/MY_KV_MULTI_INSTANCE_PROVIDER_MANAGER_MIRROR_HANDOFF.md`
Design contract: `docs/MY_KV_SERVICE_FEDERATION_CONTRACT.md`
PR: `#1196`
State: `SOURCE_IMPLEMENTED_VALIDATED / SITE_COORDINATION_RECONCILING / PROVIDER_RUNTIME_NOT_ACTIVATED`

## Implemented source

`assets/my-kv-service-federation.js` implements the provider-neutral binding and onboarding core described by the design contract.

Implemented source surfaces:

- `stegverse.kv.service-binding/v1` validation;
- `stegverse.site.my-kv.account-onboarding-request/v1` construction;
- `stegverse.kv.service-projection/v1` unified projections;
- multiple accounts from the same or different providers;
- independent relationship state per service/account binding;
- `REFERENCE_ONLY`, `SYNCED_TO_KV`, and `KV_PRIMARY_OR_SOVEREIGN` custody posture validation;
- exact `service_class × provider × account × kv_instance × relationship` binding keys;
- selectable service projections that preserve provenance and explicitly state `custody_merged=false`;
- SKAP-first onboarding request semantics with provider-native authorization fallback;
- required provider capability discovery after authorization;
- fail-closed default relationship state `NOT_CONNECTED`;
- explicit defaults of no sync, no AI interaction, no destructive mutation, no sharing, and no publication;
- credential-like field rejection in ordinary federation projections/results;
- `PENDING_INTERLOCK_INTR` account onboarding requests with `provider_operation_authorized=false`.

## Validation and coordination

`tests/my-kv-service-federation.test.cjs` covers binding validation, multi-account/multi-provider projection, independent relationship state, sensitive-field rejection, duplicate binding rejection, SKAP-first onboarding request semantics, and fail-closed behavior without a governed onboarding bridge.

Initial run `34524573983` correctly exposed an implementation defect: the generic sensitive-field scanner rejected the explicit `credential_material_present=false` sentinel. Commit `04e3490e8d8fc8bad3869376bd761d35596a208a` repaired the validator so the sentinel is allowed only when exactly false.

Follow-up My KV Multi-Instance Provider Manager run `34524646420` completed successfully. All steps passed, including the existing KV provider/request tests, the new service-federation/SKAP-first onboarding suite, DEVICE_KV transport validation, KV-set projection admission, MyKV multi-instance UI validation, syntax validation, and the combined bounded-authority/federation invariant check.

The child task's canonical `.github` continuation PR #1332 merged at `42996a4582e2fb9e4d3207dd3e45b764dc727723` after exact-head `4e6bdbaa7cf7c58bcfc375b4efe1787ada6b78ce` passed all three canonical workflows. The canonical child contract now explicitly permits bounded `EVENT_EPHEMERAL` StegOS/Node transport materialization and does not require an always-on receiver, persistent transport runtime, TestFlight deployment, or continuously resident physical process merely to prove this data path.

Site #1196 must therefore consume that child contract and must not reopen or widen the parent worker semantics. The Site branch now has its own active child claim at `data/session-work-claims.d/site-mykv-service-federation-20260910.json`; older MyKV provider/UI/transport claims remain released historical slices and are not reactivated.

Previous Site #1196 head `4c85fc41137d8162db2fb90b5e036dec5b6f24f6` passed My KV Multi-Instance Provider Manager, Cloud KV Peer Manager, Device Local KV Install, heartbeat-contract validation, and session-work-claim validation. Its repository-wide Site Handoff, Bootstrap, and Heartbeat workflows all converged on the same coordination failure: the PR branch lacked exactly one active pre-work claim. The child claim was added in commit `9082bab9af8ad79911b81992f302883121895282`; fresh exact-head validation is required before merge.

## Authority boundary

This source does not connect Gmail, Microsoft 365, iCloud, OneDrive, Google Drive, or any other provider. It does not receive or store credentials, does not call SKAP directly, does not mint Interlock/InTr admission, and does not mutate provider state.

The onboarding source constructs only a governed request whose credential destination is `SKAP_VAULT`, whose provider authorization state is false, and whose governance state is `PENDING_INTERLOCK_INTR`.

Provider credential custody remains TV/TVC + SKAP. Provider operation admission remains Interlock/InTr. Provider-specific adapters remain separately owned. TVC remains the single SKAP ciphertext custody writer for the canonical roundtrip path.

## Event-ephemeral runtime completion predicates

Authentic completion requires one bounded operation lineage; it does **not** require a continuously resident transport process. The retained Node identity/genesis/continuity context persists, while the actual transport/provider process may materialize only for the event and terminate afterward.

At minimum the authentic operation must prove:

1. the owner initiates one MyKV `Add account` or already-authorized non-destructive operation from the current device interaction surface;
2. provider-native authorization, when required, completes under TV/TVC + SKAP without ordinary KV credential persistence;
3. provider capability discovery returns an observed service set;
4. MyKV materializes only admitted non-secret service/account bindings;
5. the bounded event is admitted through the canonical Node/Interlock/InTr context rather than a second transport stack;
6. DEVICE -> KV emits the first adjacent InTr receipt;
7. KV -> SKAP emits the second receipt chained to the first while preserving TVC single-writer custody;
8. SKAP -> KV emits the third receipt chained to the second and exact SKAP ciphertext/reference readback is verified;
9. KV -> DEVICE emits the fourth receipt chained to the third and exact KV return readback is verified;
10. packet bytes match the intent commitments across the completed lineage;
11. no raw credential, refresh token, session token, magic-link token, or equivalent capability appears in ordinary KV/Site/device evidence;
12. no hosted runtime fallback or second user-operated device is used;
13. the terminal verifier records `DEVICE_KV_SKAP_ROUNDTRIP_VERIFIED` before runtime completion is claimed.

A current iPhone may be the interaction/execution surface, but physical-iPhone residency itself is not a transport predicate. The proof predicate is the authentic bounded event-ephemeral invocation plus retained Node continuity, four adjacent admitted receipts, and exact readback.

## README impact

This source adds a real federation/onboarding implementation surface but does not yet prove provider execution. The root README requires a bounded source-status entry before PR #1196 is merged. That entry must identify `STEGOS-DEVICE-KV-SKAP-ROUNDTRIP-001` as the active child owner, retain `KV-CONNECTION-REVALIDATION-WORKER-001` only as root lineage, state that event-ephemeral transport is allowed, and must not claim provider authorization, live account connection, synchronization, AI-corpus admission, external mutation, or runtime activation.

## Next

1. Update the root README with the bounded child/federation status.
2. Re-run exact-head Site #1196 claim/orchestration/bootstrap/heartbeat and MyKV validations with the new active child claim.
3. Merge #1196 only when the current head is green.
4. Execute or consume one eligible authentic bounded event-ephemeral Device -> KV -> SKAP -> KV -> Device operation through the existing TV/TVC, SKAP, Node, and Interlock/InTr authority paths.
5. Retain the four-hop receipt lineage and exact SKAP/KV readbacks; only then close the runtime blockers.

## Manual work

None at this source/reconciliation stage. Do not re-emit the Google Drive adoption request, duplicate provider authorization, duplicate SKAP ciphertext custody, create another Interlock/InTr stack, require an always-on receiver, or require a second user-operated device.
