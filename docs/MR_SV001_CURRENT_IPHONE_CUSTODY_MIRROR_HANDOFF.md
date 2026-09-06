# Current-iPhone Master Records SV001 Custody Projection Mirror Handoff

Updated: 2026-09-06
Repository: StegVerse-Labs/Site
Issue: #955
Goal: SITE-MR-SV001-CUSTODY-PROJECTION-955

## Current task source of truth

This handoff records the current source, governance, merge, claim, and runtime-evidence state for the current-iPhone SV001 -> Master Records custody continuation.

The prior contemporaneous-InTr/no-retroactive-authorization implementation is merged and its implementation claim is released. A later canonical Master Records recovery source now exists and is being projected through the already-active Site #1000 continuation claim. Authentic Master Records recovery/custody/reconstruction remains a distinct runtime predicate and is **not** established by source, CI, merge, publication, cache installation, or claim state.

## Objective

Project the canonical browser-compatible Master Records SV001 custody/reconstruction and retained-journal recovery modules to the existing current-iPhone StegOS bootstrap surface so the already-completed immutable SV001 G23 result can enter Master Records custody without rerunning autonomy and without requiring another user-operated machine.

## Canonical source dependencies

Canonical owner: `master-records/orchestration`

Custody source:
- portable source PR: `master-records/orchestration#73`
- merge: `9b617459ec0b9dfceb894ac19495ee72106d1e94`
- portable custody module: `portable/stegverse001-autonomy-custody.js` / blob `ea390cee958c67ff5d144abb43963e07f891a1ef`

Canonical retained-journal recovery source:
- PR: `master-records/orchestration#81`
- merge: `84ba89792a8e9057079d647c4909f8a510ff2559`
- portable recovery module: `portable/stegverse001-canonical-journal-recovery.js`
- exact recovery module blob: `5ca977c4214c3eec13bd2ac1109405e7f1571723`
- updated custody package blob: `70e02082d63d046101fa0a21d82e12261c891e79`
- target source receipt: `sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35`
- target claim: `SHWP-SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001-G23`
- target fencing token: `23`

Site must project the canonical recovery module and updated package byte-for-byte. Site-local code may only provide the same-device source-selection, UI materialization, governed transition carrier, and local persistence around the canonical modules.

## Authentic source runtime already established

```text
execution surface: CURRENT_USER_IPHONE
task: SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001
claim/fence: G23 / 23
transition: SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED
cycle receipt identity: sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35
device-local reconstruction: PASS / same_execution=true
TVC lease consumption: CONSUMED
```

The SV001 autonomy cycle is terminal. It MUST NOT be rerun to satisfy custody.

The retained G23 receipt identity is evidence input only. It does not authorize custody or reconstruction.

## Canonical source-recovery semantics

The prior handoff correctly rejected reconstruction from a hash, compact projection, or missing source fields. Master Records PR #81 now supplies a bounded retained-journal recovery mechanism that can reconstruct the exact historical G23 source object **only from authentic retained same-device journal material**.

The canonical recovery contract requires:

```text
exact target SHA-256: G23
exact target claim_id: SHWP-SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001-G23
exact target fence: 23
journal integrity: PASS
WorkerCoordinator checkout lineage: valid
TVC single-cycle lease issuance/consumption: valid
same-execution reconstruction: PASS
bounded completed_at search: <= 5000 ms
complete source object match count: exactly 1
hash/pointer/projection substitutes for source: false
source or CI proves authentic recovery: false
authority effect: NONE_RECOVERY_ONLY
```

Zero matches, multiple matches, journal corruption/drift, claim/fence mismatch, lease mismatch, incomplete source material, or source-hash mismatch fail closed. No field synthesis and no SV001 rerun are permitted.

The canonical source module was observed as merged source only. Authentic recovery remains unobserved until that exact module executes against the retained journal on the current iPhone and returns its exact recovery proof.

## Site authority boundary

```text
Site role: EXACT SOURCE MATERIALIZATION + SAME-DEVICE GOVERNED CARRIER + LOCAL PERSISTENCE CARRIER ONLY
Master Records recovery authority effect: NONE_RECOVERY_ONLY
Master Records custody authority: retained by master-records/orchestration
InTr/Interlock transition governance: required contemporaneously
Site custody authority: false
Site execution authority: false
Site lease issuance authority: false
Site credential authority: false
Site accreditation authority: false
Site sovereign authority: false
GitHub token runtime authority: NONE
HB grants authority: false
prior receipt grants authority: false
historical state grants retroactive authority: false
second user-operated machine required: false
external non-StegVerse machine required: false
```

## Current machine-owned current-iPhone flow

```text
normal open/resume of existing StegOS same-device surface
-> discover exact persisted canonical G23 proof if already retained
-> otherwise execute exact canonical Master Records retained-journal recovery
-> require exactly one complete recovered source object matching canonical G23 SHA
-> browser materializes exact G23 object in Master Records card
-> browser reads canonical registered Node/Interlock identity
-> browser constructs exact MACHINE_GOVERNED custody transition request
-> HB-derived carrier binding (reference/correlation only; no authority)
-> existing root /intr-service-worker.js
-> MasterRecords:SV001Custody profile
-> contemporaneous exact transition validation
-> write-once InTr admission
-> ALLOW receipt bound to G23 + Node + Interlock + request + HB reference
-> bootstrap Master Records endpoint receives exact G23 object + exact admission receipt
-> validates admission again before mutation
-> appends admission receipt to existing local journal
-> exact canonical Master Records portable custody module
-> Master Records custody object
-> Master Records reconstruction PASS
-> append exact custody/reconstruction objects to existing local journal
-> replay journal PASS
-> return portable custody proof carrying admission/custody/reconstruction bindings
-> downstream SV002 continuation only after authentic evidence exists
```

No human approval checkpoint belongs in this flow. Execution on the current iPhone does not make this transition human-owned. The shared current-iOS interaction guard remains relevant to human controls but is not an authority gate for this machine-owned transition.

Manual exact-proof import remains only a fail-closed fallback when automatic canonical source recovery cannot establish the required full object. It does not authorize custody by itself.

## Prior governance source closure

Functional implementation claim:

```text
claim: SITE-SV001-MR-INTR-GOVERNANCE-20260905
functional PR: #1067
functional merge: e8cc4ee9ffd57eea57e1111834d67f88ee6c7e5d
claim-release PR: #1088
claim-release merge: 6e3e2a5e6043e5bddca504be70da55989cebb6b3
claim state: RELEASED_COMPLETE
archive_eligible: true
```

The released implementation claim must not be reactivated or duplicated.

The focused post-merge handoff reconciliation was merged through PR #1089 as `f03c5ad8dfa62e0bd9c9187d65300429d524e7b4` and its reconciliation claim was released through PR #1090 as `5c7c98cd3e86d0b4e3bae4cd18b2687966522f32`.

## Active recovery continuation — 2026-09-06

Existing Site claim reused, not duplicated:

```text
claim: SITE-STEGOS-PERSISTENT-CARD-UX-1000-AUTO-RECOVERY-20260906
task: SITE-STEGOS-PERSISTENT-CARD-UX-1000
branch: continue/site1000-auto-sv001-recovery
state: CLAIMED_FOR_IMPLEMENTATION
```

Refreshed machine preflight:
`data/preflight/site1000-auto-sv001-recovery-20260906.json`

The preflight resolved the current Site #1000/#955 handoffs, Master Records PR #81 recovery source, canonical Task Registry generation 15, transition ownership, and current branch/claim collision state. It required continuation of the existing claim/branch rather than a duplicate implementation.

README impact is MATERIAL. The normal current-iPhone behavior changes from retained-proof/manual fallback to retained-proof -> canonical retained-journal recovery -> automatic machine-governed custody continuation. README is therefore updated in this same source change set.

Current source work on the active branch:

- `stegos-bootstrap/master-records-sv001-recovery.js`
  - exact canonical PR #81 recovery module / blob `5ca977c4214c3eec13bd2ac1109405e7f1571723`;
- `stegos-bootstrap/master-records-sv001-custody-package.json`
  - exact updated canonical package / blob `70e02082d63d046101fa0a21d82e12261c891e79`;
- `stegos-bootstrap/master-records-auto-recovery.js`
  - selects exact persisted G23 first;
  - otherwise invokes canonical journal recovery;
  - requires exact unique G23 source;
  - invokes the existing `executeMasterRecordsSv001Custody` machine-governed path automatically;
  - requires contemporaneous root-InTr admission and reconstruction PASS;
  - grants no custody/execution authority and never reruns SV001;
- `stegos-bootstrap/index.html`
  - loads canonical recovery + automatic continuation and presents manual custody as fallback only;
- `stegos-bootstrap/service-worker.js`
  - v13 shell caches both recovery files and preserves the merged custody/governance handler;
- exact successor validators are bounded to explicit new index/service-worker blob identities.

## No-retroactive-authorization invariant

The merged custody handler remains fail-closed:

```text
custody + reconstruction + matching retained admission
-> validate retained admission again
-> canonical reconstruction
-> journal replay PASS
-> idempotent PASS

custody + reconstruction + NO matching retained admission
-> FAIL_CLOSED
-> historical_state_retroactively_authorized=false
-> do not mint replacement admission
-> do not infer authorization from G23
-> do not rerun SV001

admission only OR custody only OR reconstruction only
-> PARTIAL GOVERNANCE/CUSTODY STATE
-> FAIL_CLOSED
-> explicit recovery required
-> prior admission may not authorize a later mutation
```

Canonical G23 **source recovery** and historical **governance-state recovery** are distinct. Recovering the exact G23 source object cannot repair or retroactively authorize prior custody state lacking contemporaneous InTr admission.

## Current truth

```text
prior contemporaneous-governance source repair: MERGED
prior no-retroactive-authorization source repair: MERGED
prior implementation claim: RELEASED_COMPLETE
canonical retained-journal recovery source in master-records/orchestration: MERGED
canonical recovery module exact projection on active Site branch: IMPLEMENTED
canonical updated package exact projection on active Site branch: IMPLEMENTED
automatic recovery -> existing governed custody source: IMPLEMENTED_ON_ACTIVE_BRANCH
v13 offline shell source: IMPLEMENTED_ON_ACTIVE_BRANCH
README completeness for v13 recovery semantics: IMPLEMENTED_ON_ACTIVE_BRANCH
exact-head branch/PR validation: pending
merge to Site main: pending
public propagation of v13 exact source: not observed
current-iPhone authentic G23 retained-journal recovery: not observed
current-iPhone root InTr custody ALLOW following recovery: not observed
Master Records G23 custody/reconstruction PASS following recovery: not observed
retained same-execution recovery/admission/custody/reconstruction evidence: not observed
SV002 downstream disposition: not observed
```

No runtime completion is inferred from source implementation, exact source identity, CI, merge, cache generation, or publication.

## Remaining distinct executable work

1. Complete exact source validation of the active Site recovery branch, including exact canonical recovery/package identities, v13 shell completeness, exact successor pins, and existing InTr governance validators.
2. Merge the existing claim only if exact merge-result validation passes.
3. Terminalize the Site source claim through the canonical claim-maintenance path after merge.
4. Observe public/current-device v13 installation separately; do not infer it from merge.
5. On a current iPhone that actually retains the relevant journal, normal open/resume may then execute the automatic recovery path. Only its authentic recovery proof can satisfy source recoverability.
6. Only a fresh root-InTr ALLOW plus custody/reconstruction PASS and retained evidence can satisfy Master Records runtime completion.
7. Evaluate SV002 only after those predicates are genuinely observed.

Do not create another Site InTr runtime, scheduler, WorkerCoordinator, claim/fence mechanism, credential path, or duplicate custody/recovery implementation.

## Installation / module disposition

Destination `StegVerse-Labs/Site`, active branch `continue/site1000-auto-sv001-recovery`:

Developed source, pending merge:
- `stegos-bootstrap/master-records-sv001-recovery.js` — exact canonical source, not a stub;
- `stegos-bootstrap/master-records-sv001-custody-package.json` — exact canonical package, not a stub;
- `stegos-bootstrap/master-records-auto-recovery.js` — implemented same-device source selection + automatic governed-custody carrier;
- `stegos-bootstrap/index.html` recovery wiring;
- `stegos-bootstrap/service-worker.js` v13 cache successor;
- validator/README/handoff updates.

No new runtime authority module is required or admissible.

## Archive readiness

The prior governance implementation lane is archive-ready/released.

The active #1000 recovery source claim is **not archive-ready** until exact validation, merge, and claim terminalization complete.

The broader SV001 -> Master Records runtime objective remains not runtime-archive-complete until authentic current-device recovery, contemporaneous admission, custody/reconstruction PASS, retained reconstruction evidence, and downstream disposition are observed as applicable.

## User work

Routine repository work: none.

Do not rerun SV001, synthesize G23, manually approve the machine-owned transition, or operate a second user device. After the recovery-capable source is merged and actually served/installed on the current iPhone, normal open/resume is the intended trigger; any runtime evidence must come from that authentic execution rather than manual recreation.
