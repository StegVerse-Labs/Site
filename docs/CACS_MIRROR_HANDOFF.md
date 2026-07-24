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
scripts/check_cacs_claims.py
scripts/check_cacs_public_projection.py
cacs-claims.html
assets/cacs-claims.js
scripts/check_ecosystem_chat_application.py
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
Both CACS validators bound into canonical Site application validation
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
Human/raw synchronized projection: IMPLEMENTED
Canonical application validation binding: IMPLEMENTED; CI OBSERVATION PENDING
Public browser execution: NOT YET OBSERVED
Independent correspondence reproduction: NOT YET OBSERVED
Cryptographic hash/signature contract: NOT YET IMPLEMENTED
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
presence of synchronized human/raw Site surfaces
renderer consumption of active, historical, and suppressed packet sections
```

Local implementation and aggregate binding do not constitute observed CI passage, public deployment, independent reproduction, custody, downstream ingestion, or release authority.

## Remaining work by destination

Destination `StegVerse-Labs/Site`:

```text
Observe both CACS validators in canonical application CI
Observe cacs-claims.html browser execution after deployment
Add invalid public-projection regression fixtures
Add disputed and partially-supported projection vectors
Add cryptographic canonicalization, hash, and signature contract
Add navigation from the primary governed Site surfaces
Update docs/SITE_MIRROR_HANDOFF.md after machine verification
```

Destination `GCAT-BCAT-Engine/Publisher`:

```text
Create or verify *_MIRROR_HANDOFF.md before mutation
Consume only machine-validated CACS Site projection packets
Render evidence dimensions and not_established boundaries
Publish only the active bounded Claim as current
Preserve superseded and stale history with visible qualification
Suppress or quarantine withdrawn, unsupported, and overstated Claims
Preserve stable Claim, Review, and projection identifiers
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

Add invalid projection regression vectors for duplicate classification, withdrawn-current selection, unqualified stale publication, and unsupported-current selection. Extend `scripts/check_cacs_public_projection.py` so each invalid packet is deterministically rejected. Then create the Publisher-bound projection handoff only after checking the Publisher repository handoff source of truth.

## Release posture

No tag or release is authorized. Draft adoption remains blocked on observed CI and deployed-browser verification, invalid-vector rejection, independent reproduction, downstream projections, and cryptographic custody integration.

## Archive readiness

This handoff, normative standard, schemas, lifecycle and projection fixtures, validators, synchronized Site view, canonical validation binding, and repository history preserve all continuation state without requiring this conversation.
