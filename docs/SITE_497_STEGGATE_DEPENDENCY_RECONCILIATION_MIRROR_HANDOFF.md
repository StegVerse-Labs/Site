# Site #497 StegGate Dependency Reconciliation Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Goal: `KV-CONNECTION-REVALIDATION-WORKER-001`
Site lane: `SITE-497-THIRD-PARTY-DEPENDENCY-ERADICATION`
COSV: `50000000102000`
Upstream handoff: `StegVerse-Labs/StegCore/docs/STEGGATE_HOSTED_CARRIER_RETIREMENT_MIRROR_HANDOFF.md`
Current continuation branch: `task/site-497-event-ephemeral-runtime-20260910`

## Merged provider-independent evidence

- PR #1155 merged external recovery-bundle retention, off-GitHub restore, and off-GitHub validation for archive SHA-256 `a9b81dfb7a34e7b4c627145e6ab817466b92c1ea9176fc41f76e420a2b201b0f` with 3400 verified entries.
- PR #1158 merged provider-neutral `STEGVERSE_SITE_STATIC_PUBLICATION_V1` materialization and exact per-file validation.
- PR #1162 merged the fail-closed authentic publication-observation evidence seam.
- PR #1168 merged the no-Render remediation at `9d9ffb7ef5cee256588dcdd3790846b5943867da`.
- PR #1212 merged at `11c574ad51ce0cd3a4a615eb66652879bd7f2a0a`, removing stale Render requirements and adding the publication rendezvous seam.
- PR #1214 merged at `161ac14b10bc69b9f8c3d5b68362f10501f59908`, binding Site publication to StegOS/Node Interlock/InTr exchange semantics.
- PR #1216 merged at `7a94ce3c0d2df60c8974299ac074572021812fab`, reconciling that binding after runtime-evidence search.

## No-hosted-origin invariant

Render remains prohibited for Site #497 recovery/publication. `selected_origin=null`; no hosted publication origin is canonical or admissible. Historical Render identifiers remain rejected audit evidence only.

## Canonical runtime correction

Review of the current StegOS canonical runtime lane and the active Device<->KV<->SKAP child establishes that the previous `RESIDENT_STEGVERSE`/persistent-process framing was too restrictive for this proof.

Canonical StegOS runtime evidence already proves the reusable bounded runtime lifecycle as:

```text
runtime_class = EVENT_EPHEMERAL
persistent Node identity / genesis / continuity = REQUIRED
persistent host = NOT REQUIRED
always-on receiver = NOT REQUIRED
second user-operated machine/device = NOT REQUIRED
max operations per lease = 1
```

Canonical source: `StegVerse-Labs/StegOS/docs/CANONICAL_RUNTIME_LANE_MIRROR_HANDOFF.md`.

The first authentic canonical runtime lane was observed end-to-end with lease `CRL-5290a1a72febbd11bb96c119`, runtime `WEBWORKER-9a560504aa682d2726e98ba3`, chained InTr ingress/egress receipts, evidence export, lease closure, and binding into retained Node continuity. That proof used `rendezvous_requirement=NOT_REQUIRED`; therefore it proves the reusable runtime fabric, not this Site publication rendezvous itself.

For Site publication, each authentic bounded publication event must additionally require independent public HTTPS `/intr/profile` observation using the application-neutral StegOS public-profile verifier before content-equivalence proof is accepted.

## Event-ephemeral Site publication contract

The existing file name `data/resident-publication-rendezvous-contract.json` is preserved for continuity, but schema v3 now binds the actual runtime semantics:

```text
runtime class = EVENT_EPHEMERAL
persistent Node continuity identity required = true
persistent host required = false
always-on receiver required = false
second user-operated device required = false
hosted provider required = false
Render allowed = false
GitHub Actions as runtime = false
Cloudflare quick tunnel = false
transport profile = stegverse.universal-intr.adjacent-hop/v1
Node-mediated transport required = true
HeartBeat authorizing = false
COMMIT_CANDIDATE canonical = false
```

The publication exchange must bind one exact lineage containing:

```text
Node continuity identity
runtime lease id
runtime identity
Interlock endpoint identity
exchange id
source transition id + parent
generation + fencing identity
publication artifact manifest SHA-256
InTr admission receipt
Node transport receipt
independently observed public profile SHA-256
independent HTTP byte-readback receipt
exact-path/SHA-256 equivalence receipt
candidate-result receipt
lease closure receipt after evidence export
```

The final canonical publication transition is separately admitted only after that exchange reconciles. DNS/TLS binding remains a later, separate proof.

## README maintenance

Root `README.md` remains accurate on the provider-independent boundary. No broad README rewrite is required by this correction.

## Current truth

```text
canonical reusable runtime fabric = EVENT_EPHEMERAL / OBSERVED_END_TO_END
persistent Node continuity = required
persistent transport host = not required
always-on receiver = not required
second user-operated device = not required
GitHub Actions runtime required = false
hosted publication origin selected = false
Render allowed = false
provider-neutral static publication artifact = MERGED_SOURCE_VALIDATED
publication observation evidence contract = MERGED_SOURCE_VALIDATED
Site event-ephemeral runtime reconciliation = SOURCE_IMPLEMENTED_VALIDATION_PENDING
authentic Site publication exchange observed = false
independent Site public profile observed = false
exact public-content equivalence proof = PENDING
canonical-domain DNS/TLS recovery proof = PENDING
```

## Remaining work

1. Validate and merge this EVENT_EPHEMERAL correction.
2. Execute one bounded Site publication lease using the existing canonical Node identity/continuity context; do not wait for or require an always-on resident process.
3. Bind the exact `STEGVERSE_SITE_STATIC_PUBLICATION_V1` manifest SHA-256 and Interlock/InTr exchange lineage.
4. Independently observe the event's HTTPS `/intr/profile` and bind the canonical public-profile SHA-256.
5. Perform independent exact HTTP byte readback and exact-path/SHA-256 comparison; return the result through InTr as a candidate-result receipt.
6. Export evidence, close the lease, retain the closure receipt, then separately admit the final publication transition.
7. Execute controlled `stegverse.org` DNS/TLS recovery only after event equivalence is proven.
8. At release readiness, tag/release and create downstream propagation verification for StegVerse-Labs/Sit, GCAT-BCAT-Engine/Publisher, admissibility-wiki, and stegguardian-wiki.

## Manual work

None for this source/runtime-contract correction. The historical Render service remains prohibited and unrelated to canonical execution.
