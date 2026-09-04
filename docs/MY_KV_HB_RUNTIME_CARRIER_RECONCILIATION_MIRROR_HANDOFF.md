# My KV HB Runtime Carrier Reconciliation Mirror Handoff

Repository: StegVerse-Labs/Site
Issue: #980
Branch: docs/my-kv-hb-runtime-carrier-980
Updated: 2026-09-04
State: SOURCE_RECONCILIATION_IMPLEMENTED_VALIDATION_PENDING
Authority effect: NONE
Activation effect: false
Credential authority: TV/TVC

## Purpose

Reconcile the My-KV Personal Form Profile lane with the already-established StegVerse runtime architecture.

Historical Site wording described the lane primarily as a consumer of the HB Runtime Presence / Resident Observability Contract. That projection remains useful for observation, but it is not the complete runtime architecture.

Canonical interpretation:

- the independent HB oscillator and deterministic HB-derived carrier functions are the shared runtime carrier substrate for modules;
- HB progression remains `OSCILLATOR_ONLY`;
- already-governed InTr packets and module work may be carried over deterministic HB-derived signals;
- Interlock/InTr retains transition/admission authority;
- TV/TVC retains credential authority;
- existing DEVICE_KV/module control retains execution eligibility;
- HB/oscillator grants no execution, admission, credential, routing, transition, claim/fence, receiving, publication, custody, or consequence authority.

No My-KV-specific heartbeat, oscillator, scheduler, retry clock, carrier, worker coordinator, credential path, or runtime authority is introduced.

## Site binding

Compatibility filename retained:

`data/my-kv-runtime-observability-binding.json`

Canonical schema inside that file is now:

`stegverse.site.hb-runtime-carrier-binding/v1`

The binding separates:

1. `shared_carrier` — canonical HB oscillator + deterministic HB-derived InTr carrier substrate;
2. `supplemental_observability` — the existing runtime-presence projection used for observation/reconstruction.

The old filename is retained to avoid unnecessary consumer/path churn. Filename compatibility does not define the architecture.

## Runtime consequence

The My-KV Personal Form Profile path is interpreted as:

```text
canonical HB oscillator
-> deterministic HB-derived carrier opportunity
-> already-governed DEVICE_KV / InTr transition
-> Personal Form Profile read/write execution
-> exact readback / receipt generation
-> deterministic HB-derived response carrier
-> Site UI / retained reconstruction evidence
```

HB is the common runtime carrier substrate for this lane; it is not merely an observability signal beside the runtime.

## Preserved runtime predicates

This source reconciliation does not alter or satisfy any runtime predicate. Existing evidence requirements remain:

- Personal Form Profile write consumed;
- `PROFILE_PERSISTED`;
- exact readback verified;
- subsequent `PROFILE_READ`;
- retained Node/DEVICE_KV receipt reconstruction;
- SKAP signing-profile custody separately observed;
- document-signature execution separately owner-approved and observed.

Existing current-iPhone UI observations remain exactly as previously recorded. Source/CI/merge cannot upgrade retained reconstruction or SKAP/signing predicates.

## Provider boundary

Provider writeback remains separate. The current Personal-KV provider materialization path is read-only unless a separately admitted TV/TVC provider mutation capability exists.

No Google credential/session authority is added here. The upstream Google Personal-KV source/runtime frontier remains owned by TVC and continuity-vault-kit.

## Authority invariants

```text
HB/oscillator runtime carrier: YES
HB progression dependency: OSCILLATOR_ONLY
HB execution authority: NO
HB admission authority: NO
HB credential authority: NO
HB transition authority: NO
HB routing authority: NO
HB claim/fence authority: NO
Interlock/InTr transition/admission authority: YES
TV/TVC credential authority: YES
existing DEVICE_KV runtime owner: unchanged
GitHub runtime authority: NONE
```

## Evidence boundary

This issue is source/semantic reconciliation only. It does not prove a new runtime execution, provider session, provider read/write, DEVICE_KV transition, HB-carried packet observation, SKAP custody event, document signature, public deployment, or recovery event.
