# SV002 + HIL Shared HB InTr Carrier Migration Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#808`
Branch: `feat/sv002-hil-hb-carrier-807`
State: RELEASED_COMPLETE
Updated: 2026-08-31T08:24:00-05:00
Credential authority: TV/TVC
Authority effect: NONE

## Goal

Migrate both remaining browser-originated Site Universal InTr materialization paths to the canonical shared HB-derived carrier client.

Targets:
- SV002 public observation fallback
- HIL direct upload prestage

## Required behavior

```text
generated materialization request
 -> shared StegVerseHBInTrCarrier.buildBinding(packet_id,payload_hash)
 -> insert carrier_binding
 -> recompute request_hash over the complete request body
 -> existing Node/receiver transport path
```

The browser must load `assets/hb-intr-carrier.js` before either client.

Carrier correctness remains non-authorizing and does not replace any existing Interlock/InTr admission, execution, custody, route, credential, transition, receiving, or publication gate.

## Claimed surfaces

- `assets/sv002-observe.js`
- `sv002-observe/index.html`
- `assets/hil-direct-upload-v1.js`
- `humans-as-interoperability-layer.html`
- `scripts/check_site_hb_intr_carrier_migration.py`
- `tests/test_site_hb_intr_carrier_migration.py`
- `docs/SV002_HIL_HB_INTR_CARRIER_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-sv002-hil-hb-carrier-808-20260831.json`

## Completion boundary

Exact deterministic carrier binding, request rehashing, correct script load order, validation, and merge.


## Release reconciliation — 2026-09-02

The canonical claim is already `RELEASED_COMPLETE`. Implementation PR #809 merged as `899ea0e70d3ca986c03b40469a7ca13622b79124`; terminalization PR #810 merged as `ca1ba513409c1f4ae236994a1ee965ed794062d4`.

This handoff no longer represents active ownership. Later canonical carrier-bound materialization migration supersedes its local request-mutation pattern.
