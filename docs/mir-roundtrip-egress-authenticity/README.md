# MIR Round-Trip Egress Authenticity

Canonical Goal Task: `MIR-ROUNDTRIP-EGRESS-AUTHENTICITY-001`
Canonical handoff: `docs/MIR_ROUNDTRIP_EGRESS_AUTHENTICITY_MIRROR_HANDOFF.md`
COSV: `50000000100000`

## Canonical execution order

MIR now reuses the successful StegVerse-002 browser-event mechanics instead of requiring a WorkerCoordinator event-creation claim or an externally reachable machine runtime:

```text
browser event
-> registered StegVerse Node
-> non-authorizing Universal InTr materialization request
-> write-once Node intr_outbox
-> EVENT_EPHEMERAL browser Web Worker
-> MIR RTC-007 / RTC-008 / RTC-009
-> canonical Master Records custody after every observed transition
-> exact governed-return packet retention
-> existing governed STEGVERSE_RETURN_EXIT path
```

Hard invariants:

- event is the trigger;
- idle runtime is not required;
- remote-host discovery is prohibited;
- WorkerCoordinator claim/fence is not required to create the event;
- the materialization request grants no execution authority and mints no claim/fence;
- GitHub/CI has runtime authority `NONE`;
- missing transitions are never fabricated.

## Source surfaces

- `data/mir-roundtrip-egress-sv002-route-binding.v1.json` — proven route reuse contract.
- `data/mir-roundtrip-browser-runtime-binding.v1.json` — MIR-specific browser bindings.
- `assets/canonical-master-records-transition-custody-browser.js` — canonical browser-portable Master Records custody/reconstruction.
- `assets/mir-roundtrip-sv002-browser-runtime.js` — bounded Blob-backed MIR `EVENT_EPHEMERAL` runtime.
- `assets/mir-roundtrip-browser-activation.js` — event creation/outbox/runtime/return activation.
- `mir-roundtrip/index.html` — autostart browser event surface.
- `tests/test_mir_sv002_browser_event_reimplementation.py` — source conformance.

The older MIR transition probe is comparator-only and is not the primary custody or execution mechanism. The Python event driver is also not the final SV002 execution substrate.

## Canonical custody sequence

Each actually observed state is retained/reconstructed before progression:

`MIR_EVENT_MATERIALIZATION_REQUEST_QUEUED` → `CURRENT_INTERLOCK_INTR_INGRESS_RECEIVED` → `RTC-STEGVERSE-EGRESS-007` → `RTC-INTERLOCK-INTR-TRANSPORT-008` → `RTC-FARSIDE-FINAL-009` → `MIR_DESTINATION_EVIDENCE_RETAINED` → `EXACT_GOVERNED_RETURN_PACKET_RETAINED`.

The existing external-counterpart return consumer is then used for governed return. Success records `STEGVERSE_RETURN_EXIT` and `MIR_GOVERNED_ROUND_TRIP_COMPLETE`; a real failure records `MIR_GOVERNED_RETURN_FAIL_CLOSED` without erasing earlier successful state.

## Evidence boundary

Source implementation is present. Authentic current browser execution remains required before any RTC or full-round-trip predicate is promoted. The absence of a directly connected machine host is not a blocker or a runtime predicate.
