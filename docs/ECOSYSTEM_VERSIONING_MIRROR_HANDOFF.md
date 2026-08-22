# Ecosystem Versioning Mirror Handoff

## Scope and authority

Scoped continuation for StegVerse component versioning, repository-universe discovery, repository-role classification, and user-facing status projection in `StegVerse-Labs/Site`. This handoff is subordinate to `docs/SITE_MIRROR_HANDOFF.md`.

```text
credential_authority: TV/TVC ONLY
GitHub token production/runtime authority: NONE
NON-TV/TVC secret/token authority: false
aggregate_release: NOT_AGGREGATELY_RELEASED
authority_effect: NONE
activation_effect: false
publication_effect: false
```

No classification/versioning state here grants release, runtime, activation, publication, custody, admission, route, credential, wallet, or cross-repository authority.

## Core lifecycle milestone

```text
scope: CORE-GOVERNED-LIFECYCLE-V1
repositories: 13
normalized VERSION.json declarations: 13/13
owner-local fail-closed validators installed: 13/13
validator-installation machine evidence: COMPLETE
fully contract validated with hosted/executed evidence: false
aggregate release: NOT_AGGREGATELY_RELEASED
```

Sources:

```text
data/ecosystem-version-coverage.json
scripts/check_ecosystem_version_coverage.py
data/tasks/SITE-0014-CORE-VERSION-VALIDATOR-COVERAGE.json
```

`SITE-0014` is `COMPLETE`; Site's repository controller observed `CORE_VALIDATOR_INSTALLATION=13/13`.

## Raw repository universe

```text
installed GitHub App accounts: 11/11
raw repositories enumerated: 203/203
StegVerse-Labs first page: 100
StegVerse-Labs next page: 0
repository enumeration: COMPLETE
full active-version denominator: NOT ESTABLISHED
```

Sources:

```text
data/ecosystem-repository-universe.json
scripts/check_ecosystem_repository_universe.py
data/tasks/SITE-0015-ECOSYSTEM-REPOSITORY-ENUMERATION.json
```

`SITE-0015` is `COMPLETE`; controller marker `RAW_REPOSITORIES_ENUMERATED=203` was observed. Raw enumeration is not a 203-product denominator.

## Classification architecture

Base ledger:

```text
data/ecosystem-repository-classification.json
```

Append-only wave manifests:

```text
data/ecosystem-repository-classification-wave-4.json
future: data/ecosystem-repository-classification-wave-*.json
```

Validator:

```text
scripts/check_ecosystem_repository_classification.py
```

The validator independently revalidates the machine-proven base, applies wave manifests in order, rejects repository identity duplication across waves, checks every repository against the 203-repository universe, validates class-specific version obligations, and recomputes aggregate arithmetic. This append-only model replaces risky monolithic rewrites for future waves.

Allowed classes:

```text
ACTIVE_COMPONENT
RESEARCH_FORMALISM
MIRROR_LEGACY
TELEMETRY_SUPPORT
CONTROL_METADATA
UNCLASSIFIED
```

Repository names alone are insufficient classification evidence.

## Machine-verified classification progress

```text
SITE-0016 wave 1: COMPLETE — 18 evaluated / 16 resolved / 2 UNCLASSIFIED
SITE-0017 wave 2: COMPLETE — 22 evaluated / 20 resolved / 2 UNCLASSIFIED
SITE-0018 wave 3: COMPLETE — 30 evaluated / 28 resolved / 2 UNCLASSIFIED
SITE-0019 wave 4: COMPLETE — 53 evaluated / 51 resolved / 2 UNCLASSIFIED
```

Current machine-verified aggregate:

```text
raw denominator: 203
records evaluated: 53
resolved classifications: 51
evaluated but explicitly UNCLASSIFIED: 2
not yet evaluated: 150
evaluation coverage: 26.11%
resolved classification coverage: 25.12%
active components identified: 8
research/formalism identified: 31
telemetry/support identified: 6
control metadata identified: 6
mirror/legacy resolved: 0
full active-version denominator established: false
aggregate release: NOT_AGGREGATELY_RELEASED
```

`SITE-0019` completion evidence records:

```text
ECOSYSTEM_REPOSITORY_CLASSIFICATION=PASS
CLASSIFICATION_WAVES_APPLIED=1
REPOSITORY_CLASSIFICATION_EVALUATED=53/203
REPOSITORY_CLASSIFICATION_RESOLVED=51/203
ACTIVE_COMPONENTS_IDENTIFIED=8
RESEARCH_FORMALISMS_IDENTIFIED=31
TELEMETRY_SUPPORT_IDENTIFIED=6
CONTROL_METADATA_IDENTIFIED=6
UNCLASSIFIED_EVALUATED=2
FULL_ACTIVE_VERSION_DENOMINATOR=NOT_ESTABLISHED
AGGREGATE_RELEASE=NOT_AGGREGATELY_RELEASED
AUTHORITY_EFFECT=NONE
```

## Resolved families

### TV / TVC

```text
StegVerse-Labs/TV   -> ACTIVE_COMPONENT
StegVerse-Labs/TVC  -> ACTIVE_COMPONENT
StegVerse-org/TV    -> CONTROL_METADATA
StegVerse-org/TVC   -> CONTROL_METADATA
```

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

Fail-closed unresolved:

```text
StegVerse-002/legacy_core_lite
  blocker: CURRENT_MIRROR_HANDOFF_NOT_FOUND

formalism-tests/core-lite
  blocker: INSUFFICIENT_SOURCE_OF_TRUTH
```

Active-component versioning progress:

```text
StegVerse-002/core-lite
  identity: 0.1.27 DEVELOPMENT
  VERSION.json: 95697020e9637837223dd7e45426ba535ee1017f
  validator: 2fa3901e3c02939464d1639056d5b2aa7b18a938
  existing workflow integration: d44ab534ba3a01f6e6e06ded781c0758341b5596
  canonical handoff: 8060e6af6d0019eb0642c9bd8508d9ebb5ad5a67
  hosted version-validator proof: NOT YET OBSERVED

Admissible-Existence/core-lite
  identity: CORE-LITE-SUPPORT-HARDENING-001 DEVELOPMENT
  VERSION.json: 4f102e8d5b62296e9aa92aeb2210424382034f2f
  validator: 8db63879b007363616bbb2a1a5daca7676efe172
  existing Core-Lite Intake integration: 851f9cbed7c2274d3311d99c388cbeba2cf70b73
  hosted version-validator proof: PASS — run 32553082142 / job 96982867534
  support-hardening runtime: PROVEN
  support-hardening activation: ACTIVATED
  production next-step writer: NOT_ACTIVATED
  release: NOT_CLAIMED
```

The first post-integration Admissible-Existence run exposed a handoff completeness regression after the new version validator passed. Missing canonical handoff binding/status/install-target strings were restored in `Admissible-Existence/core-lite` commit `85b4493130d4ffe9103be0e12320b8e3776daa49`; fresh whole-workflow PASS remains to be observed separately.

### Telemetry support

Six telemetry repositories are `TELEMETRY_SUPPORT` and carry schema/data obligations rather than standalone product-release identities.

### Organization control

Four `.github` repositories are `CONTROL_METADATA` and carry coordination/protocol/schema obligations rather than standalone product-release identities.

### Formalism tests

Eight `formalism-tests/*` repositories are `RESEARCH_FORMALISM`; `formalism-tests/core-lite` remains fail-closed unresolved.

### Admissible-Existence canonical source formalism

Wave 4 classifies these 23 organization-defined canonical source-formalism repositories as `RESEARCH_FORMALISM`:

```text
AE
Existence
RTG
GTG
TT
STCM
ET
learning-transition-governance
BC
CHF
RE
RE-Reduction
DC
Triad
GCAT-BCAT
ECAT-ICAT
IICT
CTA
HPS
FI
DaCo
IW
standing-proof-formalism
```

Source authority: `Admissible-Existence/.github/docs/ORGANIZATION_MATHEMATICAL_ARCHITECTURE.md`.

These records carry formalism/artifact/proof-state version obligations. Mathematical-source status does not create product release, execution, activation, or final cross-repository authority.

## Public user experience

`ecosystem-version.html` must project only machine-verified aggregate state. Current target:

```text
13/13 core declarations
13/13 core owner-local validators installed
203/203 raw repositories enumerated
53 evaluated
51 resolved
2 fail-closed unresolved
full active-component denominator: NOT ESTABLISHED
```

## Next required work

1. Reconcile `ecosystem-version.html` to the machine-verified 53/51/2 state.
2. Classify Admissible-Existence support/control repositories from their local evidence: `validator`, `tracker`, `ae-validation-factory`, `ae-validation-research`, `validation-profile-registry`; leave `SOL` unresolved until role evidence supports disposition.
3. Continue the broad StegVerse-Labs application/service classification by current handoffs.
4. For each newly resolved `ACTIVE_COMPONENT`, inspect repository-native identity before adding a normalized declaration; do not manufacture unrelated semantic versions.
5. Install owner-local fail-closed validation without multiplying redundant workflows.
6. Observe fresh whole-workflow PASS for `Admissible-Existence/core-lite` after handoff restoration.
7. Observe the exact `StegVerse-002/core-lite` version-contract workflow before upgrading it from installed to executed proof.
8. Establish the full active-version denominator only after all 203 records are resolved or explicitly excluded under evidence-backed non-product classes.
9. Measure declaration coverage, validator execution, immutable release/tag coverage, runtime proof, and activation independently.

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

The SDK remains `1.1.0 RELEASE_CANDIDATE` until governed immutable release evidence exists.

Ecosystem Chat remains independently open. Canonical recovery is still `HANDOFF_READY`, requires a fresh independent task-control fence `>20`, then G20 reconstruction, fresh parent fence, live StegVerse-local model, TVC `ROUTE_ADMITTED` with credential requirement `NONE`, exact LLM-adapter execution, measured usage, same-execution Master Records reconstruction, immutable activation receipt, Site import, and verified propagation. No stale G18 cleanup or GitHub-token/private-checkout workaround is a prerequisite.

## Session continuity

This workstream is durably recoverable from repository state without chat history. Thread continuity may be archive-safe; ecosystem-wide denominator construction, complete versioning, executed validation, aggregate release, runtime proof, and activation remain open.
