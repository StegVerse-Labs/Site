# StegBrowser — SV002 validated lane retest

Goal Task ID: `STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001`
COSV: `40000100100000`

This branch does not construct a new runtime lane. It reuses the already-validated StegVerse-002 browser-recovery implementation currently retained in Site.

## Canonical reusable baseline

Execution owner/source provenance:

- `StegVerse-002/micro-node-runtime`
- browser execution implementation profile: `experiments/self-characterization-001/EXECUTION_IMPLEMENTATION_PROFILE.v0.8.json`
- principal worker: `web_runtime/sv002_principal_worker.js`

Site execution surface:

- `assets/sv002-local-runtime-materializer.js`
- `assets/sv002-principal-worker.js`
- `assets/generated/site-browser-intr-connectors.js`

Existing regression surfaces reused unchanged:

- `tests/test_sv002_self_contained_runtime.py`
- `tests/test_sv002_canonical_destination.py`

Historical successful engineering lane:

`registered StegVerse Node -> Interlock -> InTr materialization -> bounded lease -> EVENT_EPHEMERAL browser Web Worker -> principal execution -> independent Master Records reconstruction`

Historical primary validation identity:

- node: `SV-NODE-9fdb116d9520079e71a7f82b`
- interlock: `SV-IL-300325da3411909dfa04678b`
- lease: `SV002-LEASE-ba971cbac66c88cae08b0a96`
- runtime: `SV002-WEBRUNTIME-67477bfe819f0aae4dd489f2`
- run: `SV002-BROWSER-67477bfe819f0aae4dd489f2`
- substrate: `BROWSER_WEB_WORKER_ON_VALID_STEGVERSE_NODE`

## Retest rule

The SV002 execution mechanics are the fixture. They are not to be reconstructed as a new Python/runtime path.

For StegBrowser adaptation, modify only the invocation-specific bindings required by the current Goal/COSV/manifest and owned mirror route. Preserve Node gating, Interlock/InTr admission/materialization semantics, bounded lease, EVENT_EPHEMERAL Web Worker construction, execution-time runtime identity, and receipt/reconstruction behavior.

GitHub/CI validates source only and has runtime authority `NONE`.
