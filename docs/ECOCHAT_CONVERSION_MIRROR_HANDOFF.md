# Ecosystem Chat Conversion — Mirror Handoff

## Canonical relationship

Bounded conversion handoff for the Ecosystem Chat front-door conversion on
`StegVerse-Labs/Site`. The parent Site record remains `SITE_MIRROR_HANDOFF.md`.
The design of record is `ECOSYSTEM__CHAT__SPEC__01`, landed by the principal
2026-11-15 and filed in the Ecosystem KV coordination folder
(Drive `1HNrB1YrB8zCBtmgRFBeVEXHmtVtVnW6p`, MD5 `a00002607da58d646870ba8777db8adf`),
with its build record `ECOSYSTEM__CHAT__BUILD__RECORD__01.md`
(Drive `1XGlsOCF_dNTsSv2XRPSGWvK7a5IwLQ6g`) and pairing notice
StegVerse-Labs/.github#3472 comment 6898175144. Queue identity: ECOCHAT-SITE-001,
extending Q1 of QUEUE ADDENDUM — OVERNIGHT 01.

## Goal

```text
goal_id: SITE-ECOCHAT-CONVERSION-20261115
repository: StegVerse-Labs/Site
canonical_branch: main
claim: SITE-ECOCHAT-CONVERSION-20261115 (CLAIMED_FOR_IMPLEMENTATION)
```

Convert the proving instance built 2026-11-15 into the Site's public form:

1. **Front page to the public-page standard** — `index.html` cleaned to the
   principal's page standard (as simple as any LLM page; few elements on the
   surface, depth one layer down). All incumbent wiring is preserved: every
   element id the runtime binds to, every script, the KV entry launcher, the
   node status surface. Copy and structure change; behavior contracts do not.
2. **Demos as vocabulary** — the starter surface names the filed demos
   (HELLO__CYCLE, SV RANKING segment 2026-W11, SDK SUITE GEN 05) with their
   replayable evaluation states as record content, evaluable from the first
   query once the gateway leg is live.
3. **Gateway binding record** — `data/ecochat/gateway-binding.json` records
   the sovereign gateway the incumbent SDK client already expects
   (`/api/sdk/contract`, `/api/sdk/manifest/build`, `/api/sdk/manifest/validate`,
   `/api/sdk/manifest/submit`), its implementing surface (the manifested
   intake service of ECOSYSTEM__CHAT__SPEC__01, extended with this endpoint
   idiom), and its binding state, stated honestly per state: proving instance
   on the coordinator VM (localhost, not publicly reachable) today; custody
   node at production (ECOCHAT-BIND-001). No live or activation claim is made
   from source, merge, or deployment alone.

## Grades at claim time

- Intake service (both postures), factual route, demo evaluations: WIRED at
  the proving instance, evidence in the build record above.
- This Site conversion: CLAIMED, not yet implemented.
- Public gateway reachability: NOT_YET — the binding's production form is a
  node in the principal's custody (ECOCHAT-BIND-001, principal's device act).

## Collision boundaries

- Do not modify HIL live-execution, heartbeat orchestration, SV001/SV002
  custody, InTr transport, TV/TVC, Master Records, node registration, or the
  claim registry's machine-owned surfaces.
- Do not introduce third-party runtime endpoints, provider credentials, or
  GitHub-token runtime authority (standing Site validator rule).
- Do not remove or rename any element id or script the incumbent runtime
  binds to on the front page.
- The claim registry's canonical file is not edited by this claim; the claim
  enters as an append-only fragment.

## Release condition

Release only after the conversion PRs merge, hosted validation passes
(SESSION_WORK_CLAIMS_PASS, Site Handoff Orchestrator PASS), and public
observation of stegverse.org shows the cleaned page and the binding record's
stated state — with no live-activation claim beyond that state.

## Release — 2026-11-15T18:32:11Z

Released complete. Evidence:
- Claim PR #1693 merged (`1988a7d410d08b45e955b5868ac9e592c83c2f64`); the COSV task projection it completed passes on main (SITE_COSV_TASK_PROJECTION_PASS).
- Implementation PR #1694 merged (`6c4a7235d96a25330362bc2afc81be4e8603839b`); hosted checks on its head showed only the pre-existing check-tidc-research python3.9 failure class.
- Public observation 2026-11-15: https://stegverse.org/ serves the converted page (10,837 bytes; three routes and the demos named; every runtime id, script, and starter prompt intact) and https://stegverse.org/data/ecochat/gateway-binding.json serves the binding record with binding_state PROVING_INSTANCE, publicly_reachable false — the state as filed, no live-activation claim beyond it.
- The gateway compatibility surface (/api/sdk/contract, /api/sdk/manifest/build, /api/sdk/manifest/validate, /api/sdk/manifest/submit, in the incumbent client's idiom) is implemented and tested on the proving-instance intake service.

Next, per the claim's next_task_after_release: ECOCHAT-BIND-001 custody-node binding (principal's device act first), then ECOCHAT-LANES-001 router-to-caller integration.
