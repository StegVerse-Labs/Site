# SV002 HB Carrier Target + Receipt Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#811`
Branch: `feat/sv002-hb-carrier-target-receipt-811`
State: ACTIVE_IMPLEMENTATION
Updated: 2026-08-31T08:30:00-05:00
Credential authority: TV/TVC
Authority effect: NONE

## Goal

Finish SV002's HB-derived carrier migration by enforcing the carrier contract both at runtime-target projection and ingress-receipt verification.

## Required behavior

- target projector accepts only a live universal InTr profile that advertises the canonical HB carrier profile;
- projected target records HB carrier support explicitly;
- SV002 sync compares ingress carrier evidence against the exact queued materialization request binding;
- carrier evidence remains non-authorizing;
- existing SV002 runtime/readiness/reconstruction semantics remain unchanged.

## Claimed surfaces

- `scripts/project_sv002_intr_sync_target.py`
- `tests/test_sv002_intr_sync_target_projector.py`
- `stegos-node/sv002-intr-sync.js`
- `tests/test_sv002_event_ephemeral_observation.py`
- `docs/SV002_HB_CARRIER_TARGET_RECEIPT_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-sv002-hb-carrier-target-receipt-811-20260831.json`

## Completion boundary

Exact profile enforcement + exact receipt binding validation + exact-head Site validation + merge.
