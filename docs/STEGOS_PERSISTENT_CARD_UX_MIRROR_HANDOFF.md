# StegOS Persistent Card UX Mirror Handoff

Updated: 2026-09-06
Repository: StegVerse-Labs/Site
Issue: #1000
Goal: SITE-STEGOS-PERSISTENT-CARD-UX-1000
State: AUTO_GOVERNED_RUNTIME_CONTINUATION_SOURCE_IN_PROGRESS

## Source of truth

This is the bounded continuation record for Site #1000. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`. The focused SV001 -> Master Records authority/runtime handoff is `docs/MR_SV001_CURRENT_IPHONE_CUSTODY_MIRROR_HANDOFF.md`.

## Resolved existing runtime solution

A runtime problem MUST reuse the runtime machinery already built before creating or requiring another execution surface.

Resolved canonical sources:

```text
StegVerse-Labs/.github/docs/HEARTBEAT_RUNTIME_SEPARATION_MIRROR_HANDOFF.md
StegVerse-Labs/.github/handoffs/HEARTBEAT-INDEPENDENT-OSCILLATOR-LIVE-009.json
StegVerse-Labs/.github/docs/HB_RUNTIME_PRESENCE_RESIDENT_OBSERVABILITY_MIRROR_HANDOFF.md
Site/docs/STEGOS_IPHONE_RESIDENT_TASK_PROJECTION_MIRROR_HANDOFF.md
Site/stegos-bootstrap/stegos-bootstrap.js
Site/intr-service-worker.js
master-records/orchestration canonical G23 recovery/custody modules
```

Existing HB state:

```text
protocol: HB32
progression_dependency: OSCILLATOR_ONLY
independent oscillator proof: COMPLETED / ACTIVE_PROTOCOL_VERIFIED
continuous resident process required for HB progression: false
heartbeat grants execution/transition authority: false
```

Existing same-device custody executor:
`StegOSWebBootstrap.executeMasterRecordsSv001Custody()`.

It already derives a current HB32 reference, builds the non-authorizing carrier binding, obtains a fresh root Universal InTr decision for `MasterRecords:SV001Custody`, then invokes the existing nested Master Records endpoint only after `ALLOW`.

## Defect found after v13 release

The v13 source released through Site #1092/#1093 correctly added deterministic canonical G23 recovery, but `master-records-auto-recovery.js` stopped at:

```text
RECOVERED_HASH_VERIFIED_PENDING_MACHINE_GOVERNANCE
custody_executed=false
```

That stop was a progression defect because the current-device runtime already had the exact machine-governed next-transition executor. It incorrectly converted an existing runtime solution into a passive observation/wait state.

## Current repair — Site #1096

Claim:
`SITE-SV001-AUTO-GOVERNED-CUSTODY-HB-RUNTIME-1096-20260906`.

Branch:
`fix/sv001-auto-governed-custody-hb-runtime-1096`.

Preflight:
`data/preflight/sv001-auto-governed-custody-hb-runtime-1096.json` = PASS.

README impact: **MATERIAL / UPDATED IN SAME CHANGE SET** because behavior changes from recovery-ready-only to automatic machine-owned progression through contemporaneous governance.

New bounded flow:

```text
terminal SV001 detected
-> exact retained canonical G23 proof exists?
   -> yes: validate exact G23 cycle receipt
   -> no: invoke exact canonical retained-journal recovery
-> require exact canonical G23 / unique verified recovery as applicable
-> source is evidence only; grants no authority
-> automatically invoke EXISTING StegOSWebBootstrap.executeMasterRecordsSv001Custody()
-> derive current HB32 oscillator reference (carrier/correlation only)
-> root Universal InTr MasterRecords:SV001Custody
-> require fresh write-once ALLOW for this exact transition
-> nested endpoint independently validates/retains admission
-> canonical Master Records custody
-> canonical reconstruction PASS
-> retain resulting evidence
```

No user approval checkpoint is inserted. No new scheduler is created. Existing `DOMContentLoaded`, `pageshow`, and visibility-resume lifecycle opportunities are the retry surface; they do not grant authority.

If exact source recovery fails, manual exact-proof import remains source fallback only. If exact G23 exists but current governance/custody/reconstruction fails, state becomes `EXACT_G23_PRESENT_MACHINE_GOVERNANCE_FAIL_CLOSED`; SV001 is not rerun and G23 is not synthesized.

## v14 propagation successor

Installed v13 clients otherwise could continue serving the cached v13 recovery carrier. The repair therefore advances propagation without reimplementing the runtime:

```text
stegos-bootstrap/service-worker-v13-runtime.js
  = exact released v13 service-worker blob b48c79a6faf6735e262a5f2f791ff576d4379504

stegos-bootstrap/service-worker.js
  = small v14 propagation wrapper
  -> imports exact v13 runtime predecessor
  -> sets CACHE_NAME = stegos-web-bootstrap-v14
```

The v14 wrapper exists only to force installed clients to refresh changed shell assets. Root-InTr, DEVICE_KV, HIL, Master Records, WorkerCoordinator, TV/TVC, and local-model runtime behavior remain the exact existing implementations.

## Authority boundary

```text
Task Registry: work intent / coordination
WorkerCoordinator: execution claim / fence
Interlock/InTr: current transition governance
Master Records: custody / reconstruction / observed reality
TV/TVC: credential authority
HB32 oscillator: timing/reference/correlation only
Site: exact materialization + current-device carrier

prior receipt authorizes next transition: false
successful recovery authorizes custody: false
human approval required: false
human iOS queue blocks machine transition: false
new scheduler/runtime/heartbeat: false
second user-operated machine required: false
```

## Historical source evidence retained

```text
v12 root-InTr governance PR #1067
v12 functional merge e8cc4ee9ffd57eea57e1111834d67f88ee6c7e5d
v13 G23 recovery PR #1092
v13 functional merge 612ccfd316e9df5d93fa826ce34925f315302604
v13 claim release PR #1093
v13 claim-release merge 3000010973869ec994c141846b32902c1a2db88f
post-release handoff reconciliation PR #1094
```

Those facts do not prove current-device runtime consumption.

## Runtime truth

Source/CI/merge/cache generation are not substituted for runtime evidence. Until authentic retained receipts say otherwise:

```text
v14 source consumption on authentic current iPhone: NOT YET CLAIMED
fresh root-InTr ALLOW from that automatic continuation: NOT YET CLAIMED
Master Records custody/reconstruction PASS from that continuation: NOT YET CLAIMED
SV002 downstream disposition: NOT YET CLAIMED
```

The key distinction is that the implementation no longer intentionally waits for a human/session to trigger the already-machine-owned next transition.

## Development disposition

Fully developed/reused, not scaffolds:
- canonical G23 recovery module/package;
- same-device persistent-card journal;
- current iPhone StegOS runtime;
- HB32 independent oscillator/reference derivation;
- root Universal InTr `MasterRecords:SV001Custody` profile;
- same-device Master Records custody executor;
- no-retroactive-authorization handling.

Current functional repair under Site #1096:
- automatic exact-source -> existing governed executor wiring;
- v14 propagation wrapper around exact v13 runtime;
- validators/README/handoff completeness.

## User work

Routine repository or transition-approval work: **NONE**.

Do not rerun SV001, synthesize G23, manually approve the machine-owned custody transition, or introduce another device.

## Archive readiness

Historical v12/v13 source lanes are released/archive-ready. Site #1096 remains active until validation/merge/claim release. Authentic runtime evidence remains a separate truth predicate, not a reason to build another runtime solution.
