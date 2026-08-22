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

```text
core lifecycle repositories: 13
normalized VERSION.json declarations: 13/13
owner-local fail-closed validators installed: 13/13
validator-installation coverage: 100%
fully contract validated with execution/hosted evidence: false
aggregate release: NOT_AGGREGATELY_RELEASED
```

Machine inventory: `data/ecosystem-version-coverage.json`.
Validator: `scripts/check_ecosystem_version_coverage.py`.
Task: `data/tasks/SITE-0014-CORE-VERSION-VALIDATOR-COVERAGE.json` — `COMPLETE`.
Public projection: `ecosystem-version.html`.
Shared contract: `docs/ECOSYSTEM_COMPONENT_VERSION_CONTRACT.md`.

Site's repository controller observed `CORE_VALIDATOR_INSTALLATION=13/13`. Version declaration and validator installation are not release, deployment, runtime proof, or activation.

## Raw repository universe

Canonical ledger: `data/ecosystem-repository-universe.json`.
Validator: `scripts/check_ecosystem_repository_universe.py`.
Task: `data/tasks/SITE-0015-ECOSYSTEM-REPOSITORY-ENUMERATION.json` — `COMPLETE`.

Machine-verified state:

```text
installed GitHub App accounts: 11/11
raw repositories enumerated: 203/203
StegVerse-Labs first page: 100
StegVerse-Labs next page: 0
repository enumeration: COMPLETE
repository classification: INCOMPLETE
full active-version denominator: NOT ESTABLISHED
```

The controller observed `RAW_REPOSITORIES_ENUMERATED=203`. Raw enumeration must never be interpreted as 203 standalone product components.

## Repository classification contract

Canonical ledger: `data/ecosystem-repository-classification.json`.
Validator: `scripts/check_ecosystem_repository_classification.py`.

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

### Machine-verified waves

```text
SITE-0016 wave 1: COMPLETE — 18/203 evaluated, 16 resolved, 2 explicit UNCLASSIFIED
SITE-0017 wave 2: COMPLETE — 22/203 evaluated, 20 resolved, 2 explicit UNCLASSIFIED
SITE-0018 wave 3: COMPLETE — 30/203 evaluated, 28 resolved, 2 explicit UNCLASSIFIED
```

Current machine-verified state:

```text
raw denominator: 203
records evaluated: 30
resolved classifications: 28
evaluated but explicitly UNCLASSIFIED: 2
not yet evaluated: 173
active components identified: 8
research/formalism identified: 8
telemetry/support identified: 6
control metadata identified: 6
mirror/legacy resolved: 0
full active-version denominator established: false
```

Wave 3 initially failed correctly because the ledger counted seven formalism-test repositories while eight records had actually been added. The controller reported `expected 30, got 29`. The arithmetic was corrected in commit `6f9579ce8e11a51d167edcd778c5c17909538d38`, the task marker was corrected in `7c91b6c5148aa29282f9ecb1d95503cd5e563d0d`, and `SITE-0018` subsequently completed with `REPOSITORY_CLASSIFICATION_EVALUATED=30/203`.

## Resolved families

### TV / TVC

```text
StegVerse-Labs/TV   -> ACTIVE_COMPONENT
StegVerse-Labs/TVC  -> ACTIVE_COMPONENT
StegVerse-org/TV    -> CONTROL_METADATA
StegVerse-org/TVC   -> CONTROL_METADATA
```

The Labs repositories are the current policy/credential and route/admission components. The similarly named `StegVerse-org` repositories are bounded private TrustVault/control-material surfaces and do not replace the Labs authorities.

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
  posture: legacy candidate only; do not classify from name

formalism-tests/core-lite
  blocker: INSUFFICIENT_SOURCE_OF_TRUTH
  posture: do not infer active, test-support, or mirror role from minimal README
```

New active-component versioning progress:

```text
StegVerse-002/core-lite
  repository-native identity: 0.1.27 DEVELOPMENT
  VERSION.json: installed at 95697020e9637837223dd7e45426ba535ee1017f
  owner-local validator: installed at 2fa3901e3c02939464d1639056d5b2aa7b18a938
  existing workflow integration: d44ab534ba3a01f6e6e06ded781c0758341b5596
  canonical handoff reconciliation: 8060e6af6d0019eb0642c9bd8508d9ebb5ad5a67
  hosted validator execution proof: NOT YET OBSERVED
```

### Telemetry

These six repositories are `TELEMETRY_SUPPORT`, not standalone product authorities:

```text
Admissible-Existence/telemetry
GCAT-BCAT-Engine/telemetry
master-records/telemetry
StegGhost/telemetry
StegVerse-Labs/telemetry
StegVerse-org/telemetry
```

Their obligation is schema/data versioning, not standalone product-release versioning.

### Organization control surfaces

These four repositories are `CONTROL_METADATA`:

```text
StegVerse-Labs/.github
StegVerse-org/.github
Admissible-Existence/.github
AdmittedCode/.github
```

They require control/protocol/schema identity. Their coordination state must not be promoted into product release or activation authority.

### Formalism test organization

Eight repositories are resolved as `RESEARCH_FORMALISM`:

```text
formalism-tests/Triad
formalism-tests/ECAT-ICAT
formalism-tests/GCAT-BCAT
formalism-tests/Existence
formalism-tests/Inference-Window
formalism-tests/Entropy-Reversibility
formalism-tests/Transition-Periodic-Table
formalism-tests/sandbox
```

They require research artifact/test/schema version identity rather than standalone product-release versions. `formalism-tests/core-lite` remains separately unresolved.

## Admissible-Existence source-formalism continuation

`Admissible-Existence/.github/docs/ORGANIZATION_MATHEMATICAL_ARCHITECTURE.md` identifies canonical source-formalism repositories separately from support/control infrastructure.

Next source-formalism classification set:

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

These are candidates for `RESEARCH_FORMALISM` with formalism/artifact/proof-state version obligations. Do not convert mathematical-source status into product-release authority. Support repositories such as `validator`, `tracker`, validation factories, registries, and `SOL` require separate local-role evidence before classification.

## Public user experience

`ecosystem-version.html` must project the latest machine-verified classification state without claiming a full active-component denominator until classification closes.

Current truthful projection target:

```text
13/13 core declarations
13/13 core owner-local validators installed
203/203 raw repositories enumerated
30 evaluated
28 resolved
2 fail-closed unresolved
full active-component denominator: NOT ESTABLISHED
```

## Next required work

1. Update `ecosystem-version.html` to the machine-verified 30/28/2 state.
2. Classify the 23 canonical Admissible-Existence source-formalism repositories under artifact/formalism/proof-state version obligations.
3. Separately classify Admissible-Existence support/control repositories from their local role evidence.
4. Continue the broad StegVerse-Labs application/service classification by current handoffs.
5. For each newly resolved `ACTIVE_COMPONENT`, inspect repository-native version identity before adding `VERSION.json`.
6. Add owner-local fail-closed validation without multiplying redundant workflows.
7. Keep unresolved repositories fail-closed until role evidence is sufficient.
8. Establish the full active-version denominator only after all 203 records are resolved or explicitly excluded under a justified non-product class.
9. Measure declaration, validator execution, immutable release/tag, runtime proof, and activation as separate dimensions.

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

The SDK remains `1.1.0 RELEASE_CANDIDATE` until its governed immutable release evidence exists.

Ecosystem Chat activation remains open independently of this versioning work. Current canonical recovery is `HANDOFF_READY`, requires a fresh independent task-control fence `>20`, and must then proceed through G20 reconstruction, a fresh parent fence, live StegVerse-local model, TVC `ROUTE_ADMITTED` with credential requirement `NONE`, exact LLM-adapter execution, measured usage, same-execution Master Records reconstruction, immutable activation receipt, Site import, and verified propagation. No stale G18 cleanup or GitHub-token/private-checkout workaround is a prerequisite.

## Session continuity

This workstream is durably recoverable from repository state without chat history. Thread continuity may be archive-safe, but ecosystem-wide classification, denominator construction, executed validator evidence, immutable aggregate release, runtime proof, and activation remain open.
