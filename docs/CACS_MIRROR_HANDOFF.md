# CACS Mirror Handoff

## Source of truth

This file is the current continuation record for the Claim–Artifact Correspondence Standard work in `StegVerse-Labs/Site`. It is subordinate to `docs/SITE_MIRROR_HANDOFF.md` and does not alter Site activation, execution, publication, custody, admissibility, or release authority.

## Goal

Create a normative, machine-readable, lifecycle-aware standard that prevents public claims from exceeding the evidence actually produced at a declared scope.

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
data/cacs-claim-review-supported.fixture.json
data/cacs-claim-review-overstated.fixture.json
data/cacs-claim-review-superseding.fixture.json
data/cacs-claim-review-withdrawn.fixture.json
data/cacs-claim-review-stale-evidence.fixture.json
data/cacs-public-projection.fixture.json
data/cacs-public-projection-invalid-duplicate.fixture.json
data/cacs-public-projection-invalid-withdrawn-current.fixture.json
data/cacs-public-projection-invalid-stale-unqualified.fixture.json
data/cacs-public-projection-invalid-unsupported-current.fixture.json
scripts/check_cacs_claims.py
scripts/check_cacs_public_projection.py
cacs-claims.html
assets/cacs-claims.js
scripts/check_ecosystem_chat_application.py
docs/CACS_PUBLISHER_PROJECTION_HANDOFF.md
docs/CACS_MIRROR_HANDOFF.md
```

## Implemented behavior

```text
Normative Claim–Artifact correspondence rule
Governed Claim and Claim Review objects
Mandatory not_established boundary
Multidimensional evidence profile
Scope and falsification obligations
Supported, overstated, superseding, withdrawn, and stale lifecycle vectors
Closed succession-chain and withdrawal validation
Stale-evidence qualification validation
Fail-closed public projection schema and fixture
Exactly one current bounded Claim projection
Superseded and stale historical projection
Withdrawn and overstated active-publication suppression
Stable Claim and Review identifiers
Synchronized human-readable and raw governed views
Fail-closed browser behavior when the projection packet is unavailable
Dependency-free structural, semantic, lifecycle, and projection validators
Deterministic rejection of duplicate classification
Deterministic rejection of withdrawn-current selection
Deterministic rejection of unsupported-current selection
Deterministic rejection of unqualified stale publication
Both CACS validators bound into canonical Site application validation
Publisher-bound outbound handoff prepared without destination mutation
```

## Current posture

```text
Standard status: DRAFT
Version: 0.1.0
Claim schema: IMPLEMENTED
Claim Review schema: IMPLEMENTED
Public projection schema: IMPLEMENTED
Lifecycle fixtures: IMPLEMENTED
Claim lifecycle validator: IMPLEMENTED
Public projection validator: IMPLEMENTED
Invalid public-projection regression vectors: IMPLEMENTED
Human/raw synchronized projection: IMPLEMENTED
Canonical application validation binding: IMPLEMENTED; CI OBSERVATION PENDING
Public browser execution: NOT YET OBSERVED
Independent correspondence reproduction: NOT YET OBSERVED
Cryptographic hash/signature contract: NOT YET IMPLEMENTED
Publisher outbound handoff: IMPLEMENTED
Publisher destination-owned mirror handoff: NOT FOUND BY REPOSITORY SEARCH
Publisher projection: NOT YET IMPLEMENTED
Admissibility projection: NOT YET IMPLEMENTED
Guardian projection: NOT YET IMPLEMENTED
Master-Records custody: NOT YET IMPLEMENTED
Authority effect: NONE
Release authorization: NONE
```

## Public projection contract

The canonical packet is `data/cacs-public-projection.fixture.json`. Human-readable and raw governed views resolve to this same packet through `cacs-claims.html` and `assets/cacs-claims.js`.

```text
CURRENT_BOUNDED_CLAIM
- active lifecycle only
- supported or partially supported only
- scope_correspondent = ESTABLISHED
- mandatory not_established boundaries
- mandatory visible qualifications

HISTORICAL
- SUPERSEDED_HISTORY
- STALE_HISTORY
- DISPUTED_HISTORY

SUPPRESSED FROM ACTIVE PUBLICATION
- WITHDRAWN_SUPPRESSED
- OVERSTATED_QUARANTINED
- UNSUPPORTED_QUARANTINED
```

A projection selection is not publication authorization. A browser render is not custody. A public label is not proof. A preview hash is not cryptographic verification. A review disposition grants no execution, publication, custody, admissibility, or release authority.

## Validation contract

`scripts/check_cacs_claims.py` validates Claim and Review structure, evidence vocabularies, bounded support, negative overstatement, stable references, succession chains, withdrawal handling, stale evidence, and lifecycle dispositions.

`scripts/check_cacs_public_projection.py` validates:

```text
closed public packet shape
authority_effect = NONE
one current active bounded Claim
scope correspondence for current publication
mandatory non-claims and qualifications
required superseded and stale historical classes
required withdrawn and overstated suppression classes
no Claim appearing in multiple projection classes
explicit stale, expired, or historical qualification for stale evidence
presence of synchronized human/raw Site surfaces
renderer consumption of active, historical, and suppressed packet sections
expected rejection reason for every invalid regression packet
```

Invalid regression corpus:

```text
cacs-public-projection-invalid-duplicate.fixture.json
  -> reject duplicate projection classification
cacs-public-projection-invalid-withdrawn-current.fixture.json
  -> reject non-active current Claim
cacs-public-projection-invalid-stale-unqualified.fixture.json
  -> reject stale history without explicit stale/expired qualification
cacs-public-projection-invalid-unsupported-current.fixture.json
  -> reject unsupported current Claim
```

Local implementation and aggregate binding do not constitute observed CI passage, public deployment, independent reproduction, custody, downstream ingestion, or release authority.

## Publisher-bound preparation

`GCAT-BCAT-Engine/Publisher` was verified accessible. Repository search did not locate a destination-owned `*_MIRROR_HANDOFF.md`. Therefore no Publisher mutation was performed.

`docs/CACS_PUBLISHER_PROJECTION_HANDOFF.md` preserves:

```text
source packet paths
required Publisher rendering and suppression behavior
required downstream rejection behavior
stable identifier requirements
destination preconditions
non-claims and authority boundaries
```

The outbound handoff is preparation only. It is not Publisher ingestion, deployment, validation, or publication authorization.

## Remaining work by destination

Destination `StegVerse-Labs/Site`:

```text
Observe both CACS validators in canonical application CI
Observe cacs-claims.html browser execution after deployment
Add disputed and partially-supported projection vectors
Add cryptographic canonicalization, hash, and signature contract
Add navigation from the primary governed Site surfaces
Update docs/SITE_MIRROR_HANDOFF.md after machine verification
```

Destination `GCAT-BCAT-Engine/Publisher`:

```text
Create or identify a destination-owned *_MIRROR_HANDOFF.md before mutation
Verify CACS does not displace the active Publisher goal
Consume only machine-validated CACS Site projection packets
Render evidence dimensions and not_established boundaries
Publish only the active bounded Claim as current
Preserve superseded and stale history with visible qualification
Suppress or quarantine withdrawn, unsupported, and overstated Claims
Preserve stable Claim, Review, and projection identifiers
Emit a bounded publication projection receipt with authority_effect = NONE
```

Destination `StegVerse-Labs/admissibility-wiki`:

```text
Create or verify *_MIRROR_HANDOFF.md before mutation
Document Claim admissibility separately from execution admissibility
Define correspondence and lifecycle interpretations
Preserve review and publication authority boundaries
```

Destination `StegVerse-002/stegguardian-wiki`:

```text
Create or verify *_MIRROR_HANDOFF.md before mutation
Document reviewer, dispute, quarantine, withdrawal, stale-evidence, and supersession roles
Prevent review state from granting execution or publication authority
```

Potential later destination `master-records/orchestration`:

```text
Custody canonical Claim, Claim Review, and public projection objects
Validate canonical hashes, signatures, references, and succession chains
Return reconstruction receipts without granting claim validity or execution authority
```

## Next executable step

Add disputed and partially-supported Claim, Review, and public-projection vectors, including explicit public qualification and dispute visibility. Extend both CACS validators so those vectors cannot be mislabeled as fully supported. In parallel, create or identify a destination-owned Publisher mirror handoff before any Publisher mutation.

## Release posture

No tag or release is authorized. Draft adoption remains blocked on observed CI and deployed-browser verification, disputed and partially-supported vectors, independent reproduction, downstream projections, and cryptographic custody integration.

## Archive readiness

This handoff, normative standard, schemas, lifecycle and projection fixtures, invalid regression corpus, validators, synchronized Site view, Publisher outbound handoff, canonical validation binding, and repository history preserve all continuation state without requiring this conversation.
