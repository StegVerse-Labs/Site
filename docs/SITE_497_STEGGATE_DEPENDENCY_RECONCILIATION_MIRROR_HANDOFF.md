# Site #497 StegGate Dependency Reconciliation Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Goal: `KV-CONNECTION-REVALIDATION-WORKER-001`
Site lane: `SITE-497-THIRD-PARTY-DEPENDENCY-ERADICATION`
COSV: `50000000102000`
Upstream handoff: `StegVerse-Labs/StegCore/docs/STEGGATE_HOSTED_CARRIER_RETIREMENT_MIRROR_HANDOFF.md`
Current continuation branch: `task/site-497-publication-materialization-request-20260910`

## Merged provider-independent evidence

- PR #1155 merged external recovery retention/restore/validation for archive SHA-256 `a9b81dfb7a34e7b4c627145e6ab817466b92c1ea9176fc41f76e420a2b201b0f` with 3400 verified entries.
- PR #1158 merged provider-neutral `STEGVERSE_SITE_STATIC_PUBLICATION_V1` materialization and exact validation.
- PR #1162 merged the fail-closed publication-observation evidence seam.
- PR #1168 merged the no-Render remediation at `9d9ffb7ef5cee256588dcdd3790846b5943867da`.
- PR #1212 merged at `11c574ad51ce0cd3a4a615eb66652879bd7f2a0a`, removing stale Render requirements and adding the publication rendezvous seam.
- PR #1214 merged at `161ac14b10bc69b9f8c3d5b68362f10501f59908`, binding publication to Node/Interlock/InTr exchange semantics.
- PR #1216 merged at `7a94ce3c0d2df60c8974299ac074572021812fab`, reconciling runtime evidence.
- PR #1221 merged at `f36b8aef3da40ed5e43b8a7e3b84e40904b37869` after all five exact-head gates passed, correcting the Site runtime contract to the proven canonical `EVENT_EPHEMERAL` fabric while retaining persistent Node continuity.

## No-hosted-origin invariant

Render remains prohibited for Site #497. `selected_origin=null`; no hosted publication origin is canonical or admissible.

## Canonical event-ephemeral runtime

Canonical StegOS runtime evidence proves the reusable bounded lifecycle with persistent Node identity/continuity but no persistent host, always-on receiver, or second user-operated device requirement. The first authentic application-neutral runtime proof remains substrate evidence only; Site publication requires its own bounded event plus public HTTPS verification.

Current Site publication runtime contract requires:

```text
runtime class = EVENT_EPHEMERAL
persistent Node continuity identity = required
persistent host = false
always-on receiver = false
second user-operated device = false
hosted provider = false
Render = prohibited
Universal InTr adjacent-hop transport = required
public profile observation = INDEPENDENT_PUBLIC_HTTPS
exact publication bytes/readback = required
lease closure after evidence export = required
final canonical publication transition = separately admitted
```

## Publication event materialization seam

This continuation adds a deterministic Site-specific request adapter without creating another runtime implementation.

`scripts/build_site_publication_event_request.py`:

1. materializes the existing `STEGVERSE_SITE_STATIC_PUBLICATION_V1` artifact;
2. hashes the exact `manifest.json` bytes;
3. builds one canonical `stegverse.universal-intr-transport/v1` intent for `SITE_PUBLICATION_EVENT` from `DEVICE_SYSTEM/Site:PublicationControl` to `STEGOS_ECOSYSTEM/StegOS:SitePublicationRuntime`;
4. derives one `stegverse.universal-intr-materialization-request/v1` in `QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION` state;
5. binds the exact manifest SHA-256 through envelope, transport intent, and materialization request;
6. targets the existing `StegVerse-Labs/StegOS:canonical-runtime-lane` owner;
7. grants no execution authority, claim/fence, credential authority transfer, or canonical publication standing.

`scripts/check_site_publication_event_request.py` independently regenerates and validates the complete request binding and fail-closed runtime semantics. The focused Site #497 workflow now executes this validator.

A queued materialization request is not runtime proof. Authentic completion still requires execution through the bounded runtime fabric.

## README maintenance

Root `README.md` was reviewed. Its provider-independent runtime/publication boundary remains accurate; no wording change is required for this internal request seam.

## Current truth

```text
canonical reusable runtime fabric = EVENT_EPHEMERAL / OBSERVED_END_TO_END
Site EVENT_EPHEMERAL runtime correction = MERGED_SOURCE_VALIDATED
Site publication event request adapter = SOURCE_IMPLEMENTED_VALIDATION_PENDING
publication event materialization request schema = stegverse.universal-intr-materialization-request/v1
persistent host required = false
always-on receiver required = false
second user-operated device required = false
hosted publication origin selected = false
Render allowed = false
authentic Site publication event executed = false
independent Site public profile observed = false
exact public-content equivalence proof = PENDING
canonical-domain DNS/TLS recovery proof = PENDING
```

## Remaining work

1. Validate and merge the deterministic publication event request seam.
2. Route the exact request into the existing sovereign/canonical EVENT_EPHEMERAL runtime dispatcher without creating a new runtime owner.
3. Execute one bounded Site publication lease against retained Node continuity.
4. Independently observe its HTTPS `/intr/profile` and bind the public-profile SHA-256.
5. Perform exact HTTP byte readback/path-SHA equivalence and return the result through InTr as candidate evidence.
6. Export evidence, close the lease, retain closure, then separately admit the final publication transition.
7. Perform `stegverse.org` DNS/TLS recovery proof only after content equivalence.
8. At release readiness, tag/release and create downstream propagation verification for StegVerse-Labs/Sit, GCAT-BCAT-Engine/Publisher, admissibility-wiki, and stegguardian-wiki.

## Manual work

None.
