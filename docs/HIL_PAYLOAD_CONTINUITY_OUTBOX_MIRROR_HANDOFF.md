# HIL Payload Continuity Outbox Mirror Handoff

Updated: 2026-09-20
Repository: `StegVerse-Labs/Site`
Parent goal: `SHWP-HIL-SOVEREIGN-RECEIVER-001`
PR: `#1425`

## Defect

The HIL state chain retained receiver READY and ESRL `LEASE_OPEN`, but the exact response payload required by the next custody transition remained only in HIL-specific browser IndexedDB. The existing StegOS Node importer copied hashes and materialization metadata into `stegos-node-v1 / intr_outbox` but not the exact predecessor payload. The custody successor therefore could not recover its predecessor if the HIL-specific staging record was unavailable.

## Repair

Reuse the existing StegOS Node `intr_outbox` continuity record. Bind an exact-byte base64 representation, provenance manifest, transport intent, and materialization request into the already-hashed outbox entry. Mark the copy `custody_established=false`, `tvc_admission_completed=false`, `master_records_authority=false`, and `authority_effect=NONE_LOCAL_CONTINUITY_ONLY`.

The existing HIL custody successor continues to prefer its original HIL staging store. If that record is unavailable, it reads the existing node outbox continuity entry, restores the predecessor bytes, and runs the same unchanged fail-closed `verifyStaged(...)` validation before custody.

## Authority boundary

This repair creates no new database/store, runtime, scheduler, dispatcher, watcher, claim/fence, transition authority, custody authority, credential path, or device dependency. WorkerCoordinator remains claim/fence authority, Interlock/InTr remains transition authority, TV/TVC remains credential authority, and the HIL custody transition remains responsible for establishing custody.

## Completion boundary

Source completion requires the exact PR head to pass applicable Site validation and merge. It does not retroactively claim that the historical HIL custody transition occurred. After merge, HIL continuation begins at the genuinely missing `HIL_RECEIVER_CUSTODY` transition, with READY and ESRL already retained.


## 2026-09-20 resume/custody reachability repair

Post-merge inspection found a second bounded continuity defect. The custody worker could recover exact predecessor bytes from `stegos-node-v1 / intr_outbox`, but the canonical `hil-resume.html` router and `hil-custody-activate.html` entry surface still required HIL-specific localStorage metadata before that fallback could be reached. Loss of the HIL-specific staging metadata could therefore fail closed before the repaired custody worker executed.

The successor repair makes both entry surfaces treat the existing Node outbox as the same non-authorizing predecessor continuity source already established by PR #1425. The resume router discovers a qualifying `stegos.node_hil_payload_continuity/v1` row when local submission metadata is absent, re-hashes the recovered exact bytes, and routes to the existing custody successor. The custody page may derive only the already-bound object key from the same outbox and then calls the unchanged custody worker, which remains responsible for full provenance/InTr verification and write-once custody.

No localStorage evidence is synthesized or rewritten. No new store, runtime, scheduler, claim/fence, credential path, transition authority, or custody authority is introduced. READY and ESRL `LEASE_OPEN` remain retained predecessor states; the first unresolved authentic state remains `HIL_RECEIVER_CUSTODY`.


## 2026-09-20 merge and public propagation

Site PR #1430 merged as `da1f564d1799303f9df7f5a97d55a6669e2e9b3d` after exact-head Handoff Orchestrator, Bootstrap, Heartbeat, Node IndexedDB migration, no-third-party-runtime, and all other observed PR validations passed. Subsequent public proof commit `19c611e507f6d577b331c7481d6b4fc3817ac006` observed HTTP 200 for the canonical resume URL and verified the resume-router contract against source commit `da1f564d1799303f9df7f5a97d55a6669e2e9b3d`.

This closes the source/propagation repair only. No authentic `HIL-RECEIVER-RECEIPT-v2` is retained in the repository yet. The next state remains authentic `HIL_RECEIVER_CUSTODY` from the retained G25/fence-25, READY, ESRL `LEASE_OPEN`, and exact predecessor bytes.
