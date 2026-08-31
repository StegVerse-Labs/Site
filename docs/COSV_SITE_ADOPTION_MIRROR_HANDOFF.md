# Site COSV Adoption Mirror Handoff

Updated: 2026-08-31
Repository: StegVerse-Labs/Site
Canonical profile owner: StegVerse-Labs/.github/management/COSV_PROFILE_V1.json
Authority effect: NONE

## Source of truth

Repository-wide authority remains `SITE_MIRROR_HANDOFF.md`. This handoff owns only Site-native COSV task projection and adoption accounting.

## Installed projection

```text
data/cosv/task-vector-index.json
data/cosv/task-vectors/*.json
scripts/check_cosv_task_projection.py
tests/test_cosv_task_projection.py
```

The Site repository emits its own task records using canonical `task.v1` notation:

```text
L R U I V G O C M T B E A P
width=14
credential authority=TV/TVC
authority effect=NONE
```

No Site vector grants provider, credential, publication, custody, execution, admissibility, or product-activation authority.

## Current explicit COSV surface

Four task records explicitly carried canonical COSV metadata with null vectors. Current collision-safe projection state is:

```text
SITE-SEMANTIC-SHORTHAND-396-R2                  50000000101000  EXTERNAL_PROJECTION / SOURCE OWNER RETAINED
SITE-TASK-RUNNER-SEMANTIC-LIVE-501             71000000100100  EXTERNAL_PROJECTION / SOURCE OWNER RETAINED
SITE-HOMEPAGE-GOVERNED-ECOSYSTEM-VALIDATOR-521 71000000100100  SOURCE_BOUND
SITE-MIRROR-WORKFLOW-VALIDATOR-519             DEFERRED         LEGACY_ACTIVE_CLAIM_MIGRATION_REQUIRED
```

The active #396/#501 validation claim owns those source task files, so this lane does not mutate their bindings. #519's implementation is historically merged and later runner evidence advanced beyond its validator, but its ownership remains in the legacy aggregate claim registry; the current orchestrator permits terminalization-only mutation only for pre-existing claim fragments. #519 therefore remains explicitly deferred rather than competing with that legacy claim.

#521 already declared `COMPLETE_LIVE_PROVEN`; its stale archive flag is corrected and its vector is source-bound.

The active semantic task remains machine-owned and blocked only by the existing Site activation-aware downstream-ingestion gate. It is not marked evidence-complete, activated, or propagated.

## Adoption boundary

```text
explicit COSV task surfaces discovered: 4
task vectors emitted: 3
source-bound task vectors: 1
active-owner deferred source bindings: 2
legacy-claim deferred tasks: 1
explicit COSV surface gap: 1
repository-wide active task-surface audit complete: false
repository VECTOR_PRESENT claimed: false
```

Do not promote Site to repository-level `VECTOR_PRESENT` until every current active machine task surface represented by Site's repository-wide handoff/task/claim system is audited, normalized, and either vectorized or proven terminal/exempt.

## Next machine work

1. Audit all current Site task/claim surfaces beyond the four explicit COSV-null records.
2. Migrate/reconcile the legacy #519 aggregate claim into the fragment-based retirement model before mutating its task/handoff.
3. Emit evidence-backed task.v1 records for every remaining active Site machine task.
4. Run the Site-local COSV validator and normal Site validation gates.
5. Only after the active denominator is closed, update the central ecosystem adoption manifest to Site `VECTOR_PRESENT`.
6. Preserve downstream activation/custody/publication boundaries; Site source completion is not product activation.

