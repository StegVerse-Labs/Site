# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: fully functional governed Ecosystem Chat request-response, provider, custody, comparison, and cross-entry usage path
Primary surface: ecosystem-chat.html
Usage and role surface: ecosystem-usage.html
Operational projection: governed-transitions.html
Site mode: GOVERNED_GATEWAY_WITH_LOCAL_FALLBACK
Gateway implementation: installed in StegVerse-org/LLM-adapter
Custody implementation: installed in master-records/orchestration
Public deployments and authenticated round trip: verification pending
Workflow target: exactly two operational workflows
Result: CROSS_REPOSITORY_IMPLEMENTATION_INSTALLED_LIVE_VALIDATION_PENDING
```

## Active workflows

```text
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

No workflow was added.

## Installed Site surfaces

```text
ecosystem-chat.html
ecosystem-usage.html
governed-transitions.html
assets/ecosystem-chat.js
assets/ecosystem-chat-transition-identity.js
assets/ecosystem-chat-gateway-health.js
assets/ecosystem-usage-ledger.js
assets/governed-transitions-live-custody.js
data/entry-point-roles.json
data/usage-session-fixture.json
scripts/check_ecosystem_chat_application.py
scripts/check_ecosystem_chat_boundary.py
scripts/check_ecosystem_usage_ledger.py
scripts/check_ecosystem_chat_gateway_activation.py
scripts/check_governed_transition_observatory.py
```

The shared usage surface preserves session and transition identity, origin and participating entry points, measurement owners, receipt references, evidence-classified metrics, and deduplication by `metric_owner + measurement_id`.

## Authority boundary

```text
Site display != execution.
Usage event != authority.
Usage event != admissibility.
Entry-point acceptance != authority.
Translation != admissibility.
Provider output != authority.
Provider receipt != final response receipt.
Final response receipt != Master-Records custody.
Configured fixture values != live measurements.
Usage presentation does not alter provider output or transition hashes.
RECORDED requires authenticated custody evidence and reconstructability PASS.
Site does not execute or mutate external repositories.
```

## Observed validation failures and bounded repairs

```text
Workflow: Site Bootstrap Validate
Run: 29179673207
Commit: c19e0015c24ba2f5ccd39eda6c97477d78e2a92a
Failure: stale preview-only handoff assertion
Repair: 181668077ecd3e8d686374758de051f7ba76c07f

Workflow: Site Task Runner
Run: 29191451576
Commit: 1d64d9c16b91cea0b9fbb56874193caf491d30ff
Failure: substring-count bug in hero button validation
Repair: 62d6c88df9e126978b477ac14913a9ef4dc375c0

Workflow: Site Task Runner
Run: 29192461329
Commit: 82d485c224ba9590aa05c53ff4b008b26978095f
Failure: stale continuation-panel identifier assertion
Repair: ba8e68d4906654698a736c02475077d5bef40921

Workflow: Site Task Runner
Run: 29197743889
Commit: ca3914d4a9fca0f669a275801c32c5169c34db2f
Job: run-site-task
Failing command: python scripts/check_ecosystem_chat_boundary.py
Failure class: obsolete HPS visualization assertion
Observed blocker: missing fixtures/ecosystem-chat/hps-visualization.example.json; current page and renderer no longer declare the HPS preview surface
Repair: 49373bae2f92521df052397a033212d3e9d982f9
Repair scope: removed only the obsolete verify_hps_visualization validator and invocation
Authority effect: NONE
State change authorized by repair: false
Diagnostic artifact: site-task-diagnostic-29197743889-1
Artifact ID: 8261471385
Artifact digest: sha256:f7212ac35e4d945e26be053b8664a6a38673ab32fb7d958d3621ad95ed673c34
```

The repair aligns validation with the current declared Site surface. It does not add, restore, or remove user-facing HPS functionality; does not deploy; does not configure credentials; and does not alter authority, release, custody, or provider posture.

## Next task

```text
1. Verify current-main Site Task Runner and Site Bootstrap Validate on commit 49373bae2f92521df052397a033212d3e9d982f9 or a documented successor.
2. Preserve passing Site validation and task diagnostic receipts.
3. Link Ecosystem Usage Ledger prominently from Ecosystem Chat and primary navigation only after current-main validation is green.
4. Ingest live gateway usage events instead of fixture fallback when the authenticated transport prerequisite is available.
5. Render governed-vs-recursive paired output and delta bars.
6. Add session filtering, export, and receipt navigation.
7. Deploy gateway and custody production blueprints only with explicit deployment authority.
8. Configure credentials only through authorized secret-management paths.
9. Verify one public provider-used or explicit deterministic-fallback response and the same transition reaching RECORDED custody.
10. Run the orchestration live round-trip verifier before activation claims.
```

## Remaining files or modules

```text
StegVerse-Labs/Site
  -> prominent Ecosystem Usage Ledger navigation
  -> live gateway usage ingestion
  -> governed-vs-recursive paired output and delta bars
  -> session filtering, export, and receipt navigation

StegVerse-org/LLM-adapter
  -> provider usage emission during live lifecycle
  -> authenticated session-usage retrieval

StegVerse-org/core-node-runtime-demo
  -> runtime usage emission during governed execution

master-records
  -> custody usage events, deduplication index, and session reconstruction pointers
```

## Release posture

Role descriptions, shared usage display, transition prepend rendering, local cross-entry aggregation, deduplication, fixtures, and validation are installed. Live event transport, Master-Records custody, public endpoint verification, current-main green evidence, and an observed identity-preserving RECORDED transition remain activation gates. No deployment, release, merge, or tag is authorized by this handoff.

## Archive readiness

This handoff preserves the current provider, gateway, custody, cross-entry role, usage-ledger, validation, repair, authority-boundary, and continuation state. Earlier conversation context is not required.
