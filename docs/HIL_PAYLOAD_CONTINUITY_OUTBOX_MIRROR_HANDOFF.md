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
