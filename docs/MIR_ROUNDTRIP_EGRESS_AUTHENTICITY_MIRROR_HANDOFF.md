# MIR round-trip egress authenticity mirror handoff

Updated: 2026-09-17
Goal Task ID: `MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001`
Root collaboration Goal Task ID: `MIR-STEGVERSE-SEPARATION-OF-POWERS-EVIDENCE-CONTRACT-001`
Canonical custody Goal Task ID: `CANONICAL-MASTER-RECORDS-STATE-TRANSITION-CUSTODY-001`
COSV ID: `50000000100000`
Status: `ACTIVE / SV002 BROWSER-EVENT MECHANICS REIMPLEMENTED FOR MIR / SOURCE VALIDATION PENDING / AUTHENTIC CURRENT EVENT EXECUTION PENDING`

## Correct execution fixture

The successful StegVerse-002 mechanism is the fixture:

```text
browser event
-> registered StegVerse Node
-> non-authorizing Universal InTr materialization request
-> write-once Node intr_outbox
-> bounded EVENT_EPHEMERAL browser Web Worker
-> execution-time runtime identity
-> transition receipts
-> Master Records custody/reconstruction
```

No idle runtime, Remote Desktop host, resident shell, replacement scheduler, replacement dispatcher, second device, WorkerCoordinator event-creation gate, or Python execution substrate is required.

## MIR browser implementation

The MIR implementation now uses that browser-event architecture directly:

- `data/mir-roundtrip-browser-runtime-binding.v1.json` — MIR Goal/COSV/destination binding and hard SV002 initiation invariants.
- `assets/canonical-master-records-transition-custody-browser.js` — reusable browser-portable canonical Master Records transition custody/reconstruction using the ecosystem canonical receipt schema; custody grants no transition/execution authority.
- `assets/mir-roundtrip-sv002-browser-runtime.js` — Blob-backed `EVENT_EPHEMERAL` MIR Web Worker materializer on the registered Node event path.
- `assets/mir-roundtrip-browser-activation.js` — standing browser event activation; queues the non-authorizing materialization request, invokes the event runtime, retains exact MIR return bytes, and attempts the existing governed-return consumer.
- `mir-roundtrip/index.html` — deterministic browser event surface; autostarts on page activation and permits bounded re-observation of the unchanged event.
- `tests/test_mir_sv002_browser_event_reimplementation.py` — hard regression assertions for `NO_IDLE_RUNTIME_REQUIRED`, `NO_REMOTE_HOST_DISCOVERY`, `EVENT_IS_THE_TRIGGER`, `NO_EVENT_CLAIM_OR_FENCE`, `EVENT_EPHEMERAL`, canonical custody, and no Python-driver dependency in the browser page.
- `.github/workflows/mir-sv002-browser-event-conformance.yml` — source-only validation; GitHub runtime authority remains `NONE`.

The prior `.github/scripts/execute_mir_event_driven_roundtrip.py` is not the primary MIR runtime. It may remain conformance scaffolding only.

## Canonical transition custody

The browser runtime submits every observed transition through canonical Master Records custody before progressing:

```text
MIR_EVENT_MATERIALIZATION_REQUEST_QUEUED
CURRENT_INTERLOCK_INTR_INGRESS_RECEIVED
RTC-STEGVERSE-EGRESS-007
RTC-INTERLOCK-INTR-TRANSPORT-008
RTC-FARSIDE-FINAL-009
MIR_DESTINATION_EVIDENCE_RETAINED
EXACT_GOVERNED_RETURN_PACKET_RETAINED
```

The activation surface then uses the existing `StegVerseExternalCounterpartReturnConsumer.consumeRetainedPacket(...)` path. If governed return succeeds it canonically records `STEGVERSE_RETURN_EXIT` and `MIR_GOVERNED_ROUND_TRIP_COMPLETE`; if it fails, the observed fail-closed return state is itself canonically recorded as `MIR_GOVERNED_RETURN_FAIL_CLOSED`.

No missing transition is fabricated and Master Records never grants transition authority.

## Current evidence boundary

The browser-event source implementation is now materialized. Authentic execution of the current MIR event has not yet been observed, so RTC-007/008/009, `STEGVERSE_RETURN_EXIT`, and full communication completion remain unpromoted until the actual browser event produces those receipts.

The correct next evidence source is the MIR browser event itself at `/mir-roundtrip/`, not a directly reachable machine host.
