# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns HIL continuation in `StegVerse-Labs/Site` and is subordinate to `docs/SITE_MIRROR_HANDOFF.md`.

Read in order with:

1. `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`
2. `docs/SITE_MIRROR_HANDOFF.md`
3. `docs/HIL_SITE_MIRROR_HANDOFF.md`
4. `docs/HIL_EXECUTION_SESSION_PROMPT.md`
5. `docs/HIL_MIRROR_HANDOFF.md`
6. `docs/HIL_PILOT_VALIDATION_MIRROR_HANDOFF.md`
7. `docs/HIL_ANNOUNCEMENT_DERIVATION_MIRROR_HANDOFF.md`
8. `docs/HIL_END_TO_END_PROTOCOL.md`
9. `docs/HIL_V1_UPLOAD_MIRROR_HANDOFF.md`
10. `docs/HIL_START_ANNOUNCEMENT.md`
11. all HIL machine-state and failure-evidence records.

## Primary objective

Start the HIL experiment and complete the first full governed participant lifecycle as soon as possible.

Success requires a real participant to complete the end-to-end workflow with preserved exact bytes, valid receipts, durable custody, reconstruction, governed review, separately authenticated publication, Site projection, HIL Master Record release, and downstream verification.

## Readiness classes

The repository operates two explicitly separate readiness classes:

1. `ANNOUNCEMENT_READY_WITH_MANAGED_RETURN`: exact v1.1 paper and prompt, unchanged response PDF, verified package, optional local receipt, and a managed receiving acknowledgment that claims no governed custody.
2. Production receiver activation: live route and D1 binding, exact-byte custody, controlled-cycle PASS, machine-published readiness, hosted restart persistence, genuine participant receipt, private review, separately authenticated publication, Site projection, Master Record release, and downstream verification.

Managed-return readiness is not production activation.

## Canonical contract

```text
Repository: StegVerse-Labs/Site
Participant launch: https://stegverse.org/hil-study-launch.html
Managed return: https://stegverse.org/hil-managed-return.html
Production participant surface: https://stegverse.org/hil/upload/
Receiver route: stegverse.org/api/hil/*
Worker: src/worker.js
Binding: HIL_REGISTRY
Backend: portable-sqlite-chunks-v1
Primary: v1.1 / a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Prompt: HIL-PROMPT-v1.1 / cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
Test case: HIL-E2E-001
Synthetic boundaries: research_data=false; authority_effect=false
```

## Current pilot state

`data/hil-pilot-ledger.json` remains fail-closed:

```text
Claude Opus 5: MODEL_REQUEST_INITIATED_RESPONSE_NOT_RECEIVED
ChatGPT Medium 5.6: MODEL_REQUEST_INITIATED_RESPONSE_NOT_RECEIVED
model requests initiated: 2
completed response PDFs: 0
verified return packages: 0
managed receiving acknowledgments: 0
governed receiver receipts: 0
```

No response completion, receipt, governed custody, registry commitment, private review, publication, endorsement, or Master Record release is established.

The pilot toolchain now includes:

```text
data/schemas/hil-pilot-ledger.schema.json
scripts/validate_hil_pilot_ledger.py
data/schemas/hil-managed-receiving-acknowledgment.schema.json
scripts/ingest_hil_pilot_return.py
data/schemas/hil-pilot-comparison.schema.json
scripts/generate_hil_pilot_comparison.py
scripts/test_hil_pilot_validation.py
```

The deterministic pilot suite contains 16 positive and negative cases and is bound into canonical Site validation.

## Managed acknowledgment boundary

```text
custody_status: MANAGED_RETURN_PRESERVED_NO_GOVERNED_CUSTODY
registry_status: NOT_REGISTERED
review_status: NOT_REVIEWED
publication_status: NOT_PUBLISHED
authority_effect: false
```

The acknowledgment proves only receipt and verification of a participant-managed artifact. It does not establish server custody, registry commitment, reconstruction, review acceptance, publication, endorsement, or authority.

## Machine-derived announcement status

The manually maintained announcement posture has been replaced by deterministic fail-closed derivation.

Verified implementation commits:

```text
035949885f185f45756c8b0b5a8947e5231d7171  derivation generator
3f8077e0bc989334280d194a738455ae73094767  deterministic tests
9ae0802f89f29d55853e5235a103cde961673246  strict status schema
fcf87a376a8628572411286507e7a8dd706365e3  machine-derived status v2
bb36d1f7b761bff694729f2674caeeb5ff9e30da  announcement workflow binding
02b1108aa6e5a12af7cd2e9d120b0ac4ba03b20a  canonical Site validation binding
```

Current derived status:

```text
schema_version: HIL-ANNOUNCEMENT-STATUS-v2
announcement_state: ANNOUNCEMENT_READY_WITH_MANAGED_RETURN
participant_intake_state: OPEN_MANAGED_RETURN
announcement_permitted: true
participant_warning_required: true
production_receiver.ready: false
authority_effect: false
```

The derivation verifies canonical PDF signature, byte size, SHA-256, prompt identity, ledger identity and authority boundaries, required managed-return components, deployment state, controlled-cycle state, participant readiness, and optional restart-persistence evidence.

It supports only:

```text
ANNOUNCEMENT_NOT_READY
ANNOUNCEMENT_READY_WITH_MANAGED_RETURN
ANNOUNCEMENT_READY_WITH_PRODUCTION_RECEIVER
```

Production promotion requires deployment readiness, controlled-cycle PASS, participant readiness PASS, upload authorization, and restart-persistence PASS. No static artifact or configuration can promote the state.

## Orchestration state

`SITE-0001-HIL-ANNOUNCEMENT-DERIVATION` is recorded as a completed parallel-safe task in both Site orchestration and the transition-driven heartbeat.

Continuity commits:

```text
0dfd93e3cf46cf5d6915283a124c727349752e4a  Site orchestration completion record
a549cd7665578782bb28b6b043f062f6e00f5fc1  heartbeat advancement
74d8c47b65a1c71a076be50cba6a5c3d3af4101f  dedicated derivation mirror handoff
1828b3ad8c835361a523ecbfdf6550a001c2a5e6  pilot handoff reconciliation
```

The active upload task remains separate:

```text
Task: SITE-0001-UPLOAD
Owner: external-active-session
Claimed paths:
- humans-as-interoperability-layer.html
- assets/hil-*
- scripts/check_hil_*upload*
State: RUNNING
```

This completed tranche did not modify those paths. The current work sequence remains running and the exclusive production slice is still queued behind the canonical idle barrier.

## Exact production failure evidence

The known controlled-cycle run, job, complete logs, and artifact were retrieved directly and preserved in `data/hil-controlled-cycle-failure-evidence-30569491378.json` at commit `aa93ec509eaf8dd5c14f4f5ada72cda542e9cc07`.

```text
Workflow: hil-controlled-cycle.yml
Run ID: 30569491378
Run head: 04116dd23e6797406b603a06d30f24666e8778a3
Run conclusion: failure
Job ID: 90962296249
Job: participant-readiness-gate
First failed step: Capture and validate live runtime readiness
Endpoint: https://stegverse.org/api/hil/readiness
HTTP status: 404
curl exit: 22
Provider message: The requested URL returned error: 404
```

Failure artifact:

```text
Artifact ID: 8770179722
Name: hil-participant-readiness-30569491378-1
Size: 1155 bytes
Digest: sha256:b202bf1fb6341a6d5fde36c72a347b544284981a1b42c1f8b8e4bc1f3c2d0edd
Created: 2026-07-30T18:13:57Z
Expires: 2026-10-28T18:13:52Z
Expired: false
```

All packet generation, submission, retrieval, custody verification, negative-case verification, and participant-readiness enforcement steps were skipped after readiness failed.

## Current verified production state

```text
Deployment trigger commit: d5d1598a8c523e8665e4550ee5c272df09256379
Deployment state: deployed=false
Deployment readiness: ready=false
Deployment failure marker: deployment_step_failed_before_live_probe
Controlled-cycle result: failure
Participant readiness: NOT_YET_VERIFIED
participant_ready: false
upload_button_authorized: false
production submission: absent
production receiver receipt: absent
exact-byte custody: unproven
negative cases: not executed after readiness failure
hosted restart persistence: unproven
release/tag authority: false
```

The logs prove only that the production domain did not serve `/api/hil/readiness` during the controlled cycle. They do not prove the cause of the deployment failure, the existence or absence of `HIL_REGISTRY`, the configured Worker route, or the exact Cloudflare permission/resource defect.

## Exact external-authority block

The current GitHub connector can inspect jobs, steps, complete logs, artifacts, and rerun controls only for already-known identifiers. It cannot enumerate or dispatch the push-triggered `HIL Cloudflare Receiver Deploy` workflow. No direct Cloudflare Worker, route, deployment, D1, binding, custom-domain, or runtime-log controls are exposed.

The blocked operation is retrieval of the deployment run associated with trigger commit `d5d1598a8c523e8665e4550ee5c272df09256379`, including its run ID, deployment job, failed step, and full provider logs; alternatively, direct inspection of the serving Cloudflare Worker/D1 control plane.

No deployment defect was guessed and no speculative repair was applied.

## Next production path

1. Retrieve the deployment run/job/logs for trigger commit `d5d1598a8c523e8665e4550ee5c272df09256379`, or inspect Cloudflare directly.
2. Preserve the exact failed provider operation.
3. Repair only the proven defect.
4. Verify or create `HIL_REGISTRY` and bind it to `src/worker.js`.
5. Route only `stegverse.org/api/hil/*`, preserving unrelated routes.
6. Require `/api/hil/probes` HTTP 200.
7. Require `/api/hil/readiness` HTTP 200, `state: READY`, and exact v1.1 identities.
8. Run the controlled cycle and verify receipt, status, exact bytes, hash, size, chunks, provenance, custody, and deterministic negative cases.
9. Publish participant readiness only from successful evidence.
10. Prove a real hosted redeployment/restart persistence cycle.
11. Verify the public upload and received pages end-to-end.
12. Complete a genuine participant submission, private review, separately authenticated publication, Site projection, HIL Master Record release, release/tag evaluation, and authorized downstream verification.

## Next pilot path

When an actual response arrives, preserve its bytes unchanged and run:

```text
python scripts/ingest_hil_pilot_return.py RESPONSE.pdf PACKAGE.json [--local-receipt RECEIPT.json] --output ACK.json
python scripts/validate_hil_pilot_ledger.py
```

Only after at least two verified return packages exist may `scripts/generate_hil_pilot_comparison.py` create a governed comparison skeleton.

## Remaining modules and destinations

```text
StegVerse-Labs/Site:
- observe workflow conclusions for the new derivation and validation commits
- finish the separately owned HIL upload surface
- retrieve exact deployment run/job/provider evidence
- prove live Worker route and HIL_REGISTRY operation
- controlled-cycle PASS and restart-persistence PASS
- genuine participant submission and receiver receipt
- authenticated private review and append-only publication
- Site projection and HIL Master Record release

Authorized only after verified activation and release:
- master-records/orchestration
- GCAT-BCAT-Engine/Publisher
- StegVerse-Labs/admissibility-wiki
- StegVerse-002/stegguardian-wiki
- StegVerse-Labs/Sit only after repository identity and role are independently verified
```

## Release posture

No tag or release is authorized. Production receiver activation, restart persistence, genuine participant receipt, private review, publication, Master Record release, and downstream verification remain unproven.

## Next-session prompt

Use the connected GitHub repository directly and continue HIL activation in `StegVerse-Labs/Site`. Read `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`, `docs/SITE_MIRROR_HANDOFF.md`, `docs/HIL_SITE_MIRROR_HANDOFF.md`, `docs/HIL_EXECUTION_SESSION_PROMPT.md`, `docs/HIL_MIRROR_HANDOFF.md`, `docs/HIL_PILOT_VALIDATION_MIRROR_HANDOFF.md`, and `docs/HIL_ANNOUNCEMENT_DERIVATION_MIRROR_HANDOFF.md` in that order, then inspect the newest repository head, orchestration state, heartbeat, and all HIL machine-state and failure-evidence records. Preserve the active upload owner and claimed paths. When general Actions listing is available, inspect workflow conclusions for the announcement derivation tranche and repair only proven defects. For production, retrieve the push-triggered `HIL Cloudflare Receiver Deploy` run associated with commit `d5d1598a8c523e8665e4550ee5c272df09256379`, or inspect the corresponding Cloudflare Worker/D1 deployment directly. Preserve the exact failed step and provider error, repair only the proven defect, then continue through scoped routing, `HIL_REGISTRY`, probes/readiness, exact-byte controlled-cycle PASS, negative cases, machine-derived production readiness, hosted restart persistence, genuine participant receipt, private review, authenticated publication, Site projection, Master Record release, release/tag evaluation, and authorized downstream verification. Update every applicable handoff and machine-state record before responding. Stop only at live success or one exact newly proven external-authority blocker.

## Archive readiness

The current implementation, exact controlled-cycle logs and artifact identity, machine-derived announcement state, orchestration continuity, remaining modules, authority boundaries, and continuation prompt are preserved in repository evidence. Complete thread is ready for archiving without any additional part of the thread needed to move forward.
