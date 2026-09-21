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


## 2026-09-21 state-only custody predicate repair

The first concrete post-`LEASE_OPEN` defect was in the existing Site custody transition itself: resume/custody validation still made named execution-surface and other-machine fields predicates of `HIL_RECEIVER_CUSTODY`. That incorrectly turned runtime location metadata into transition authority.

The bounded repair removes those device predicates from the custody transition while retaining the actual state dependencies: task/request/lease identity, G25/fence-25, no successor claim minting, TV/TVC credential boundary, predecessor non-custodial state, exact response SHA-256, provenance, canonical InTr ingress/materialization, write-once custody persistence/readback, custody receipt hash, and downstream nonclaims. Retained `browser_context_id` and `node_id`, when present on the accepted lease, are carried as lineage metadata rather than compared to hard-coded execution-device constants. READY and ESRL `LEASE_OPEN` remain retained and are not replayed. Source validation must not be interpreted as authentic custody success.


## 2026-09-21 custody controller convergence repair

The first deterministic execution break after the state-only custody repair was in `hil-custody-activate.html`: `ensureWorker()` resolved after a 2.5-second timer even when `navigator.serviceWorker.controller` was still absent. The next POST to `/stegos-bootstrap/portable-workercoordinator/hil-custody-v1` could therefore bypass the already-existing service-worker custody handler and fall through to ordinary network handling.

The bounded repair keeps the existing service worker and custody route. It waits for actual controller acquisition; if the first load remains uncontrolled, it performs one automatic convergence reload and then resumes from retained state. If control is still absent after that bounded retry, it fails closed instead of issuing the custody POST outside the handler. READY, ESRL `LEASE_OPEN`, G25/fence-25, exact-byte/provenance/InTr checks, write-once custody, and downstream authority boundaries are unchanged.


## 2026-09-21 partial custody recovery repair

After service-worker routing is guaranteed, the next deterministic retry defect is the write-once custody-object boundary. If an earlier attempt persisted the exact custody object and stopped before its receipt write, every later attempt fails unconditionally.

The custody path now reuses that write-once object only after validating its schema, pending state, object key, retained lease, task, G25/fence-25, response hash, exact-byte SHA-256, provenance, and InTr receipt chain. Any mismatch remains fail-closed. A matching partial object proceeds to the existing receipt construction/write/readback path; no object is rewritten and no predecessor state is replayed.
