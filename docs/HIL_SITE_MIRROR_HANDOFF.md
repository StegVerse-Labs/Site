# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public HIL experiment surface in `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide activation authority and must be used together with:

- `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`
- `docs/HIL_EXECUTION_SESSION_PROMPT.md`

Every session that materially changes HIL state must update this file before responding.

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

## Verified current state — 2026-07-30

### Participant surfaces

- Submission page implemented and fail-closed.
- Received page implemented with exact-byte and receipt verification.
- Grouped participant FAQ implemented.
- Repeated `rigel@stegverse.org` / `HIL Priority` recovery path implemented.
- Public readiness remains `NOT_YET_VERIFIED`; uploads remain disabled.

### Receiver code

`src/worker.js` implements:

- `/api/hil/probes`
- `/api/hil/readiness`
- production submission intake
- receipt generation
- submission status
- exact-byte chunk persistence through `HIL_REGISTRY`
- exact-byte reconstruction and content retrieval
- diagnostic validation

`wrangler.jsonc` identifies `src/worker.js` as the Worker entrypoint and requests Worker-first routing for `/api/hil/*`.

### Controlled-cycle execution

The controlled-cycle supervisor successfully removed the prior silent-failure condition.

Latest verified controlled run:

```text
Run ID: 30569491378
Dispatched: 2026-07-30T18:13:48Z
Completed: 2026-07-30T18:14:04Z
Conclusion: failure
First failed step: Capture and validate live runtime readiness
Failure: https://stegverse.org/api/hil/readiness returned HTTP 404
```

Machine-readable result: `data/hil-controlled-cycle-latest.json`.

This proves the controlled workflow executes and reports, but the production Worker route is not serving the HIL API.

### Cloudflare deployment attempt

A deployment workflow was added at `.github/workflows/hil-cloudflare-deploy.yml` and executed.

Latest machine-readable deployment result:

```json
{"schema_version":"HIL-RECEIVER-DEPLOYMENT-RESULT-v1","deployed":false,"ready":false,"failure":"deployment_step_failed_before_live_probe","authority_effect":false}
```

Commit recording that result: `e6f06765df79d5915096cc47ed88ed07f0475025`.

The workflow requires:

- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`
- `HIL_REGISTRY_DATABASE_ID`

The run failed before the live probe, but the current repository result does not identify which credential or provider action failed. A future session must inspect the deployment run/job logs or use direct Cloudflare controls. It must not assume all three values are missing.

## Why a new session may still be blocked

A session prompt transfers knowledge, not authority. Cloudflare being connected in another chat or visible in the product does not guarantee that the current session exposes Cloudflare actions. Likewise, GitHub repository access does not grant Cloudflare deployment access or reveal GitHub secret values.

Every continuation session must first discover its actual connectors and then choose the shortest available route:

### Environment A — direct Cloudflare controls available

1. Inspect Workers, routes, D1 databases, bindings, and deployment state directly.
2. Create or identify the HIL D1 database.
3. Bind it as `HIL_REGISTRY`.
4. Deploy `src/worker.js` on `stegverse.org/api/hil/*`.
5. Verify live probes/readiness.
6. Continue through controlled cycle, readiness publication, restart persistence, and public-page verification.

### Environment B — GitHub Actions write access but no Cloudflare connector

1. Inspect the exact deployment workflow run and failed job logs.
2. Determine one exact missing secret, permission, account resource, or invalid configuration.
3. Repair repository code/workflow defects directly.
4. Rerun when possible.
5. Only request user action when one proven provider credential/resource cannot be supplied through connected tools.

### Environment C — repository read/write only, no Actions execution and no Cloudflare controls

1. Improve documentation or code only when it directly reduces the external block.
2. Do not create more orchestration layers.
3. Leave one precise next-session prompt naming this handoff and the exact unavailable authority.

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

## Prior attempted solutions and outcomes

1. Manual-dispatch controlled cycle: installed but difficult to initiate from the connected GitHub interface.
2. Push-triggered autostart: created; did not provide sufficient run visibility.
3. Controlled-cycle supervisor: created; succeeded in dispatching and persisting the actual run result.
4. Controlled production cycle: executed; failed immediately because `/api/hil/readiness` returned 404.
5. Cloudflare deployment workflow: created and executed; failed before live probe.
6. No-stop execution prompt: created; new sessions remained blocked when their actual tool set lacked Cloudflare actions.
7. Cross-session protocol: created to prevent connector assumptions and repeated rediscovery.

## Shortest known path to activation

1. Inspect the exact failed Cloudflare deployment job logs.
2. Use direct Cloudflare controls when present; otherwise repair the one exact GitHub secret/configuration failure.
3. Deploy the Worker with `HIL_REGISTRY` bound and the API route active.
4. Require live readiness HTTP 200/READY.
5. Execute `RUN CONTROLLED HIL CYCLE` until PASS.
6. Verify readiness publication commit.
7. Cause a real deployment transition.
8. Execute `VERIFY HIL RESTART PERSISTENCE` until PASS.
9. Verify submission and received pages end-to-end.
10. Announce only after all criteria pass.

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

Update this file with:

- latest commit SHAs;
- latest run IDs and conclusions;
- exact failing step and error;
- current live endpoint responses;
- any created or removed provider resources;
- current shortest execution path;
- remaining terminal criteria.

Then append a ready-to-paste next-session prompt to the user response that points to:

- `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`
- `docs/HIL_SITE_MIRROR_HANDOFF.md`
- `docs/HIL_EXECUTION_SESSION_PROMPT.md`
