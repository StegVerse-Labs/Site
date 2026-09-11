# StegSocials bounded-group runtime proof mirror handoff

Updated: 2026-09-10

- Goal Task ID: `SS-KV-SKAP-SOCIAL-RELEASE-001`
- COSV: `60000000102000`
- Parent: `StegVerse-Labs/StegSocials/docs/STEGSOCIALS_NATIVE_STEGBROWSER_TRANSPORT_MIRROR_HANDOFF.md`
- Status: `ACTIVE`

## Merged implementation

Site PR #1209 merged at `a934718e4b490945d7e287876fd58e56f57110d9` after exact-head validation passed all four relevant workflows. The final source head was `e1aa4b27e4f383b71a632b5b52258e490def7f18`.

The merged path exposes machine-readable same-device observation evidence without reclassifying local construction as external InTr admission:

```text
owner-selected already-proven bounded-group CAS request
-> independent DEVICE_KV pre-state exact-byte/hash verification
-> registered StegVerse Node
-> GeneratedInTr COMMIT_CANDIDATE
-> HB correlation binding (non-authorizing)
-> Node outbox/materialization identity retained
-> existing MyKV resident worker
-> existing bounded-group DEVICE_KV atomic CAS receiver
-> independent DEVICE_KV post-state exact-byte/hash verification
-> secret-free runtime observation JSON
```

Merged source:

```text
assets/stegsocials-bounded-group-node-intr-bridge.js
assets/stegsocials-bounded-group-runtime-proof.js
stegsocials-bounded-group-runtime-proof.html
tests/stegsocials-bounded-group-runtime-proof.test.cjs
docs/STEGSOCIALS_BOUNDED_GROUP_RUNTIME_PROOF_README.md
.github/workflows/stegsocials-post-preparation.yml
```

`commitObserved()` retains the exact Node ID, Interlock ID, Node outbox hash, query request ID, GeneratedInTr packet/payload identity, materialization ID/request hash, minimized HB correlation observation, resident receipt commitment, and exact CAS result. The legacy `commit()` behavior remains backward-compatible and returns the CAS result only.

The runtime-proof surface verifies the current persisted row against `expected_previous_etag` before committing and independently verifies the final persisted row against `next_state_etag` afterward. It reuses `stegverse-device-local-intr-v1 / kv_files`; no second KV database or worker/runtime is created.

## Validation reconciliation

The initial CI run exposed two test/runtime harness defects rather than architecture defects:

1. the proof module used unqualified `atob`, which is not available in the Node VM test sandbox; the source now resolves the browser primitive through `root.atob` and fails closed when unavailable;
2. the stale-etag negative test used `assert.rejects` around a synchronous fail-closed precondition; it now uses `assert.throws` for that exact synchronous boundary.

Final exact-head workflows on `e1aa4b27e4f383b71a632b5b52258e490def7f18`:

```text
Site Bootstrap Validate - No Non-TV/TVC Credential Authority: PASS
Ecosystem Heartbeat Orchestration: PASS
StegSocials Post Preparation: PASS
Site Handoff Orchestrator: PASS
```

## Critical evidence boundary

`external_intr_admission_observed` remains `false` and `external_intr_admission_receipt_ref` remains `null` for this local observation. GeneratedInTr construction, local Node outbox creation, resident service-worker execution, and deterministic CI may not be promoted into external InTr admission evidence.

HB remains correlation/freshness only and cannot grant transition authority. TV/TVC remains credential authority. Site remains non-publishing and receives no provider credential material.

## Remaining runtime work

1. Exercise the merged proof surface on the retained current iPhone with an authentic already-proven publication/destruction CAS request and retain the emitted pre/post DEVICE_KV proof.
2. Bind a separately authentic external InTr admission receipt to the exact query/materialization identity; do not infer it from local construction.
3. Complete TV/TVC-SKAP -> retained StegBrowser credential/session execution.
4. Produce authentic Facebook/LinkedIn/Instagram publication result + terminal destruction evidence.
5. Execute at least two in-scope bounded-group posts without renewed approval and prove replay/stale/widening refusal.
6. Feed publication output and committed group state into Personal-KV custody and Master Records reconstruction.
7. Reconcile the authentic runtime evidence into the canonical task record and downstream propagation surfaces.

## Current task state

The canonical task registry remains `ACTIVE` with `checkout_state=BLOCKED_RUNTIME_ACTIVATION`. Source instrumentation for the local bounded-group DEVICE_KV observation seam is now merged and validated; the remaining blockers are authentic resident SKAP/social credential activation, native StegBrowser social publication runtime, and current-iPhone bounded-group runtime proof.

## Manual work

None at present. Owner interaction is required only at an authentic credential/session/platform boundary that cannot be satisfied from already admitted TV/TVC-SKAP material.
