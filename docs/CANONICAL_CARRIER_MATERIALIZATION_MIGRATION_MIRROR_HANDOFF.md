# Canonical Carrier-Bound Materialization Migration Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: #821
Branch: `feat/canonical-carrier-materialization-821-v2`
State: RELEASED_COMPLETE
Updated: 2026-08-31T09:55:00-05:00
Credential authority: TV/TVC
Authority effect: NONE

## Goal

Consume the merged StegOS #138 carrier-aware generated Universal InTr connector in Site and retire consumer-local materialization mutation/rehashing where the canonical generator can own the complete request.

## Upstream

- StegVerse-Labs/StegOS PR #139
- merge: 13c9305e848bf10a6198e2f29b71eb4b63d25ebd
- browser artifact digest: sha256:cf66df87931c2fcd93c8ad2a23c8915eab410648995d2deae8de51e9ece4e243

## First consumers

- HIL direct upload
- SV002 public observation

DEVICE_KV remains separately bounded until its inline portable payload extension is represented canonically by the generator rather than reintroduced as post-generation mutation.

## Required behavior

1. copy the exact merged generated browser artifact + manifest;
2. derive the HB carrier binding through `StegVerseHBInTrCarrier`;
3. pass that binding directly to `StegVerseGeneratedInTr.buildMaterializationRequest(..., carrierBinding)`;
4. remove consumer-local insertion of `carrier_binding`;
5. remove consumer-local deletion/recomputation of `request_hash`;
6. verify generated artifact identity and carrier-aware request hashing in Site tests.

## Claimed surfaces

- `assets/generated/site-browser-intr-connectors.js`
- `assets/generated/site-browser-intr-connectors.manifest.json`
- `assets/hil-direct-upload-v1.js`
- `assets/sv002-observe.js`
- `tests/canonical-generated-intr.test.cjs`
- `scripts/check_generated_intr_connector.py`
- `docs/CANONICAL_CARRIER_MATERIALIZATION_MIGRATION_MIRROR_HANDOFF.md`

## Completion boundary

Exact artifact copy, two consumer migrations, Site validation, merge, then continue with DEVICE_KV inline-payload canonicalization.


## Release reconciliation — 2026-09-02

The canonical claim is already `RELEASED_COMPLETE`. Current-main replacement PR #826 merged as `a0efa5ef7abb5d4814c017b84703b14b82010edc`.

HIL and SV002 now use the canonical generated carrier-bound materialization builder. This handoff no longer owns the shared generated connector or HIL/SV002 client paths.
