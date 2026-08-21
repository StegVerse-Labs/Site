# Ecosystem Versioning Mirror Handoff

## Scope and authority

This is the scoped continuation record for StegVerse ecosystem component versioning, repository-universe discovery, repository-role classification, and user-facing version/status projection in `StegVerse-Labs/Site`.

It is subordinate to `docs/SITE_MIRROR_HANDOFF.md`. Incoming work remains candidate workload only. This handoff grants no release, activation, runtime, publication, custody, admission, credential, route, wallet, or cross-repository authority.

```text
credential_authority: TV/TVC ONLY
GitHub token production/runtime authority: NONE
NON-TV/TVC secret/token authority: false
aggregate_release: NOT_AGGREGATELY_RELEASED
authority_effect: NONE
activation_effect: false
publication_effect: false
```

## Core lifecycle versioning milestone

Exact scope: `CORE-GOVERNED-LIFECYCLE-V1`.

Machine inventory: `data/ecosystem-version-coverage.json`.
Public projection: `ecosystem-version.html`.
Shared declaration contract: `docs/ECOSYSTEM_COMPONENT_VERSION_CONTRACT.md`.

Current verified state:

```text
core lifecycle repositories: 13
normalized VERSION.json declarations: 13/13
owner-local fail-closed validators installed: 13/13
validator-installation coverage: 100%
fully contract validated with execution/hosted evidence: false
aggregate release: NOT_AGGREGATELY_RELEASED
```

`SITE-0014-CORE-VERSION-VALIDATOR-COVERAGE` is `COMPLETE`; Site's repository controller observed `CORE_VALIDATOR_INSTALLATION=13/13`.

Version declaration and validator installation are not release, deployment, runtime proof, or activation.

## Raw ecosystem repository universe

Canonical raw-universe ledger: `data/ecosystem-repository-universe.json`.
Validator: `scripts/check_ecosystem_repository_universe.py`.
Task: `data/tasks/SITE-0015-ECOSYSTEM-REPOSITORY-ENUMERATION.json`.

Machine-verified state:

```text
installed GitHub App accounts: 11/11
raw repositories enumerated: 203
StegVerse-Labs page 0 count: 100
StegVerse-Labs page 100 count: 0
raw repository enumeration: COMPLETE
repository classification: INCOMPLETE
full active-version denominator: NOT ESTABLISHED
```

`SITE-0015-ECOSYSTEM-REPOSITORY-ENUMERATION` is `COMPLETE`; the controller observed `RAW_REPOSITORIES_ENUMERATED=203`.

Raw enumeration must never be interpreted as 203 standalone product components. Repository role, current handoff authority, legacy/mirror status, and version obligation must be resolved first.

## Repository classification contract

Canonical classification ledger: `data/ecosystem-repository-classification.json`.
Validator: `scripts/check_ecosystem_repository_classification.py`.
Task: `data/tasks/SITE-0016-REPOSITORY-CLASSIFICATION-WAVE-1.json`.

Allowed classes:

```text
ACTIVE_COMPONENT
RESEARCH_FORMALISM
MIRROR_LEGACY
TELEMETRY_SUPPORT
CONTROL_METADATA
UNCLASSIFIED
```

Classification requires repository-local handoff, boundary documentation, or current live authority evidence. Repository names alone are insufficient.

Current machine-verified first-wave state:

```text
raw denominator: 203
records evaluated: 18
resolved classifications: 16
evaluated but explicitly UNCLASSIFIED: 2
not yet evaluated: 185
active components identified: 8
telemetry/support identified: 6
control metadata identified: 2
research/formalism identified: 0
mirror/legacy resolved: 0
full active-version denominator established: false
```

`SITE-0016-REPOSITORY-CLASSIFICATION-WAVE-1` is `COMPLETE`; Site's repository controller observed `REPOSITORY_CLASSIFICATION_EVALUATED=18/203`.

## Resolved families

### TV / TVC

```text
StegVerse-Labs/TV   -> ACTIVE_COMPONENT
StegVerse-Labs/TVC  -> ACTIVE_COMPONENT
StegVerse-org/TV    -> CONTROL_METADATA
StegVerse-org/TVC   -> CONTROL_METADATA
```

The Labs repositories are the current policy/credential and route/admission authority components. The similarly named `StegVerse-org` repositories are bounded private TrustVault/control-material surfaces and do not replace the Labs authorities.

### Core-Lite

Distinct active scoped components:

```text
Data-Continuation/core-lite
StegVerse-002/core-lite
Admissible-Existence/core-lite
master-records/core-lite
GCAT-BCAT-Engine/core-lite
GCAT-BCAT-Engine/core-lite-prod
```

They are not treated as one duplicate component; each repository documents a different scoped role.

Fail-closed unresolved:

```text
StegVerse-002/legacy_core_lite
  blocker: CURRENT_MIRROR_HANDOFF_NOT_FOUND
  posture: legacy candidate only; do not classify from name

formalism-tests/core-lite
  blocker: INSUFFICIENT_SOURCE_OF_TRUTH
  posture: do not infer active, test-support, or mirror role from minimal README
```

### Telemetry

All six observed telemetry repositories are `TELEMETRY_SUPPORT`, not standalone product authorities:

```text
Admissible-Existence/telemetry
GCAT-BCAT-Engine/telemetry
master-records/telemetry
StegGhost/telemetry
StegVerse-Labs/telemetry
StegVerse-org/telemetry
```

Their version obligation is schema/data versioning, not a standalone product-release version.

## Public user experience

`ecosystem-version.html` currently exposes:

```text
13/13 core version declarations
13/13 owner-local version validators installed
203/203 raw repositories enumerated
18 evaluated
16 resolved
2 fail-closed unresolved
```

The page intentionally states that the full active-component version denominator is not yet established.

## Next required classification work

Highest-priority continuation after collision check:

1. Classify organization `.github` control/coordination repositories from their current handoffs, without treating control-plane source completeness as product activation.
2. Reconcile mirrored formalism families across `Admissible-Existence` and `formalism-tests` as research/provenance surfaces before assigning version obligations.
3. Classify the broad `StegVerse-Labs` application/service set by current repository handoffs: Site-adjacent user products, runtimes, authorities, finance/payment surfaces, media/music surfaces, observatories/research, support/control, legacy/mirrors, and empty/bootstrap repositories.
4. For every newly resolved `ACTIVE_COMPONENT`, inspect existing version identity before adding `VERSION.json`; do not overwrite repository-native product/research version domains.
5. For `RESEARCH_FORMALISM`, prefer artifact/schema/research version contracts where a standalone product semantic version would misrepresent the repository.
6. For `CONTROL_METADATA` and `TELEMETRY_SUPPORT`, require protocol/schema/data identity sufficient for reconstruction without inflating the active product denominator.
7. Keep every unresolved repository fail-closed until its role is established from current evidence.
8. Establish the full active-version denominator only after all 203 repository records are resolved or explicitly excluded under a justified non-product class.
9. Then measure full active-component declaration coverage, validator coverage, immutable release/tag coverage, runtime proof, and activation as separate dimensions.

## Release and activation boundary

Never infer:

```text
raw enumeration = classification
classification = versioning
version declaration = validation
validator installed = validator passed
validation = release
release candidate = release
main branch = release
workflow pass = runtime proof
deployment = activation
component release = ecosystem aggregate release
```

The SDK remains `1.1.0 RELEASE_CANDIDATE`; its target tag/package publication remain governed TV/TVC work, not completed publication.

Ecosystem Chat activation also remains open independently of this versioning work. It still requires the fresh fenced sovereign same-carrier execution, TVC `ROUTE_ADMITTED`, exact LLM-adapter execution, measured usage, same-execution Master Records reconstruction, immutable zero-blocker receipt, Site activation, and verified downstream propagation.

## Session continuity

This versioning/classification workstream is durably recoverable from repository state without chat history.

Thread continuity may be archive-safe after this handoff is present, but the product/versioning goal itself is not complete while classification, full denominator construction, validator execution evidence, immutable aggregate release, runtime proof, and activation remain open.
