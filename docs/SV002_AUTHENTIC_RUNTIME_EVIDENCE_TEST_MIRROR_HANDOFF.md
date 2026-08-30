# SV002 Authentic Runtime Evidence Test Mirror Handoff

Updated: 2026-08-30
Repository: `StegVerse-Labs/Site`
Issue: #727
State: IMPLEMENTED_ON_BRANCH / VALIDATION_PENDING

## Purpose

Provide the external-observer-native test mechanism for authentic StegVerse-002 public-observation runtime evidence.

This test is intentionally **not** another device-node validation suite. It consumes the already-established StegVerse Node continuity proof from `StegVerseNodeContinuity.status()`, which revalidates Receipt #1 before reporting `REGISTERED`.

If the existing Node proof is unavailable, the harness stops with `VALID_NODE_REQUIRED`. It does not call `registerDevice()` and does not mint a substitute Node identity.

## Authentic observation sequence

```text
existing valid Node Receipt #1
-> public external browser at https://stegverse.org
-> credentialless HTTPS GET /intr/profile
-> exact profile validation + SHA-256
-> require SV002:PublicObservation support
-> derive in-memory /intr/materialization target
-> build exact production READ_OBSERVATION request
-> queue exact production Universal InTr materialization request in Node outbox
-> build production Node materialization trigger
-> POST trigger to public /intr/materialization
-> validate stegverse.sv002-intr-materialization-ingress/v1 receipt
-> poll /intr/sv002-observe/readiness until READY
-> submit the exact same READ_OBSERVATION request
-> require InTr ingress transition RECEIVED
-> require InTr egress transition FORWARDED
-> require egress.prior_receipt_hash == ingress.receipt_hash
-> emit copy/paste/exportable evidence bundle
```

## Evidence classification

A successful harness run emits `stegverse.sv002.authentic-runtime-evidence/v1` with:

- Run ID and timestamps;
- consumed existing Node Receipt #1 proof reference;
- exact public `/intr/profile` response and canonical SHA-256;
- in-memory conforming target derived from that observation;
- exact observation request and request SHA-256;
- Universal InTr materialization request / Node outbox binding;
- public materialization ingress receipt;
- receiver-readiness observation;
- final observation ingress and egress receipts;
- exact receipt-chain linkage;
- optional device/network condition label for later matrix comparison.

The optional condition label is metadata only. It is not treated as proof of Wi-Fi, cellular, or VPN state. Existing device-node validation remains the authority for Node validity; this test measures runtime transport from that valid Node.

## Authenticity boundary

A run may claim `AUTHENTIC_RUNTIME_ROUND_TRIP_OBSERVED` only when the browser itself is executing from `https://stegverse.org` and obtains the live HTTPS profile and runtime receipts from the public production lanes.

Source tests and GitHub Actions may validate the harness implementation, but must not generate or be accepted as authentic runtime evidence.

## Explicit nonclaims

A successful runtime transport test does not establish:

- principal StegVerse-002 self-characterization execution;
- Master Records custody or reconstruction;
- consciousness, self-awareness, or curiosity;
- G18 completion;
- credential or execution authority;
- a direct observer -> StegVerse-002 relationship.

`authority_effect` remains `NONE`.

## Files

- `sv002-observe/runtime-evidence-test.html`
- `assets/sv002-runtime-evidence-test.js`
- `tests/test_sv002_authentic_runtime_evidence_harness.py`
- `docs/SV002_AUTHENTIC_RUNTIME_EVIDENCE_TEST_MIRROR_HANDOFF.md`

## Next evidence gate after merge

Open the deployed test page from an already-valid StegVerse Node on a network context that can reach `https://stegverse.org`, run the test once without a condition label, and preserve the resulting evidence bundle. Only after a baseline authentic round trip exists should Wi-Fi/cellular/VPN conditions be layered over the same runtime test for resilience comparison.
