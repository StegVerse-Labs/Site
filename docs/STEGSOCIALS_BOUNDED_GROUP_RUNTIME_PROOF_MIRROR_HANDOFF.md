# StegSocials bounded-group runtime proof mirror handoff

Updated: 2026-09-10

- Goal Task ID: `SS-KV-SKAP-SOCIAL-RELEASE-001`
- COSV: `60000000102000`
- Parent: `StegVerse-Labs/StegSocials/docs/STEGSOCIALS_NATIVE_STEGBROWSER_TRANSPORT_MIRROR_HANDOFF.md`
- Status: `ACTIVE`

## Implemented on this branch

The previously merged local path now exposes machine-readable observation evidence without reclassifying it as external admission:

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

New/updated source:

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

## Critical evidence boundary

`external_intr_admission_observed` remains `false` and `external_intr_admission_receipt_ref` remains `null` for this local observation. GeneratedInTr construction, local Node outbox creation, resident service-worker execution, and deterministic CI may not be promoted into external InTr admission evidence.

HB remains correlation/freshness only and cannot grant transition authority. TV/TVC remains credential authority. Site remains non-publishing and receives no provider credential material.

## Remaining runtime work

1. Validate and merge this instrumentation.
2. Exercise it on the retained current iPhone with an authentic already-proven publication/destruction CAS request and retain the emitted pre/post DEVICE_KV proof.
3. Bind a separately authentic external InTr admission receipt to the exact query/materialization identity; do not infer it from local construction.
4. Complete TV/TVC-SKAP -> retained StegBrowser credential/session execution.
5. Produce authentic Facebook/LinkedIn/Instagram publication result + terminal destruction evidence.
6. Execute at least two in-scope bounded-group posts without renewed approval and prove replay/stale/widening refusal.
7. Feed publication output and committed group state into Personal-KV custody and Master Records reconstruction.

## Manual work

None while source validation remains executable. Owner interaction is required only at an authentic credential/session/platform boundary that cannot be satisfied from already admitted TV/TVC-SKAP material.
