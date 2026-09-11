# StegSocials ERL Assisted Drafting Mirror Handoff

Updated: 2026-09-11

## Goal Task ID

`SS-EVIDENCE-COMPARISON-001`

## COSV

`40000100100000`

## Purpose

Make the standard StegSocials preparation path useful without requiring the user to manually author the first draft. A selected ERL artifact can be read from the current device-local KV, verified byte-for-byte against its stored SHA-256/size metadata, deterministically summarized into a platform-shaped editable draft, and then passed into the existing standard preparation + Save draft to My KV path.

## Standard flow

```text
My KV -> ERL artifact -> Prepare post -> Draft from ERL
-> exact local ERL byte/hash verification
-> deterministic source/relevance extraction
-> editable platform-shaped draft
-> canonical stegverse.stegsocials.post-preparation/v1 bundle
-> optional Save draft to My KV
-> exact saved-draft byte readback
-> portable standard-flow evidence JSON export
-> manual copy/share/publication
```

## Merged implementation evidence

- Site PR #1148 merged at `7a7d66045074cb066d1e948b24afede183e1413b`, establishing exact saved-draft content-byte verification.
- Site PR #1152 merged the ERL-assisted drafting implementation at `38be9d952ef4cbf30b9fa15cdedee1f3b5dc1242`.
- Site PR #1167 merged the current-iPhone resident-DEVICE_KV source-identity / empty-ERL clarification at `bb3ccf4280f1843fb7e85e726d5c7dba0f9a4c11`. Its final head passed My KV Directory Landing, StegSocials Post Preparation, StegSocials ERL Assisted Drafting, Site Handoff Orchestrator, Site Bootstrap Validate, and Ecosystem Heartbeat Orchestration.
- Site PR #1170 merged the post-merge claim/handoff reconciliation at `4cba19048241244058d5e0e1921090219042a15f`; its required StegSocials/Handoff/Bootstrap/Heartbeat gates passed.
- Site PR #1226 merged the synchronous current-iPhone owner-file-picker repair at `a9c6dc3c18f0dbbf6d54f6cf68c772e582aa8fa3`. The final head passed My KV Directory Landing, StegSocials Post Preparation, StegSocials ERL Assisted Drafting, Site Bootstrap, Ecosystem Heartbeat, ERL provider-proof projection, and no-third-party-runtime checks.

The current StegSocials canonical coordination remains `SS-EVIDENCE-COMPARISON-001` / COSV `40000100100000`.

## Authentic current-iPhone observation already retained

The owner opened live Site `My KV -> ERL` and saw:

```text
Directory loaded from your KnowledgeVault.
No files available to display
This directory is currently empty.
```

That observation established a valid resident directory projection and exposed ambiguous wording. It did not establish a Google Drive or other cloud-KV read. PR #1167 repaired that ambiguity: the deployed source now identifies the current resident `DEVICE_KV` projection, uses a dedicated ERL empty state, and says separate cloud KV content is not included unless connected/materialized into the active set.

The current resident ERL directory was empty at the time of the observation. The existing owner-controlled `Import owner-controlled files` path remains the intended bounded recovery path from iPhone Files if an ERL artifact must be staged into the resident admission flow.

A later authentic current-iPhone retry (retained source screenshot `IMG_2616.png`, 667806 bytes, SHA-256 `f4fde2dd19a61aca887ff017e8bd61db80c5e791aa4098b71ce9326af06c6426`) showed the status changing to “Choose owner-controlled files from this device” while no native picker opened and the resident ERL projection stayed empty. Source inspection identified the cause: `pickFiles(request)` ran only after the asynchronous Node-status promise settled, outside iOS Safari's transient user-activation window. The repair invokes the chooser synchronously during the tap, then verifies Node registration before any `File.arrayBuffer()`, hashing, persistence, or admission queue operation. Selection alone remains non-authorizing and does not prove KV admission.

## Standard-flow evidence retention

Site PR #1207 merged the bounded evidence-export implementation at `161bb9450b7d499ad2474d2a296b2d8c3be27ce7` after all twelve triggered checks passed. The export control remains disabled until canonical KV admission and independent exact stored-byte readback agree on the preparation bundle, canonical path, SHA-256, and size. The resulting `stegverse.site.stegsocials-standard-flow-evidence/v1` JSON retains the browser user-agent/platform/language observation while explicitly setting `physical_device_identity_claimed=false`, `cloud_provider_readback_observed=false`, and all provider/credential authority fields false.

Source or CI validation proves the export contract, not an authentic current-iPhone execution. The downloaded JSON from that physical flow remains the required observation artifact.

## Current machine state

```text
ERL_ASSISTED_STANDARD_DRAFTING_MERGED=true
EMPTY_RESIDENT_ERL_STATE_CLARITY_REPAIR_MERGED=true
POSTMERGE_RECONCILIATION_MERGED=true
CURRENT_IPHONE_EMPTY_RESIDENT_ERL_DIRECTORY_OBSERVED=true
CURRENT_IPHONE_CORRECTED_PAGE_REOBSERVATION_COMPLETE=true
CURRENT_IPHONE_FILE_PICKER_USER_ACTIVATION_FAILURE_OBSERVED=true
IOS_SYNCHRONOUS_PICKER_REPAIR_SOURCE_IMPLEMENTED=true
IOS_SYNCHRONOUS_PICKER_REPAIR_MERGED=true
CLOUD_KV_INSPECTED_BY_THAT_DEVICE_READ=false
CURRENT_IPHONE_ERL_ADMISSION_PENDING=true
STANDARD_FLOW_EVIDENCE_EXPORT_SOURCE_IMPLEMENTED=true
STANDARD_FLOW_EVIDENCE_EXPORT_MERGED=true
CURRENT_IPHONE_PREPARE_SAVE_EXACT_READBACK_AND_EXPORT_PENDING=true
```

## Remaining work

1. Confirm the deployed Site serves the merged synchronous iOS picker repair.
2. On the current iPhone, reload `My KV -> ERL`, tap `Import owner-controlled files`, and verify that the native Files picker opens from the original tap.
3. Select the intended ERL artifact and allow staging -> canonical KV admission/readback to proceed. Picker opening and file selection do not establish admission; do not expect the artifact to appear until canonical admission/readback succeeds.
4. Once the ERL artifact is readable from the resident KV, execute `Prepare post -> Draft from ERL -> Save draft to My KV`; after exact readback succeeds, tap `Export standard-flow evidence` and retain the downloaded JSON.
5. Keep automated/scheduled social-provider publication in the separate premium task.

## Manual work

After deployment, the current iPhone must retry the same import tap and complete authentic admission/readback. No Google Drive KV #2 adoption retry is part of this task.

## State

`ERL_ASSISTED_STANDARD_DRAFTING_MERGED / STANDARD_FLOW_EVIDENCE_EXPORT_MERGED / IOS_SYNCHRONOUS_PICKER_REPAIR_MERGED / CURRENT_IPHONE_DEPLOYED_RETRY_PENDING / DEVICE_ERL_ADMISSION_DRAFT_READBACK_EXPORT_PENDING`
