# CACS Publisher Projection Handoff

## Status

```text
Source: StegVerse-Labs/Site
Destination: GCAT-BCAT-Engine/Publisher
Destination repository: VERIFIED ACCESSIBLE
Destination *_MIRROR_HANDOFF.md: NOT FOUND BY REPOSITORY SEARCH
Destination mutation authorized by this handoff: NO
Authority effect: NONE
```

This is an outbound preparation record. It does not mutate `GCAT-BCAT-Engine/Publisher`, grant publication authority, establish downstream ingestion, or replace a destination-owned source of truth.

## Source packet

```text
data/cacs-public-projection.fixture.json
schemas/cacs-public-projection.schema.json
scripts/check_cacs_public_projection.py
cacs-claims.html
assets/cacs-claims.js
```

The source packet selects one active bounded Claim, preserves superseded and stale history, suppresses withdrawn and overstated Claims from active publication, and exposes synchronized human-readable and raw governed projections.

## Required destination behavior

Publisher must:

1. consume only a machine-validated CACS projection packet;
2. preserve `projection_id`, `claim_id`, and `review_id` values;
3. publish only `CURRENT_BOUNDED_CLAIM` as current;
4. render evidence dimensions, qualifications, and `not_established` boundaries with the Claim;
5. preserve `SUPERSEDED_HISTORY`, `STALE_HISTORY`, and `DISPUTED_HISTORY` as visibly qualified history;
6. suppress `WITHDRAWN_SUPPRESSED`, `OVERSTATED_QUARANTINED`, and `UNSUPPORTED_QUARANTINED` from current publication;
7. fail closed when the packet, identifiers, required qualifications, or validation evidence are missing;
8. emit a publication projection receipt without claiming custody, admissibility, execution authority, or release authority.

## Required rejection behavior

Publisher must reject or quarantine any packet that:

```text
classifies one Claim in multiple projection classes
selects a withdrawn Claim as current
selects an unsupported or overstated Claim as current
publishes stale evidence without explicit stale, expired, or historical qualification
removes not_established boundaries
changes stable Claim or Review identifiers
asserts authority_effect other than NONE
```

The Site validator currently contains deterministic negative vectors for the first four conditions.

## Destination precondition

Before any mutation of `GCAT-BCAT-Engine/Publisher`:

```text
1. locate and read the destination repository's authoritative continuation or mirror handoff;
2. if none exists, create a destination-owned handoff that declares its current goal and authority boundary;
3. verify the proposed CACS work does not displace an active destination task;
4. bind the projection validator into the destination's canonical validation path;
5. retain the first exact downstream ingestion or rendering failure.
```

## Non-claims

This handoff does not establish:

- successful Publisher ingestion;
- deployed publication rendering;
- independent reproduction;
- cryptographic authenticity;
- Master-Records custody;
- claim validity beyond the bounded Site fixture;
- publication, execution, admissibility, or release authority.

## Next executable action

Create or identify a destination-owned `*_MIRROR_HANDOFF.md` in `GCAT-BCAT-Engine/Publisher`, then implement a fail-closed consumer and renderer against the CACS source packet without changing the source identifiers or authority boundaries.
