# CACS Mirror Handoff

## Source of truth

This file is the current continuation record for the Claim–Artifact Correspondence Standard work in `StegVerse-Labs/Site`. It is subordinate to `docs/SITE_MIRROR_HANDOFF.md` for the Site activation goal and must not alter that goal's authority or release posture.

## Goal

Create a normative and machine-readable standard that prevents claims from exceeding the evidence actually produced at a declared scope.

## Implemented files

```text
docs/CLAIM_ARTIFACT_CORRESPONDENCE_STANDARD.md
schemas/cacs-claim.schema.json
schemas/cacs-claim-review.schema.json
data/cacs-claim.fixture.json
data/cacs-overstated-claim.fixture.json
data/cacs-claim-review-supported.fixture.json
data/cacs-claim-review-overstated.fixture.json
scripts/check_cacs_claims.py
scripts/check_ecosystem_chat_application.py
docs/CACS_MIRROR_HANDOFF.md
```

## Implemented behavior

```text
Normative claim-artifact correspondence rule
Governed Claim object definition
Governed Claim Review object definition
Mandatory not_established boundary
Multidimensional evidence profile
Artifact-class permitted-conclusion boundaries
Scope declaration requirements
Falsification obligations
Correspondence review outcomes
Fail-closed public labeling rule
StegVerse authority-boundary integration
Draft JSON Schema for Claim objects
Draft JSON Schema for Claim Review objects
Bounded supported Claim fixture
Overstated Claim negative fixture
Supported and overstated Claim Review fixtures
Dependency-free structural and semantic validator
Stable claim-to-review linkage validation
Overstated-claim quarantine validation
CACS validator bound into canonical Site application validation
```

## Current posture

```text
Standard status: DRAFT
Version: 0.1.0
Machine-readable claim schema: IMPLEMENTED
Machine-readable Claim Review schema: IMPLEMENTED
Supported fixture: IMPLEMENTED
Overstated fixture: IMPLEMENTED
Supported review fixture: IMPLEMENTED
Overstated review fixture: IMPLEMENTED
Dependency-free validator: IMPLEMENTED
Canonical application validation binding: IMPLEMENTED; CI OBSERVATION PENDING
Independent correspondence reproduction: NOT YET OBSERVED
Versioning and supersession vectors: NOT YET IMPLEMENTED
Stale-evidence vectors: NOT YET IMPLEMENTED
Human/raw claim projection: NOT YET IMPLEMENTED
Publisher projection: NOT YET IMPLEMENTED
Admissibility projection: NOT YET IMPLEMENTED
Guardian projection: NOT YET IMPLEMENTED
Authority effect: NONE
Release authorization: NONE
```

## Validation contract

`scripts/check_cacs_claims.py` verifies:

```text
required Claim and Claim Review fields
closed object shapes for governed fixtures
allowed correspondence statuses
evidence-dimension and review-finding vocabularies
mandatory scope_correspondent dimension
mandatory falsification conditions
mandatory not_established boundaries
bounded supported-claim correspondence
universal or overbroad assertion detection for the negative vector
overstated status and quarantine disposition
stable Claim-to-Claim-Review references
unique claim_id and review_id values
authority_effect = NONE for reviews
```

The validator is dependency-free and is executed by `scripts/check_ecosystem_chat_application.py`. Local implementation and aggregate binding do not constitute observed CI execution, independent reproduction, publication approval, or release authority.

## Remaining work by destination

Destination `StegVerse-Labs/Site`:

```text
Observe CACS validation in canonical application CI
Add versioning, supersession, withdrawal, and stale-evidence Claim and Review vectors
Add cryptographic hash and signature contract without treating preview markers as proof
Expose human-readable and raw governed claim projections
Add public display rules for qualifications, disputes, supersession, and withdrawal
Update docs/SITE_MIRROR_HANDOFF.md after machine verification
```

Destination `GCAT-BCAT-Engine/Publisher`:

```text
Add claim publication projection
Render evidence dimensions and not_established boundaries
Reject or visibly qualify unsupported, overstated, stale, or disputed claims
Preserve stable claim and review identifiers
Consume only machine-validated Site projection packets
```

Destination `StegVerse-Labs/admissibility-wiki`:

```text
Document claim admissibility separately from execution admissibility
Define correspondence status interpretation
Preserve review authority boundaries
Document that claim review does not grant execution authority
```

Destination `StegVerse-002/stegguardian-wiki`:

```text
Document guardian review and dispute roles
Define claim quarantine, withdrawal, and supersession handling
Prevent review status from granting execution or publication authority
```

Potential later destination `master-records/orchestration`:

```text
Custody canonical Claim and Claim Review objects
Validate hashes, signatures, references, and supersession chains
Return reconstruction receipts without granting claim validity or execution authority
```

## Next executable step

Add versioned Claim and Claim Review fixtures covering supersession, withdrawal, and stale evidence; extend the validator to enforce closed succession chains, prohibit active publication of withdrawn claims, and require explicit qualification when evidence becomes stale.

## Release posture

No tag or release is authorized. Draft adoption criteria remain incomplete: observed machine validation, independent reproduction, versioning and stale-evidence tests, governed public projections, downstream projections, and cryptographic custody integration.

## Archive readiness

This handoff, the normative standard, schemas, fixtures, validator, canonical application binding, and repository commit history preserve the current CACS continuation state without requiring conversation context.
