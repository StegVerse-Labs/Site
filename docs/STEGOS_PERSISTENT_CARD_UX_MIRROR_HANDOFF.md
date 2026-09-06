# StegOS Persistent Card UX Mirror Handoff

Updated: 2026-09-06
Repository: StegVerse-Labs/Site
Issue: #1000
Goal: SITE-STEGOS-PERSISTENT-CARD-UX-1000

## Source of truth

This file is the bounded continuation record for Site issue #1000. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`. The completed SV001 custody authority boundary remains `docs/MR_SV001_CURRENT_IPHONE_CUSTODY_MIRROR_HANDOFF.md`.

## Objective

Establish a reusable same-device operational-card UX contract, beginning with `stegos-bootstrap/`, while making canonical legacy G23 evidence recovery automatic when sufficient retained same-device material exists.

Required behavior:

```text
logical workflow section -> card
completed card -> green border
incomplete/blocked card -> red border
hydrating card -> neutral temporary state only
completed device-local data -> restored on later visits to this device
reusable text/input/output -> adjacent Copy Text control
purpose/remediation/troubleshooting needed -> dedicated per-card help page
same-device exact evidence exists -> automatic reuse before manual import
legacy canonical G23 full proof absent -> automatic exact hash-verified journal recovery attempt
successful recovery -> recovery-ready only / no custody authority
custody mutation -> existing contemporaneous root-InTr governance path only
manual paste/import -> fail-closed fallback when exact retained material is insufficient
```

## Authority boundary

UI persistence, card coloring, copy controls, help pages, offline caching, and canonical G23 recovery create no execution, custody, lease, credential, admission, publication, activation, or sovereign authority.

The previously completed StegVerse-001 bounded-autonomy cycle is terminal and MUST NOT be rerun merely to satisfy Master Records custody or recreate missing evidence. Canonical G23 remains the only custody-eligible source; G24 is retained duplicate non-custodial evidence.

## Existing persistent-card source state

Destination `StegVerse-Labs/Site` already provides:

- `stegos-bootstrap/index.html`
  - loads the persistent card UX layer;
  - starts SV001 from device-history discovery;
  - makes same-device Master Records proof discovery the normal path;
  - prevents normal SV001 rerun once terminal;
  - retains exact manual proof input as fallback.
- `stegos-bootstrap/persistent-card-ux.js`
  - uses the existing same-device IndexedDB store;
  - persists per-card snapshots under `ui-card-state:*`;
  - restores completed card data on revisit;
  - applies green/red border semantics;
  - installs Copy Text controls;
  - adds per-card help links;
  - scans local state for terminal SV001 execution;
  - reuses an exact retained full SV001 proof when present;
  - preserves `authority_effect: NONE`.
- `stegos-bootstrap/help/*.html`
  - dedicated pages exist for all eleven cards.

## Historical offline-shell progression

```text
v10 predecessor service-worker blob: 048ae96f211e28314fa91c6a34cbc29ec13a2a26
v11 complete card shell blob: 9fdb5a580002c3a881f1523938ab1c0bcb127546
v12 root-InTr governed custody shell: merged/released through SITE-SV001-MR-INTR-GOVERNANCE-20260905
v12 functional merge: e8cc4ee9ffd57eea57e1111834d67f88ee6c7e5d
v12 claim release merge: 6e3e2a5e6043e5bddca504be70da55989cebb6b3
```

The v12 successor established that new SV001 Master Records custody/reconstruction mutation requires a contemporaneous root Universal InTr ALLOW bound to canonical G23, registered Node/Interlock, machine-governed authority class, request, and current HB-derived carrier reference. Historical custody without the retained contemporaneous admission is not retroactively authorized.

## Canonical Master Records recovery owner — 2026-09-06

Canonical owner: `master-records/orchestration`.

Merged source:

```text
issue: master-records/orchestration#64
recovery PR: master-records/orchestration#81
merge: 84ba89792a8e9057079d647c4909f8a510ff2559
recovery module: portable/stegverse001-canonical-journal-recovery.js
recovery module blob: 5ca977c4214c3eec13bd2ac1109405e7f1571723
updated custody package blob: 70e02082d63d046101fa0a21d82e12261c891e79
canonical G23 target: sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35
canonical claim/fence: G23 / 23
unique recovered completed_at: 2026-09-03T15:05:16.887Z
```

The recovery primitive validates the retained journal chain, WorkerCoordinator G23/fence lineage, TVC issuance, external binding, same-execution reconstruction PASS, and single-cycle lease consumption. It accepts recovery only when exactly one complete candidate reproduces the canonical source hash within the bounded evidence-derived timestamp interval. Zero matches, multiple matches, missing links, lineage drift, excessive bounds, or hash mismatch fail closed.

The canonical hash is a verification predicate, not substitute source material.

## Refreshed machine preflight — 2026-09-06

Durable preflight evidence: Site issue #1000 comment `5557912138`.

The live state was reconciled against:

- this handoff and Site issue #1000;
- `docs/MR_SV001_CURRENT_IPHONE_CUSTODY_MIRROR_HANDOFF.md` / issue #955;
- Master Records task `MR-STEGVERSE001-BOUNDED-AUTONOMY-001`;
- current-user iOS interaction queue and machine-owned exclusion;
- the released v12 root-InTr custody-governance claim;
- open PR/collision state;
- the merged Master Records #81 recovery implementation.

A prior unmerged working branch `continue/site1000-auto-sv001-recovery` had become 43 commits behind current `main` after v12 root-InTr governance merged. It is superseded and MUST NOT be merged as-is.

Preflight disposition:

```text
PASS / REBASE_BY_FRESH_CONTINUATION_FROM_CURRENT_MAIN
reuse existing #1000 UX task: true
reuse existing #955 custody carrier: true
reuse merged v12 root-InTr governance: true
new InTr runtime: false
new WorkerCoordinator: false
new credential path: false
SV001 rerun: false
README impact required: true
```

README impact is material because the runtime prerequisite/interface/failure behavior changes from legacy full-object absence requiring manual exact-proof fallback to automatic deterministic same-device journal recovery before fallback. `README.md` is updated in the same change set and explicitly preserves the source-vs-runtime distinction and root-InTr authority boundary.

## v13 canonical G23 auto-recovery continuation — 2026-09-06

Fresh continuation branch:

`continue/site1000-auto-sv001-recovery-v12`

Active claim:

`SITE-STEGOS-PERSISTENT-CARD-UX-1000-AUTO-RECOVERY-20260906`

Implemented source:

- `stegos-bootstrap/master-records-sv001-recovery.js`
  - exact byte projection of canonical Master Records recovery blob `5ca977c4214c3eec13bd2ac1109405e7f1571723`.
- `stegos-bootstrap/master-records-sv001-custody-package.json`
  - exact byte projection of canonical updated package blob `70e02082d63d046101fa0a21d82e12261c891e79`.
- `stegos-bootstrap/master-records-auto-recovery.js`
  - waits for terminal same-device SV001 hydration;
  - reuses an exact persisted proof first;
  - otherwise reads the existing same-device journal and invokes the canonical recovery primitive;
  - requires `RECOVERED_HASH_VERIFIED`, exactly one candidate, and `NONE_RECOVERY_ONLY`;
  - fills the existing Master Records carrier with the complete recovered source object;
  - sets `RECOVERED_HASH_VERIFIED_PENDING_MACHINE_GOVERNANCE`;
  - does not execute custody;
  - leaves custody waiting on `CONTEMPORANEOUS_INTERLOCK_INTR_GOVERNANCE_FOR_SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION`;
  - retries on open/resume opportunities without creating a daemon or second execution surface.
- `stegos-bootstrap/index.html`
  - loads exact recovery before the automatic recovery carrier;
  - documents automatic same-device recovery and root-InTr custody boundary.
- `stegos-bootstrap/service-worker.js`
  - advances explicit shell cache from v12 to `stegos-web-bootstrap-v13` only so installed clients can receive the recovery assets;
  - preserves the already-merged root-InTr governance/custody implementation unchanged;
  - adds the two recovery assets to the explicit shell.
- validators
  - preserve exact successor admission without wildcard/prefix matching;
  - require exact canonical recovery blobs;
  - verify v13 shell, G23 target, recovery non-authority, existing root-InTr gate, and no retroactive authorization.

## Runtime truth

The v13 source continuation does not change runtime truth by itself.

Still requiring authentic current-iPhone observation:

```text
canonical G23 source object recovered from retained same-device journal: NOT YET OBSERVED
contemporaneous root-InTr custody ALLOW: NOT YET OBSERVED
Master Records custody materialized: NOT YET OBSERVED
Master Records reconstruction PASS: NOT YET OBSERVED
SV002 adversarial disposition: NOT YET OBSERVED
```

Source, CI, merge, publication, deployment, or cache generation must not be substituted for any of those predicates.

## Collision rule

Do not alter canonical Master Records validation logic or WorkerCoordinator/TVC authority semantics. Do not create a second InTr runtime, scheduler, claim/fence authority, resident executor, or credential path. Do not use G24 for custody. Do not retroactively authorize historical state. Do not route the machine-owned custody transition through the human interaction queue. Do not claim authentic runtime execution from source/UI/cache changes.

## Completion predicates

1. Every StegOS bootstrap workflow section is represented as a stateful card. **SOURCE IMPLEMENTED.**
2. Card completion state deterministically maps to green/red border semantics after hydration. **SOURCE IMPLEMENTED.**
3. Completed card data survives reload/revisit on the same device. **SOURCE IMPLEMENTED; LIVE BROWSER REVISIT PROOF PENDING.**
4. Reusable text surfaces expose Copy Text. **SOURCE IMPLEMENTED.**
5. Dedicated help routes exist for cards needing explanation/remediation/troubleshooting. **SOURCE IMPLEMENTED.**
6. SV001 completed state is restored and does not present rerun as the normal path. **SOURCE IMPLEMENTED; LIVE SAME-DEVICE PROOF PENDING.**
7. Exact persisted SV001 proof is reused when present. **SOURCE IMPLEMENTED; LIVE SAME-DEVICE PROOF PENDING.**
8. Legacy canonical G23 automatically attempts exact retained-journal recovery before manual fallback. **SOURCE IMPLEMENTED; REPOSITORY VALIDATION PENDING.**
9. Recovery remains non-authorizing and does not bypass contemporaneous root-InTr custody governance. **SOURCE IMPLEMENTED; REPOSITORY VALIDATION PENDING.**
10. Persistent-card, recovery, and all help assets are explicit v13 shell assets. **SOURCE IMPLEMENTED; REPOSITORY VALIDATION PENDING.**
11. Exact canonical recovery module/package blobs are admitted without wildcard equivalence. **SOURCE IMPLEMENTED; REPOSITORY VALIDATION PENDING.**
12. README completeness accompanies the material recovery/cache change. **SOURCE IMPLEMENTED; REPOSITORY VALIDATION PENDING.**
13. No authority boundary is widened. **SOURCE IMPLEMENTED; REPOSITORY VALIDATION PENDING.**

## Remaining machine work

- execute the bounded #1000 validation workflow and exact StegOS projection checks;
- merge only after focused and relevant Site validations pass;
- release the active #1000 continuation claim;
- then observe authentic deployed/current-iPhone v13 recovery separately from source merge;
- after authentic recovery, reuse the existing root-InTr machine-governance path for custody/reconstruction;
- only after authentic reconstruction PASS may the existing SV002 continuation advance.

## Archive readiness

Not archive-ready while the v13 continuation claim remains active/unmerged. After validated merge and claim release, this source continuation can be archived while authentic current-device recovery/custody/SV002 remain separate runtime predicates.
