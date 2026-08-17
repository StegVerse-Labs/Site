# GP10 Workspace Mirror Handoff

Status: ACTIVE PROJECT — SITE WORKSTREAM VALIDATED / CREDENTIAL-CLEAN TRANSPORT RELEASED
Updated: 2026-08-17
Goal ID: `GP10-SITE-SECURE-GUIDED-WORKSPACE-001`
Originating session goal: provide a simplified, logically narrowing GP10 evidence and commercial-posture workspace, a beginner examples surface, and browser security controls that treat applicable federal cybersecurity requirements as a minimum baseline rather than a target ceiling.
Repository: `StegVerse-Labs/Site`
Canonical branch: `main`

## Canonical ownership

- GP10 domain logic, schemas, evidence custody, ingestion, runtime validation, and commercial governance remain canonical in `StegVerse-Labs/GP10`.
- Site owns the unlisted browser workspace, examples surface, browser-side security controls, Site isolation verification, and non-authorizing hosted-page observation.
- Canonical GP10 continuation: `StegVerse-Labs/GP10/GP10_MIRROR_HANDOFF.md`.
- Canonical Site continuation: this file and `data/operations/gp10_workspace_tasks.json`.
- Site is not the source of truth for GP10 evidence, approval, custody, runtime authority, or commercial authority.
- Credential authority is TV/TVC. No NON-TV/TVC project/provider secret or token is a required GP10 Site validation dependency.

MERGED INTO: `StegVerse-Labs/Site/docs/GP10_WORKSPACE_MIRROR_HANDOFF.md`

The originating GP10 Site session remains released. The credential-clean transport remediation was completed under Site #268 without reopening GP10 product authority.

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

State: `COMPLETE` / `RELEASED_IMPLEMENTATION_CLAIM`.

### `GP10-SITE-DEPLOYMENT-OBSERVATION`

State: `COMPLETE` / `RELEASED_MACHINE_VALIDATION_CLAIM`.

Historical evidence:

```text
tested_commit: 80fbf35d2a824f689050c7ec69e579c2ddf8f196
workflow_run: 30780334497
job: 91583581262
artifact: 8843410533
artifact_digest: sha256:417f8160a6bf9d7eb211da3da4ef236dbe453d930905c1cb4bf8d128cc42ddb6
receipt_commit: 018a58f5c60434d51ea3762e2bba119a94eaeaac
workspace_sha256: 2a151a37ebfa9937f64f67b285151f4895b81e875076226e4fdcba18215b1f48
examples_sha256: 502d385f3c534365e5488f10b8011efb988a5634734df5b086177c7d3133701f
result: PASS
```

Those artifact/writeback mechanics are immutable historical evidence, not continuing custody requirements.

### `SITE-GP10-GITHUB-TOKEN-WRITEBACK-RETIREMENT-R1-20260817`

```text
former_state: CLAIMED_FOR_IMPLEMENTATION
state: MERGED_INTO_CANONICAL_WORKSTREAM
role: RELEASED_INTEGRATION
PR: #367
final_head: 850af41a7acf31bb32d1a24e4d7b838916129fa1
merge: 96423f16cf6d3f440630d322cc5d5c196e4fa672
claim_release_commit: 2ba971bbde99f6eca43a4087bf89d7deb4c9b9f6
task_registry_release_commit: 5fb78008a98108aed686a8c61e657a21970c01e8
GP10 workspace security: 32054495179 SUCCESS
GP10 job: 95461396822 SUCCESS
Site Handoff Orchestrator: 32054495369 SUCCESS
Ecosystem Heartbeat Orchestration: 32054495300 SUCCESS
Site Bootstrap Validate: 32054495168 SUCCESS
Bootstrap job: 95461397278 SUCCESS
Check StegFin Phone Projection: 32054495265 SUCCESS
authority_effect: NONE
runtime_activation_effect: NONE
custody_authority_effect: NONE
```

Released workflow boundary:

```text
permissions: {}
credential-bearing environment refusal: PASS
anonymous exact-SHA public Site fetch: PASS
preinstalled Python: PASS
actions/checkout: REMOVED
actions/setup-python: REMOVED
actions/upload-artifact: REMOVED
contents write: REMOVED
repository commit/push writeback: REMOVED
GitHub token consumption: REMOVED
check_gp10_workspace.py: PASS
check_gp10_workspace_deployment.py: RETAINED for main/non-PR observation
PR deployment observation: BLOCKED_PR_NOT_DEPLOYED_MAIN
historical committed receipts: RETAINED IMMUTABLY
future GitHub artifact/repository custody: NONE
GP10_VALIDATION_ONLY: PASS
GP10_REPOSITORY_WRITEBACK: NONE
GP10_ARTIFACT_CUSTODY: NONE
GP10_RUNTIME_CONTROL_PLANE_AUTHORITY: NONE
```

Bootstrap evidence also proved `SESSION_WORK_CLAIMS_PASS`, `SITE_HANDOFF_ORCHESTRATION_PASS`, `ECOSYSTEM_HEARTBEAT_ORCHESTRATION_PASS`, canonical Site application PASS, ST-017 sandbox PASS, workflow inventory `101 / canonical 3 / migration-required 98 / placeholders 0`, and StegFin `wallet_review=USER_ONLY`, `signing_broadcast=USER_ONLY`, `hosted_runtime_authority=NONE`.

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
- SHA-256 browser integrity receipts over local candidate/evidence/review state;
- explicit receipt limits: integrity does not prove truth, identity, authority, custody, approval, or execution authority;
- fail-closed static verification of policy, adaptive UX, examples synchronization, authority denial, and public-navigation isolation;
- exact-byte hosted deployment observation remains available without GitHub writeback or artifact custody.

The complete control contract and static-host limitations are in `docs/GP10_WORKSPACE_SECURITY_BASELINE.md`. This is not a federal compliance certification.

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
- Exported bundles continue through GP10 validation and ingestion contracts.
- The adjacent Site-security goal remains preserved in `StegVerse-Labs/GP10/docs/SESSION_ADJACENT_SITE_SECURITY_TRANSFER_2026-08-02.md` and GP10 Issue #1.
- No Publisher, wiki, Master-Records, or public Site propagation is authorized before a genuine GP10 release and destination-owned verification.

## Incomplete work and durable owners

1. Authenticated durable service — `data/operations/gp10_workspace_tasks.json#GP10-SITE-AUTHENTICATED-SERVICE`; BLOCKED until a named StegVerse service owner, approved domain/scope, authentication design, privacy terms, deployment authority, and security controls exist.
2. Real field validation and commercial activation — `StegVerse-Labs/GP10/data/operations/continuation_tasks.json`.

There are no unspecified external tasks. No wallet, HIL, provider, Master Record, publication, commercial, or runtime authority is assigned to the released Site remediation.

## Session consolidation and archive conditions

The originating GP10 Site session remains archive-safe: unique UX/security requirements and historical deployment evidence are durable. The Site #268 credential-clean remediation is complete and transferred into this handoff, `data/operations/gp10_workspace_tasks.json`, and `data/session-work-claims.json`.

## Completion metrics

Original GP10 Site denominator: 14 required repository/control deliverables.

- Original task completion: 13/14 = 93%.
- Developed-file completion: 14/14 = 100%.
- Original validation completion: 11/11 = 100%.
- Original integration completion: 6/6 = 100%.
- Original goal activation: 10/11 = 91%.
- Originating-session consolidation: 1/1 = 100%.
- Credential-clean Site #268 remediation: COMPLETE / RELEASED.
- Scaffolding or stubs in current static Site security scope: 0.
- Missing required files: 0.
