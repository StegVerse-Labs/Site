# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public HIL experiment surface in `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide activation authority and must be read with:

1. `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`
2. `docs/HIL_EXECUTION_SESSION_PROMPT.md`
3. `docs/HIL_MIRROR_HANDOFF.md`

Every session that materially changes or inspects HIL activation state must update this file before responding.

## Current goal

Make the HIL v1.1 experiment publicly usable and announcement-ready: participants must be able to download the canonical Primary, obtain one unchanged LLM response PDF, submit it through the governed Site intake, receive a durable receipt, reload the exact stored bytes, and review the received packet without manual intervention.

## Terminal success criteria

The experiment is ready for announcement only when all of the following are verified live:

1. `https://stegverse.org/api/hil/probes` returns HTTP 200.
2. `https://stegverse.org/api/hil/readiness` returns HTTP 200 with `state: READY` and the exact v1.1 contract.
3. The controlled synthetic packet is accepted through the production endpoint.
4. A production receipt is issued.
5. Status and exact PDF bytes are retrieved.
6. SHA-256, size, chunk count, provenance, custody, and authority boundaries pass.
7. All deterministic negative cases pass.
8. `data/hil-participant-readiness.json` is published with `state: TEST_PARTICIPANT_PACKET_PASSED` and `upload_button_authorized: true`.
9. The same synthetic packet survives a real hosted deployment/restart or replacement and passes restart-persistence verification.
10. `https://stegverse.org/hil/upload/` enables submission only when live and published readiness both pass.
11. `hil-accepted.html` reloads the stored packet and receipt and displays success only after exact-byte verification.
12. A genuine participant can reliably submit an unchanged PDF and receive a usable received page.

## Canonical surfaces and files

```text
Repository: StegVerse-Labs/Site
Canonical service: https://stegverse.org/hil/upload/
Operational receiver base: https://stegverse.org
Primary page source: humans-as-interoperability-layer.html
Received page: hil-accepted.html
FAQ: hil-faq.html
Receiver runtime: src/worker.js
Base Wrangler config: wrangler.jsonc
Custody binding: HIL_REGISTRY
Custody backend: portable-sqlite-chunks-v1
Participant readiness: data/hil-participant-readiness.json
Latest controlled-cycle result: data/hil-controlled-cycle-latest.json
Latest receiver deployment result: data/hil-receiver-deployment-latest.json
Execution prompt: docs/HIL_EXECUTION_SESSION_PROMPT.md
Deployment handoff: docs/HIL_MIRROR_HANDOFF.md
Cross-session protocol: docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md
Announcement packet: docs/HIL_START_ANNOUNCEMENT.md
```

## Canonical v1.1 chain

```text
Primary version: v1.1
Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Protocol: HIL-PROTOCOL-v1.1
Prompt: HIL-PROMPT-v1.1
Prompt SHA-256: cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
Provenance schema: HIL-RESPONSE-PROVENANCE-v1.1
Receipt schema: HIL-RECEIVER-RECEIPT-v2
Public readiness schema: HIL-PUBLIC-PARTICIPANT-READINESS-v1
Controlled test case: HIL-E2E-001
```

## Verified implementation state

The participant submission page, received page, grouped FAQ, and repeated `rigel@stegverse.org` / `HIL Priority` recovery path are implemented and fail-closed. `src/worker.js` implements `/api/hil/probes`, `/api/hil/readiness`, production submission intake, receipt generation, submission status, exact-byte chunk persistence through `HIL_REGISTRY`, reconstruction, retrieval, and diagnostic validation. `wrangler.jsonc` identifies `src/worker.js` as the Worker entrypoint and requests Worker-first routing for `/api/hil/*`.

Public readiness remains `NOT_YET_VERIFIED`; uploads remain disabled.

## Latest verified controlled-cycle result

```text
Run ID: 30569491378
Job ID: 90962296249
Dispatched: 2026-07-30T18:13:48Z
Completed: 2026-07-30T18:14:04Z
Conclusion: failure
First failed step: Capture and validate live runtime readiness
Failure: https://stegverse.org/api/hil/readiness returned HTTP 404
curl exit code: 22
```

Machine-readable result: `data/hil-controlled-cycle-latest.json`.

This proves the controlled workflow executes and reports, but the production Worker route is not serving the HIL API.

## Latest recorded deployment result

```json
{"schema_version":"HIL-RECEIVER-DEPLOYMENT-RESULT-v1","deployed":false,"ready":false,"failure":"deployment_step_failed_before_live_probe","authority_effect":false}
```

Commit recording that result: `e6f06765df79d5915096cc47ed88ed07f0475025`.

The deployment workflow requires GitHub Actions secrets `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, and `HIL_REGISTRY_DATABASE_ID`, plus a live D1 binding named `HIL_REGISTRY`. Secret names in the workflow do not prove that values, permissions, or provider resources exist.

## Connector and authority state — 2026-07-30T22:29Z

- Current repository head inspected: `4d9559b7e99a94ca1d8d6ab61f3d8efe05f066c2` (`docs(hil): record final-activation authority inspection`).
- Direct GitHub repository read/write controls are available.
- GitHub Actions job, step, artifact, log, and rerun controls are available only after a run ID or job ID is known.
- No action in the current GitHub connector can enumerate push-triggered workflow runs or dispatch the HIL deployment workflow.
- `fetch_commit_workflow_runs` is limited to pull-request-associated runs and cannot identify the push-triggered deployment run.
- No direct Cloudflare, Workers, D1, route, binding, deployment, or provider-control connector is exposed in this session.
- Fresh deployment trigger commit remains `d5d1598a8c523e8665e4550ee5c272df09256379`.
- The trigger commit exposes no combined status/check entries through the available connector.
- No newer receiver deployment observation exists after the trigger.
- `data/hil-receiver-deployment-latest.json` remains unchanged with `deployment_step_failed_before_live_probe`.
- `data/hil-participant-readiness.json` remains `NOT_YET_VERIFIED`, `participant_ready: false`, and `upload_button_authorized: false`.
- No live submission ID, receipt ID, controlled-cycle PASS, or restart-persistence PASS exists.

## Exact proven external-authority block

The current session cannot enumerate the push-triggered `HIL Cloudflare Receiver Deploy` workflow run and cannot inspect or mutate Cloudflare Worker, route, D1 database, `HIL_REGISTRY` binding, deployment, or custom-domain state directly. Because the fresh run ID is unavailable, the available GitHub job/log actions cannot inspect the failed deployment command or provider error. Guessing which secret, permission, account resource, route, or binding failed would violate the fail-closed activation rules.

The next session must expose at least one of:

1. GitHub Actions workflow-run listing or dispatch for `.github/workflows/hil-cloudflare-deploy.yml`; or
2. Direct Cloudflare Workers and D1 controls for the account serving `stegverse.org`.

## Required execution path when authority becomes available

1. Enumerate the newest `HIL Cloudflare Receiver Deploy` run and inspect its exact failed job step and logs, or inspect Cloudflare state directly.
2. Repair only the proven credential, permission, resource, route, binding, or configuration defect.
3. Create or identify the HIL D1 database and bind it as `HIL_REGISTRY`.
4. Deploy `src/worker.js` only on `stegverse.org/api/hil/*`, preserving unrelated routes.
5. Require `/api/hil/probes` HTTP 200 and `/api/hil/readiness` HTTP 200 with `state: READY`.
6. Run `RUN CONTROLLED HIL CYCLE` until PASS.
7. Verify readiness publication contains the live submission ID, receipt ID, response SHA-256, size, chunk count, custody backend, exact-byte retrieval, positive-cycle PASS, negative-case PASS, and upload authorization.
8. Cause a real hosted deployment/restart and run `VERIFY HIL RESTART PERSISTENCE` until PASS.
9. Verify the public upload and received pages end-to-end with live production data.
10. Determine announcement and release/tag readiness only after every terminal criterion passes.
11. Propagate verified activation evidence to `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki` only after activation proof exists.

## Relevant workflows and controls

```text
.github/workflows/hil-cloudflare-deploy.yml
.github/workflows/hil-controlled-cycle.yml
.github/workflows/hil-controlled-cycle-autostart.yml
.github/workflows/hil-controlled-cycle-supervisor.yml
.github/workflows/hil-publish-readiness.yml
.github/workflows/hil-live-probe.yml
.github/workflows/hil-restart-persistence.yml
controls/DEPLOY_HIL_RECEIVER.txt
controls/RUN_CONTROLLED_HIL_CYCLE.txt
```

## False completion conditions

```text
code implemented != deployed
workflow installed != executed
workflow executed != passed
credential variable named != credential available
Cloudflare connected elsewhere != Cloudflare actions available here
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

## Required update before every session ends

Record latest commit SHAs, run IDs and conclusions, exact failing step and error, live endpoint responses, provider resources, connector availability, shortest execution path, and remaining terminal criteria. Then append a ready-to-paste next-session prompt naming every applicable handoff.

## Session inspection — 2026-07-30T22:59Z

- Re-read the ten user-designated authority and machine-state files at authority-inspection commit `19be2bc6859b97f1cbe654083af064b3a0a8d4ed` before attempting activation.
- The connector control plane returned `status: not_installed` for the named `Cloudflare` plugin in this session.
- The session tool inventory exposes GitHub repository operations but no Cloudflare namespace or action for account state, Workers, routes, D1 databases, bindings, deployments, custom domains, logs, or restarts.
- Therefore the exact unavailable control is the Cloudflare connector itself, not a guessed token scope or D1 permission inside an accessible account.
- Direct deployment, D1 creation/inspection, `HIL_REGISTRY` binding, route mutation, restart, and provider-side verification could not lawfully be attempted.
- Repository evidence remains fail-closed: controlled cycle `30569491378` failed, deployment state remains `deployment_step_failed_before_live_probe`, participant readiness remains `NOT_YET_VERIFIED`, and no submission ID or receipt ID exists.
- No readiness, research, authority, activation, publication, or release state was promoted.
