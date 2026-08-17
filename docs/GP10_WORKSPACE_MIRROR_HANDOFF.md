# GP10 Workspace Mirror Handoff

Status: ACTIVE PROJECT — SITE WORKSTREAM VALIDATED / CREDENTIAL-CLEAN REMEDIATION IN PROGRESS
Updated: 2026-08-17
Goal ID: `GP10-SITE-SECURE-GUIDED-WORKSPACE-001`
Originating session goal: provide a simplified, logically narrowing GP10 evidence and commercial-posture workspace, a beginner examples surface, and browser security controls that treat applicable federal cybersecurity requirements as a minimum baseline rather than a target ceiling.
Repository: `StegVerse-Labs/Site`
Canonical branch: `main`
Active remediation branch: `chore/site-gp10-token-writeback-retirement-20260817`

## Canonical ownership

- GP10 domain logic, schemas, evidence custody, ingestion, runtime validation, and commercial governance remain canonical in `StegVerse-Labs/GP10`.
- Canonical GP10 continuation is `StegVerse-Labs/GP10/GP10_MIRROR_HANDOFF.md` and its repository-native task/claim registries.
- Site owns the unlisted browser workspace, examples surface, browser-side security controls, Site isolation verification, and non-authorizing hosted-page observation.
- Site is not the source of truth for GP10 evidence, approval, custody, runtime authority, or commercial authority.
- Credential authority is TV/TVC. No NON-TV/TVC project/provider secret or token is permitted as a required GP10 Site validation dependency.

MERGED INTO: `StegVerse-Labs/Site/docs/GP10_WORKSPACE_MIRROR_HANDOFF.md`

## Authoritative Site files

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
- `docs/receipts/gp10-site/` (historical immutable receipts only)

## Completed historical Site claims

### `GP10-SITE-SECURITY-HARDENING`

State: COMPLETE / RELEASED_IMPLEMENTATION_CLAIM.

The browser security controls, static validation, adaptive UX, examples synchronization, authority denial, and public-navigation isolation remain complete.

### `GP10-SITE-DEPLOYMENT-OBSERVATION`

State: COMPLETE / RELEASED_MACHINE_VALIDATION_CLAIM.

Historical evidence remains immutable:

```text
tested_commit: 80fbf35d2a824f689050c7ec69e579c2ddf8f196
workflow_run: 30780334497
job: 91583581262
artifact: 8843410533
artifact_digest: sha256:417f8160a6bf9d7eb211da3da4ef236dbe453d930905c1cb4bf8d128cc42ddb6
receipt_commit: 018a58f5c60434d51ea3762e2bba119a94eaeaac
workspace_sha256: 2a151a37ebfa9937f64f67b285151f4895b81e875076226e4fdcba18215b1f48
examples_sha256: 502d385f3c534365e5488f10b8011efb988a5634734df5b086177c7d3133701f
exact_byte_match: true
result: PASS
```

Those historical GitHub artifact/writeback mechanics are evidence of a past observation, not continuing custody or authority requirements.

## Active credential-clean remediation claim

```text
claim_id: SITE-GP10-GITHUB-TOKEN-WRITEBACK-RETIREMENT-20260817
task_id: SITE-GP10-GITHUB-TOKEN-WRITEBACK-RETIREMENT-20260817
branch: chore/site-gp10-token-writeback-retirement-20260817
role: IMPLEMENTATION_VALIDATION
state: CLAIMED_FOR_IMPLEMENTATION
parent_cleanup: Site#268
credential_authority: TV/TVC
github_runtime_control_plane_authority: NONE
execution_authority_effect: NONE
custody_authority_effect: NONE
```

Installed transition in `.github/workflows/gp10-workspace-security.yml`:

```text
permissions: {}
actions/checkout: REMOVED
actions/setup-python: REMOVED
actions/upload-artifact: REMOVED
contents: write: REMOVED
repository git commit/push writeback: REMOVED
GH_TOKEN/GITHUB_TOKEN consumption: REMOVED
credential-bearing environment refusal: INSTALLED
anonymous exact-SHA public Site source fetch: INSTALLED
preinstalled Python validation: INSTALLED
check_gp10_workspace.py: RETAINED
check_gp10_workspace_deployment.py: RETAINED for main/non-PR observation
historical committed receipts: RETAINED IMMUTABLY
new GitHub artifact/issue/repository custody: NONE
```

Pull requests perform source/security validation and explicitly record deployment observation as blocked because a PR head is not deployed `main`. Main/non-PR runs may observe hosted pages, but the observation remains ephemeral workflow-log evidence and grants no execution, release, publication, custody, or commercial authority.

Release requires exact-head credential refusal PASS, anonymous exact-source fetch PASS, static checker PASS, Site claim/orchestration/bootstrap checks PASS, StegFin projection PASS, workflow authority-boundary PASS, merge, claim release, and parent cost-containment handoff reconciliation.

## Preserved interaction requirements

1. Show one logical decision at a time.
2. Hide fields that do not follow from prior answers.
3. Skip economics and threshold pages when a hard-stop condition controls the result.
4. Preserve missing information as missing; never synthesize evidence, prices, thresholds, or approval.
5. Maintain a separate beginner examples page with safe synthetic files and plain-language governance explanations.
6. Keep both pages unlisted and marked `noindex`, `nofollow`, and `noarchive`.
7. Preserve `execution_authority: false` and browser-local uncustodied state.
8. Site remains an interface and never becomes canonical GP10 evidence or authority.

## Implemented security controls

- same-origin-only script execution through document CSP;
- denial of plugins, mutable base URI, remote form submission, frames, media, workers, and external connections;
- `no-referrer` policy;
- 15-minute inactivity lock and five-minute background lock;
- file-input clearing on lock and page hide;
- GP10-namespaced local-data clearing;
- SHA-256 browser integrity receipts over local candidate/evidence/review state;
- explicit receipt limits: integrity does not prove truth, identity, authority, custody, approval, or execution authority;
- fail-closed static verification of security, UX, examples synchronization, authority denial, and navigation isolation;
- exact-byte hosted-page observation remains available without repository writeback or GitHub-hosted custody.

The complete control contract remains in `docs/GP10_WORKSPACE_SECURITY_BASELINE.md`. This is not a federal compliance certification.

## Validation commands

```bash
python3 scripts/check_gp10_workspace.py
python3 scripts/check_gp10_workspace_deployment.py \
  --commit "$(git rev-parse HEAD)" \
  --run-id local \
  --output /tmp/gp10-workspace-deployment-receipt.json
```

Hosted validation is source/test observation only. It may not become production/runtime/control-plane authority and may not export TV/TVC protected values.

## Cross-repository integration

- Source authority: `StegVerse-Labs/GP10`.
- Site does not promote browser records into repository custody.
- Exported bundles continue through GP10 validation and ingestion contracts.
- The adjacent Site-security goal remains preserved in `StegVerse-Labs/GP10/docs/SESSION_ADJACENT_SITE_SECURITY_TRANSFER_2026-08-02.md` and GP10 Issue #1.
- No Publisher, wiki, Master-Records, or public Site propagation is authorized before a genuine GP10 release and destination-owned verification.

## Incomplete work and durable owners

1. `GP10-SITE-GITHUB-TOKEN-WRITEBACK-RETIREMENT-20260817` — active on the named Site branch; released only after exact-head validation and merge.
2. Authenticated durable service — `data/operations/gp10_workspace_tasks.json#GP10-SITE-AUTHENTICATED-SERVICE`; BLOCKED until a named StegVerse service owner, approved domain/scope, authentication design, privacy terms, deployment authority, and security controls exist.
3. Real field validation and commercial activation — owned by `StegVerse-Labs/GP10/data/operations/continuation_tasks.json`.

There are no unspecified external tasks. No wallet, provider, HIL, Master Record, commercial, or execution authority is assigned to this Site remediation.

## Session consolidation and archive conditions

The originating GP10 Site session remains archive-safe: its unique UX/security requirements and historical deployment evidence are durable. The current credential-clean remediation is a separate Site #268 workstream and is fully described by this handoff, `data/operations/gp10_workspace_tasks.json`, and `data/session-work-claims.json`.

## Completion metrics

Original GP10 Site denominator: 14 required repository/control deliverables.

- Original task completion: 13/14 = 93%.
- Developed-file completion: 14/14 = 100%.
- Original validation completion: 11/11 = 100%.
- Original integration completion: 6/6 = 100%.
- Original goal activation: 10/11 = 91%.
- Originating-session consolidation: 1/1 = 100%.
- Current credential-clean remediation: implemented, exact-head validation pending.
- Scaffolding or stubs in current static Site security scope: 0.
- Missing required files: 0.
