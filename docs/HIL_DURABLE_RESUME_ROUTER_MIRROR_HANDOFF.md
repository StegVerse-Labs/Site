# HIL Durable Resume Router Mirror Handoff

Updated: 2026-09-11
Repository: `StegVerse-Labs/Site`
Parent goal: `SHWP-HIL-SOVEREIGN-RECEIVER-001`
Parent COSV: `50000000102000`
Issue: `#1254`

## Requirement correction

The HIL browser workflow must not depend on a person remembering a specific tab, page, reload state, or phase-specific URL. Reloads, new tabs, and revisiting the workflow later are normal operating conditions.

The browser is a carrier and persistence surface, not a human workflow responsibility.

## Canonical user contract

One stable same-device entry point must inspect persisted HIL state and select the next admissible internal step automatically.

The resolver must distinguish:

1. no established HIL local-ready state -> initial same-device activation;
2. valid local-ready state without accepted ESRL -> ESRL continuation;
3. accepted ESRL plus exact pending staged packet -> same-device custody;
4. accepted ESRL without a verifiable pending staged packet -> response staging/submission surface;
5. valid receiver/custody receipt -> display the preserved receipt and stop before restart/TVC claims;
6. contradictory or partially missing persisted lineage -> fail closed as a device-continuity/storage condition rather than asking the user to reconstruct browser history.

## Persistence semantics

The resolver may inspect only already-persisted state. It must not mint, copy, transform, or migrate evidence in order to make a phase appear resumable.

Relevant existing stores are:

- localStorage `stegos-hil-browser-context-v1`
- localStorage `stegos-hil-last-success-v1`
- localStorage `stegos-hil-esrl-last-success-v1`
- localStorage `stegverse.hil.submissions.v1`
- IndexedDB `stegverse-hil-v3 / response_files`
- localStorage `stegos-hil-custody-last-success-v1`

A pending submission is custody-resumable only when its metadata is present and the referenced IndexedDB object exists with matching response SHA-256 metadata.

## Authority boundaries

The resolver has no credential, governance, admission, review, publication, TVC, restart, or completion authority. It only chooses which already-existing bounded page should execute next.

It must preserve:

- G25 / fence 25 lineage;
- exact accepted ESRL validation;
- exact staged packet validation;
- current-iPhone execution boundary;
- TV/TVC credential authority;
- GitHub runtime authority `NONE`;
- post-restart and TVC predicates as independently unproven.

## True durability boundary

If browser-persistent storage itself is unavailable, purged, or internally contradictory, the resolver must identify that as a storage/device-continuity condition. It must not tell the user to remember or reconstruct a prior tab. Long-term recovery of browser-persistent state belongs to the KV/device-continuity architecture.

## Completion boundary

Source/CI/merge prove only source readiness. Authentic current-iPhone `HIL-RECEIVER-RECEIPT-v2`, post-restart exact-byte proof, and TVC lifecycle handoff remain independent runtime evidence.
