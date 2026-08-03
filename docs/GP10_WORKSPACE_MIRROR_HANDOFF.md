# GP10 Workspace Mirror Handoff

Status: ACTIVE PROJECT — CANONICAL SITE CONTINUATION
Updated: 2026-08-02
Goal ID: `GP10-SITE-SECURE-GUIDED-WORKSPACE-001`
Originating session goal: provide a simplified, logically narrowing GP10 evidence and commercial-posture workspace, a beginner examples surface, and browser security controls that treat applicable federal cybersecurity requirements as a minimum baseline rather than a target ceiling.
Repository: `StegVerse-Labs/Site`
Branch: `main`

## Canonical ownership

- GP10 domain logic, schemas, evidence custody, ingestion, runtime validation, and commercial governance remain canonical in `StegVerse-Labs/GP10`.
- This repository owns the unlisted browser workspace, examples surface, browser-side security controls, Site isolation verification, hosted-page observation, and committed Site validation receipts.
- Canonical GP10 continuation: `StegVerse-Labs/GP10/GP10_MIRROR_HANDOFF.md`.
- Canonical Site continuation: this file and `data/operations/gp10_workspace_tasks.json`.

MERGED INTO: `StegVerse-Labs/Site/docs/GP10_WORKSPACE_MIRROR_HANDOFF.md`

The originating session has released its Site implementation and observation claims. Remaining runtime observation and service-boundary tasks are repository-owned and do not require the conversation.

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
- `docs/receipts/gp10-site/`
- `docs/GP10_WORKSPACE_HANDOFF.md` (legacy redirect)

## Claims and collision controls

### Released implementation claim

- Task: `GP10-SITE-SECURITY-HARDENING`
- Claimant: originating-session Site browser-security lane
- Role: `RELEASED_IMPLEMENTATION_CLAIM`
- Created: `2026-08-02T19:30:00-05:00`
- Released: `2026-08-02T20:00:00-05:00`
- Release evidence: committed security baseline, security module, page policies, checker enforcement, workflow, task registry, and this handoff
- Collision boundary preserved: no GP10 repository validator, runtime workflow, receipt, schema, or claimed runtime surface was modified through this Site claim

### Machine-owned deployment validation

- Task: `GP10-SITE-DEPLOYMENT-OBSERVATION`
- Owner: `StegVerse-Labs/Site:.github/workflows/gp10-workspace-security.yml`
- Role: `MACHINE_OWNED`
- State: `RETRY` until a committed PASS receipt is inspected
- Registry: `data/operations/gp10_workspace_tasks.json`
- Release condition: `docs/receipts/gp10-site/deployment-<tested-commit>.json` records PASS and proves exact hosted-byte equality plus all required markers
- Failure behavior: FAILED, missing, artifact-only, or stale evidence cannot satisfy the task
- Claim expiration: PASS completes the task; FAILED renews it only with a deterministic blocker

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
- repository-native preservation of both PASS and FAILED security/deployment receipts using `[skip ci]` recursion protection.

The complete control contract and static-host limitations are in `docs/GP10_WORKSPACE_SECURITY_BASELINE.md`. This is not a federal compliance certification.

## Implementation evidence

- `c26119235f6a7d2c5d81aaa2f7808611ab8ec948` — canonical Site mirror handoff created.
- `ced107e0633ba759b7e83850a7e0c87d87b48f68` — security baseline committed.
- `1cec5f979b2d7dacffc77754a375097097a0d8b1` — browser security module committed.
- `89f39a7b8d5ce80a04e998bfacac85c546b4ea92` — workspace CSP and security module binding.
- `ca99c9be6c3afc2d1bff924adb06a718577c4f05` — examples CSP and security module binding.
- `902d6760a10a0ec8c51f7b25c6f48c083106c5cb` — fail-closed checker extended.
- `8ddae3a3d82a91294d7bf14df1f49bfa5511ed50` — repository-native security workflow.
- `68ea949803f72a4cdef9bde0eff53b3da9927ac9` — exact-byte deployment observer.
- `e7cf9a12183ebad73416c8884cec11e82b9843b8` — hosted observation integrated into workflow.
- `c6c92a7030423356cc667e57e32373586ab16705` — deployment task assigned to machine ownership.
- `d5ad115ad4705499343540303b670b49bdf838ba` — deployment observer continuation addendum.
- `64f9c33a8f5c05ec84b3d7ff80b115eb8780058c` — workflow made self-preserving for PASS and FAILED receipts.
- `80fbf35d2a824f689050c7ec69e579c2ddf8f196` — canonical task bound to committed receipt evidence.

## Validation

Static command:

```bash
python3 scripts/check_gp10_workspace.py
```

Deployment command:

```bash
python3 scripts/check_gp10_workspace_deployment.py \
  --commit "$(git rev-parse HEAD)" \
  --run-id local \
  --output validation/gp10-workspace-deployment-receipt.json
```

Hosted workflow:

- `.github/workflows/gp10-workspace-security.yml`
- trigger: relevant push, pull request, or manual dispatch
- transient outputs: `validation/gp10-workspace-security-receipt.txt` and `validation/gp10-workspace-deployment-receipt.json`
- durable outputs: `docs/receipts/gp10-site/security-<tested-commit>.txt` and `docs/receipts/gp10-site/deployment-<tested-commit>.json`
- artifact: `gp10-workspace-security-<tested-commit>`
- result semantics: PASS only after static validation and deployment observation both succeed; receipts are preserved even when either fails

No hosted PASS is asserted until a committed PASS receipt is inspected.

## Cross-repository integration

- Source authority: `StegVerse-Labs/GP10`.
- Site does not promote browser records into repository custody.
- Exported bundles must continue through GP10 validation and ingestion contracts.
- The adjacent Site-security goal is preserved in `StegVerse-Labs/GP10/docs/SESSION_ADJACENT_SITE_SECURITY_TRANSFER_2026-08-02.md` and Issue #1.
- No Publisher, wiki, Master-Records, or public Site propagation is authorized before a genuine GP10 release and destination-owned verification.

## Incomplete work and durable owners

1. Hosted deployment observation — owner and release condition: `data/operations/gp10_workspace_tasks.json#GP10-SITE-DEPLOYMENT-OBSERVATION`.
2. Authenticated durable service — owner and release condition: `data/operations/gp10_workspace_tasks.json#GP10-SITE-AUTHENTICATED-SERVICE`.
3. Real field validation and commercial activation — owner: `StegVerse-Labs/GP10/data/operations/continuation_tasks.json`.

There are no unspecified external tasks.

## Session consolidation and archive conditions

The unique Site UX and federal-floor security requirements are committed here, in the security baseline, task registry, automated workflow, committed receipt path, GP10 transfer record, and Issue #1. Remaining work has named repository owners, collision boundaries, deterministic evidence, and machine-observable release conditions.

No Site-specific project decision, requirement, owner, blocker, evidence path, or next action depends on the originating conversation. Archiving that session does not impair execution.

## Completion metrics

Denominator: 14 required Site repository/control deliverables.

- Task completion: 12/14 = 86%.
- Developed-file completion: 14/14 = 100%.
- Validation completion: 9/11 = 82% (hosted execution and committed PASS inspection pending).
- Integration completion: 6/6 = 100%.
- Propagation completion: 1/1 = 100% for transfer into canonical GP10 continuation; release propagation remains GP10-release-bound.
- Goal activation: 9/11 = 82%.
- Session consolidation: 1/1 = 100%.
- Originating-session archival readiness for this Site goal: 100%.
- Scaffolding or stubs: 0 in the current static Site security scope.
- Missing required files: 0.
