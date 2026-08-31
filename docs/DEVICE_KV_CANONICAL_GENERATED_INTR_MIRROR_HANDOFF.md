# DEVICE_KV Canonical Generated InTr Migration Mirror Handoff

Repository: `StegVerse-Labs/Site`
Issue: `#835`
Branch: `feat/device-kv-canonical-generated-intr-833-v2`
State: ACTIVE_IMPLEMENTATION
Updated: 2026-08-31T11:34:00-05:00
Credential authority: TV/TVC
Authority effect: NONE

## Goal

Remove the remaining private Universal InTr intent/materialization constructor from the My KV portable direct-source bridge and consume the exact merged StegOS generated connector.

## Upstream

- StegVerse-Labs/StegOS #143 / PR #144
- merge: `a07b83f7676eaabcc0111fb9dc00e3163bc5e339`
- browser artifact: `sha256:6205bbdf7aacb5020313ac874c5d2ac999843070cd4a12263e428e3b3074042b`
- registry: `sha256:83cc33beede49accb364d1f3c32a02f975bbf555fabf4136704dab70d611e97f`
- device-kv profile: `sha256:4cb18a97611a1dc9ab4bb85d3e86da025074aded539113969cfdcf9ef4c3afef`

## Canonical path

```text
portable inline payload
 -> StegVerseGeneratedInTr.buildIntent("device-kv", exact canonical bytes, "REQUEST", operation_id)
 -> StegVerseHBInTrCarrier.buildBinding(packet_id, payload_hash)
 -> StegVerseGeneratedInTr.buildMaterializationRequest(
      "device-kv",
      intent,
      "inline://materialization_request.portable_payload",
      carrier_binding,
      {portable_payload: inlinePayload}
    )
 -> StegVerse Node outbox
 -> DEVICE_KV sync
```

## Invariants

- only `portable_payload` is profile-allowed;
- carrier binding is non-authorizing;
- generated request owns `request_hash`;
- no consumer-local materialization ID/body/hash construction;
- no provider credential or provider-operation authority;
- existing IndexedDB exact-file staging and readback remain intact.

## Claimed surfaces

- `assets/my-kv-portable-direct-source-bridge.js`
- `assets/generated/site-browser-intr-connectors.js`
- `assets/generated/site-browser-intr-connectors.manifest.json`
- `tests/canonical-generated-intr.test.cjs`
- `tests/test_device_kv_intr_sync.py`
- `scripts/check_generated_intr_connector.py`
- `docs/DEVICE_KV_CANONICAL_GENERATED_INTR_MIRROR_HANDOFF.md`
- `data/session-work-claims.d/site-device-kv-canonical-generated-intr-833-20260831.json`

## Completion boundary

Exact artifact copy, DEVICE_KV bridge migration, validation, merge, claim terminalization, then continue into resident continuity-vault-kit admission/persistence/readback.
