# StegOS Persistent Card UX Mirror Handoff

Updated: 2026-09-06
Repository: StegVerse-Labs/Site
Issue: #1000
Goal: SITE-STEGOS-PERSISTENT-CARD-UX-1000

## Source of truth

This file is the bounded continuation record for Site issue #1000. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`. The current SV001 custody/recovery authority boundary remains `docs/MR_SV001_CURRENT_IPHONE_CUSTODY_MIRROR_HANDOFF.md`.

## Objective

Maintain a reusable same-device operational-card UX while making completed local workflow state automatically reusable without manufacturing authority or forcing users to recreate machine evidence.

Current required behavior:

```text
logical workflow section -> card
completed card -> green border
incomplete/blocked card -> red border
hydrating card -> neutral temporary state only
completed device-local data -> restored on later visits to this device
reusable text/input/output -> adjacent Copy Text control
purpose/remediation/troubleshooting needed -> dedicated per-card help page
same-device exact evidence exists -> automatic reuse before manual import
legacy exact source absent but canonical retained journal sufficient -> canonical exact recovery
canonical exact recovery succeeds -> automatic existing machine-governed custody continuation
manual paste/import -> fail-closed fallback only
terminal SV001 -> never rerun merely for later custody/reconstruction
```

## Authority boundary

UI persistence, card coloring, copy controls, help pages, offline caching, source recovery presentation, and automatic browser continuation create no execution, custody, lease, credential, admission, publication, activation, or sovereign authority.

Canonical authority remains separated:
- Task Registry: work intent/coordination;
- WorkerCoordinator: execution claim/fence;
- Interlock/InTr: governed transition ingress/egress;
- Master Records: observed reality, custody, and reconstruction;
- TV/TVC: credential authority;
- HB: reference/correlation only, never authority.

The current SV001 -> Master Records transition is `MACHINE_GOVERNED`, `human_approval_required=false`, `current_governance_required=true`, and `prior_receipt_authorizes_transition=false`.

## Base persistent-card implementation

Previously merged source established:
- `stegos-bootstrap/index.html` stateful cards;
- `stegos-bootstrap/persistent-card-ux.js` same-device IndexedDB snapshots, red/green state, Copy Text, help links, terminal SV001 discovery, exact retained proof reuse;
- all eleven `stegos-bootstrap/help/*.html` routes;
- explicit offline-shell caching;
- deterministic source validation.

The terminal SV001 state must remain terminal even when a historical full proof snapshot is absent.

## Governed custody predecessor

The v12 shell successor previously added the machine-owned SV001 Master Records custody path through the existing root Universal InTr runtime. Functional PR #1067 merged as `e8cc4ee9ffd57eea57e1111834d67f88ee6c7e5d`; its claim was released through PR #1088. The merged path requires contemporaneous root-InTr admission and prohibits retroactive authorization of custody state.

v12 source/merge never established current-device custody runtime evidence.

## Canonical retained-journal recovery source

`master-records/orchestration` later merged PR #81 as `84ba89792a8e9057079d647c4909f8a510ff2559`, providing:

```text
portable/stegverse001-canonical-journal-recovery.js
blob: 5ca977c4214c3eec13bd2ac1109405e7f1571723
updated custody package blob: 70e02082d63d046101fa0a21d82e12261c891e79
target G23: sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35
target claim: SHWP-SHWP-STEGVERSE001-BOUNDED-AUTONOMY-RUNTIME-001-G23
target fence: 23
recovery authority effect: NONE_RECOVERY_ONLY
```

The canonical module can reconstruct the exact historical G23 full source object only from authentic retained journal material. It validates journal integrity, WorkerCoordinator checkout lineage, TVC single-cycle lease issuance/consumption, same-execution reconstruction, bounded timestamp search, and exact unique SHA-256 match. Zero/multiple matches or any inconsistency fail closed. Hashes/pointers/projections never substitute for source.

## Machine preflight — 2026-09-06

Durable preflight:
`data/preflight/site1000-auto-sv001-recovery-20260906.json`

Resolved before functional mutation:
- this handoff;
- `docs/MR_SV001_CURRENT_IPHONE_CUSTODY_MIRROR_HANDOFF.md`;
- Master Records canonical custody/recovery handoff and PR #81 source;
- `.github` canonical Task Registry generation 15;
- SV001 Master Records transition ownership evaluation;
- existing active branch/claim and open-PR collision state.

Disposition:
`CONTINUE_EXISTING_CLAIM_ONLY_AND_RECONCILE_ONTO_CURRENT_MAIN_BEFORE_FURTHER_FUNCTIONAL_EDITS`.

Existing branch/claim were reused; no duplicate was created:

```text
branch: continue/site1000-auto-sv001-recovery
claim: SITE-STEGOS-PERSISTENT-CARD-UX-1000-AUTO-RECOVERY-20260906
state: CLAIMED_FOR_IMPLEMENTATION
```

The stale branch was reconciled onto then-current `main` before further functional changes so the already-merged root-InTr/no-retroactive-authority implementation remained the base.

README impact:

```text
readme_impact_required: true
material_function_change: true
readme_path: README.md
readme_updated_in_same_change_set: true
reason: normal current-iPhone behavior now adds canonical journal recovery and automatic machine-governed custody continuation before manual fallback
```

## v13 recovery-capable source — active branch

Destination `StegVerse-Labs/Site`:

- `stegos-bootstrap/master-records-sv001-recovery.js`
  - exact canonical recovery module;
  - blob `5ca977c4214c3eec13bd2ac1109405e7f1571723`;
  - not a Site-local rewrite or stub.
- `stegos-bootstrap/master-records-sv001-custody-package.json`
  - exact updated canonical package;
  - blob `70e02082d63d046101fa0a21d82e12261c891e79`.
- `stegos-bootstrap/master-records-auto-recovery.js`
  - exact retained canonical G23 proof first;
  - canonical retained-journal recovery second;
  - requires exactly one complete G23 source object;
  - automatically calls the existing `StegOSWebBootstrap.executeMasterRecordsSv001Custody` path;
  - requires returned InTr-governed reconstruction PASS;
  - fails closed without rerunning SV001;
  - grants no custody/execution authority.
- `stegos-bootstrap/index.html`
  - loads both recovery modules after persistent-card support;
  - explains automatic recovery/continuation;
  - labels manual custody as fallback.
- `stegos-bootstrap/service-worker.js`
  - cache generation `stegos-web-bootstrap-v13`;
  - explicitly caches canonical recovery and automatic continuation assets;
  - preserves existing governed custody endpoint and no-retroactive-authorization behavior.
- `README.md`
  - documents v13 semantics, recovery predicates, fallback, authority boundaries, and non-runtime inference rule.
- validators
  - exact canonical recovery/package blob identities;
  - explicit v13 shell assets;
  - automatic existing custody API use;
  - no-human-approval/no-rerun markers;
  - exact index/service-worker successor blob pins.

## Runtime semantics

Normal current-iPhone open/resume is intended to perform:

```text
terminal SV001 discovered
-> exact persisted G23 proof?
   yes -> use it
   no -> canonical retained-journal recovery
-> exactly one complete canonical G23 source?
   no -> FAIL_CLOSED / manual exact-proof fallback only
   yes -> automatic existing machine-governed custody API
-> root Universal InTr contemporaneous ALLOW required
-> Master Records custody/reconstruction PASS required
-> retain evidence
```

The current-iOS human interaction guard still controls human mutation controls. It does not become a human approval gate for this machine-owned transition.

## Collision rule

Do not:
- create another InTr runtime, scheduler, WorkerCoordinator, claim/fence mechanism, recovery implementation, credential path, or custody module;
- change DEVICE_KV/HIL authority semantics;
- synthesize missing G23 fields;
- accept G24/duplicate evidence as G23;
- rerun terminal SV001 for recovery;
- infer runtime recovery/custody from source, CI, merge, cache generation, or publication.

## Completion predicates

1. Stateful card UX / red-green / Copy Text / help routes. **MERGED SOURCE.**
2. Same-device card persistence and terminal SV001 guard. **MERGED SOURCE; LIVE REVISIT OBSERVATION DISTINCT.**
3. Exact retained-proof reuse before fallback. **MERGED SOURCE.**
4. Canonical Master Records recovery module and updated package projected byte-for-byte. **IMPLEMENTED ON ACTIVE BRANCH.**
5. Automatic exact retained-proof -> canonical recovery -> existing governed custody continuation. **IMPLEMENTED ON ACTIVE BRANCH.**
6. v13 shell explicitly caches recovery assets. **IMPLEMENTED ON ACTIVE BRANCH.**
7. README completeness for material runtime/failure semantics. **IMPLEMENTED ON ACTIVE BRANCH.**
8. Exact source validation and merge-result validation. **PENDING.**
9. Merge and source-claim terminalization. **PENDING.**
10. Public/current-iPhone v13 installation. **NOT OBSERVED.**
11. Authentic current-iPhone canonical G23 recovery. **NOT OBSERVED.**
12. Authentic contemporaneous root-InTr custody ALLOW. **NOT OBSERVED.**
13. Master Records custody/reconstruction PASS and retained evidence. **NOT OBSERVED.**
14. SV002 downstream disposition. **NOT OBSERVED.**

## Remaining machine work

1. Run exact-head PR validation on the existing branch/claim.
2. Repair only actual validation/merge-result defects without widening authority or duplicating machinery.
3. Merge only after exact merge-result validation passes.
4. Terminalize the existing source claim through canonical claim maintenance.
5. Keep deployment/current-device/runtime predicates distinct and fail-closed until observed.

Downstream propagation remains inappropriate until the relevant release/runtime predicates are genuinely reached.

## User work

Routine repository work: none.

Do not rerun SV001, synthesize G23, manually approve the machine-owned custody transition, or use a second user-operated machine. After the recovery-capable source is merged and actually served/installed on the current iPhone, normal open/resume is the intended runtime trigger.

## Archive readiness

Issue #1000 source lane is **not archive-ready** while the active recovery claim remains unmerged/unreleased. The prior v12 governance implementation is released. The broader runtime objective remains open separately until authentic current-device evidence exists.
