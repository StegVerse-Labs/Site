# Site #497 StegGate Dependency Reconciliation Mirror Handoff

Updated: 2026-09-10
Repository: `StegVerse-Labs/Site`
Goal: `KV-CONNECTION-REVALIDATION-WORKER-001`
Site lane: `SITE-497-THIRD-PARTY-DEPENDENCY-ERADICATION`
COSV: `50000000102000`
Upstream handoff: `StegVerse-Labs/StegCore/docs/STEGGATE_HOSTED_CARRIER_RETIREMENT_MIRROR_HANDOFF.md`
Current continuation: sovereign dispatcher claim/consumer for Site publication event materialization

## Merged provider-independent evidence

- PR #1155 merged external recovery retention/restore/validation for archive SHA-256 `a9b81dfb7a34e7b4c627145e6ab817466b92c1ea9176fc41f76e420a2b201b0f` with 3400 verified entries.
- PR #1158 merged provider-neutral `STEGVERSE_SITE_STATIC_PUBLICATION_V1` materialization and exact validation.
- PR #1162 merged the fail-closed publication-observation evidence seam.
- PR #1168 merged the no-Render remediation at `9d9ffb7ef5cee256588dcdd3790846b5943867da`.
- PR #1212 merged at `11c574ad51ce0cd3a4a615eb66652879bd7f2a0a`, removing stale Render requirements and adding the publication rendezvous seam.
- PR #1214 merged at `161ac14b10bc69b9f8c3d5b68362f10501f59908`, binding publication to Node/Interlock/InTr exchange semantics.
- PR #1216 merged at `7a94ce3c0d2df60c8974299ac074572021812fab`, reconciling runtime evidence.
- PR #1221 merged at `f36b8aef3da40ed5e43b8a7e3b84e40904b37869`, correcting Site to the proven canonical `EVENT_EPHEMERAL` fabric while retaining persistent Node continuity.
- PR #1222 merged at `e73ced90a9f466bd559ec7eb88e0f4bf069be826` after all five exact-head gates passed, adding the deterministic Site publication event request/materialization seam.

## No-hosted-origin invariant

Render remains prohibited for Site #497. `selected_origin=null`; no hosted publication origin is canonical or admissible.

## Canonical event-ephemeral runtime

Canonical StegOS runtime evidence proves the reusable bounded lifecycle with persistent Node identity/continuity but no persistent host, always-on receiver, or second user-operated device requirement. Site publication requires its own bounded event and independent public HTTPS verification.

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

## Merged publication event request seam

`scripts/build_site_publication_event_request.py` and `scripts/check_site_publication_event_request.py` are now merged/source-validated. They deterministically:

1. materialize `STEGVERSE_SITE_STATIC_PUBLICATION_V1`;
2. hash exact `manifest.json` bytes;
3. build canonical `stegverse.universal-intr-transport/v1` operation `SITE_PUBLICATION_EVENT`;
4. derive `stegverse.universal-intr-materialization-request/v1` with state `QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION`;
5. preserve the exact manifest SHA-256 through envelope, transport and materialization identities;
6. target `StegVerse-Labs/StegOS:canonical-runtime-lane`;
7. grant no execution authority, claim/fence, credential transfer, or canonical publication standing.

The source request seam is complete. A queued materialization request remains non-runtime evidence until consumed by the sovereign dispatcher.

## Dispatcher continuation boundary

The existing `.github` sovereign runtime already contains task-specific materialization consumers such as HIL and Device/KV. The HIL consumer must not be repurposed because it is intentionally bound to `HIL:Ingress`, HIL ingress receipts, the HIL ESRL bridge, and its admitted HIL task.

The parent `KV-CONNECTION-REVALIDATION-WORKER-001` registry currently remains `HANDOFF_READY` with `claim_id=null` and explicitly requires a fresh independent claim; parent-claim reuse is prohibited. Therefore the next `.github` implementation is a fresh claimed Site-publication materialization consumer/dispatcher binding, not an unclaimed mutation of the parent runtime.

## README maintenance

Root `README.md` was reviewed during the source continuation. Its provider-independent runtime/publication boundary remains accurate.

## Current truth

```text
canonical reusable runtime fabric = EVENT_EPHEMERAL / OBSERVED_END_TO_END
Site EVENT_EPHEMERAL runtime correction = MERGED_SOURCE_VALIDATED
Site publication event request adapter = MERGED_SOURCE_VALIDATED
publication event materialization request schema = stegverse.universal-intr-materialization-request/v1
parent worker registry = HANDOFF_READY / fresh independent claim required
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

1. Establish a fresh independent `.github` claim for the Site publication materialization consumer under this goal/COSV; do not reuse the parent claim.
2. Implement the Site-specific consumer in the existing sovereign dispatcher, validating destination `STEGOS_ECOSYSTEM / StegOS:SitePublicationRuntime` and the exact `SITE_PUBLICATION_EVENT` request before invoking the canonical runtime lane.
3. Execute one bounded Site publication lease against retained Node continuity.
4. Independently observe HTTPS `/intr/profile` and bind public-profile SHA-256.
5. Perform exact HTTP byte readback/path-SHA equivalence and return candidate evidence through InTr.
6. Export evidence, close the lease, retain closure, then separately admit the final publication transition.
7. Perform `stegverse.org` DNS/TLS recovery proof only after content equivalence.
8. At release readiness, tag/release and create downstream propagation verification for StegVerse-Labs/Sit, GCAT-BCAT-Engine/Publisher, admissibility-wiki, and stegguardian-wiki.

## Manual work

None.
