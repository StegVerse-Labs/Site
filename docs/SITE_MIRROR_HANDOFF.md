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
data/ecosystem-usage-config.json
scripts/check_ecosystem_chat_application.py
scripts/check_ecosystem_chat_boundary.py
scripts/check_ecosystem_usage_ledger.py
scripts/check_ecosystem_chat_gateway_activation.py
scripts/check_governed_transition_observatory.py
```

The shared usage surface preserves session and transition identity, origin and participating entry points, measurement owners, receipt references, evidence-classified metrics, and deduplication by `metric_owner + measurement_id`.

## Usage session retrieval and continuation

Installed behavior:

```text
?session_id=<canonical-session-id>
-> configured authenticated usage API when available
-> synchronized local ledger fallback
-> configured fixture fallback only when allowed
-> fail closed when the requested session cannot be resolved
```

`data/ecosystem-usage-config.json` now declares the retrieval boundary. A configured API must be same-origin or HTTPS, and a returned payload must preserve the requested session identity.

The page now includes:

```text
session filter and direct session loading
JSON export of the active deduplicated session
receipt links into governed-transitions.html
prominent return path to Ecosystem Chat
explicit LIVE_USAGE_API / SYNCHRONIZED_LOCAL_LEDGER / CONFIGURED_FIXTURE_FALLBACK source labels
```

Browser synchronization continues through:

```text
localStorage key: stegverse.transitionUsageEvents.v1
```

Exported JSON preserves the active session id, source classification, unique events, lineage, metric ownership, evidence classes, and receipt references. Export is presentation and portability only; it is not Master-Records custody.

## Authority boundary

```text
Site display != execution.
Usage retrieval != authority.
Usage event != authority.
Usage display != admissibility.
Entry-point acceptance != authority.
Translation != admissibility.
Provider output != authority.
Provider receipt != final response receipt.
Final response receipt != Master-Records custody.
Configured fixture values != live measurements.
JSON export != custody.
Usage presentation does not alter provider output or transition hashes.
Site does not execute or mutate repositories.
Site does not execute or mutate external repositories.
RECORDED requires the authenticated custody service receipt.
RECORDED requires authenticated custody evidence and reconstructability PASS.
No release tag is authorized.
```

## Validation surface

The existing Site application validation invokes:

```text
python scripts/check_ecosystem_chat_application.py
  -> python scripts/check_ecosystem_usage_ledger.py
```

The usage checker now verifies:

```text
public role and usage surface
one session identity
metric-owner plus measurement-id deduplication
valid evidence classes and null UNAVAILABLE values
transition usage prepend
session filter and direct loading
same-origin or HTTPS live API restriction
explicit live, synchronized-local, and fixture source labels
JSON export
receipt navigation
non-authority retrieval and display posture
```

## Observed validation failures and bounded repairs

```text
Workflow: Site Bootstrap Validate
Run: 29179673207
Failure: stale preview-only handoff assertion
Repair: 181668077ecd3e8d686374758de051f7ba76c07f

Workflow: Site Task Runner
Run: 29191451576
Failure: substring-count bug in hero button validation
Repair: 62d6c88df9e126978b477ac14913a9ef4dc375c0

Workflow: Site Task Runner
Run: 29192461329
Failure: stale continuation-panel identifier assertion
Repair: ba8e68d4906654698a736c02475077d5bef40921

Workflow: Site Task Runner
Run: 29197743889
Commit: ca3914d4a9fca0f669a275801c32c5169c34db2f
Failing command: python scripts/check_ecosystem_chat_boundary.py
Failure: obsolete HPS visualization assertion
Repair: 49373bae2f92521df052397a033212d3e9d982f9
Authority effect: NONE

Workflow: Site Bootstrap Validate
Run: 29197932988
Commit: 4e0239370aa85794af106039fddb65bd35c035fb
Job: bootstrap-validate
Failing command: python scripts/check_site_media_pipeline_mirror.py
Failure: canonical handoff safety-assertion text drift
Missing assertions: Site does not execute or mutate repositories.; RECORDED requires the authenticated custody service receipt.; No release tag is authorized.
Repair scope: restored the three exact canonical assertions without changing Site behavior, deployment, credentials, custody, provider, workflow, or release posture
Authority effect: NONE
Validation artifact: site-application-validation-result
Artifact ID: 8261521156
Artifact digest: sha256:0f9591f14bb2937f8c12d9ca83603efca51e541c21dd0e902eb77e52bb6f389a
```

The repairs align validation with the current declared Site surface and preserve canonical safety language. They do not change user-facing authority, release, custody, deployment, credentials, workflow inventory, or provider posture.

## Next task

```text
1. Verify current-main Site Task Runner and Site Bootstrap Validate on the canonical-safety repair commit or a documented successor.
2. Preserve passing Site validation and task diagnostic receipts.
3. Add the direct Usage Ledger link inside ecosystem-chat.html primary navigation after current-main validation is green.
4. Connect usage_api_base to an authenticated deployed session-usage service.
5. Render governed-vs-recursive paired output and delta bars.
6. Deploy gateway and custody production blueprints only with explicit deployment authority.
7. Verify one public provider-used or deterministic-fallback response and the same transition reaching RECORDED custody.
```

## Remaining files or modules

```text
StegVerse-Labs/Site
  -> direct Usage Ledger link inside ecosystem-chat.html navigation
  -> deployed authenticated live usage retrieval
  -> governed-vs-recursive paired output and delta bars
  -> public retrieval and receipt-navigation verification

StegVerse-org/LLM-adapter
  -> provider usage emission during live lifecycle
  -> authenticated session-usage retrieval

StegVerse-org/core-node-runtime-demo
  -> runtime usage emission during governed execution

master-records
  -> custody usage events, deduplication index, and session reconstruction pointers
```

## Release posture

Role descriptions, shared usage display, transition prepend rendering, local cross-entry aggregation, deduplication, bounded live retrieval configuration, session filtering, JSON export, receipt navigation, fixtures, and validation are installed. Live event transport, Master-Records custody, public endpoint verification, current-main green evidence, and an observed identity-preserving RECORDED transition remain activation gates. No deployment, release, merge, or tag is authorized by this handoff. No release tag is authorized.

## Archive readiness

This handoff preserves the current provider, gateway, custody, cross-entry role, usage-ledger, retrieval, export, validation, repair, authority-boundary, and continuation state. Earlier conversation context is not required.