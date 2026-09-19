# Site COSV Adoption Mirror Handoff

Updated: 2026-09-18
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



## Terminal-source reconciliation — 2026-09-18

`SITE-CURRENT-NEWS-RELEASES-967` is now terminal in its owning publication lane. The Site task is `PUBLICATION_VERIFIED_COMPLETE`, its publication claim is `RELEASED_COMPLETE`, and the canonical organization COSV projection merged in `StegVerse-Labs/.github` commit `3ad023ab017e5e7a266d2c4139fedc18c4c76d9c` as:

```text
SITE-CURRENT-NEWS-RELEASES-967  71000000100100
lifecycle=COMPLETE
archive_ready=true
blocker_count=0
evidence_complete=true
thread_required=false
activated=false
propagated=false
```

The repository-local projection therefore mirrors that exact vector without reopening or mutating the retired publication task. Its index binding is now `EXTERNAL_PROJECTION_TERMINAL_SOURCE`, which is distinct from both `SOURCE_BOUND` and `EXTERNAL_PROJECTION_SOURCE_BINDING_DEFERRED_ACTIVE_OWNER`.

The Site-local validator requires a terminal external projection to correspond to an already-terminal source task and to preserve the non-authorizing COSV boundary. For this task it requires `publication_verified=true`, `state=PUBLICATION_VERIFIED_COMPLETE`, `COMPLETE`, `archive_ready=true`, `evidence_complete=true`, zero blockers, no thread requirement, and no activation or propagation claim.

Updated adoption accounting:

```text
task vectors emitted: 4
source-bound task vectors: 1
active-owner deferred source bindings: 2
terminal external source bindings: 1
legacy-claim deferred tasks: 1
explicit COSV surface gap: 1
repository-wide active task-surface audit complete: false
repository VECTOR_PRESENT claimed: false
```

This reconciliation does not change publication evidence, publication authority, runtime, credentials, custody, execution, admissibility, activation, or propagation. It only removes stale Site-local COSV projection state after the owning task terminalized.


### Canonical validation integration — 2026-09-18

The canonical Site Bootstrap workflow now executes the Site-local COSV validator and focused projection unittest on every push and pull request:

```text
python3 scripts/check_cosv_task_projection.py
python3 -m unittest tests.test_cosv_task_projection
```

This closes the prior verification gap where normal Site validation could pass without directly exercising the repository-local COSV projection contract. The step is validation-only and uses no credential, mutation, publication, runtime, or activation authority.


## Active denominator reconciliation — 2026-09-18

The explicit five-task COSV surface is now fully classified without mutating still-owned source semantics:

```text
SITE-SEMANTIC-SHORTHAND-396-R2                  50000000101000  EXTERNAL_PROJECTION_MACHINE_OWNED_SOURCE
SITE-TASK-RUNNER-SEMANTIC-LIVE-501             71000000100100  EXTERNAL_PROJECTION_TERMINAL_SOURCE
SITE-HOMEPAGE-GOVERNED-ECOSYSTEM-VALIDATOR-521 71000000100100  SOURCE_BOUND
SITE-CURRENT-NEWS-RELEASES-967                  71000000100100  EXTERNAL_PROJECTION_TERMINAL_SOURCE
SITE-MIRROR-WORKFLOW-VALIDATOR-519              71000000100100  EXTERNAL_PROJECTION_TERMINAL_SOURCE
```

#396 is not terminalized: its source implementation and public route are complete, but its downstream activation-aware ingestion predicate remains authentic and unsatisfied. Its vector therefore remains MACHINE_OWNED with one blocker, evidence incomplete, activated=false, and propagated=false.

#501 is terminal from its existing source evidence and released claim. #519 is terminal after PR #520 merged, later Site Task Runner 33071012941 advanced beyond the repaired validator, the legacy aggregate claim was retired through the installed tombstone mechanism in PR #1400, and the temporary migration owner was released in PR #1401.

Explicit-surface accounting is now closed:

```text
explicit COSV task surfaces discovered: 5
task vectors emitted: 5
source-bound task vectors: 1
external machine-owned source bindings: 1
active-owner deferred source bindings: 0
terminal external source bindings: 3
legacy-claim deferred tasks: 0
explicit COSV surface gap: 0
```

Repository-wide adoption is not promoted. The validator now loads the canonical aggregate claim registry plus all claim fragments and terminalization tombstones through check_session_work_claims.py, computes the effective active claim denominator, and fails closed on repository VECTOR_PRESENT while active task IDs remain outside this explicit COSV index.

```text
repository active task-surface audit complete: false
repository VECTOR_PRESENT claimed: false
repository VECTOR_PRESENT blocker: UNINDEXED_ACTIVE_CLAIM_TASKS_REMAIN
```

No competing runtime, credential, publication, custody, admissibility, activation, propagation, or claim authority is created by this accounting reconciliation.


## Repository-wide successor activation — 2026-09-18

Canonical successor: `SITE-COSV-REPOSITORY-WIDE-ADOPTION-001`.

The canonical Task Registry successor was registered at generation 73 via StegVerse-Labs/.github PR #2185 (`cc46bd9aad20f03299d79833833c9365e533bb03`). Site now carries an exclusive bounded claim for the denominator closure work and a source-bound non-authorizing task.v1 projection:

```text
SITE-COSV-REPOSITORY-WIDE-ADOPTION-001  20010000101000  SOURCE_BOUND
lifecycle=CLAIMED_IMPLEMENTATION
authority_effect=NONE
repository VECTOR_PRESENT=false
```

The effective claim denominator was recomputed through the canonical claim loader semantics at Site main `9c83949986a134c54fe720691fe28a9b7dfe5f66`. The authoritative branch loader reports 52 effective active claims / 52 active task IDs after installing the successor claim and the #506 terminalization. The branch simultaneously installs the successor claim and safely retires one stale aggregate owner, so one active task ID is now indexed by the successor itself; the effective unindexed active task-ID count is 51.

The retired aggregate claim is `SITE-HIL-V1-1-VALIDATOR-506-20260826`. Retirement is evidence-backed rather than inferred: PR #507 merged at `3538beebbbeab37550ad62fb1e9c2d1e7e9788a1`; later Site Task Runner runs 33044661032 and 33045293923 completed successfully; the HIL handoff already records Site#506 CLOSED/COMPLETED; and `data/tasks/SITE-HIL-V1-1-VALIDATOR-506.json` is already reconciled to `RELEASED / SATISFIED_BY_EXISTING_STATE`.

Current incremental accounting on the successor branch:

```text
explicit COSV task surfaces discovered: 5
task vectors emitted: 6
source-bound task vectors: 2
repository-claim task vectors: 1
effective active claims observed: 52
effective active task IDs observed: 52
unindexed active task IDs observed: 51
repository active task-surface audit complete: false
repository VECTOR_PRESENT claimed: false
repository VECTOR_PRESENT blocker: UNINDEXED_ACTIVE_CLAIM_TASKS_REMAIN
```

This successor does not mutate still-owned source semantics and does not reinterpret authentic blockers such as Site #396. Further progress should continue by retiring only claims whose release predicates are already evidenced and by adding owner-faithful active vectors or explicit exemptions for the remaining active task IDs. No runtime, credential, publication, custody, admissibility, activation, propagation, or execution authority is created by this accounting work.


## Repository-wide denominator increment — 2026-09-19

Canonical successor remains `SITE-COSV-REPOSITORY-WIDE-ADOPTION-001`; current organization Task Registry generation observed before this batch is 84.

This increment distinguishes terminal ownership from still-live source ownership instead of treating age or historical merge state as completion.

### Evidence-backed stale-owner retirement

`SITE-FINAL-ACTIVATION-PENDING-RECONCILIATION-525` is terminalized through the installed bounded aggregate-claim tombstone mechanism. Its source task already records:

```text
state=RELEASED
disposition=SATISFIED_BY_EXISTING_STATE
remaining=[]
archive_eligible=true
PR #527 merge=38ac8d802b5ed1efca77a29940737d7c8ae0fe8e
Site Task Runner 33044661032=SUCCESS
later full runner 33045293923=SUCCESS
handoff reconciliation=bda61df34cf96ea6f1b4094f60e4de3226893744
```

The corresponding Site-local COSV projection is therefore terminal `71000000100100` with no activation or propagation claim.

### Still-live owner projections

The following owners remain active because their own canonical task records still retain unsatisfied validation/merge/runner predicates:

```text
SITE-HPS-USER-FIRST-VALIDATOR-508
SITE-UNIFIED-GOVERNED-VALIDATOR-510
SITE-MIRROR-GOAL-VALIDATOR-517
SITE-LLM-FREE-TIER-TRUST-USER-FIRST-523
```

They are projected as `EXTERNAL_PROJECTION_SOURCE_BINDING_DEFERRED_ACTIVE_OWNER` with vector `20010000101000`. This indexes their active state for denominator accounting without writing COSV state back into the owner task files, changing their remaining predicates, or asserting completion.

### Incremental accounting

The branch starts from current main accounting of 53 effective active task IDs / 52 unindexed. Retiring #525 and indexing four still-live owner task IDs yields the expected branch accounting:

```text
effective active claims: 52
effective active task IDs: 52
active indexed task IDs: 5
unindexed active task IDs: 47
task vectors emitted: 11
active-owner external projections: 4
terminal external source bindings: 4
repository VECTOR_PRESENT: false
blocker: UNINDEXED_ACTIVE_CLAIM_TASKS_REMAIN
```

The canonical validator remains authoritative for the exact branch denominator. It now verifies projection-mode totals incrementally instead of hard-coding the prior six-vector snapshot. If concurrent claim changes alter the denominator, the stored accounting must be reconciled to the loader output before merge.

Site #396 remains unchanged as `EXTERNAL_PROJECTION_MACHINE_OWNED_SOURCE` with its authentic downstream-ingestion blocker. No runtime, credential, publication, custody, admissibility, execution, activation, propagation, or governance authority is created by this accounting increment.


## Repository-wide zero-gap candidate — 2026-09-19

Canonical successor remains `SITE-COSV-REPOSITORY-WIDE-ADOPTION-001`. The organization Task Registry was re-read at generation 110 before this reconciliation and the successor remained ACTIVE.

Current Site main had advanced to `a47295d546d9ba6af014b96d509e0dad2455500e`. Those concurrent changes changed the denominator source state in two material ways:

- `ADMISSIBILITY-RECONSTRUCTABLE-SINGULARITY-001` is now released complete in its own Site claim fragment and is therefore no longer part of the active denominator.
- `ENTERPRISE-HOST-PROVIDER-ERADICATION-001` is now an active aggregate Site owner and is included in the claim-source projections.

Current-main owner accounting before this branch's ERL claim retirement resolves to 49 effective active task IDs: 38 active fragment owners plus 11 effective aggregate owners after the existing bounded aggregate tombstones.

### Evidence-backed fragment retirement

`SS-ERL-KV-PROPAGATION-VERIFICATION-001` is canonically terminal:

```text
Task Registry generation observed: 110
canonical coordination_state: RETIRED
completion.claimed: true
completion.validated: true
canonical COSV: 71000000100101
Site PR #1174 merge: ca106480cd78a35fffa107e73a678219ca918bb1
PR #1174 merged_at: 2026-09-09T14:24:10Z
Site handoff state: UPDATE_REQUIRED_IMPLEMENTED / VALIDATED / MERGED
```

The historical Site claim fragment still advertised `CLAIMED_FOR_VALIDATION`. The claim loader therefore now supports the same bounded terminal metadata override for fragment claims that it already supported for aggregate claims. The original fragment is not rewritten; a separate terminalization row records only claim ID, terminal state, PR, release commit/time, and archive eligibility.

After that evidence-backed retirement, the effective active denominator candidate is 48.

### Full live-owner projection

Every remaining live active owner is represented without modifying its source task/claim semantics. `data/cosv/active-claim-projections.json` records task ID, exact claim ID/state, claim source, handoff source, and a task.v1 vector derived only from that live claim state. It explicitly records:

```text
source_semantics_mutated=false
completion_inferred=false
evidence_complete=false
activated=false
propagated=false
```

Claim-source vectors are lifecycle projections, not claims that implementation, validation, integration, blocking predicates, runtime activation, or publication completed.

Site #396 remains unchanged as the existing machine-owned external source projection with its authentic blocker.

### Zero-gap gating

The Site COSV validator now computes the active denominator from:

```text
active_claims(load_registry())
```

and validates claim-source projection rows against those exact live claim objects. Repository `VECTOR_PRESENT=true` is accepted only when:

```text
effective active claims == stored active claim count
effective active task IDs == stored active task-ID count
active task IDs - indexed task IDs == empty set
repository_unindexed_active_task_ids_observed == 0
repository_unindexed_active_claim_tasks_present == false
repository_vector_present_blocker == null
repository_active_task_surface_audit_complete == true
```

Current branch candidate accounting is:

```text
effective active claims: 48
effective active task IDs: 48
unindexed active task IDs: 0
task vectors/index rows: 55
claim-source live vectors: 43
retired canonical task vectors: 1
repository VECTOR_PRESENT candidate: true
```

This is not repository truth until exact-head hosted validation passes, the exact validated head merges, and the post-merge canonical loader again returns zero unindexed active task IDs. No runtime, credential, publication, custody, admissibility, governance, execution, activation, or propagation authority is created by this repository-accounting projection.


### Exact-head validation repair — 2026-09-19

Initial PR #1420 exact-head validation exposed two concrete defects before merge:

1. the newly added `ENTERPRISE-HOST-PROVIDER-ERADICATION-001` live projection pointed to the older cleanup handoff instead of the exact aggregate claim handoff `SITE_MIRROR_HANDOFF.md`; that projection binding is corrected;
2. the StegOS persistent-card gate still required the superseded `SOVEREIGN_LOCAL_DISCOVERY_WITH_OPTIONAL_THIRD_PARTY_FALLBACKS` gateway shape even though current main already uses `SOVEREIGN_LOCAL_DISCOVERY_ONLY` with no third-party fallback routes. The validator is aligned to the existing current-main provider-neutral contract without modifying gateway runtime semantics.

The COSV unit test is also bundle-aware so bundled live-claim projections are validated without assuming an individual `vector_ref` file per live claim.
