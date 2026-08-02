# Governed Site Measurement Mirror Handoff

## Canonical relationship

This capability-specific handoff is subordinate to `docs/SITE_MIRROR_HANDOFF.md` and does not compete with it. It preserves the complete continuation state for Site task `SITE-0001-GOVERNED-MEASUREMENT`, issue #143, and PR #146.

## Active goal

```text
goal_id: SITE-0001-GOVERNED-MEASUREMENT
originating_session_goal: measure VA Claim Guide visits and meaningful interactions without weakening StegVerse governance, PII integrity, or veteran privacy
repository: StegVerse-Labs/Site
branch: goal/governed-site-measurement
canonical_issue: 143
canonical_pull_request: 146
canonical_task: data/tasks/SITE-0001-GOVERNED-MEASUREMENT.json
```

## Authority and ownership

```text
canonical_owner: StegVerse-Labs/Site repository-machine-observer
implementation_claim: MACHINE_OWNED
validation_claim: CLAIMED_FOR_VALIDATION by .github/workflows/governed-site-measurement.yml
integration_claim: CLAIMED_FOR_INTEGRATION by PR #146
claim_created_at: 2026-08-02T07:05:58Z
claim_release_condition: PR merged and hosted validation, page binding, aggregate persistence, deployed rejection tests, expiry evidence, and authoritative handoff synchronization complete
external_tasks_allowed: false
external_session_ownership_allowed: false
```

## Preserved requirements

The measurement layer must remain first party, fail closed, aggregate only, and content blind. It must not collect or derive question text, claim facts, diagnoses, filenames, identifiers, cookies, persistent sessions, exact location, referrer histories, fingerprints, cross-site behavior, or session replay.

Measurement evidence grants no identity, admissibility, custody, publication, claim-status, filing, or activation authority.

## Authoritative files

```text
data/governed-site-measurement-policy.json
schemas/governed-site-measurement-event.schema.json
scripts/check_governed_site_measurement.py
scripts/test_governed_site_measurement_fixtures.py
tests/governed-site-measurement/valid-events.json
tests/governed-site-measurement/rejected-events.json
tests/governed-site-measurement/test-collector.js
assets/governed-site-measurement.js
api/governed-measurement.js
va-disability-claim-guide.html
.github/workflows/governed-site-measurement.yml
data/tasks/SITE-0001-GOVERNED-MEASUREMENT.json
docs/GOVERNED_SITE_MEASUREMENT.md
```

## Completed work and evidence

```text
policy and task foundation: commits 9bdfdaf39da8ed82e4ab7b2fd3a2d8b257146a7f through f2d4e31daf321681adb0559d9c9ce8a2ff4bfc89
positive and adversarial fixtures: commits e873bd0971331586951b19d9da2ce180f213e9bd, d3b37a6e4fdb17d3ede7d99a81ddcbdda9a9943f, 8b14e9ba94713cb4301ed331bf4b499a8a964044
browser client: commits 41496a30b5ae3dd13024e75105f8720515dac7f8, b4d80e1b9ff1a82dab4e48cfcaefd9041e74df20
first-party collector: cbbd328f5e004025e76f4d57ddf9f3039abc86b0
collector adversarial tests: c7c4fa8ab911ca0de5c0e50907ecbe9d8b02e1a1
CI integration: e4d7bc4037027698f9042627ac5601d5807410b1, a6a8a9ef12afe93b31bd562a4edde4ae8c68fca8, d1f213043f89aa69892b014f3b37902de0e656c7
VA Claim Guide page binding: 741beecabb2225da711df573d85b4cb8c5db0c60
machine task consolidation: f362afa0afb6d7b003b630d69311df8a66b96a27
```

Hosted evidence already inspected:

```text
Site Handoff Orchestrator run 30737149190: SUCCESS
Site Bootstrap Validate run 30737149194: SUCCESS
Governed Site Measurement run 30738651658: FAILED correctly on fixture/schema mismatch
failed job: 91471951223
foundation validation artifact: 8829991118
foundation artifact digest: sha256:281b4eda95ebff17e72520614283dc0e99f4c6c3b4b8b37e11c95dc2fd7fc92f
orchestration artifact: 8829984160
orchestration digest: sha256:c3dcdeda47f67bad17bd4578199f74ee760dd05189371b0624426d1cc538b6e7
```

The first governed-measurement run proved the gate was active by rejecting missing `policy_version` and undeclared `target` and `error_code` fields. Those defects were corrected in later commits.

## Current classification

```text
policy: COMPLETE AND PREVIOUSLY VALIDATED
schema: COMPLETE AND PREVIOUSLY VALIDATED
fixtures: IMPLEMENTED; CORRECTED HOSTED VALIDATION PENDING
browser client: IMPLEMENTED; PAGE BOUND; HOSTED VALIDATION PENDING
collector: IMPLEMENTED; UNIT TEST INSTALLED; HOSTED VALIDATION PENDING
aggregate projection contract: IMPLEMENTED IN COLLECTOR
aggregate persistence service: BLOCKED
runtime deployment: BLOCKED
raw-event expiry evidence: MISSING
cross-repository propagation: BLOCKED UNTIL SITE ACTIVATION
```

## Exact incomplete tasks

1. Observe the next completed run of `.github/workflows/governed-site-measurement.yml` for commit `d1f213043f89aa69892b014f3b37902de0e656c7` or later. Required result: policy, fixtures, collector adversarial tests, browser client, and page binding all PASS.
2. Install or identify the canonical aggregate-only persistence service consumed through `GOVERNED_MEASUREMENT_AGGREGATE_URL`. Owner: Site deployment control plane. Release condition: service accepts only aggregate projections and returns a durable receipt.
3. Deploy `api/governed-measurement.js`. Owner: Site deployment automation. Release condition: direct runtime observation of approved-event acceptance and prohibited-field rejection.
4. Persist runtime receipts under `data/governed-site-measurement/receipts/` for accepted event, rejected PII, rejected unknown field, rejected content capture, aggregate update, and raw-event expiry.
5. Update `data/tasks/SITE-0001-GOVERNED-MEASUREMENT.json` after each evidence transition.
6. Merge PR #146 only after required checks pass and no conflicting Site ownership exists.
7. After Site activation, install source and consumer contracts for `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki`. Propagation before verified Site activation is prohibited.

## Automation

`.github/workflows/governed-site-measurement.yml` is the canonical validation owner. It triggers on the policy, schema, task, collector, client, guide page, handoff, tests, and workflow itself. It fails closed on schema drift, fixture acceptance errors, collector privacy failures, identity/content-capture source terms, and missing or duplicate page binding.

`data/tasks/SITE-0001-GOVERNED-MEASUREMENT.json` is the persistent execution and collision-control state consumed by the repository task observer.

## Validation commands

```bash
python scripts/check_governed_site_measurement.py
python scripts/test_governed_site_measurement_fixtures.py
node tests/governed-site-measurement/test-collector.js
python scripts/validate_application.py
python scripts/site_handoff_orchestrator.py
```

## Cross-repository dependencies

```text
source authority: StegVerse-Labs/Site
publication consumer after activation: GCAT-BCAT-Engine/Publisher
admissibility consumer after activation: StegVerse-Labs/admissibility-wiki
guardian consumer after activation: StegVerse-002/stegguardian-wiki
master-records: no raw visitor-event custody is authorized; only governed aggregate receipts may be considered after a separate custody contract
```

## Session consolidation

```text
MERGED INTO: StegVerse-Labs/Site issue #143, PR #146, data/tasks/SITE-0001-GOVERNED-MEASUREMENT.json, and this handoff
transferred session goals: privacy-preserving visit measurement; interaction measurement; PII and claim-content prohibition; first-party collector; fail-closed schema; machine-owned continuation; no external tasks; aggregate-only evidence; authority non-escalation; page binding; CI validation; deployment and propagation gates
unique chat-only requirements remaining: none
```

The originating session may be archived once this file, the task record, issue, PR, and workflow preserve the state and no session-specific mutation remains underway. Runtime activation work continues repository-natively and does not require the originating chat history.

## Archive conditions

```text
session consolidation: COMPLETE after this handoff commit
repository goal activation: NOT COMPLETE
session archival does not imply repository activation
all unresolved work has a named repository owner and machine-observable release condition
```

## Percentages

```text
developed files: 15/16 = 94%
validation: 5/8 = 63% pending corrected hosted run and runtime evidence
integration: 5/7 = 71% pending aggregate service and deployment
propagation: 0/3 = 0% correctly blocked
repository goal activation: 56%
session consolidation: 5/5 = 100%
```
