# HIL Final Activation — No-Stop Execution Prompt

Use this prompt in a new ChatGPT/Codex session with GitHub and Cloudflare access enabled.

---

You are continuing the StegVerse HIL experiment activation in `StegVerse-Labs/Site`.

Do not ask Rigel for status, confirmation, prioritization, or permission. Do not stop after adding scaffolding, workflows, diagnostics, or documentation. Continue until one of these two terminal conditions is reached:

1. **SUCCESS:** the live experiment accepts the canonical synthetic test packet, stores the exact bytes durably, returns a valid receipt, retrieves identical bytes, passes SHA-256/size/chunk verification, passes negative cases, survives a real deployment/restart persistence check, publishes `data/hil-participant-readiness.json` with `state: TEST_PARTICIPANT_PACKET_PASSED` and `upload_button_authorized: true`, and the public submission and received pages work at `https://stegverse.org/hil/upload/` and the corresponding received URL; or
2. **EXTERNAL AUTHORITY BLOCK:** you have exhausted every connected GitHub and Cloudflare action and can identify one exact unavailable credential, permission, account resource, or provider control that only Rigel can supply. In that case, provide one minimal action with exact UI location and value type required. Do not provide a list of speculative possibilities.

## Current verified state

Repository: `StegVerse-Labs/Site`

Known live failure:
- Controlled-cycle run ID: `30569491378`
- The first failed step was `Capture and validate live runtime readiness`.
- `https://stegverse.org/api/hil/readiness` returned HTTP 404.
- `src/worker.js` already implements `/api/hil/readiness`, submission, status, content retrieval, exact-byte chunk custody, and receipt logic.
- `wrangler.jsonc` sets `main: src/worker.js` and `run_worker_first: ["/api/hil/*"]`.
- The Worker is not currently serving the production route.

Observable control files already exist:
- `controls/RUN_CONTROLLED_HIL_CYCLE.txt`
- `data/hil-controlled-cycle-attempt.json`
- `data/hil-receiver-deployment-result.json`

Current deployment result:
```json
{"schema_version":"HIL-RECEIVER-DEPLOYMENT-RESULT-v1","deployed":false,"ready":false,"failure":"deployment_step_failed_before_live_probe","authority_effect":false}
```

Relevant workflows:
- `.github/workflows/hil-controlled-cycle.yml`
- `.github/workflows/hil-controlled-cycle-autostart.yml`
- `.github/workflows/hil-controlled-cycle-supervisor.yml`
- `.github/workflows/hil-publish-readiness.yml`
- `.github/workflows/hil-live-probe.yml`
- `.github/workflows/hil-restart-persistence.yml`
- the Cloudflare deployment workflow added in the latest HIL work

Participant surfaces already exist:
- `humans-as-interoperability-layer.html`
- `hil-accepted.html`
- `hil-faq.html`
- `assets/hil-participant-readiness-gate-v1.js`
- `data/hil-participant-readiness.json`

Support path:
- To: `rigel@stegverse.org`
- Subject: `HIL Priority`

## Required execution order

1. Inspect the Cloudflare deployment workflow and its run logs. Determine the exact failing command and exact missing/invalid resource.
2. Use connected Cloudflare controls directly if available. Do not route through another workflow when direct deployment is possible.
3. Ensure a D1 database exists for HIL custody. Bind it as `HIL_REGISTRY` in the deployed Worker configuration.
4. Ensure the Worker route covers `stegverse.org/api/hil/*` without replacing unrelated Site routes.
5. Deploy `src/worker.js` and verify:
   - `/api/hil/probes` returns HTTP 200;
   - `/api/hil/readiness` returns HTTP 200 and `state: READY`;
   - the exact Primary, prompt, provenance, maximum size, and custody contract match repository validators.
6. Run the controlled production cycle using the exact phrase `RUN CONTROLLED HIL CYCLE`.
7. Inspect the controlled-cycle artifact and logs. Repair any failure immediately and rerun until PASS.
8. Confirm `data/hil-participant-readiness.json` is committed with the verified submission ID, receipt ID, response SHA-256, size, chunk count, custody backend, exact-byte retrieval, positive cycle pass, negative cases pass, and upload authorization.
9. Cause or verify a real hosted redeployment/restart after the successful synthetic submission.
10. Run restart persistence using `VERIFY HIL RESTART PERSISTENCE` and the exact original submission evidence. Repair and repeat until PASS.
11. Verify the public upload page enables submission only when both live receiver readiness and published participant readiness pass.
12. Verify the received page reloads the stored packet and receipt and displays success only after exact-byte verification.
13. Do not enable publication, scientific endorsement, Master Record release, or participant-data publication as part of the synthetic infrastructure test.
14. Only after all infrastructure gates pass, mark the experiment ready for public participant announcement.

## Non-negotiable rules

- A commit is not completion.
- A workflow trigger is not completion.
- A configured binding is not completion.
- A passing fixture is not live evidence.
- Do not add another dependency unless it replaces at least one existing dependency.
- Do not lower the acceptance standard to obtain a green result.
- Do not manually set readiness to PASS.
- Never claim success without a live submission ID, receipt ID, response hash, exact-byte retrieval, controlled-cycle PASS, and restart-persistence PASS.
- Preserve synthetic-test boundaries: `research_data: false`, `authority_effect: false`, no publication authority.
- Continue autonomously through completion or until the single exact external-authority block is proven.

## Final response format

When successful, state the live URLs, submission ID, receipt ID, SHA-256, controlled-cycle result, restart-persistence result, and announcement readiness.

When externally blocked, state only:
- the exact blocked action;
- the exact missing permission/credential/resource;
- the one minimal action Rigel must perform;
- the exact continuation command or prompt to run immediately afterward.

Do not provide another broad status recap.
