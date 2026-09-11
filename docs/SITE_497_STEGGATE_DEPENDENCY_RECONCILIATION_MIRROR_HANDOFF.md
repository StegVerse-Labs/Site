# Site #497 StegGate Dependency Reconciliation Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Goal: `KV-CONNECTION-REVALIDATION-WORKER-001`
Site lane: `SITE-497-THIRD-PARTY-DEPENDENCY-ERADICATION`
COSV: `50000000102000`
Upstream handoff: `StegVerse-Labs/StegCore/docs/STEGGATE_HOSTED_CARRIER_RETIREMENT_MIRROR_HANDOFF.md`
Current continuation branch: `task/site-497-intr-runtime-binding-20260910`

## Merged provider-independent evidence

- PR #1155 merged external recovery-bundle retention, off-GitHub restore, and off-GitHub validation for archive SHA-256 `a9b81dfb7a34e7b4c627145e6ab817466b92c1ea9176fc41f76e420a2b201b0f` with 3400 verified entries.
- PR #1158 merged provider-neutral `STEGVERSE_SITE_STATIC_PUBLICATION_V1` materialization and exact per-file validation.
- PR #1162 merged the fail-closed authentic publication-observation evidence seam.
- PR #1168 merged the no-Render remediation at `9d9ffb7ef5cee256588dcdd3790846b5943867da` after all exact-head Site gates passed.
- PR #1212 merged at `11c574ad51ce0cd3a4a615eb66652879bd7f2a0a`, removing stale Render requirements and adding the resident publication rendezvous source seam.
- PR #1213 merged at `475c2523aab7a4a0568c12f0cd92f67e9496c86d`, reconciling the canonical handoff after PR #1212.

## No-hosted-origin invariant

Render is prohibited for Site #497 recovery/publication. `data/publication-origin-selection-2026-09-09.json` requires `selection_state=NO_HOSTED_ORIGIN_SELECTED`, `selected_origin=null`, and includes `RENDER` in `prohibited_providers_for_this_lane`. Historical Render service/deploy identifiers remain only as `REJECTED_DO_NOT_USE` audit evidence and are ineligible for equivalence proof or DNS binding.

## StegOS / Node Interlock-InTr runtime binding

The resident publication rendezvous now consumes the existing StegOS/Node Universal Interlock semantics rather than inventing a Site-specific runtime protocol.

```text
runtime class = RESIDENT_STEGVERSE
transport profile = stegverse.universal-intr.adjacent-hop/v1
candidate protocol ref = SV-INTERLOCK-v0.4-candidate
candidate protocol canonical adoption claimed = false
Universal Interlock runtime activation claimed = false
transition admission required = true
Node-mediated transport required = true
direct KV-to-KV transport = prohibited
direct SKAP-to-SKAP transport = prohibited
HeartBeat authorizing = false
endpoint identity grants authority = false
Node identity equals KV identity = false
transport receipt grants transition authority = false
COMMIT_CANDIDATE changes canonical state = false
```

The authentic exchange must bind the following evidence to one exact exchange/transition lineage:

```text
resident Node identity
Interlock endpoint identity
exchange id
source transition id + parent
generation
fencing identity
publication artifact manifest SHA-256
InTr admission receipt
Node transport receipt
independent HTTP readback receipt
exact-path/SHA-256 equivalence receipt
candidate-result receipt
```

Site source or CI may validate the shape and fail-closed semantics only. It may not populate these runtime observations or claim canonical Universal Interlock adoption. The final publication transition remains separately admitted after candidate evidence returns through InTr.

## README maintenance

Root `README.md` was reviewed against this continuation. Its provider-independent boundary remains accurate and does not require a broad rewrite.

## Current truth

```text
canonical runtime = RESIDENT_STEGVERSE
GitHub Actions runtime required = false
hosted publication origin selected = false
Render allowed = false
provider-neutral static publication artifact = MERGED_SOURCE_VALIDATED
publication observation evidence contract = MERGED_SOURCE_VALIDATED
resident publication rendezvous base contract = MERGED_SOURCE_VALIDATED
Node/Interlock/InTr resident binding = SOURCE_IMPLEMENTED_VALIDATION_PENDING
authentic resident InTr exchange observed = false
resident executor observed = false
resident endpoint identity observed = false
Interlock transition admission observed = false
Node transport observed = false
independent public readback = PENDING
exact public-content equivalence proof = PENDING
canonical-domain DNS/TLS recovery proof = PENDING
```

## Remaining work

1. Validate and merge the Node/Interlock/InTr resident-rendezvous binding.
2. Consume authentic resident executor, Node identity, endpoint identity, transition/generation/fencing, InTr admission, and Node transport evidence from the sovereign runtime lane; do not synthesize any of it in Site or CI.
3. Bind the exact `STEGVERSE_SITE_STATIC_PUBLICATION_V1` manifest SHA-256 to that exchange.
4. Perform independent HTTP byte readback and exact-path/SHA-256 comparison against the resident endpoint and return that result through InTr as a candidate-result receipt.
5. Admit the final canonical publication transition separately only after the complete exchange reconciles.
6. Execute controlled `stegverse.org` DNS/TLS recovery only after resident equivalence is proven.
7. At release readiness, tag/release and create the separate downstream propagation-verification task for StegVerse-Labs/Sit, GCAT-BCAT-Engine/Publisher, admissibility-wiki, and stegguardian-wiki.

## Manual work

None for this source continuation. The historical Render service is prohibited by canonical contracts; deleting that historical service remains the separate physical cleanup if it has not already been deleted.
