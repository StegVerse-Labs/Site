# Current-iPhone Master Records SV001 Custody Projection Mirror Handoff

Updated: 2026-09-06
Repository: StegVerse-Labs/Site
Issue: #955
Goal: SITE-MR-SV001-CUSTODY-PROJECTION-955

## Current task source of truth

This handoff records the current source, governance, merge, claim, recovery, and runtime-evidence state for the current-iPhone SV001 -> Master Records custody continuation.

The contemporaneous root-InTr governance implementation is merged and released. Canonical deterministic G23 recovery source now also exists in the Master Records owner and is being projected into Site. Authentic current-iPhone recovery, Master Records custody/reconstruction, and SV002 disposition remain distinct runtime predicates and are **not** established by source, CI, merge, publication, deployment, or cache generation.

## Objective

Use the existing current-iPhone StegOS surface to carry the already-completed canonical G23 SV001 source object into Master Records custody without rerunning autonomy, without requiring another user-operated machine, and without allowing Site to become custody or transition authority.

For the legacy G23 execution whose full proof snapshot predates persistent-card retention, attempt exact deterministic hash-verified recovery from retained same-device journal evidence before manual exact-proof fallback.

## Canonical Master Records dependencies

Canonical owner: `master-records/orchestration`.

Portable custody source:

```text
issue: master-records/orchestration#72
PR: #73
merge: 9b617459ec0b9dfceb894ac19495ee72106d1e94
portable custody module blob: ea390cee958c67ff5d144abb43963e07f891a1ef
```

Canonical retained-journal recovery source:

```text
canonical task: MR-STEGVERSE001-BOUNDED-AUTONOMY-001
recovery issue: master-records/orchestration#64
recovery PR: #81
recovery merge: 84ba89792a8e9057079d647c4909f8a510ff2559
recovery module: portable/stegverse001-canonical-journal-recovery.js
recovery module blob: 5ca977c4214c3eec13bd2ac1109405e7f1571723
updated custody package blob: 70e02082d63d046101fa0a21d82e12261c891e79
```

Site must project the canonical recovery module and updated package byte-for-byte. Site-local code may only provide same-device discovery/recovery request, governance request, and local persistence carriage around canonical modules.

## Authentic canonical SV001 source identity already established

```text
execution surface: CURRENT_USER_IPHONE
task: SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001
claim/fence: G23 / 23
transition: SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED
canonical cycle receipt identity: sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35
device-local reconstruction: PASS / same_execution=true
TVC lease consumption: CONSUMED
```

G24 remains retained duplicate terminal evidence and is non-custodial.

The SV001 autonomy cycle is terminal. It MUST NOT be rerun to satisfy custody or recreate evidence.

The retained G23 identity is evidence input and recovery verification target only. It does not authorize custody or substitute for the complete object.

## Canonical source-recovery semantics — 2026-09-06

The previously open source-object recovery gap is now source-implemented by `master-records/orchestration#81`.

The canonical recovery primitive reconstructs the complete G23 cycle object only after validating:

- retained hash-linked journal integrity;
- canonical WorkerCoordinator G23/fence 23 lineage and self-hash;
- TVC single-cycle lease issuance and self-hash;
- external WorkerCoordinator/TVC binding;
- terminal receipt naming the canonical G23 cycle hash;
- same-execution reconstruction PASS;
- TVC lease consumption `CONSUMED`;
- evidence-derived bounded completion-time interval.

The recovery search succeeds only when exactly one complete candidate reproduces the canonical G23 SHA-256. For the retained canonical window, the unique candidate carries:

`completed_at=2026-09-03T15:05:16.887Z`.

Fail-closed conditions include zero matches, multiple matches, missing/invalid journal links, inconsistent claim/fence/lease lineage, excessive timestamp bounds, or any hash mismatch.

Therefore the correct distinction is now:

```text
canonical deterministic recovery source implemented: true
authentic current-iPhone recovery actually observed: false
known G23 hash alone is source object: false
missing fields may be approximated/synthesized: false
terminal SV001 may be rerun: false
successful recovery itself grants custody authority: false
```

## Site authority boundary

```text
Site role: EXACT SOURCE MATERIALIZATION + SAME-DEVICE RECOVERY/GOVERNANCE/PERSISTENCE CARRIER ONLY
Master Records custody authority: master-records/orchestration
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
successful recovery grants custody authority: false
historical state grants retroactive authority: false
human approval required: false
human iOS interaction queue blocks transition: false
second user-operated machine required: false
external non-StegVerse machine required: false
```

## Current machine-owned current-iPhone flow

```text
terminal canonical G23 detected on same-device history
-> exact persisted full proof present?
   -> yes: reuse exact proof
   -> no: invoke exact canonical retained-journal recovery
-> recovery must return RECOVERED_HASH_VERIFIED / unique_match_count=1
-> complete exact canonical G23 source object available to Site carrier
-> browser carrier reads canonical registered Node/Interlock identity
-> browser constructs exact MACHINE_GOVERNED custody transition request
-> HB-derived carrier binding (reference/correlation only; no authority)
-> existing root /intr-service-worker.js
-> MasterRecords:SV001Custody profile
-> contemporaneous exact transition validation
-> write-once InTr ALLOW/DENY receipt
-> ALLOW receipt bound to G23 + Node + Interlock + request + HB reference
-> bootstrap Master Records endpoint receives exact G23 object + exact admission receipt
-> validates admission again before mutation
-> appends admission receipt to existing local journal
-> exact canonical Master Records portable module
-> Master Records custody object
-> Master Records reconstruction PASS
-> append exact custody/reconstruction objects to existing local journal
-> replay journal PASS
-> portable custody proof carrying admission/custody/reconstruction bindings
-> downstream SV002 continuation
```

No human approval checkpoint belongs in this machine-owned flow. Execution on the current iPhone does not make it human-owned.

## Contemporaneous root-InTr governance implementation

Functional implementation claim:

```text
claim: SITE-SV001-MR-INTR-GOVERNANCE-20260905
functional PR: #1067
functional merge: e8cc4ee9ffd57eea57e1111834d67f88ee6c7e5d
claim-release PR: #1088
claim-release merge: 6e3e2a5e6043e5bddca504be70da55989cebb6b3
claim state: RELEASED_COMPLETE
```

The released implementation introduced a bounded `MasterRecords:SV001Custody` profile on the existing root Universal InTr service worker. It did not create another InTr runtime.

The exact custody transition requires:

```text
transition: SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION
authority_class: MACHINE_GOVERNED
human_approval_required: false
current_governance_required: true
prior_receipt_authorizes_transition: false
source: exact canonical G23
registered Node/Interlock binding: required
HB-derived carrier: reference/correlation only
```

The nested bootstrap service worker independently validates the admission receipt and appends it before any new custody/reconstruction mutation.

## No retroactive authorization

The merged path remains fail closed:

```text
custody + reconstruction + matching retained contemporaneous admission
-> validate admission again
-> canonical reconstruction
-> journal replay PASS
-> idempotent PASS

custody + reconstruction + no matching retained admission
-> FAIL_CLOSED
-> historical_state_retroactively_authorized=false
-> do not mint replacement admission
-> do not infer authorization from G23/recovery
-> do not rerun SV001

admission only OR custody only OR reconstruction only
-> PARTIAL STATE
-> FAIL_CLOSED
-> explicit recovery required
-> prior admission may not authorize a later mutation
```

A recovered G23 source object changes source availability only. It does not alter these transition-governance rules.

## Site v13 recovery continuation preflight — 2026-09-06

Durable preflight: Site issue #1000 comment `5557912138`.

A prior unmerged recovery working branch had become 43 commits behind `main` after the root-InTr v12 repair merged. That branch is superseded and must not be merged as-is.

Fresh continuation:

```text
branch: continue/site1000-auto-sv001-recovery-v12
claim: SITE-STEGOS-PERSISTENT-CARD-UX-1000-AUTO-RECOVERY-20260906
reuse #1000 persistent-card capability: true
reuse #955 custody carrier: true
reuse merged root-InTr v12 governance: true
new InTr runtime: false
new WorkerCoordinator: false
new credential path: false
README impact required: true
```

The README is updated in the same change set because automatic canonical recovery changes runtime prerequisites/interface/failure behavior.

## v13 recovery projection source

The fresh continuation adds:

- exact `stegos-bootstrap/master-records-sv001-recovery.js` from canonical blob `5ca977c4214c3eec13bd2ac1109405e7f1571723`;
- exact updated `stegos-bootstrap/master-records-sv001-custody-package.json` blob `70e02082d63d046101fa0a21d82e12261c891e79`;
- `stegos-bootstrap/master-records-auto-recovery.js` as a non-authorizing Site carrier;
- bootstrap page loading and recovery-ready presentation;
- explicit service-worker shell successor `stegos-web-bootstrap-v13` so installed clients can receive the recovery assets;
- exact recovery-blob and root-InTr preservation validation.

The recovery carrier:

```text
reuses exact persisted proof first
otherwise reads existing same-device journal
invokes exact canonical recovery
requires RECOVERED_HASH_VERIFIED
requires unique_match_count=1
requires authority_effect=NONE_RECOVERY_ONLY
fills exact recovered source into existing custody carrier
sets RECOVERED_HASH_VERIFIED_PENDING_MACHINE_GOVERNANCE
custody_executed=false
waits for contemporaneous root-InTr governance
```

Manual exact-proof input remains a fail-closed fallback when exact retained material is insufficient.

## Runtime truth after source implementation

The source recovery path is implemented, but authentic current-device execution remains unobserved until real retained evidence says otherwise:

```text
canonical G23 identity observed: true
canonical journal-recovery source merged in MR owner: true
exact recovery projection present in Site branch: source fact only
authentic current-iPhone G23 full source recovery: NOT OBSERVED
current-device root-InTr custody ALLOW: NOT OBSERVED
Master Records G23 custody: NOT OBSERVED
Master Records reconstruction PASS: NOT OBSERVED
retained same-execution admission/custody/reconstruction chain: NOT OBSERVED
SV002 disposition: NOT OBSERVED
```

No runtime completion may be inferred from merge, validation, source projection, publication, deployment, or claim release.

## Remaining distinct executable work

Repository/source lane:

1. validate exact recovery module/package projection and v13 shell successor;
2. validate preservation of the merged root-InTr custody governance path;
3. merge only after focused/relevant Site validations pass;
4. release the active recovery continuation claim.

Runtime lane after source release:

1. observe authentic current-iPhone canonical G23 recovery from retained same-device journal;
2. obtain contemporaneous root-InTr ALLOW for the machine-owned custody transition;
3. execute canonical Master Records custody/reconstruction and retain the admission/custody/reconstruction chain;
4. require reconstruction PASS;
5. only then evaluate downstream SV002 disposition.

Do not create another Site InTr runtime, scheduler, WorkerCoordinator, claim/fence mechanism, credential path, or duplicate custody implementation.

## Installation/module disposition

Developed source:
- canonical Master Records portable custody projection;
- merged root-InTr Master Records governance profile;
- no-retroactive-authorization semantics;
- exact canonical G23 recovery primitive in Master Records owner;
- exact recovery/package Site projection on the active branch;
- automatic same-device recovery carrier;
- v13 offline-shell recovery propagation;
- deterministic recovery/root-InTr validators.

Not scaffolds/stubs:
- the above paths are implemented source.

Not established as runtime-complete:
- current-iPhone recovered full G23 object;
- root-InTr custody ALLOW;
- Master Records custody/reconstruction PASS;
- retained same-execution chain;
- SV002 disposition.

## Archive readiness

The former root-InTr source implementation claim is released/archive-eligible.

The active v13 recovery continuation is not archive-ready until validation, merge, and claim release. After that source closure, authentic recovery/custody/SV002 remain separate runtime predicates.

## User work

Routine repository work: none.

Do not rerun SV001, synthesize the source object, manually approve the machine-owned custody transition, or provide another user-operated machine.
