# CACS Mirror Handoff

## Source of truth

This file is the authoritative continuation record for Claim–Artifact Correspondence Standard work in `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` and grants no Site activation, execution, publication, custody, admissibility, or release authority.

## Goal

Create a normative, machine-readable, lifecycle-aware standard that prevents public claims from exceeding the evidence actually produced at a declared scope.

## Implemented contract

```text
Claim and Claim Review schemas
multidimensional evidence profiles
mandatory scope, falsification, and not_established boundaries
supported and overstated vectors
supersession, withdrawal, and stale-evidence lifecycle vectors
partially-supported and disputed evidence vectors
closed succession-chain validation
fail-closed public projection packet
current, historical, disputed, stale, withdrawn, unsupported, and overstated display classes
synchronized human-readable and raw governed Site views
invalid projection rejection corpus
Publisher-bound outbound handoff
canonical Site application-validation binding
```

## Implemented files

```text
docs/CLAIM_ARTIFACT_CORRESPONDENCE_STANDARD.md
schemas/cacs-claim.schema.json
schemas/cacs-claim-review.schema.json
schemas/cacs-public-projection.schema.json

data/cacs-claim.fixture.json
data/cacs-overstated-claim.fixture.json
data/cacs-superseding-claim.fixture.json
data/cacs-withdrawn-claim.fixture.json
data/cacs-stale-evidence-claim.fixture.json
data/cacs-partially-supported-claim.fixture.json
data/cacs-disputed-claim.fixture.json

data/cacs-claim-review-supported.fixture.json
data/cacs-claim-review-overstated.fixture.json
data/cacs-claim-review-superseding.fixture.json
data/cacs-claim-review-withdrawn.fixture.json
data/cacs-claim-review-stale-evidence.fixture.json
data/cacs-claim-review-partially-supported.fixture.json
data/cacs-claim-review-disputed.fixture.json

data/cacs-public-projection.fixture.json
data/cacs-public-projection-partially-supported.fixture.json
data/cacs-public-projection-disputed.fixture.json
data/cacs-public-projection-invalid-duplicate.fixture.json
data/cacs-public-projection-invalid-withdrawn-current.fixture.json
data/cacs-public-projection-invalid-stale-unqualified.fixture.json
data/cacs-public-projection-invalid-unsupported-current.fixture.json

scripts/check_cacs_claims.py
scripts/check_cacs_public_projection.py
scripts/check_cacs_dispute_partial.py
scripts/check_ecosystem_chat_application.py

cacs-claims.html
assets/cacs-claims.js
docs/CACS_PUBLISHER_PROJECTION_HANDOFF.md
docs/CACS_MIRROR_HANDOFF.md
```

## Evidence-status and projection rules

```text
SUPPORTED
- may be current only at the declared scope
- scope_correspondent must be ESTABLISHED
- unestablished dimensions remain visible

PARTIALLY_SUPPORTED
- may be current only when scope_correspondent remains ESTABLISHED
- must be visibly labeled partial
- every partial and unestablished dimension remains visible
- cannot be labeled fully supported, verified, universal, or complete

DISPUTED
- disputed dimensions remain DISPUTED in Claim and Review records
- scope-disputed Claims cannot be selected as current
- public history uses DISPUTED_HISTORY
- dispute reason must remain visible
- cannot be presented as confirmed, verified, or current assurance

SUPERSEDED OR STALE
- preserved as qualified history
- never presented as the active current Claim

WITHDRAWN, UNSUPPORTED, OR OVERSTATED
- suppressed or quarantined from active publication
```

A public projection selection is not publication authorization. A browser render is not custody. A public label is not proof. A preview hash is not cryptographic verification. A Review disposition has `authority_effect = NONE`.

## Validation

`scripts/check_cacs_claims.py` validates core Claim, Review, lifecycle, succession, withdrawal, stale-evidence, and correspondence rules.

`scripts/check_cacs_public_projection.py` validates the canonical projection and deterministic rejection of duplicate classification, withdrawn-current selection, unsupported-current selection, and unqualified stale publication.

`scripts/check_cacs_dispute_partial.py` validates:

```text
partially-supported Claim and Review linkage
qualified-publication disposition
visible partial-support labeling
prohibition on full-support labeling
scope correspondence required for a partial current Claim
DISPUTED evidence preservation in Claim and Review
DISPUTED_HISTORY public classification
dispute visibility
prohibition on disputed-current selection
prohibition on confirmed or current-assurance mislabeling
authority_effect = NONE
```

All three validators are bound into `scripts/check_ecosystem_chat_application.py`. Implementation and binding are not observed CI passage or deployed-browser verification.

## Current posture

```text
Standard status: DRAFT
Version: 0.1.0
Core schemas and fixtures: IMPLEMENTED
Lifecycle vectors: IMPLEMENTED
Invalid projection corpus: IMPLEMENTED
Partially-supported vector: IMPLEMENTED
Disputed vector: IMPLEMENTED
Human/raw synchronized projection: IMPLEMENTED
Canonical application binding: IMPLEMENTED; CI OBSERVATION PENDING
Public browser execution: NOT YET OBSERVED
Independent reproduction: NOT YET OBSERVED
Cryptographic canonicalization/hash/signature contract: NOT YET IMPLEMENTED
Primary Site navigation: NOT YET IMPLEMENTED
Publisher destination projection: NOT YET IMPLEMENTED
Admissibility projection: NOT YET IMPLEMENTED
Guardian projection: NOT YET IMPLEMENTED
Master-Records custody: NOT YET IMPLEMENTED
Authority effect: NONE
Release authorization: NONE
```

## Downstream status

`docs/CACS_PUBLISHER_PROJECTION_HANDOFF.md` defines the bounded outbound contract. `GCAT-BCAT-Engine/Publisher` is accessible, but repository search did not identify a destination-owned `*_MIRROR_HANDOFF.md`; no destination mutation is authorized until one is created or identified and confirmed not to displace the active Publisher goal.

The same handoff-first rule applies to `StegVerse-Labs/admissibility-wiki` and `StegVerse-002/stegguardian-wiki`.

Potential later custody destination: `master-records/orchestration`, which may validate hashes, signatures, references, and succession chains and return reconstruction receipts without granting claim validity or execution authority.

## Next executable step

Implement the cryptographic canonicalization boundary without treating preview markers as proof:

```text
1. Define canonical JSON serialization for Claim, Claim Review, and public projection objects.
2. Define hash input exclusions and immutable fields.
3. Add deterministic canonicalization fixtures and expected SHA-256 values.
4. Add a dependency-free verifier that rejects mutation, key reordering ambiguity, invalid hashes, and unsupported signature claims.
5. Preserve signature state as NOT_VERIFIED until a real signing and trust-root path exists.
6. Bind the verifier into canonical Site application validation.
7. Add navigation to cacs-claims.html from the primary governed Site surfaces.
```

## Release posture

No tag or release is authorized. Draft adoption remains blocked on observed CI and deployed-browser verification, independent reproduction, cryptographic verification, downstream projections, and custody integration.

## Archive readiness

This handoff, the normative standard, schemas, fixtures, validators, synchronized Site view, Publisher outbound handoff, canonical validation binding, and repository history preserve continuation state without requiring this conversation.
