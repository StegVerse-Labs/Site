# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns HIL continuation in `StegVerse-Labs/Site` and is subordinate to `docs/SITE_MIRROR_HANDOFF.md`. Read in order with `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`, `docs/HIL_EXECUTION_SESSION_PROMPT.md`, `docs/HIL_MIRROR_HANDOFF.md`, `docs/HIL_END_TO_END_PROTOCOL.md`, `docs/HIL_V1_UPLOAD_MIRROR_HANDOFF.md`, `docs/HIL_START_ANNOUNCEMENT.md`, and the HIL machine-state records.

## Current goal

Operate two explicitly separate readiness classes:

1. `ANNOUNCEMENT_READY_WITH_MANAGED_RETURN`: exact v1.1 paper and prompt, unchanged response PDF, verified package, optional local receipt, and managed receiving acknowledgment that claims no governed custody.
2. Production receiver activation: live route and D1 binding, exact-byte custody, controlled-cycle PASS, machine-published readiness, restart persistence, genuine participant receipt, private review, separately authenticated publication, Site projection, Master Record release, and downstream verification.

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
```

## Reconciled repository state

The session began from head `b38224de52ad64222937097ca42c3d31aa878e8d`, which is newer than `89f51b293804439739bda2746017d311e41e7038` and preserves concurrent authority-inspection work from `5907fe983c77c36b1305234df3c44e28bdde87de`, `d036a797bacfe22c5905ff3b661673dbd1034207`, and `b38224de52ad64222937097ca42c3d31aa878e8d`.

Newest pilot implementation commits in this session:

```text
96e5e91649c22d02191c874d08911baf52666072  data/schemas/hil-pilot-ledger.schema.json
e3eeddccc3153851d0631e5aad43c4c77d118175  scripts/validate_hil_pilot_ledger.py
c4c86010a2cf73cab3e435b34bf65595506bfb32  data/schemas/hil-managed-receiving-acknowledgment.schema.json
616056e210db4a6d9c98aa10255c9dac90c96f40  scripts/ingest_hil_pilot_return.py
192b7cdac1b7a3c6b4267f260e8411a57f3f783a  data/schemas/hil-pilot-comparison.schema.json
0e5ee803c57a46803f9ab4f9fa0a27508ee77667  scripts/generate_hil_pilot_comparison.py
```

Latest production-authority inspection head before this handoff update: `20da57673f3bdd42507e47980b34896e54cd1e86`.

## Pilot state and semantics

`data/hil-pilot-ledger.json` remains unchanged and fail-closed:

```text
Claude Opus 5: MODEL_REQUEST_INITIATED_RESPONSE_NOT_RECEIVED
ChatGPT Medium 5.6: MODEL_REQUEST_INITIATED_RESPONSE_NOT_RECEIVED
completed response PDFs: 0
verified return packages: 0
managed receiving acknowledgments: 0
governed receiver receipts: 0
```

No response completion, receipt, custody, registry, review, publication, or Master Record status was invented.

The new ledger validator enforces JSON Schema, unique submission IDs, canonical paper/prompt identities, count reconciliation, complete response identity before non-pending status, and no registry claim without custody.

The managed acknowledgment schema requires successful PDF signature/hash/size, package canonical hash, paper identity, and prompt identity verification while fixing these boundaries:

```text
custody_status: MANAGED_RETURN_PRESERVED_NO_GOVERNED_CUSTODY
registry_status: NOT_REGISTERED
review_status: NOT_REVIEWED
publication_status: NOT_PUBLISHED
authority_effect: false
```

The ingestion utility accepts an unchanged PDF, package JSON, and optional local receipt; verifies `%PDF-`, SHA-256, byte size, package canonical hash, paper identity, prompt identity, and optional receipt bindings; then emits only the managed acknowledgment above.

The comparison generator is fail-closed until at least two verified response packages exist. It creates an explicit rubric skeleton and preserves agreement, disagreement, uncertainty, limitations, and withheld claims without inferring response content.

## Current verified production state

```text
Controlled-cycle run: 30569491378
Controlled-cycle job: 90962296249
Conclusion: failure
First failed step: Capture and validate live runtime readiness
Exact live result: https://stegverse.org/api/hil/readiness returned HTTP 404; curl exit 22
Deployment state: deployed=false, ready=false
Deployment failure: deployment_step_failed_before_live_probe
Participant readiness: NOT_YET_VERIFIED
participant_ready: false
upload_button_authorized: false
production submission: absent
production receiver receipt: absent
restart persistence: unproven
```

## Current-session production authority inspection — 2026-07-31T00:52Z

- Read the five required handoffs in full and in order.
- Verified `main` at `20da57673f3bdd42507e47980b34896e54cd1e86` before handoff mutation.
- Verified requested handoff commits `b38224de52ad64222937097ca42c3d31aa878e8d` and `b9f2892a962ac11e3e7caa51d827058c109a1486` are ancestors of current `main` by eight and seven commits respectively.
- Queried the only available commit-associated workflow-run action for trigger commit `d5d1598a8c523e8665e4550ee5c272df09256379`; it returned `workflow_runs: []` and is explicitly restricted to pull-request-triggered runs.
- The GitHub connector provides job, step, log, artifact, and rerun actions only for already-known run/job IDs. It does not provide general workflow-run enumeration or workflow dispatch for `.github/workflows/hil-cloudflare-deploy.yml`.
- No direct Cloudflare Worker, deployment, route, D1, binding, or runtime-log controls are exposed.
- Therefore the exact deployment run ID, job ID, failed step, and complete provider error cannot be retrieved in this environment. No provider defect was guessed, readiness remains fail-closed, and no release or downstream propagation was attempted.

## Exact production authority block

The available GitHub connector can inspect known run/job IDs but cannot enumerate or dispatch the push-triggered `HIL Cloudflare Receiver Deploy` workflow. It exposes no direct Cloudflare Worker, route, deployment, D1, binding, log, restart, or custom-domain controls. Therefore the newest deploy run ID, deploy job ID, exact failed deployment step, and provider error cannot be retrieved in this session. No deployment defect was guessed or repaired.

The next execution environment requires either general GitHub Actions workflow-run listing/dispatch for `.github/workflows/hil-cloudflare-deploy.yml`, or direct Cloudflare Workers/D1 control-plane access.

## Next production path

1. Retrieve the newest deployment run/job/logs or inspect Cloudflare directly.
2. Repair only the proven defect.
3. Verify `HIL_REGISTRY` and route only `stegverse.org/api/hil/*` to `src/worker.js`.
4. Require `/api/hil/probes` HTTP 200.
5. Require `/api/hil/readiness` HTTP 200, `READY`, and exact v1.1 identities.
6. Run the complete controlled cycle and verify receipt, status, exact bytes, hash, size, chunks, provenance, custody, and deterministic negative cases.
7. Publish readiness only from the successful source run.
8. Prove real hosted restart/replacement persistence.
9. Continue through genuine participant submission, private review, separately authenticated publication, Site projection, Master Record release, release/tag evaluation, and authorized downstream verification.

## Next pilot path

When an actual response arrives, preserve its bytes unchanged and run:

```text
python scripts/ingest_hil_pilot_return.py RESPONSE.pdf PACKAGE.json [--local-receipt RECEIPT.json] --output ACK.json
python scripts/validate_hil_pilot_ledger.py
```

Only after two entries have verified return packages may `scripts/generate_hil_pilot_comparison.py` create a comparison skeleton for governed content review.

## Remaining modules and destinations

```text
StegVerse-Labs/Site:
- bind the new validators into canonical application validation/CI
- add fixtures for valid and invalid ledger, package, acknowledgment, and comparison records
- derive announcement status from machine evidence
- obtain exact deployment run/job/log evidence
- prove live Worker route and HIL_REGISTRY operation
- controlled-cycle PASS and restart-persistence PASS
- genuine participant submission and receiver receipt
- authenticated private review and append-only publication
- Site projection and HIL Master Record release

Authorized only after verified release:
- master-records/orchestration
- GCAT-BCAT-Engine/Publisher
- StegVerse-Labs/admissibility-wiki
- StegVerse-002/stegguardian-wiki
- StegVerse-Labs/Sit only after repository identity is independently verified
```

## Release posture

No tag or release is authorized. Production receiver activation, restart persistence, genuine participant receipt, private review, publication, Master Record release, and downstream verification remain unproven.

## Next-session prompt

Use the connected GitHub repository directly and continue HIL activation in `StegVerse-Labs/Site`. Read `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`, `docs/HIL_MIRROR_HANDOFF.md`, `docs/HIL_SITE_MIRROR_HANDOFF.md`, `docs/HIL_EXECUTION_SESSION_PROMPT.md`, and `docs/SITE_MIRROR_HANDOFF.md` in that order, then inspect the newest repository head and HIL machine-state files. First retrieve the push-triggered `HIL Cloudflare Receiver Deploy` run and job associated with trigger commit `d5d1598a8c523e8665e4550ee5c272df09256379` using general GitHub Actions workflow-run listing/dispatch, or inspect the corresponding Cloudflare Worker/D1 deployment directly. Retrieve the exact failed step and complete provider error, repair only the proven defect, then continue through scoped Worker deployment, `HIL_REGISTRY`, probes/readiness, exact v1.1 controlled-cycle PASS, exact-byte custody and retrieval, negative cases, machine-derived readiness, restart persistence, public upload/received verification, release/tag evaluation, and authorized downstream verification. Do not repeat connector discovery already preserved except to verify this session's actual actions. Update both HIL handoffs before responding and stop only at complete live success or one exact newly proven external-authority blocker.

## Archive readiness

The complete continuation state is preserved in repository handoffs, machine-state records, schemas, utilities, commit history, and the prompt above. Complete thread is ready for archiving without any additional part of the thread needed to move forward.
