# StegOS Persistent Card UX Mirror Handoff

Updated: 2026-09-06
Repository: StegVerse-Labs/Site
Issue: #1000
Goal: SITE-STEGOS-PERSISTENT-CARD-UX-1000
State: SOURCE_REPAIR_COMPLETE_AUTHENTIC_RUNTIME_EVIDENCE_PENDING

## Source of truth

This is the bounded continuation record for Site #1000. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`. The focused SV001 -> Master Records runtime/authority record is `docs/MR_SV001_CURRENT_IPHONE_CUSTODY_MIRROR_HANDOFF.md`.

The SV001 runtime progression seam repair is complete. Site #1096 was implemented by PR #1098 and merged as `4bb0eafae549ef7b0874d341d2e8f9a11f293595`; its claim was terminalized by PR #1099 and is `RELEASED_COMPLETE / archive_eligible=true` on `main`. Site #955 was already reconciled after release through Site #1100. This handoff must not reopen or duplicate that canonical #955 coordination state.

Authentic current-device progression remains evidence-driven and is not established by source, CI, merge, cache generation, or handoff text.

## Reuse existing runtime solutions first

A runtime problem MUST reuse the runtime machinery already built before creating or requiring another execution surface.

Canonical resolved sources include:

```text
StegVerse-Labs/.github/docs/HEARTBEAT_RUNTIME_SEPARATION_MIRROR_HANDOFF.md
StegVerse-Labs/.github/handoffs/HEARTBEAT-INDEPENDENT-OSCILLATOR-LIVE-009.json
StegVerse-Labs/.github/docs/HB_RUNTIME_PRESENCE_RESIDENT_OBSERVABILITY_MIRROR_HANDOFF.md
Site/docs/STEGOS_IPHONE_RESIDENT_TASK_PROJECTION_MIRROR_HANDOFF.md
Site/stegos-bootstrap/stegos-bootstrap.js
Site/intr-service-worker.js
master-records/orchestration canonical G23 recovery/custody modules
```

Resolved heartbeat state:

```text
protocol: HB32
progression_dependency: OSCILLATOR_ONLY
independent oscillator proof: COMPLETED / ACTIVE_PROTOCOL_VERIFIED
continuous resident process required for HB progression: false
heartbeat grants execution/transition authority: false
```

The existing same-device custody executor is `StegOSWebBootstrap.executeMasterRecordsSv001Custody()`.

It validates exact canonical G23, derives a current HB32 reference, builds the existing non-authorizing Node/Interlock carrier binding, obtains a fresh root Universal InTr decision for `MasterRecords:SV001Custody`, and invokes canonical Master Records custody/reconstruction only after `ALLOW`.

## Persistent-card capability

The Site implementation provides reusable same-device operational cards, exact completed-state persistence/reuse, green/red completion semantics, Copy Text controls, per-card help routes, terminal SV001 rerun prevention, exact retained-proof discovery, canonical G23 deterministic recovery, and fail-closed manual exact-proof fallback.

The completed SV001 cycle remains terminal. G23 is the canonical custody-eligible source; retained G24 duplicate evidence is not substituted.

## Completed runtime-seam repair

The v13 recovery carrier previously stopped at:

```text
RECOVERED_HASH_VERIFIED_PENDING_MACHINE_GOVERNANCE
custody_executed=false
```

That was a progression defect because the exact machine-governed next-transition executor already existed.

The released #1096 behavior is:

```text
terminal SV001 detected
-> exact retained canonical G23 proof OR exact canonical retained-journal recovery
-> validate exact canonical G23
-> source/recovery grants no authority
-> automatically invoke existing StegOSWebBootstrap.executeMasterRecordsSv001Custody()
-> derive current HB32 oscillator reference
-> root Universal InTr MasterRecords:SV001Custody
-> require fresh write-once ALLOW
-> nested endpoint validates/retains admission
-> canonical Master Records custody
-> canonical reconstruction PASS
-> retain/replay evidence
```

No human approval checkpoint is inserted. No new scheduler, runtime, heartbeat, oscillator, WorkerCoordinator, InTr boundary, credential path, or custody implementation is created. Existing page/resume lifecycle opportunities remain the retry surface.

If exact source recovery fails, manual exact-proof import remains source fallback only. If exact G23 exists but current governance/custody/reconstruction fails, the carrier fails closed without rerunning SV001 or synthesizing G23.

## v14 propagation successor

Installed v13 clients could otherwise continue serving the old recovery carrier. The released propagation successor is:

```text
stegos-bootstrap/service-worker-v13-runtime.js
  exact released v13 runtime blob b48c79a6faf6735e262a5f2f791ff576d4379504

stegos-bootstrap/service-worker.js
  v14 propagation wrapper
  -> importScripts("./service-worker-v13-runtime.js")
  -> CACHE_NAME = "stegos-web-bootstrap-v14"
```

The wrapper forces shell refresh while preserving the exact existing runtime/governance implementation.

## Authority boundary

```text
Task Registry: work intent / coordination
WorkerCoordinator: execution claim / fence
Interlock/InTr: governed transition ingress/egress
Master Records: observed reality / custody / reconstruction
TV/TVC: credential authority
HB32: timing/reference/correlation only
Site: exact source materialization + same-device presentation/carrier

prior receipt authorizes next transition: false
successful recovery authorizes custody: false
human approval required: false
human iOS queue blocks machine transition: false
new scheduler/runtime/heartbeat: false
second user-operated machine required: false
```

## Canonical release evidence

```text
v12 root-InTr governance PR #1067
v12 functional merge e8cc4ee9ffd57eea57e1111834d67f88ee6c7e5d
v13 G23 recovery PR #1092
v13 functional merge 612ccfd316e9df5d93fa826ce34925f315302604
v13 claim release PR #1093
#1096 functional repair PR #1098
#1096 functional merge 4bb0eafae549ef7b0874d341d2e8f9a11f293595
#1096 claim-release PR #1099
#1096 claim-release merge c58d3959f485d614240e700c16e8ab372cebf7c8
#955 post-release reconciliation: Site #1100
```

These are source/coordination facts only and do not establish authentic current-device custody.

## Runtime truth

Until retained authentic receipts establish otherwise:

```text
v14 source consumption on authentic current iPhone: NOT YET CLAIMED
fresh root-InTr ALLOW from automatic continuation: NOT YET CLAIMED
Master Records custody/reconstruction PASS: NOT YET CLAIMED
retained same-execution progression chain: NOT YET CLAIMED
SV002 downstream disposition: NOT YET CLAIMED
```

Missing runtime evidence is not a reason to create another runtime implementation. Diagnose against the already-existing HB32/oscillator/carrier/InTr/custody path before proposing any new runtime component.

## Coordination reconciliation

Machine preflight: `data/preflight/site1000-sv001-runtime-release-reconcile-20260906.json` = `PASS`.

README disposition: `NO_README_CHANGE_REQUIRED`. This reconciliation changes stale coordination/status text and corrects a historical preflight path list only. It changes no repository behavior, runtime semantics, interfaces, governance/authority boundaries, evidence semantics, prerequisites, dependencies, failure behavior, or capability meaning. The material runtime/README change was already completed in PR #1098.

The historical #1096 preflight `admitted_mutation_scope` is corrected to include `scripts/check_stegos_ipod_bootstrap_projection.py`, which was part of the actual validated and released repair change set.

A previous reconciliation PR #1102 was closed without merge after current `main` was found to contain newer canonical #955 reconciliation state. That branch is not a valid continuation and must not be revived.

## Development disposition

Fully developed/released, not scaffolds:
- persistent-card state/reuse UX;
- canonical G23 recovery module/package projection;
- current-iPhone StegOS runtime;
- HB32 independent oscillator/reference derivation;
- root Universal InTr `MasterRecords:SV001Custody` profile;
- automatic exact-G23 -> existing governed executor continuation;
- canonical Master Records custody/reconstruction;
- no-retroactive-authorization handling;
- v14 propagation successor.

Remaining uninstalled independent runtime module identified by this lane: **none**.

## User work

Routine repository or transition-approval work: **NONE**.

Do not rerun SV001, synthesize G23, manually approve the machine-owned custody transition, or introduce another user-operated device.

## Archive readiness

The #1096 source implementation lane is released/archive-ready. Site #1000 remains open for its broader reusable-card objective, but this SV001 runtime-repair sublane is complete.

Authentic runtime completion remains a separate evidence predicate and must not be inferred from source, validation, merge, cache generation, publication, or this handoff reconciliation.
