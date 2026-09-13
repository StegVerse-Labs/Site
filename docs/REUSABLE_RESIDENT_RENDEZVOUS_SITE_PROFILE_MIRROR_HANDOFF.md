# Reusable Resident Rendezvous Site Profile Mirror Handoff

Updated: 2026-09-13
Repository: `StegVerse-Labs/Site`
Goal Task: `GADI-RUNTIME-CLOSURE-001`
COSV: `10100000100000`
Reusable component: `RTC-RESIDENT-RENDEZVOUS-010`
Status: `SOURCE_IMPLEMENTED / VALIDATION_PENDING / RUNTIME_EVIDENCE_PENDING`

## Purpose

Propagate the merged reusable resident-rendezvous component into the existing browser producer without creating a second transport client. `assets/kv-ui/resident-rendezvous-client.js` retains its legacy StegOS/KV exports and behavior while adding registered profile-aware discovery, request construction, and submission.

## Legacy compatibility

`stegos_kv_intr_chain` remains the default profile. Existing `buildResidentRequest`, `buildRendezvousRequest`, `submit`, and `submitDiscovered` behavior remains bound to request `RESIDENT-EXEC-STEGOS-KV-INTR-CHAIN-003`, including the historical Node Receipt #1 provenance requirement. That provenance remains transport/provenance data only; it is not user-verification authority.

## GADI profile

`gadi_runtime_observation` builds the exact canonical `RESIDENT-OBSERVE-GADI-RUNTIME-001` resident request. Discovery is consumer-scoped with `?consumer=gadi_runtime_observation`. The outer transport correlation is derived from the exact inner request digest as `transport-correlation:sha256:<digest>` and is not a credential, user-verification proof, or execution authorization.

`submitConsumerDiscovered()` does not invoke Node Receipt #1 resolution for GADI. Returned metadata declares `user_verification_authority=KV/SKAP Vault` and `target_node_identity_role=ROUTING_ONLY`.

## Authority

The browser client grants no authority. KV/SKAP Vault remains sole user-verification authority; WorkerCoordinator remains claim/fence authority; Interlock/InTr remains transition/admission authority; TV/TVC remains credential/provider/release authority; Master Records remains custody/reconstruction authority. The gateway remains `gateway_execution_authority=NONE`.

## Evidence boundary

Source tests prove profile selection, exact GADI packet construction, consumer-scoped discovery, transport-correlation derivation, no Node Receipt dependency for the GADI profile, no credentialed fetch, and zero gateway authority. They do not prove a resident received or consumed the packet.

## Next step

After validation/merge, attempt the canonical GADI packet over the merged Site -> Service Gateway -> reusable resident rendezvous -> registered GADI consumer route. Require an authentic ACK and GADI consumption receipt; do not infer runtime success from source/CI.

## Manual work

None.
