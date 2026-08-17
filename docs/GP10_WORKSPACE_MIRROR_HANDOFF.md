# GP10 Workspace Mirror Handoff

Status: ACTIVE PROJECT — SITE WORKSTREAM VALIDATED / CREDENTIAL-CLEAN REMEDIATION IN PROGRESS
Updated: 2026-08-17
Goal ID: `GP10-SITE-SECURE-GUIDED-WORKSPACE-001`
Originating session goal: provide a simplified, logically narrowing GP10 evidence and commercial-posture workspace, a beginner examples surface, and browser security controls that treat applicable federal cybersecurity requirements as a minimum baseline rather than a target ceiling.
Repository: `StegVerse-Labs/Site`
Canonical branch: `main`
Active remediation branch: `claim/site-gp10-github-token-writeback-retirement-r1-20260817`

## Canonical ownership

- GP10 domain logic, schemas, evidence custody, ingestion, runtime validation, and commercial governance remain canonical in `StegVerse-Labs/GP10`.
- This repository owns the unlisted browser workspace, examples surface, browser-side security controls, Site isolation verification, and non-authorizing hosted-page observation.
- Canonical GP10 continuation: `StegVerse-Labs/GP10/GP10_MIRROR_HANDOFF.md`.
- Canonical Site continuation: this file and `data/operations/gp10_workspace_tasks.json`.
- Site is not the source of truth for GP10 evidence, approval, custody, runtime authority, or commercial authority.
- Credential authority is TV/TVC; no NON-TV/TVC project/provider secret or token is a required GP10 Site validation dependency.

MERGED INTO: `StegVerse-Labs/Site/docs/GP10_WORKSPACE_MIRROR_HANDOFF.md`

The originating session has released its Site implementation and observation claims. Remaining service-boundary and GP10 commercial tasks are owned by durable repository owners. The current credential-clean remediation is a separate Site #268 cleanup lane and does not reopen GP10 product authority.

## Authoritative files

- `gp10-workspace.html`
- `gp10-workspace-examples.html`
- `assets/gp10-workspace.js`
- `assets/gp10-evidence-integration.js`
- `assets/gp10-workspace-wizard.js`
- `assets/gp10-validation-feedback.js`
- `assets/gp10-examples-adaptive.js`
- `assets/gp10-security.js`
- `scripts/check_gp10_workspace.py`
- `scripts/check_gp10_workspace_deployment.py`
- `docs/GP10_WORKSPACE_SECURITY_BASELINE.md`
- `docs/GP10_WORKSPACE_DEPLOYMENT_OBSERVER_ADDENDUM.md`
- `data/operations/gp10_workspace_tasks.json`
- `.github/workflows/gp10-workspace-security.yml`
- `docs/receipts/gp10-site/` (historical immutable receipts)
- `docs/GP10_WORKSPACE_HANDOFF.md` (legacy redirect)

## Claim state

### `GP10-SITE-SECURITY-HARDENING`

- State: `COMPLETE`
- Role: `RELEASED_IMPLEMENTATION_CLAIM`
- Released: `2026-08-02T20:00:00-05:00`
- Collision boundary: no GP10 repository validator, workflow, schema, receipt, or claimed runtime surface was modified through this Site claim.

### `GP10-SITE-DEPLOYMENT-OBSERVATION`

- State: `COMPLETE`
- Role: `RELEASED_MACHINE_VALIDATION_CLAIM`
- Tested commit: `80fbf35d2a824f689050c7ec69e579c2ddf8f196`
- Workflow run: `30780334497`
- Job: `91583581262`
- Artifact: `8843410533`
- Artifact digest: `sha256:417f8160a6bf9d7eb211da3da4ef236dbe453d930905c1cb4bf8d128cc42ddb6`
- Receipt commit: `018a58f5c60434d51ea3762e2bba119a94eaeaac`
- Durable receipt: `docs/receipts/gp10-site/deployment-80fbf35d2a824f689050c7ec69e579c2ddf8f196.json`
- Result: `PASS`

The historical job, steps, logs, artifact, committed receipts, hashes, marker results, receipt persistence, and final enforcement were directly inspected before release. Those historical artifact/writeback mechanics are immutable evidence of the completed observation, not continuing custody requirements.

### `SITE-GP10-GITHUB-TOKEN-WRITEBACK-RETIREMENT-R1-20260817`

- State: `CLAIMED_FOR_IMPLEMENTATION`
- Role: `IMPLEMENTATION_VALIDATION`
- Parent: `StegVerse-Labs/Site#268`
- Branch: `claim/site-gp10-github-token-writeback-retirement-r1-20260817`
- Goal: preserve GP10 Site static and hosted-page validation while removing GitHub token, repository writeback, and artifact-custody mechanics.
- Credential authority: `TV/TVC`
- GitHub runtime/control-plane authority: `NONE`
- Execution authority effect: `NONE`
- Custody authority effect: `NONE`
- Release condition: exact-head GP10 workflow, Site Handoff Orchestrator, Ecosystem Heartbeat, Site Bootstrap, and StegFin projection PASS; merge; claim release; task/handoff reconciliation.

Installed workflow boundary:

```text
permissions: {}
credential-bearing environment refusal: INSTALLED
anonymous exact-SHA public Site fetch: INSTALLED
preinstalled Python: USED
actions/checkout: REMOVED
actions/setup-python: REMOVED
actions/upload-artifact: REMOVED
contents write: REMOVED
repository commit/push writeback: REMOVED
GitHub token consumption: REMOVED
check_gp10_workspace.py: RETAINED
check_gp10_workspace_deployment.py: RETAINED for main/non-PR observation
PR deployment observation: BLOCKED_PR_NOT_DEPLOYED_MAIN
historical committed receipts: RETAINED IMMUTABLY
future GitHub artifact/repository custody: NONE
```

## Preserved interaction requirements

1. Show one logical decision at a time.
2. Hide fields that do not follow from prior answers.
3. Skip economics and threshold pages when a hard-stop condition already controls the result.
4. Preserve missing information as missing; never synthesize evidence, prices, thresholds, or approval.
5. Maintain a separate beginner examples page with safe synthetic files and plain-language governance explanations.
6. Keep both pages unlisted and marked `noindex`, `nofollow`, and `noarchive`.
7. Preserve `execution_authority: false` and browser-local uncustodied state.
8. Site is an interface and must not become the source of truth for GP10 evidence or authority.

## Implemented security controls

- same-origin-only script execution through document CSP;
- denial of plugins, mutable base URI, remote form submission, frames, media, workers, and external connections;
- `no-referrer` policy;
- 15-minute inactivity lock and five-minute background lock;
- file-input clearing on lock and page hide;
- explicit GP10-namespaced local-data clearing;
- SHA-256 browser integrity receipts over the current candidate, evidence packets, and review queue;
- explicit receipt limits: integrity does not prove truth, identity, authority, custody, approval, or execution authority;
- fail-closed static verification of policy, adaptive UX, examples synchronization, authority denial, and public-navigation isolation;
- exact-byte hosted deployment observation with bounded retries and cache-busting;
- historical repository-native PASS/FAILED receipts remain preserved; new GitHub writeback/artifact custody is being retired by the active Site #268 claim.

The complete control contract and static-host limitations are in `docs/GP10_WORKSPACE_SECURITY_BASELINE.md`. This is not a federal compliance certification.

## Observed validation evidence

Workflow run `30780334497` completed successfully on Ubuntu 24.04 with Python 3.12.13.

- Static checker: `PASS`.
- Workspace hosted/local SHA-256: `2a151a37ebfa9937f64f67b285151f4895b81e875076226e4fdcba18215b1f48`.
- Examples hosted/local SHA-256: `502d385f3c534365e5488f10b8011efb988a5634734df5b086177c7d3133701f`.
- Exact byte equality: `true` for both pages.
- CSP marker: present on both pages.
- `no-referrer`: present on both pages.
- `gp10-security.js`: present on both pages.
- noindex/noarchive marker: present on both pages.
- no-execution-authority marker: present on both pages.
- Attempts used: `1`.
- Historical receipt persistence step: `success`.
- Historical artifact upload step: `success`.
- Final enforcement step: `success`.

The historical artifact contains two receipt files and has digest `sha256:417f8160a6bf9d7eb211da3da4ef236dbe453d930905c1cb4bf8d128cc42ddb6`.

## Validation commands

```bash
python3 scripts/check_gp10_workspace.py
python3 scripts/check_gp10_workspace_deployment.py \
  --commit "$(git rev-parse HEAD)" \
  --run-id local \
  --output /tmp/gp10-workspace-deployment-receipt.json
```

Future relevant commits may retain credential-clean validation and non-authorizing hosted-page observation. They must not require GitHub token, repository writeback, or GitHub artifact custody to preserve GP10 authority or completion state.

## Cross-repository integration

- Source authority: `StegVerse-Labs/GP10`.
- Site does not promote browser records into repository custody.
- Exported bundles must continue through GP10 validation and ingestion contracts.
- The adjacent Site-security goal is preserved in `StegVerse-Labs/GP10/docs/SESSION_ADJACENT_SITE_SECURITY_TRANSFER_2026-08-02.md` and Issue #1.
- No Publisher, wiki, Master-Records, or public Site propagation is authorized before a genuine GP10 release and destination-owned verification.

## Incomplete work and durable owners

1. Credential-clean Site validation transport — active claim `SITE-GP10-GITHUB-TOKEN-WRITEBACK-RETIREMENT-R1-20260817` on the named claim branch; release condition is exact-head validation and merge.
2. Authenticated durable service — `data/operations/gp10_workspace_tasks.json#GP10-SITE-AUTHENTICATED-SERVICE`; blocked until a named service owner, domain, scope, authentication design, privacy terms, and deployment authority exist.
3. Real field validation and commercial activation — `StegVerse-Labs/GP10/data/operations/continuation_tasks.json`.

There are no unspecified external tasks and no wallet, HIL, provider, Master Record, publication, commercial, or runtime authority assigned to this remediation.

## Session consolidation and archive conditions

The unique originating Site UX and federal-floor security requirements remain implemented, deployed, observed, receipt-bound, and transferred. The originating GP10 session remains archive-safe. The active credential-clean remediation is fully durable in the current claim registry and this handoff and does not depend on the originating chat.

## Completion metrics

Denominator: 14 required original Site repository/control deliverables.

- Original task completion: 13/14 = 93%.
- Developed-file completion: 14/14 = 100%.
- Original validation completion: 11/11 = 100%.
- Original integration completion: 6/6 = 100%.
- Propagation completion: 1/1 = 100% for transfer into canonical GP10 continuation; release propagation remains GP10-release-bound.
- Original goal activation: 10/11 = 91%.
- Originating-session consolidation: 1/1 = 100%.
- Originating-session archival readiness for this Site goal: 100%.
- Current credential-clean remediation: `CLAIMED_FOR_IMPLEMENTATION`; exact-head validation pending.
- Scaffolding or stubs: 0 in the current static Site security scope.
- Missing required files: 0.
