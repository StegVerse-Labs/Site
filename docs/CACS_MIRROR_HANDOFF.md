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
data/cacs-superseding-claim.fixture.json
data/cacs-withdrawn-claim.fixture.json
data/cacs-stale-evidence-claim.fixture.json
data/cacs-claim-review-supported.fixture.json
data/cacs-claim-review-overstated.fixture.json
data/cacs-claim-review-superseding.fixture.json
data/cacs-claim-review-withdrawn.fixture.json
data/cacs-claim-review-stale-evidence.fixture.json
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
Superseding Claim lifecycle fixture
Withdrawn Claim lifecycle fixture
Stale-evidence Claim lifecycle fixture
Supported, overstated, superseding, withdrawn, and stale Claim Review fixtures
Dependency-free structural, semantic, and lifecycle validator
Stable Claim-to-Claim-Review linkage validation
Overstated-claim quarantine validation
Closed supersession-reference validation
Withdrawal reason and withdrawal disposition validation
Evidence-valid-through expiration validation
Stale-evidence qualified-publication validation
CACS validator bound into canonical Site application validation
```

## Current posture

```text
Standard status: DRAFT
Version: 0.1.0
Machine-readable Claim schema: IMPLEMENTED
Machine-readable Claim Review schema: IMPLEMENTED
Supported fixture: IMPLEMENTED
Overstated fixture: IMPLEMENTED
Supersession vector: IMPLEMENTED
Withdrawal vector: IMPLEMENTED
Stale-evidence vector: IMPLEMENTED
Dependency-free validator: IMPLEMENTED
Canonical application validation binding: IMPLEMENTED; CI OBSERVATION PENDING
Independent correspondence reproduction: NOT YET OBSERVED
Human/raw claim projection: NOT YET IMPLEMENTED
Public qualification renderer: NOT YET IMPLEMENTED
Cryptographic hash/signature contract: NOT YET IMPLEMENTED
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
closed governed fixture shapes
allowed correspondence, lifecycle, finding, and disposition vocabularies
mandatory scope_correspondent dimension
mandatory falsification conditions
mandatory not_established boundaries
bounded supported-claim correspondence
universal or overbroad assertion detection for the negative vector
overstated status and quarantine disposition
stable Claim-to-Claim-Review references
unique claim_id and review_id values
authority_effect = NONE for reviews
known and non-self-referential supersession targets
newer timestamps for superseding Claims and Reviews
single active successor per superseded Claim
active lifecycle for successor Claims
withdrawn status, reason, and review disposition
expired evidence_valid_through for stale Claims
qualified-publication disposition for stale evidence
visible historical, stale, or expired qualification language
required positive, negative, supersession, withdrawal, and stale vectors
```

The validator uses a fixed validation instant for deterministic stale-evidence fixtures. This test clock is a fixture mechanism and is not runtime time authority. Local implementation and aggregate binding do not constitute observed CI execution, independent reproduction, publication approval, custody, or release authority.

## Public lifecycle rules established

```text
A superseded Claim remains historical evidence but is not the active public Claim.
A successor must identify the exact Claim it supersedes.
A Claim cannot supersede itself or an unknown Claim.
Two active successors cannot silently claim the same predecessor.
A withdrawn Claim cannot be actively published as supported.
Historical display of a withdrawn Claim must expose the withdrawal reason.
Expired evidence may remain inspectable only with explicit stale or historical qualification.
Stale historical evidence cannot establish current implementation, policy, delegation, pilot, or production assurance.
A review disposition does not grant execution, publication, custody, admissibility, or release authority.
```

## Remaining work by destination

Destination `StegVerse-Labs/Site`:

```text
Observe CACS validation in canonical application CI
Add machine-readable public projection packet and fail-closed renderer rules
Expose synchronized human-readable and raw governed Claim projections
Add dispute and supersession-chain display behavior
Add cryptographic hash and signature contract without treating preview markers as proof
Add invalid lifecycle vectors for regression rejection
Update docs/SITE_MIRROR_HANDOFF.md after machine verification
```

Destination `GCAT-BCAT-Engine/Publisher`:

```text
Add claim publication projection
Render evidence dimensions and not_established boundaries
Reject or visibly qualify unsupported, overstated, stale, withdrawn, or disputed Claims
Render only the active Claim as current while preserving superseded history
Preserve stable Claim and Review identifiers
Consume only machine-validated Site projection packets
```

Destination `StegVerse-Labs/admissibility-wiki`:

```text
Document claim admissibility separately from execution admissibility
Define correspondence and lifecycle status interpretation
Preserve review authority boundaries
Document that Claim review does not grant execution authority
```

Destination `StegVerse-002/stegguardian-wiki`:

```text
Document guardian review and dispute roles
Define Claim quarantine, withdrawal, stale-evidence, and supersession handling
Prevent review status from granting execution or publication authority
```

Potential later destination `master-records/orchestration`:

```text
Custody canonical Claim and Claim Review objects
Validate hashes, signatures, references, and supersession chains
Return reconstruction receipts without granting claim validity or execution authority
```

## Next executable step

Create a machine-readable CACS public projection fixture and validator contract that selects the active Claim, preserves superseded history, suppresses active publication of withdrawn Claims, and visibly qualifies stale, partially supported, disputed, or overstated records. Then expose the same packet through synchronized human-readable and raw governed Site views.

## Release posture

No tag or release is authorized. Draft adoption criteria remain incomplete: observed machine validation, independent reproduction, governed public projections, downstream projections, and cryptographic custody integration.

## Archive readiness

This handoff, the normative standard, schemas, lifecycle fixtures, validator, canonical application binding, and repository commit history preserve the current CACS continuation state without requiring conversation context.
