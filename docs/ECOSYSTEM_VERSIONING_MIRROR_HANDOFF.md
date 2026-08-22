# Ecosystem Versioning Mirror Handoff

## Scope and authority

Canonical continuation for StegVerse ecosystem repository enumeration, role classification, component-version normalization, fail-closed owner-local validation, and user-facing status projection in `StegVerse-Labs/Site`.

This workstream is subordinate to `docs/SITE_MIRROR_HANDOFF.md` and the repository orchestration state. It grants no release, runtime, activation, publication, custody, route, credential, wallet, or cross-repository execution authority.

```text
credential_authority: TV/TVC ONLY
GitHub token production/runtime authority: NONE
NON-TV/TVC secret/token authority: false
aggregate_release: NOT_AGGREGATELY_RELEASED
authority_effect: NONE
activation_effect: false
publication_effect: false
```

## Repository orchestration admission

Before the latest Site projection mutation, the parent handoff and current orchestration state were read:

```text
docs/SITE_MIRROR_HANDOFF.md
data/site-orchestration-state.json
data/ecosystem-heartbeat-state.json
```

Current orchestration state records `SITE-0020-REPOSITORY-CLASSIFICATION-WAVE-5` in `completed_parallel_safe_tasks`. Version/status projection is parallel-safe and does not claim HIL upload-owned paths or the queued exclusive live-HIL activation task.

## Core lifecycle milestone

```text
scope: CORE-GOVERNED-LIFECYCLE-V1
repositories: 13
normalized VERSION.json declarations: 13/13
owner-local fail-closed validators installed: 13/13
validator-installation machine evidence: COMPLETE
fully contract validated with fresh hosted/executed evidence: false
aggregate release: NOT_AGGREGATELY_RELEASED
```

Sources:

```text
data/ecosystem-version-coverage.json
scripts/check_ecosystem_version_coverage.py
data/tasks/SITE-0014-CORE-VERSION-VALIDATOR-COVERAGE.json
```

## Raw repository universe

```text
installed GitHub App accounts: 11/11
raw repositories enumerated: 203/203
repository enumeration: COMPLETE
full active-version denominator: NOT ESTABLISHED
```

Sources:

```text
data/ecosystem-repository-universe.json
scripts/check_ecosystem_repository_universe.py
data/tasks/SITE-0015-ECOSYSTEM-REPOSITORY-ENUMERATION.json
```

Raw enumeration is not a 203-product denominator.

## Classification architecture

Base ledger:

```text
data/ecosystem-repository-classification.json
```

Append-only waves:

```text
data/ecosystem-repository-classification-wave-4.json
data/ecosystem-repository-classification-wave-5.json
future: data/ecosystem-repository-classification-wave-*.json
```

Validator:

```text
scripts/check_ecosystem_repository_classification.py
```

The validator independently revalidates the machine-proven base, applies wave manifests in order, rejects duplicate repository identities across waves, verifies every repository against the 203-repository universe, checks class-specific version obligations, and recomputes aggregate arithmetic.

Allowed classes:

```text
ACTIVE_COMPONENT
RESEARCH_FORMALISM
MIRROR_LEGACY
TELEMETRY_SUPPORT
CONTROL_METADATA
UNCLASSIFIED
```

Repository names alone are never sufficient classification evidence.

`MIRROR_LEGACY` is a governed provenance class, not an ignore/delete class. It must carry `PROVENANCE_AND_DISPOSITION_VERSION_REQUIRED`.

## Machine-verified classification progress

```text
SITE-0016 wave 1: COMPLETE — 18 evaluated / 16 resolved / 2 UNCLASSIFIED
SITE-0017 wave 2: COMPLETE — 22 evaluated / 20 resolved / 2 UNCLASSIFIED
SITE-0018 wave 3: COMPLETE — 30 evaluated / 28 resolved / 2 UNCLASSIFIED
SITE-0019 wave 4: COMPLETE — 53 evaluated / 51 resolved / 2 UNCLASSIFIED
SITE-0020 wave 5: COMPLETE — 59 evaluated / 57 resolved / 2 UNCLASSIFIED
```

Current machine-proven aggregate:

```text
raw denominator: 203
records evaluated: 59
resolved classifications: 57
evaluated but explicitly UNCLASSIFIED: 2
not yet evaluated: 144
evaluation coverage: 29.06%
resolved classification coverage: 28.08%
active components identified: 10
research/formalism identified: 31
telemetry/support identified: 7
control metadata identified: 7
mirror/legacy identified: 2
full active-version denominator established: false
aggregate release: NOT_AGGREGATELY_RELEASED
```

`SITE-0020` durable completion evidence:

```text
state: COMPLETE
validator_command: python scripts/check_ecosystem_repository_classification.py
success_marker: REPOSITORY_CLASSIFICATION_EVALUATED=59/203
success_marker_seen: true
authority_effect: NONE
activation_effect: false
publication_effect: false
```

Task source:

```text
data/tasks/SITE-0020-REPOSITORY-CLASSIFICATION-WAVE-5.json
```

## Resolved role families

### TV / TVC

```text
StegVerse-Labs/TV  -> ACTIVE_COMPONENT
StegVerse-Labs/TVC -> ACTIVE_COMPONENT
StegVerse-org/TV   -> CONTROL_METADATA
StegVerse-org/TVC  -> CONTROL_METADATA
```

### Core-Lite active components

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

### Telemetry / support

Seven repositories are now identified as telemetry/support, including `Admissible-Existence/tracker`. Their obligations are schema/data/provenance identities rather than standalone product-release versions.

### Control metadata

Seven repositories are control/protocol/profile surfaces, including `Admissible-Existence/validation-profile-registry`. They do not issue execution or product activation authority.

### Formalism / research

31 repositories are identified as research/formalism surfaces. This includes eight formalism-test repositories and the 23 canonical Admissible-Existence source-formalism repositories named by the organization mathematical architecture.

The 23 canonical source-formalism repositories are:

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

Mathematical-source classification does not create product, release, execution, activation, or final cross-repository authority.

### Mirror / legacy dispositions

```text
Admissible-Existence/ae-validation-research -> MIRROR_LEGACY / DEPRECATED_NOTIFY_ONLY
Admissible-Existence/SOL                    -> MIRROR_LEGACY / DEPRECATED_NOTIFY_ONLY
```

Both have explicit disposition evidence, zero unique active capability requiring migration, and require separately admitted reactivation before any future implementation work.

## Active-component versioning progress

### StegVerse-002/core-lite

```text
identity: 0.1.27 DEVELOPMENT
VERSION.json: 95697020e9637837223dd7e45426ba535ee1017f
owner-local validator: 2fa3901e3c02939464d1639056d5b2aa7b18a938
existing-workflow integration: d44ab534ba3a01f6e6e06ded781c0758341b5596
canonical handoff reconciliation: 8060e6af6d0019eb0642c9bd8508d9ebb5ad5a67
fresh hosted version-validator proof: NOT YET OBSERVED
release: NOT_CLAIMED
runtime/activation: PENDING
```

### Admissible-Existence/core-lite

```text
identity: CORE-LITE-SUPPORT-HARDENING-001 DEVELOPMENT
VERSION.json: 4f102e8d5b62296e9aa92aeb2210424382034f2f
owner-local validator: 8db63879b007363616bbb2a1a5daca7676efe172
existing-workflow integration: 851f9cbed7c2274d3311d99c388cbeba2cf70b73
hosted version-validator proof: PASS — run 32553082142 / job 96982867534
support-hardening runtime: PROVEN
support-hardening activation: ACTIVATED
production next-step writer: NOT_ACTIVATED
release: NOT_CLAIMED
```

The first post-integration workflow exposed handoff-completeness drift after the new version validator passed. Required canonical binding/status/install-target terms were restored at `85b4493130d4ffe9103be0e12320b8e3776daa49`. Fresh whole-workflow PASS after that restoration remains to be directly observed.

### Admissible-Existence/validator

Wave 5 resolved Validator as an `ACTIVE_COMPONENT` with repository-native role `VALIDATION_AUTHORITY_LAYER`.

Normalized identity work completed in the current pass:

```text
component_version: AEX-VALID-20260729-01
version_stage: DEVELOPMENT
VERSION.json: 0cba9a190108df74e26974165a7408140907139f
owner-local fail-closed validator: 20583dbe564e1ed6ff3fc3ca2d327f6bc00eb646
existing Validate Validator workflow integration: a39475e04b2ef00705963a13ab5a887866ea5d42
historical evaluator hosted proof: run 31188248490 / job 92898192340 SUCCESS
historical support activation proof: runs 31188595365 and 31188732813 SUCCESS
fresh hosted execution of new normalized version check: NOT YET DIRECTLY OBSERVED
release_ready: false
publication_authorized: false
execution_authorized: false
authority_effect: NONE
```

The declaration preserves the distinction between a proven evaluator runtime/support-completeness scope and release/execution authority.

### Admissible-Existence/ae-validation-factory

Wave 5 resolved the Factory as an `ACTIVE_COMPONENT` because it is the live procedural validation/alignment orchestrator.

Current repository evidence includes independent hosted validation of its strict RTG/TT result path and a release-candidate boundary, but no repository-native component version token has yet been established. RTG/TT profile versions must not be reused as a Factory product version.

```text
normalized component identity: OPEN
release_candidate: true
release_authorized: false
publication_authorized: false
execution_authorized: false
creates_authority: false
```

Next step is to derive a deterministic Factory-owned identity from its own build-state contract before installing a normalized declaration.

## Public user experience

Current projection:

```text
ecosystem-version.html @ 4642a966b4513bd0b645bc46a9518738eaf4425d
13/13 core declarations
13/13 core owner-local validators installed
203/203 raw repositories enumerated
59 evaluated
57 resolved
2 fail-closed unresolved
10 active components identified
31 research/formalism
7 telemetry/support
7 control metadata
2 mirror/legacy
full active-component denominator: NOT ESTABLISHED
aggregate release: NOT_AGGREGATELY_RELEASED
```

The page has been simplified so user-facing state emphasizes what is usable, what is proven, and what is still open rather than exposing stale internal wave arithmetic.

## Ecosystem Chat operational boundary

Ecosystem Chat remains independently open.

Current canonical recovery remains:

```text
recovery: RECOVER-SHWP-ECOSYSTEM-CHAT-INFERENCE-001-ORPHAN-HB28
state: HANDOFF_READY
executor: AUTHORIZED
claim mode: AUTHORIZED_FOR_INDEPENDENT_TASK_CONTROL_CLAIM
fresh recovery fence: strictly >20
G18 terminalization prerequisite: false
GitHub-token runtime authority: NONE
credential authority: TV/TVC
```

Required live sequence remains:

```text
recovery fresh claim/fence >20
-> G20 custody reconstruction PASS
-> recovery COMPLETED
-> separate fresh parent fence >20
-> StegVerse-local private model held live on same carrier
-> TVC ROUTE_ADMITTED with credential requirement NONE
-> exact LLM-adapter execution
-> measured usage persistence
-> same-execution Master Records provider-usage reconstruction PASS
-> transition reconstruction PASS
-> immutable zero-blocker receipt
-> Site activation/import
-> verified downstream propagation
```

No source, CI, hosted model, Render, GitHub token, old G18 cleanup, or stale G20 authority may substitute for that live execution.

## Next required work

1. Observe fresh hosted execution of `Admissible-Existence/validator` normalized version check.
2. Observe the repaired whole-workflow pass for `Admissible-Existence/core-lite`.
3. Observe the exact `StegVerse-002/core-lite` version-contract workflow before promoting installed -> executed proof.
4. Derive and install a deterministic Factory-owned normalized component identity without borrowing RTG/TT profile versions.
5. Continue append-only repository classification from current handoffs, prioritizing high-confidence StegVerse-Labs application/service families.
6. For every newly identified `ACTIVE_COMPONENT`, inspect repository-native identity before creating `VERSION.json`.
7. Establish the full active-component denominator only after all 203 repository roles are resolved or explicitly excluded under evidence-backed non-product classes.
8. Measure declaration coverage, validator execution, immutable release/tag coverage, runtime proof, deployment, propagation, and activation independently.
9. Continue Ecosystem Chat recovery/fresh-parent execution only through the authorized resident task-control path; do not create a second heartbeat, scheduler, model route, or credential path.

## Never-equate boundary

```text
raw enumeration != classification
classification != versioning
version declaration != validator execution
validator installed != validator passed
validation != release
release candidate != release
main branch != immutable release
workflow pass != runtime proof
deployment != activation
component activation != ecosystem aggregate release
research/formalism standing != product authority
mirror/legacy disposition != deletion from provenance
```

## Session continuity

This workstream is durably recoverable from repository state without chat history. Thread continuity may be archive-safe, but ecosystem-wide denominator construction, complete active-component version coverage, fresh executed validation, immutable aggregate release, runtime proof, and activation remain open.
