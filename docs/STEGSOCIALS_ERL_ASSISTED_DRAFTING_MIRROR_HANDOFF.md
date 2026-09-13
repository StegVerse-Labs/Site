# StegSocials ERL Assisted Drafting Mirror Handoff

Updated: 2026-09-12

## Goal Task ID

`SS-EVIDENCE-COMPARISON-001`

## COSV

`40000100100000`

## Authority invariant — NO DEVICE VERIFICATION

There is no device verification, device attestation, physical-device identity gate, or device-bound user authority requirement in this flow.

Devices are interchangeable StegOS transport nodes. User verification and user authority are maintained through KV/SKAP. Interlock/InTr governs transitions. Client/platform/user-agent/hardware metadata is non-authoritative transport observation only and must never become an admission, identity, evidence-validity, or authority predicate.

Historical iPhone observations remain historical transport observations only. They do not create an iPhone requirement and do not establish device identity or authority.

## Purpose

Make the standard StegSocials preparation path useful without requiring the user to manually author the first draft. A selected ERL artifact can be read through canonical KV, verified byte-for-byte against its stored SHA-256/size metadata, deterministically summarized into a platform-shaped editable draft, and passed into the existing preparation + Save draft to My KV path.

## Standard flow

```text
My KV -> ERL artifact -> Prepare post -> Draft from ERL
-> exact ERL byte/hash verification
-> deterministic source/relevance extraction
-> editable platform-shaped draft
-> canonical stegverse.stegsocials.post-preparation/v1 bundle
-> optional Save draft to My KV
-> canonical KV admission
-> exact saved-draft byte readback
-> portable standard-flow evidence JSON export
-> manual copy/share/publication
```

## Merged implementation evidence

- Site PR #1148 merged exact saved-draft content-byte verification at `7a7d66045074cb066d1e948b24afede183e1413b`.
- Site PR #1152 merged ERL-assisted drafting at `38be9d952ef4cbf30b9fa15cdedee1f3b5dc1242`.
- Site PR #1167 repaired resident-KV source wording at `bb3ccf4280f1843fb7e85e726d5c7dba0f9a4c11`.
- Site PR #1207 merged portable standard-flow evidence export at `161bb9450b7d499ad2474d2a296b2d8c3be27ce7`.
- Site PR #1208 reconciled the export release at `0cf699f3717b09832c423f76ff5c22c270566d25`.
- Site PR #1226 repaired synchronous iOS file-picker activation ordering at `a9c6dc3c18f0dbbf6d54f6cf68c772e582aa8fa3`.
- Site PR #1228 reconciled that repair at `c46217e013604549a5e91c923348e162d3891bb4`.
- Site PR #1229 retained live served-source observation at `f222a18ab2797699c59d260a4383dbe3cea13418`.
- Site PR #1231 corrected duplicate screenshot evidence classification at `24850d97bee599a151f18c21ac64add59c963765`.
- Site PR #1284 merged the no-device-verification standard-flow evidence correction at `1ca01b07dd3531060fd50c73bad68f0668771ace`. Exact PR head `b21f7a7b4bf861b9a46ac06342e825563cbffd44` passed the standard-flow exact-content readback validation and associated Site validation lanes before merge.

The iOS-specific work above repaired a browser interaction defect only. It is not an identity/authority mechanism and must not be generalized into a device-verification requirement.

## Corrected standard-flow evidence export

The merged Site source emits `stegverse.site.stegsocials-standard-flow-evidence/v1` without device-verification semantics.

The export requires only:

```text
preparation task/bundle/path binding
canonical KV admission state
admitted hash readback
exact content readback
path / SHA-256 / size agreement
no cloud-provider inference
no provider-call / credential / provider-operation authority
```

The export does not require or emit device/client metadata as an evidence-validity or authority predicate. Instead it states the governing architecture directly:

```text
identity_authority_source=KV_SKAP_ONLY
transport_node_role=NON_AUTHORITATIVE_INTERCHANGEABLE
```

Arbitrary transport metadata may exist elsewhere for diagnostics, but it is ignored for identity, authority, admission, and evidence validity.

## Historical transport observations

Earlier owner-supplied screenshots established that a resident KV projection and file-picker UI were reachable from the user's then-current iPhone and helped identify an iOS transient-user-activation ordering defect. Those observations remain useful historical debugging evidence.

They do **not** establish a required device, a verified device, a device-bound user, or a device-bound authority source.

## Reusable Task Component Model

The standard/manual lane does not add a second KV runtime, second Interlock/InTr implementation, or bespoke task-specific resident dispatcher. It reuses the canonical Goal transport composition for `SS-EVIDENCE-COMPARISON-001`:

```text
RTC-ROUNDTRIP-003
RTC-INTERLOCK-INTR-TRANSPORT-008
RTC-EVIDENCE-CUSTODY-004
```

The adjacent child `SS-EVIDENCE-STANDARD-KV-FLOW-001` remains an execution projection of this same Goal Task. It is not a replacement Goal Task and remains `INACTIVE / UNCLAIMED` until authentic execution is actually admitted through the existing runtime owners.

## Remaining work

Source correction is complete. Remaining work is authentic runtime evidence only:

1. An eligible StegOS transport/execution node is authentically admitted through the existing Interlock/InTr path for the bounded standard KV transition.
2. Execute `Prepare post -> Draft from ERL -> Save draft to My KV` through the existing standard flow.
3. Observe canonical KV admission and exact saved-draft byte readback matching path, SHA-256, and size.
4. Export `stegverse.site.stegsocials-standard-flow-evidence/v1` from that authentic execution.
5. Validate the resulting artifact with the merged StegSocials standard-flow verifier.
6. Retain the verified observation through the existing evidence/custody path without inferring device identity, provider execution, premium publication authority, or unrelated runtime claims.

No persistent runtime, second user-operated device, device verification, or device attestation is a prerequisite. Automated/scheduled social-provider publication remains in the separate premium task.

## Manual work

None until an eligible StegOS transport/execution node is exposed and authentically admitted through the authorized runtime path. When available, use that single admitted node to import/select the intended ERL artifact and complete canonical KV save/readback/export. No device verification, device identity, or device attestation step is required.

## State

`ERL_ASSISTED_STANDARD_DRAFTING_MERGED / STANDARD_FLOW_EVIDENCE_EXPORT_MERGED / SITE_PR1284_NO_DEVICE_VERIFICATION_CORRECTION_MERGED / KV_SKAP_ONLY_USER_VERIFICATION_AUTHORITY / TRANSPORT_NODES_INTERCHANGEABLE / REUSABLE_COMPONENT_COMPOSITION_PRESERVED / CHILD_STANDARD_KV_FLOW_INACTIVE_UNCLAIMED / AUTHENTIC_ADMITTED_STEGOS_NODE_NOT_OBSERVED / AUTHENTIC_KV_ADMISSION_DRAFT_READBACK_EXPORT_PENDING / PREMIUM_PROVIDER_PUBLICATION_SEPARATE`
