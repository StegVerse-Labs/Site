# StegOS Persistent Card UX Mirror Handoff

Updated: 2026-09-06
Repository: StegVerse-Labs/Site
Issue: #1000
Goal: SITE-STEGOS-PERSISTENT-CARD-UX-1000
State: SOURCE_RELEASED_RUNTIME_EVIDENCE_PENDING

## Source of truth

This file is the bounded continuation record for Site issue #1000. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`. The SV001 -> Master Records custody/recovery boundary remains `docs/MR_SV001_CURRENT_IPHONE_CUSTODY_MIRROR_HANDOFF.md`.

This revision supersedes earlier in-file statements that described the v13 recovery continuation as active, unmerged, or awaiting repository validation. The source continuation is now merged and its source claim is released. Runtime recovery/custody evidence remains separate and unobserved.

## Objective

Provide reusable same-device StegOS operational cards while automatically attempting canonical legacy G23 source recovery from authentic retained same-device journal evidence before manual exact-proof fallback, without rerunning terminal SV001 or moving execution/custody/transition authority into Site.

## Canonical authority separation

```text
Task Registry = work intent / coordination
WorkerCoordinator = execution claim / fence
Interlock/InTr = governed transition ingress / egress
Master Records = observed reality / custody / reconstruction
TV/TVC = credential authority
HB = reference / correlation only; grants no authority
Site = exact source materialization + same-device presentation/recovery carrier
```

The custody transition remains:

```text
transition: SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION
authority_class: MACHINE_GOVERNED
current_governance_required: true
human_approval_required: false
prior_receipt_authorizes_transition: false
```

No human interaction queue becomes an approval gate for this machine-owned transition.

## Persistent-card capability

The merged Site implementation provides:

- `stegos-bootstrap/index.html`: stateful cards, terminal SV001 history-first behavior, same-device Master Records recovery presentation, manual exact-proof fallback.
- `stegos-bootstrap/persistent-card-ux.js`: IndexedDB card snapshots, green/red completion semantics, Copy Text, help links, terminal SV001 discovery, exact retained-proof reuse, authority effect none.
- `stegos-bootstrap/help/*.html`: dedicated help routes for all eleven cards.
- `stegos-bootstrap/service-worker.js`: explicit offline shell, current generation `stegos-web-bootstrap-v13`.

The completed SV001 cycle is terminal. It MUST NOT be rerun merely to satisfy later custody/reconstruction or recreate missing evidence. G23 is the canonical custody-eligible source; retained G24 duplicate terminal evidence is non-custodial.

## Canonical Master Records G23 recovery

Canonical owner: `master-records/orchestration`.

```text
recovery PR: master-records/orchestration#81
recovery merge: 84ba89792a8e9057079d647c4909f8a510ff2559
recovery module: portable/stegverse001-canonical-journal-recovery.js
recovery module blob: 5ca977c4214c3eec13bd2ac1109405e7f1571723
updated custody package blob: 70e02082d63d046101fa0a21d82e12261c891e79
canonical G23 SHA: sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35
canonical claim/fence: G23 / 23
```

The exact recovery primitive validates retained journal integrity, WorkerCoordinator G23/fence lineage, TVC issuance/consumption, same-execution reconstruction, bounded completion-time evidence, and exact unique SHA-256 reconstruction. Zero matches, multiple matches, missing links, lineage drift, excessive bounds, incomplete source material, or hash mismatch fail closed. The known hash is only a verification predicate and never substitutes for the complete source object.

## v12 governance predecessor

The contemporaneous root-InTr custody governance source merged through Site PR #1067 as:

`e8cc4ee9ffd57eea57e1111834d67f88ee6c7e5d`.

Its source claim `SITE-SV001-MR-INTR-GOVERNANCE-20260905` was released through PR #1088 / merge `6e3e2a5e6043e5bddca504be70da55989cebb6b3`.

The path requires a fresh root Universal InTr admission before a new Master Records custody/reconstruction mutation and prohibits retroactive authorization. Historical custody/reconstruction without the matching retained contemporaneous admission fails closed; admission-only/custody-only/reconstruction-only partial state also fails closed.

## v13 recovery source release — canonical current state

Fresh canonical continuation branch:
`continue/site1000-auto-sv001-recovery-v12`.

Source claim:
`SITE-STEGOS-PERSISTENT-CARD-UX-1000-AUTO-RECOVERY-20260906`.

Functional source PR:
`#1092`.

Functional merge:
`612ccfd316e9df5d93fa826ce34925f315302604`.

Claim-release PR:
`#1093`.

Claim-release merge:
`3000010973869ec994c141846b32902c1a2db88f`.

Source claim state:
`RELEASED_COMPLETE / archive_eligible=true`.

Superseded experimental PR #1091 was closed without merge after current `main` established #1092 as the canonical continuation. It MUST NOT be resurrected or merged as a competing implementation.

The merged v13 source includes:

- exact `stegos-bootstrap/master-records-sv001-recovery.js` canonical blob `5ca977c4214c3eec13bd2ac1109405e7f1571723`;
- exact `stegos-bootstrap/master-records-sv001-custody-package.json` blob `70e02082d63d046101fa0a21d82e12261c891e79`;
- `stegos-bootstrap/master-records-auto-recovery.js`, which reuses exact persisted proof first and otherwise invokes canonical retained-journal recovery;
- `stegos-bootstrap/index.html` recovery-ready presentation;
- `stegos-bootstrap/service-worker.js` v13 explicit recovery assets;
- README and validators updated in the same material source change.

The canonical merged recovery carrier stops at:

```text
RECOVERED_HASH_VERIFIED_PENDING_MACHINE_GOVERNANCE
custody_executed=false
waits_for=CONTEMPORANEOUS_INTERLOCK_INTR_GOVERNANCE_FOR_SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION
```

Recovery success grants no custody authority. The existing root-InTr machine-governance path remains the only admissible route to custody/reconstruction.

## Validation evidence

PR #1092 exact-head validation completed successfully for the relevant source and orchestration checks, including:

- Validate StegOS Persistent Card UX — SUCCESS
- Site Bootstrap Validate — SUCCESS
- Site Handoff Orchestrator — SUCCESS
- Ecosystem Heartbeat Orchestration — SUCCESS
- Ecosystem Visual Render Transport validation — SUCCESS

Those are source/merge-result facts only. They do not establish authentic current-device recovery or custody.

PR #1093 was claim-registry-only terminalization. Its final canonical terminal metadata preserves the implementation ownership fields and records PR #1093 plus functional release commit `612ccfd316e9df5d93fa826ce34925f315302604`.

## README completeness

The v13 recovery change materially changed runtime prerequisites/interface/failure behavior, so README was updated in the same functional source change set. The later claim release and this handoff reconciliation are status-only and require no further README mutation.

Post-merge reconciliation preflight:
`data/preflight/site1000-g23-recovery-handoff-reconcile-20260906.json`.

README disposition for this documentation-only reconciliation:
`NO_README_CHANGE_REQUIRED`.

## Runtime truth

Do not infer any of the following from source, CI, merge, release, cache generation, documentation, or publication:

```text
public/current-iPhone v13 installation: NOT OBSERVED IN THIS HANDOFF
canonical G23 source recovered from retained current-iPhone journal: NOT OBSERVED
root-InTr custody ALLOW after authentic recovery: NOT OBSERVED
Master Records custody materialization: NOT OBSERVED
Master Records reconstruction PASS: NOT OBSERVED
retained recovery/admission/custody/reconstruction chain: NOT OBSERVED
SV002 downstream disposition based on that chain: NOT OBSERVED
```

## Remaining admissible work

No further Site #1000 source implementation is presently required by this handoff.

The next distinct work is runtime observation on the authentic current iPhone after the merged v13 source is actually served/installed. Normal open/resume may attempt deterministic G23 journal recovery. Only an authentic recovery proof can establish recoverability. Only a fresh root-InTr ALLOW plus Master Records custody/reconstruction PASS and retained evidence can establish runtime custody completion.

Do not create another recovery implementation, InTr runtime, scheduler, WorkerCoordinator, claim/fence mechanism, credential path, or second user-operated device.

## Installation / development disposition

Destination: `StegVerse-Labs/Site`.

Fully developed and merged, not scaffolds/stubs:
- canonical recovery module projection;
- canonical updated custody package projection;
- same-device automatic recovery carrier;
- v13 offline-shell recovery asset projection;
- persistent-card UX and retained-proof reuse;
- root-InTr custody governance predecessor;
- exact source validators and README semantics.

Remaining uninstalled module identified by this source lane: **none**.

Actual current-device installation/propagation is an evidence predicate, not a missing source module.

## User work

Routine repository work: none.

Do not rerun SV001, synthesize G23, manually approve the machine-owned custody transition, or use a second user-operated machine.

## Archive readiness

The #1000 v13 **source lane is archive-ready/released** after PR #1092 and claim release #1093.

The broader SV001 -> Master Records runtime objective is **not runtime-archive-complete** until authentic current-device recovery, contemporaneous InTr admission, custody/reconstruction PASS, retained evidence, and downstream disposition are observed as applicable.
