# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public HIL experiment surface in `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for repository-wide activation authority and must be read with:

1. `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`
2. `docs/HIL_EXECUTION_SESSION_PROMPT.md`
3. `docs/HIL_MIRROR_HANDOFF.md`
4. `docs/HIL_V1_UPLOAD_MIRROR_HANDOFF.md`
5. `docs/HIL_RUNTIME_DEPLOYMENT_HANDOFF.md`
6. `docs/SITE_MIRROR_HANDOFF.md`
7. `data/site-orchestration-state.json`
8. `data/ecosystem-heartbeat-state.json`
9. `data/hil-controlled-cycle-latest.json`
10. `data/hil-receiver-deployment-latest.json`
11. `data/hil-participant-readiness.json`

Every session that materially changes or inspects HIL activation state must update this file before responding.

## Current goal

Make the HIL v1.1 experiment publicly usable and announcement-ready through verified Primary and prompt, participant PDF response, provenance-bound submission, live receiver readiness, exact-byte durable custody, canonical receipt, status/content retrieval, controlled-cycle verification, real hosted replacement persistence, genuine participant submission, separately authenticated private review and append-only publication, Site projection, HIL Master Record release, and downstream release-verification propagation.

## Canonical surfaces and contract

```text
Repository: StegVerse-Labs/Site
Participant surface: https://stegverse.org/hil/upload/
Receiver base: https://stegverse.org
Worker source: src/worker.js
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
Public readiness schema: HIL-PUBLIC-PARTICIPANT-READINESS-v1
Controlled test case: HIL-E2E-001
```

Cloudflare R2 is not a protocol requirement. Exact PDF bytes are intended to persist as ordered, individually hashed chunks through the SQL-compatible `HIL_REGISTRY` custody contract. A deployment-specific D1 UUID must not be committed as substitute evidence.

## Terminal success criteria

Activation remains incomplete until all of the following are live and evidenced:

1. `/api/hil/probes` and `/api/hil/readiness` return HTTP 200, with readiness `READY` and the exact v1.1 contract.
2. The canonical synthetic packet passes production intake with `research_data: false` and `authority_effect: false`.
3. Receipt, accepted status, exact-byte retrieval, byte length, SHA-256, chunk count, custody state, and deterministic negative cases pass.
4. The evidence manifest hashes every retained evidence file.
5. `data/hil-participant-readiness.json` is machine-published from the specific successful source run with `TEST_PARTICIPANT_PACKET_PASSED` and upload authorization true.
6. The same submission and exact bytes survive a real hosted deployment replacement or restart.
7. A genuine participant submission succeeds.
8. Private review and append-only publication occur through separate authentication and authority.
9. Site projection and a validated HIL Master Record release exist.
10. Required downstream release verification is propagated only from approved release evidence.

## Verified implementation state

The participant upload and received surfaces are implemented fail-closed. `src/worker.js` is intended to implement probes, readiness, production intake, receipt generation, status, SQL chunk persistence, reconstruction, exact-byte retrieval, and validation. Workflow definitions exist for live probe, controlled cycle, readiness publication, and restart persistence. These repository artifacts are implementation evidence, not live activation proof.

The readiness publication workflow is concurrency-aware: it checks out the current default branch, downloads artifacts from the exact triggering workflow run, verifies receipt/status/manifest consistency, records source run identifiers and head SHA, rebases against the newest default branch, and retries a bounded push. It cannot publish unless the triggering participant-readiness gate succeeds.

## Current machine state — verified 2026-07-30

```text
Default branch: main
Repository head before this handoff update: 9247c46b4fe51e433ba2f1bbfff4ef6a24a65536
Latest HIL deployment-block commit: 75b51445207a5ae2facc01a1d3d229867d9f9ac1
Controlled-cycle run: 30569491378
Controlled-cycle job: 90962296249
Controlled-cycle conclusion: failure
First failed step: Capture and validate live runtime readiness
Persisted controlled-cycle state: passed=false
Persisted deployment state: deployed=false, ready=false
Persisted deployment failure: deployment_step_failed_before_live_probe
Public participant readiness: NOT_YET_VERIFIED
Participant ready: false
Upload button authorized: false
Live submission ID: absent
Live receipt ID: absent
Restart-persistence PASS: absent
```

GitHub job inspection confirms steps after live readiness were skipped: synthetic packet generation, production submission, status/content retrieval, acceptance validation, and deterministic rejection checks did not execute. Evidence packaging still ran, but it is failure evidence only.

## Session inspection — 2026-07-30T23:51Z

- Read the canonical HIL Site handoff first, then the v1 upload and runtime deployment handoffs.
- Inspected the current default-branch head and latest HIL-related commits.
- Re-read `data/hil-controlled-cycle-latest.json`, `data/hil-receiver-deployment-latest.json`, and `data/hil-participant-readiness.json` from `main`.
- Inspected controlled-cycle job `90962296249`; readiness failed and all positive-path production verification steps were skipped.
- Inspected `.github/workflows/hil-publish-readiness.yml`; the intended concurrency hardening and source-run provenance binding are present.
- Attempted independent network probes from the available web and container surfaces. The web fetch surface returned cache/safety failures and the container could not resolve `stegverse.org`; therefore this session did not obtain a new trustworthy HTTP observation and does not replace the repository’s last verified HTTP 404 with an assumption.
- The connected GitHub surface exposes known-run job/artifact/log inspection and rerun actions, but no general push-run listing or workflow dispatch action that can discover the unknown deployment run generated by the control commit.
- No Cloudflare Worker, route, D1, binding, deployment, log, restart, or replacement control is exposed in this session.
- No runtime state, readiness, submission, receipt, participant data, review, publication, release, or downstream projection was promoted.

## Exact blocker

The first real blocker is deployment observability and provider authority, not the readiness-publication workflow. The repository records deployment failure before the live probe, while the known controlled-cycle run observes the public readiness route as unavailable. This session cannot discover the relevant push-triggered deployment run or inspect/mutate the hosted Worker and `HIL_REGISTRY` binding directly. Guessing a secret, permission, route, database, or binding defect would violate fail-closed activation.

The next execution environment must expose at least one of:

1. GitHub Actions workflow-run listing or dispatch for `.github/workflows/hil-cloudflare-deploy.yml`, with jobs and logs; or
2. direct hosted Worker and SQL-compatible registry controls for the `stegverse.org/api/hil/*` route.

## Next executable path

1. Discover the newest HIL receiver deployment run and inspect the exact failed step and provider error.
2. Repair only the proven defect while retaining provider-neutral `HIL_REGISTRY` chunk custody and no mandatory R2.
3. Deploy and independently verify live probes/readiness plus a real registry operation.
4. Run the governed controlled cycle to PASS and preserve its complete evidence artifact.
5. Publish readiness only from that exact successful source run.
6. Cause or observe a real hosted replacement and run restart-persistence verification against the original submission.
7. Continue through genuine participant, private review, separately authenticated publication, Site projection, Master Record release, and authorized downstream propagation.

## Remaining modules, evidence, and destinations

```text
StegVerse-Labs/Site:
- exact deployment run/job/log evidence
- live Worker route and HIL_REGISTRY operation proof
- controlled-cycle PASS artifact and manifest
- machine-published public readiness
- hosted restart/replacement persistence PASS artifact
- genuine participant submission and canonical receipt
- authenticated private-review record
- separately authenticated append-only publication record
- data/hil-responses.json update
- data/hil-master-records.json update
- HIL-MASTER-RECORD-RELEASE-v1 validation and release/tag evidence

Authorized post-release verification destinations:
- master-records/orchestration
- GCAT-BCAT-Engine/Publisher
- StegVerse-Labs/admissibility-wiki
- StegVerse-002/stegguardian-wiki
- StegVerse-Labs/Sit only after repository identity is independently verified
```

## Authority boundaries

```text
code implemented != deployed
workflow installed != executed
workflow executed != passed
readiness file edited != readiness proven
synthetic infrastructure evidence != participant research
receiver acceptance != private acceptance
private acceptance != publication
publication != custody
Site projection != endorsement
Master Record release != custody
controlled cycle passed != hosted persistence passed
```

## Archive readiness

Repository handoffs, machine-state files, workflow identifiers, commits, and this inspection preserve the complete continuation state. Complete thread is ready for archiving without any additional part of the thread needed to move forward.
