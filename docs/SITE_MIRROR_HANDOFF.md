# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: fully functional governed Ecosystem Chat request-response, provider, custody, comparison, and cross-entry usage path
Primary surface: ecosystem-chat.html
Usage and role surface: ecosystem-usage.html
Comparison surface: ecosystem-comparison.html
Operational projection: governed-transitions.html
Workflow target: exactly two operational workflows
Result: implementation installed; live validation pending
```

## Active workflows

```text
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

No workflow was added.

## Installed usage and role surface

```text
ecosystem-usage.html
assets/ecosystem-usage-ledger.js
data/entry-point-roles.json
data/usage-session-fixture.json
data/ecosystem-usage-config.json
scripts/check_ecosystem_usage_ledger.py
```

The usage surface preserves one session identity across entry points, deduplicates by `metric_owner + measurement_id`, preserves evidence classes, prepends usage before each transition, supports session lookup, JSON export, and receipt navigation.

## Installed governed-versus-recursive comparison surface

```text
ecosystem-comparison.html
assets/ecosystem-comparison.js
data/llm-route-comparison-fixture.json
scripts/check_ecosystem_comparison.py
scripts/check_ecosystem_chat_application.py invokes the comparison checker
```

Proof path:

```text
one task identity
-> StegVerse governed route
-> external recursive route
-> common telemetry contract
-> evidence-classified route metrics
-> external_recursive - stegverse_governed deltas
-> receipt references
-> fail-closed Site rendering
```

The comparison page renders governed and recursive output summaries, route posture, cost, latency, model calls, tokens, tools, retries, node activations, receipts, and delta cards.

Current comparison data is classified `CONFIGURED_FIXTURE`. It is not a live provider or runtime measurement.

## Required comparison invariants

```text
same_task_identity == true
same_output_requirement == true
comparison_is_authority == false
comparison_is_admissibility == false
configured_values_are_measured == false
```

The canonical delta formula is:

```text
external_recursive - stegverse_governed
```

Positive values therefore mean the external recursive route used more of the displayed metric.

## Authority boundary

```text
Site display != execution.
Usage retrieval != authority.
Usage event != authority.
Usage display != admissibility.
Comparison != authority.
Comparison != admissibility.
Entry-point acceptance != authority.
Translation != admissibility.
Provider output != authority.
Provider receipt != final response receipt.
Final response receipt != Master-Records custody.
Configured fixture values != live measurements.
JSON export != custody.
Usage and comparison presentation do not alter provider output or transition hashes.
Site does not execute or mutate repositories.
Site does not execute or mutate external repositories.
RECORDED requires the authenticated custody service receipt.
RECORDED requires authenticated custody evidence and reconstructability PASS.
No release tag is authorized.
```

## Validation surface

```text
python scripts/check_ecosystem_chat_application.py
  -> python scripts/check_ecosystem_usage_ledger.py
  -> python scripts/check_ecosystem_comparison.py
```

The comparison checker verifies:

```text
public comparison page and renderer exist
exactly one STEGVERSE_GOVERNED route exists
exactly one EXTERNAL_RECURSIVE route exists
like-for-like task and output identity are preserved
valid MEASURED / CONFIGURED / DERIVED / UNAVAILABLE classes
UNAVAILABLE values remain null
configured values are not represented as measured
canonical delta formula is preserved
comparison does not claim authority or admissibility
fail-closed rendering exists
```

## Remaining files or modules

```text
StegVerse-Labs/Site
  -> direct Usage Ledger and Route Comparison links inside ecosystem-chat.html primary navigation
  -> deployed authenticated live usage retrieval
  -> live paired-result ingestion replacing configured comparison fixture
  -> public retrieval, comparison, and receipt-navigation verification

StegVerse-org/LLM-adapter
  -> automatic provider usage emission
  -> authenticated session-usage retrieval
  -> live external recursive route endpoint

StegVerse-org/core-node-runtime-demo
  -> automatic runtime usage emission
  -> live governed route endpoint

master-records
  -> custody usage and comparison events
  -> deduplication and reconstruction indexes
```

## Release posture

Role descriptions, shared usage display, transition prepends, local aggregation, session filtering, JSON export, receipt navigation, governed-versus-recursive route rendering, delta rendering, fixtures, and validation are installed. Live transport, live paired results, Master-Records custody, public endpoint verification, current-main green evidence, and an observed identity-preserving RECORDED transition remain activation gates. No deployment, release, merge, or tag is authorized by this handoff. No release tag is authorized.

## Archive readiness

This handoff preserves the provider, gateway, custody, cross-entry usage, route comparison, validation, authority boundaries, and continuation state. Earlier conversation context is not required.
