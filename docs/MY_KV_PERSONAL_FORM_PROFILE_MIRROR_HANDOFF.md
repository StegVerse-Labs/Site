# My KV Personal Form Profile Mirror Handoff

Repository: StegVerse-Labs/Site
Updated: 2026-09-04
State: SOURCE_IMPLEMENTED_RUNTIME_VALIDATION_REQUIRED
Authority effect: NONE
Activation effect: false

## Goal

Make repeated personal/business filing information enterable once from My KV on the current device and persist it to the user's Personal KnowledgeVault.

Canonical KV record:
`_Entities/Self/Personal_Form_Profile.json`

Canonical schema owner:
`StegVerse-Labs/continuity-vault-kit/schemas/personal-form-profile.schema.json`

## Implemented source

- My KV Step 3 now includes Reusable Form Information.
- TVC Unique ID and SSN/ITIN may be entered as private KV facts.
- default organizer, registered agent, effective-on-filing preference, and accounting-year close month are supported.
- a SKAP e-signature reference may be stored; reusable signature material itself is prohibited from ordinary KV.
- device-local DEVICE_KV admits `PERSONAL_FORM_PROFILE` read/write.
- writes are exact-path replacement candidates with exact-readback requirement.
- current-device sync routes `PERSONAL_FORM_PROFILE` to the resident device-local receiver.
- browser bridge fails closed when the resident receiver is unavailable.

## SKAP boundary

The profile may contain only:
`skap://signing/<profile-id>`

It may never contain reusable signature image/key material and may never set automatic signature application.

A signing profile reference is not signing authorization.

## Runtime completion

Requires current-iPhone observation of:
1. Personal Form Profile save;
2. exact readback receipt;
3. later profile load;
4. SKAP Vault signing profile setup through an authentic SKAP runtime, separately.

Source merge/availability is not runtime proof.

## Canonical HB runtime consolidation

This lane consumes the shared StegVerse-Labs HB Runtime Presence / Resident Observability Contract rather than an independent runtime-signal implementation.

Shared owner:
- `StegVerse-Labs/.github/docs/HB_RUNTIME_PRESENCE_RESIDENT_OBSERVABILITY_MIRROR_HANDOFF.md`
- `StegVerse-Labs/.github/management/HB_RUNTIME_PRESENCE_RESIDENT_OBSERVABILITY_CONTRACT.json`
- `StegVerse-Labs/.github/heartbeat_runtime/runtime_presence_projection.py`
- `StegVerse-Labs/.github/scripts/project_hb_runtime_presence.py`
- canonical merge: `6358375c81fedb579cb6fcac59946268ea485ebb`

Site binding:
- `data/my-kv-runtime-observability-binding.json`

No new heartbeat, scheduler, worker coordinator, carrier, or runtime authority was introduced.

## Post-consolidation integration

Implemented:
- connected owner KnowledgeVault contains exact `_Entities/Self/Personal_Form_Profile.json`;
- continuity-vault-kit bounded Google Drive materialization scope includes that path;
- canonical DEVICE_KV handles both `PERSONAL_CONTACT_PROFILE` and `PERSONAL_FORM_PROFILE`;
- Site read responses include persisted profile hash;
- My KV form bridge exposes detailed readback evidence;
- Save path requires `PROFILE_PERSISTED`, exact readback, immediate subsequent `PROFILE_READ` with the same profile hash, and non-personal Node evidence append.

Automatic provider writeback is not claimed. Current provider binding is `READ_ONLY_MATERIALIZATION`.

## Current-iPhone UI observations

Observed on the current iPhone:

```text
Reusable form information loaded from Personal KV.
```

and later:

```text
Reusable form information saved and verified in your Personal KV.
```

The current source emits the save success only after the write/read sequence completes in-browser. Therefore the UI/runtime observation remains legitimate evidence that the browser path reached its success state. It is not by itself retained reconstruction evidence.

## Exported Node evidence verification — 2026-09-04 15:56 CDT

The owner exported `stegos.node_physical_evidence_export.v1` from the same current iPhone and supplied it for verification.

Observed export facts:

```text
node_id = SV-NODE-7cc15c50428ba0c7db01d5fe
canonical_chain_receipt_count = 1
local_receipt_head.receipt_number = 1
last_personal_kv_sync = null
sections = Device Registration only
```

The export contains only the genesis `NODE_REGISTERED` receipt. It contains no `stegos.node_capability_receipt.v1` for `my-kv-personal-form-profile`, no write/read step receipts, and no `stegos.node_personal_kv_sync_observation.v1` marker.

Therefore:

```text
PERSONAL_FORM_PROFILE_WRITE_UI_SEQUENCE_OBSERVED = true
PERSONAL_FORM_PROFILE_READ_UI_OBSERVED = true
PERSONAL_FORM_PROFILE_RETAINED_NODE_RECEIPTS_PRESENT = false
PERSONAL_FORM_PROFILE_RETAINED_RECEIPT_RECONSTRUCTION_PROVEN = false
```

The export does not prove that the browser write/read sequence never occurred; it proves that the canonical Node export at 2026-09-04T20:55:37.660Z did not retain those receipts.

This supersedes any prior assumption that the successful UI sequence had already produced reconstructable Node evidence.

Exact remaining predicate is now evidence retention/re-execution on the current served Site source, not a new HB runtime implementation.

If a new save on the current deployed source succeeds, the subsequent Node export must contain at minimum:
- one `stegos.node_capability_receipt.v1` with capability `my-kv-personal-form-profile`, step `write`, state `PROFILE_PERSISTED`;
- one corresponding receipt with step `read`, state `PROFILE_READ`;
- matching profile hash references;
- non-null `last_personal_kv_sync`.

Until that export exists, reconstruction remains fail-closed.

SKAP signing-profile custody remains a separate TV/TVC-gated predicate and is not advanced by this export.
