# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public HIL experiment surface in `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for repository-wide activation authority and must be read with:

1. `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`
2. `docs/HIL_EXECUTION_SESSION_PROMPT.md`
3. `docs/HIL_MIRROR_HANDOFF.md`
4. `docs/SITE_MIRROR_HANDOFF.md`
5. `data/site-orchestration-state.json`
6. `data/ecosystem-heartbeat-state.json`
7. `data/hil-controlled-cycle-latest.json`
8. `data/hil-receiver-deployment-latest.json`
9. `data/hil-participant-readiness.json`

Every session that materially changes or inspects HIL activation state must update this file before responding.

## Current goal

Make the HIL v1.1 experiment publicly usable and announcement-ready: participants must be able to download the canonical Primary, obtain one unchanged LLM response PDF, submit it through the governed Site intake, receive a durable receipt, reload the exact stored bytes, and review the received packet without manual intervention.

## Terminal success criteria

Announcement readiness requires all of the following to be verified live:

1. `https://stegverse.org/api/hil/probes` returns HTTP 200.
2. `https://stegverse.org/api/hil/readiness` returns HTTP 200 with `state: READY` and the exact v1.1 contract.
3. The canonical synthetic packet is accepted through production with `research_data: false` and `authority_effect: false`.
4. A production submission ID and receipt ID are issued.
5. Exact stored PDF bytes are retrieved.
6. SHA-256, size, chunk count, provenance, custody, and authority boundaries pass.
7. Deterministic negative cases pass.
8. `data/hil-participant-readiness.json` is machine-published with `state: TEST_PARTICIPANT_PACKET_PASSED` and `upload_button_authorized: true`.
9. The packet survives a real hosted redeployment/restart and passes persistence verification.
10. `/hil/upload/` and `hil-accepted.html` work end-to-end against live production data.
11. A genuine participant can reliably submit an unchanged PDF and receive a usable received page.

## Canonical surfaces and contract

```text
Repository: StegVerse-Labs/Site
Canonical service: https://stegverse.org/hil/upload/
Receiver base: https://stegverse.org
Worker source: src/worker.js
Worker route: stegverse.org/api/hil/*
Wrangler config: wrangler.jsonc
Custody binding: HIL_REGISTRY
Custody backend: portable-sqlite-chunks-v1
Primary version: v1.1
Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Protocol: HIL-PROTOCOL-v1.1
Prompt: HIL-PROMPT-v1.1
Prompt SHA-256: cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
Provenance schema: HIL-RESPONSE-PROVENANCE-v1.1
Receipt schema: HIL-RECEIVER-RECEIPT-v2
Readiness schema: HIL-PUBLIC-PARTICIPANT-READINESS-v1
Controlled test case: HIL-E2E-001
```

## Verified implementation state

The participant upload page, received page, FAQ, and recovery path are implemented and fail-closed. `src/worker.js` implements probes, readiness, production intake, receipt generation, status, D1 chunk persistence through `HIL_REGISTRY`, reconstruction, exact-byte retrieval, and validation. The implementation is not production proof.

## Latest machine state

```text
Repository head inspected before this update: 0d873e6ad980ab781d5d35ce6c5eaca0d54d4895
Controlled-cycle run: 30569491378
Controlled-cycle job: 90962296249
Controlled-cycle conclusion: failure
First failed step: Capture and validate live runtime readiness
Observed failure: https://stegverse.org/api/hil/readiness returned HTTP 404
Deployment result: deployed=false, ready=false
Deployment failure marker: deployment_step_failed_before_live_probe
Participant readiness: NOT_YET_VERIFIED
Participant ready: false
Upload button authorized: false
Live submission ID: absent
Live receipt ID: absent
Restart-persistence PASS: absent
```

## Session inspection — 2026-07-30T23:10Z

- Read the ten user-designated authority and machine-state files in order and inspected the latest repository commits.
- Direct GitHub repository administration, read, write, commit, workflow-job, workflow-step, artifact, log, and rerun actions are exposed.
- The exposed GitHub action set does not include workflow-run listing or workflow dispatch for `.github/workflows/hil-cloudflare-deploy.yml`.
- `fetch_commit_workflow_runs` was executed against deployment-trigger commit `d5d1598a8c523e8665e4550ee5c272df09256379` and returned an empty run list because the available wrapper does not expose the required push-triggered run.
- Plugin discovery returned no Cloudflare plugin. No Cloudflare account, Worker, route, D1, binding, deployment, custom-domain, logging, rollback, or restart action exists in this session.
- Therefore the exact unavailable control is direct Cloudflare provider access, combined with absent GitHub Actions push-run listing/dispatch. This is not evidence of a particular token, permission, database, route, or binding defect.
- No provider mutation, readiness promotion, synthetic submission, receipt issuance, restart, or release action was performed without runtime authority.
- `research_data: false` and `authority_effect: false` remain preserved.

## Exact proven external-authority block

The current session cannot inspect or mutate the Cloudflare account serving `stegverse.org`, and cannot enumerate or dispatch the push-triggered HIL deployment workflow to obtain its run ID. GitHub job and log actions require a known run or job ID. Consequently the exact failed provider command and resource-level error remain inaccessible; guessing a token scope, account ID, D1 database, binding, route, or deployment defect would violate fail-closed activation.

The next execution environment must expose at least one of:

1. direct Cloudflare Workers and D1 account controls for `stegverse.org`; or
2. GitHub Actions workflow-run listing or dispatch plus logs for `.github/workflows/hil-cloudflare-deploy.yml`.

## Required execution path when authority becomes available

1. Inspect the newest deployment run and exact failed step/log, or inspect Cloudflare state directly.
2. Repair only the proven credential, permission, resource, route, binding, or configuration defect.
3. Identify or create the HIL D1 database and bind it as `HIL_REGISTRY`.
4. Deploy `src/worker.js` only to `stegverse.org/api/hil/*`, preserving unrelated routes.
5. Verify `/api/hil/probes` and `/api/hil/readiness` live.
6. Run the controlled production cycle until PASS.
7. Machine-publish readiness from runtime evidence.
8. Perform a real hosted redeployment/restart and verify persistence.
9. Verify upload and received pages end-to-end.
10. Determine announcement and release/tag readiness only after every terminal criterion passes.
11. Propagate verified evidence to `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki` only after activation proof exists.

## False completion conditions

```text
code implemented != deployed
workflow installed != executed
workflow executed != passed
credential variable named != credential available
configuration present != provider resource verified
readiness file manually edited != readiness proven
controlled cycle passed != restart persistence passed
pages published != participant submission reliable
```

## Authority boundaries

```text
visible summary != governed response packet
response generation != submission
submission != receiver receipt
receiver receipt != review approval
review approval != publication authority
synthetic infrastructure fixture != participant research data
participant readiness != scientific endorsement
announcement ready != announcement published
```

## Archive readiness

Repository handoffs, machine-state files, commits, workflows, and receipts preserve the complete continuation state. No additional conversation context is required.