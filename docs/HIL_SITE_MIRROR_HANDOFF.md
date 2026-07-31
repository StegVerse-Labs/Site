# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public HIL experiment surface in `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for repository-wide activation authority and must be read with:

1. `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`
2. `docs/HIL_EXECUTION_SESSION_PROMPT.md`
3. `docs/HIL_MIRROR_HANDOFF.md`
4. `docs/HIL_END_TO_END_PROTOCOL.md`
5. `docs/HIL_V1_UPLOAD_MIRROR_HANDOFF.md`
6. `docs/HIL_START_ANNOUNCEMENT.md`
7. `data/hil-participant-readiness.json`
8. `data/hil-controlled-cycle-latest.json`
9. `data/hil-receiver-deployment-latest.json`
10. `data/hil-announcement-status.json`
11. `data/hil-repair-policy.json`
12. `data/hil-operational-model.json`
13. `data/hil-pilot-ledger.json`

Every session that materially changes or inspects HIL activation state must update this file before responding.

## Current goal

Operate the HIL v1.1 experiment through two explicitly separated readiness classes:

1. `ANNOUNCEMENT_READY_WITH_MANAGED_RETURN` — canonical paper, exact prompt, local response validation, hash-bound package, local preparation receipt, verified participant-managed return, and receiving acknowledgment without claims of governed custody.
2. Production receiver activation — live probes/readiness, exact-byte durable custody, canonical receiver receipt, status/content retrieval, negative cases, restart persistence, participant readiness publication, genuine participant submission, private review, append-only publication, Site projection, Master Record release, and downstream verification.

## Canonical contract

```text
Repository: StegVerse-Labs/Site
Participant launch: https://stegverse.org/hil-study-launch.html
Managed return: https://stegverse.org/hil-managed-return.html
Production participant surface: https://stegverse.org/hil/upload/
Receiver base: https://stegverse.org
Worker source: src/worker.js
Custody binding: HIL_REGISTRY
Custody backend: portable-sqlite-chunks-v1
Primary version: v1.1
Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Prompt version: HIL-PROMPT-v1.1
Prompt SHA-256: cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
```

## Current verified production state

```text
Repository head before this session: 73b1e33eec5a60849a075a63fdc7087badceac5e
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
Live receiver receipt ID: absent
Restart-persistence PASS: absent
```

No production state was promoted in this session.

## Managed-return authority

The existing public HIL FAQ authorizes:

```text
return/support address: rigel@stegverse.org
required subject: HIL Priority
```

This permits a concrete participant-managed email return path. It does not grant server submission, durable governed custody, registry commit, exact-byte server reconstruction, review acceptance, or publication authority.

## Session implementation — 2026-07-31T00:22Z

### Pilot ledger

Created `data/hil-pilot-ledger.json` in commit `1a9a59b0646a1e1562f729a43588b60d94604a51`.

The ledger records the two initiated pilot requests:

- Claude Opus 5 / Anthropic
- ChatGPT Medium 5.6 / OpenAI

Both remain `MODEL_REQUEST_INITIATED_RESPONSE_NOT_RECEIVED`. Counts remain:

```text
model requests initiated: 2
completed response PDFs confirmed: 0
verified return packages: 0
managed receiving acknowledgments: 0
governed receiver receipts: 0
```

The ledger includes the required response PDF, package, receipt, return, custody, registry, review, consent, and withheld-claims fields. Pending entries explicitly report `NO_CUSTODY`, `NOT_REGISTERED`, and `NOT_REVIEWED`.

### Mobile participant workflow

Updated `hil-study-launch.html` in commit `a5b164e38ab945ae867c500bbd239650e5da7746`.

Implemented:

- separate `Open canonical PDF` and `Download canonical PDF` controls;
- exact SHA-256 verification before the download control saves the canonical PDF;
- Safari versus browser-managed download guidance for iPhone;
- explicit instruction to save files to Files;
- clearer exact-prompt copy control;
- clear required package versus optional local receipt labels;
- deterministic filenames beginning `HIL-PARTICIPANT-RETURN-` and `HIL-LOCAL-RECEIPT-`;
- explicit statement that the required return pair is the unchanged PDF plus package JSON.

### Managed return

Updated `hil-managed-return.html` in commit `f518d5235e191c480e1c69bb01e7036ee825736d`.

Implemented:

- concrete authorized destination `rigel@stegverse.org`;
- required subject `HIL Priority` and package-bound subject/body generation;
- explicit two-file requirement;
- local receipt identified as optional and non-custodial;
- iPhone Files guidance;
- recovery path when the share sheet cannot attach both files;
- strict v1.1 package schema, PDF hash, and size verification;
- explicit statement that share-sheet completion does not prove delivery or custody.

## Activation authority inspection — 2026-07-31T00:24Z

- Read the five documents specified by the continuation request in order.
- Inspected handoff commit `19be2bc6859b97f1cbe654083af064b3a0a8d4ed`, the newest repository commits, all three machine-state records, and the deploy, controlled-cycle, and restart-persistence workflows.
- The GitHub connector exposes repository reads/writes and known-run job, step, artifact, log, and rerun actions. It exposes neither general workflow-run listing nor workflow dispatch.
- `fetch_commit_workflow_runs` was tested for trigger commit `d5d1598a8c523e8665e4550ee5c272df09256379`; the PR-only action returned no runs and did not reveal the push-triggered deployment execution.
- Cloudflare Workers/D1 plugin discovery returned no available plugin or provider-control action.
- Re-inspected controlled-cycle job `90962296249` and complete logs. The exact readiness command against `https://stegverse.org/api/hil/readiness` returned HTTP 404 and curl exit code 22 at `2026-07-30T18:13:57Z`.
- All packet generation, production submission, status/content retrieval, exact-byte verification, deterministic negative-case, and participant-ready enforcement steps were skipped.
- Failure evidence artifact `hil-participant-readiness-30569491378-1`, artifact ID `8770179722`, was uploaded; it grants no activation authority.
- Updated `docs/HIL_MIRROR_HANDOFF.md` in commit `5907fe983c77c36b1305234df3c44e28bdde87de`.
- A concurrent update to this file was detected and preserved before applying this inspection record.
- No production state, readiness, receipt, custody, restart proof, release, or downstream propagation was promoted.

## Current session authority re-verification — 2026-07-31T00:27Z

- Inspected current repository head `d036a797bacfe22c5905ff3b661673dbd1034207`, reference commit `5907fe983c77c36b1305234df3c44e28bdde87de`, and trigger commit `d5d1598a8c523e8665e4550ee5c272df09256379`.
- Re-read the deployment state, controlled-cycle state, participant readiness, deployment workflow, and trigger control file. No newer live evidence exists.
- Current trigger-commit workflow retrieval returned `workflow_runs: []`; combined commit status returned `statuses: []`.
- The current connector still exposes no general push-run enumeration or workflow dispatch, and no direct Cloudflare Workers/D1 control plane.
- Therefore the deploy run ID, deploy job ID, exact failed step, and complete provider error remain inaccessible. No defect was guessed or repaired.
- `docs/HIL_MIRROR_HANDOFF.md` was updated in commit `b38224de52ad64222937097ca42c3d31aa878e8d` with this exact external-authority result.

## Production blocker

The production blocker remains deployment observability and provider authority. The current session cannot enumerate or dispatch the push-triggered `HIL Cloudflare Receiver Deploy` workflow and cannot inspect or mutate the Cloudflare Worker, route, D1 database, `HIL_REGISTRY` binding, deployment version, logs, restart, or custom-domain state.

Because both the deployment run ID and provider control plane are unavailable, the exact failed deployment command and provider error remain inaccessible. No speculative token, permission, database, binding, route, or workflow repair is authorized.

## Next executable production path

1. Discover the newest `.github/workflows/hil-cloudflare-deploy.yml` run and inspect its exact failed job step and logs, or inspect Cloudflare state directly.
2. Repair only the proven defect.
3. Verify `HIL_REGISTRY` and route only `stegverse.org/api/hil/*` to `src/worker.js`.
4. Require `/api/hil/probes` HTTP 200.
5. Require `/api/hil/readiness` HTTP 200 with `READY` and exact v1.1 identities.
6. Run the complete controlled cycle and preserve the PASS artifact.
7. Verify receipt, status, exact bytes, hash, size, chunks, provenance, custody, and negative cases.
8. Machine-publish participant readiness only from the successful source run.
9. Prove real hosted replacement/restart persistence.
10. Continue through genuine participant submission, private review, separately authenticated publication, Site projection, Master Record release, release/tag evaluation, and authorized downstream verification.

## Next pilot path

When either response arrives:

1. Preserve the exact PDF bytes unchanged.
2. Generate or inspect the v1.1 package and optional local receipt.
3. Verify PDF signature, byte size, PDF SHA-256, package canonical hash, canonical paper identity, and prompt identity.
4. Record managed receipt separately from governed receiver custody.
5. Update `data/hil-pilot-ledger.json` without converting pending status into custody or registry claims.
6. Produce a governed comparison artifact using an explicit rubric and preserve disagreement and uncertainty as data.

## Remaining modules and destinations

```text
StegVerse-Labs/Site:
- schema and validator for data/hil-pilot-ledger.json
- managed receiving acknowledgment receipt definition
- verified pilot-package ingestion utility
- governed pilot comparison schema and generator
- announcement-status derivation from machine evidence
- exact deployment run/job/log evidence
- live Worker route and HIL_REGISTRY operation proof
- controlled-cycle PASS artifact and manifest
- machine-published public readiness
- hosted restart/replacement persistence PASS
- genuine participant submission and canonical receiver receipt
- authenticated private review
- separately authenticated append-only publication
- HIL Master Record release and tag evidence

Authorized post-release verification destinations:
- master-records/orchestration
- GCAT-BCAT-Engine/Publisher
- StegVerse-Labs/admissibility-wiki
- StegVerse-002/stegguardian-wiki
- StegVerse-Labs/Sit only after repository identity is independently verified
```

## Authority boundaries

```text
local preparation != submission
managed email return != governed receiver custody
email attachment preservation != registry commit
receiving acknowledgment != exact-byte server reconstruction
receiver receipt != private acceptance
private acceptance != publication
publication != endorsement
static page deployed != production receiver activated
workflow installed != workflow passed
```

## Release posture

No tag or release is authorized. Production receiver activation, restart persistence, genuine participant receipt, private review, publication, Master Record release, and downstream verification remain unproven.

## Archive readiness

This handoff, the pilot ledger, commit history, machine-state records, connector inspection results, and public-page contracts preserve the complete continuation state. Complete thread is ready for archiving without any additional part of the thread needed to move forward.
