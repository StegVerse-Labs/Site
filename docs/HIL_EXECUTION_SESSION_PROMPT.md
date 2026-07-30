# HIL Final Activation — No-Stop Execution Prompt

You are continuing the StegVerse HIL experiment activation in `StegVerse-Labs/Site`.

Before taking any action, read these files in order:

1. `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`
2. `docs/HIL_SITE_MIRROR_HANDOFF.md`
3. `docs/HIL_EXECUTION_SESSION_PROMPT.md`
4. `docs/SITE_MIRROR_HANDOFF.md`

Then inspect the latest commits and these machine-readable files:

- `data/hil-controlled-cycle-latest.json`
- `data/hil-receiver-deployment-latest.json`
- `data/hil-participant-readiness.json`

## Tool discovery is mandatory

Discover which connectors and actions are actually available in this session before choosing an execution path.

Do not assume Cloudflare access exists because another session had it, the user connected Cloudflare elsewhere, or this prompt mentions it. A prompt transfers context, not credentials or connector authority.

Use direct Cloudflare controls when available. Use GitHub workflows only when direct provider controls are unavailable or the workflow is the governed execution mechanism.

## Mission

Do not ask Rigel for status, confirmation, prioritization, or permission. Do not repeat questions answered by the repository handoff. Do not stop after adding scaffolding, workflows, diagnostics, or documentation.

Continue until one of these terminal conditions is reached:

1. **SUCCESS:** the live experiment accepts the canonical synthetic test packet, stores the exact bytes durably, returns a valid receipt, retrieves identical bytes, passes SHA-256/size/chunk verification, passes negative cases, survives a real deployment/restart persistence check, publishes `data/hil-participant-readiness.json` with `state: TEST_PARTICIPANT_PACKET_PASSED` and `upload_button_authorized: true`, and the public submission and received pages work reliably; or
2. **PROVEN EXTERNAL AUTHORITY BLOCK:** every actually available GitHub, Cloudflare, and provider action has been exhausted, and one exact unavailable credential, permission, account resource, or provider control is proven to require Rigel. Do not list speculative possibilities.

## Current verified blocker

The latest controlled cycle executed and failed:

```text
Run ID: 30569491378
Conclusion: failure
First failed step: Capture and validate live runtime readiness
Observed result: https://stegverse.org/api/hil/readiness returned HTTP 404
```

`src/worker.js` already implements the HIL API. The Worker is not serving the production route.

The latest deployment attempt produced:

```json
{"schema_version":"HIL-RECEIVER-DEPLOYMENT-RESULT-v1","deployed":false,"ready":false,"failure":"deployment_step_failed_before_live_probe","authority_effect":false}
```

Do not assume which Cloudflare value or action failed. Inspect the actual deployment run/job logs or direct Cloudflare state.

## Required execution order

1. Inspect actual connector availability.
2. Inspect the latest Cloudflare deployment workflow run and exact failed job step/logs when GitHub Actions data is available.
3. If direct Cloudflare controls exist, inspect Workers, routes, D1 databases, bindings, deployments, and account state directly.
4. Identify or create the HIL custody database and bind it as `HIL_REGISTRY`.
5. Route `stegverse.org/api/hil/*` to `src/worker.js` without replacing unrelated routes.
6. Deploy and verify:
   - `/api/hil/probes` returns HTTP 200;
   - `/api/hil/readiness` returns HTTP 200 and `state: READY`;
   - the exact Primary, prompt, provenance, size, and custody contract match repository validators.
7. Run the controlled production cycle using `RUN CONTROLLED HIL CYCLE`.
8. Inspect evidence and logs. Repair and rerun until PASS.
9. Confirm `data/hil-participant-readiness.json` is committed with verified submission ID, receipt ID, response SHA-256, size, chunk count, custody backend, exact-byte retrieval, positive-cycle PASS, negative-case PASS, and upload authorization.
10. Cause or independently verify a real hosted redeployment/restart after the successful synthetic submission.
11. Run restart persistence using `VERIFY HIL RESTART PERSISTENCE`. Repair and repeat until PASS.
12. Verify the public upload page and received page end-to-end with live production data.
13. Preserve synthetic-test boundaries: `research_data: false`, `authority_effect: false`, no publication authority.
14. Mark announcement readiness only after every terminal success criterion in `docs/HIL_SITE_MIRROR_HANDOFF.md` passes.

## Non-negotiable rules

- A commit is not completion.
- A workflow trigger is not completion.
- A configured binding is not completion.
- A passing fixture is not live evidence.
- Do not manually set readiness to PASS.
- Do not add another dependency unless it removes or replaces at least one existing dependency.
- Do not claim a connector exists without discovering it in this session.
- Do not lower the acceptance standard to obtain a green result.
- Never claim success without live submission ID, receipt ID, response hash, exact-byte retrieval, controlled-cycle PASS, and restart-persistence PASS.
- Before responding, update `docs/HIL_SITE_MIRROR_HANDOFF.md` with all material changes.
- At the end of the response, provide a ready-to-paste next-session prompt naming all required handoffs, even after success.

## Response when successful

State only the operational proof needed for announcement:

- live URLs;
- submission ID;
- receipt ID;
- SHA-256;
- controlled-cycle result;
- restart-persistence result;
- public-page verification;
- announcement readiness.

## Response when externally blocked

State only:

- the exact blocked action;
- the exact failed command or provider operation;
- the exact missing permission, credential, or resource proven by logs or direct inspection;
- one minimal action Rigel must perform;
- a ready-to-paste next-session prompt pointing to all required handoffs.

Do not provide another broad status recap.
