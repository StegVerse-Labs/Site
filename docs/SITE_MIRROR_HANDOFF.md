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

## Prepared authenticated usage retrieval boundary

```text
data/ecosystem-usage-live-contract.json
assets/ecosystem-usage-auth-client.js
scripts/check_ecosystem_usage_auth_contract.py
scripts/check_ecosystem_chat_application.py
```

Current posture:

```text
contract status: PREPARED_NOT_DEPLOYED
route template: /api/usage/sessions/{session_id}
authentication mode: same_origin_session
same-origin browser credentials: allowed
cross-origin browser credentials: prohibited
Site-configured bearer tokens: prohibited
query-string tokens: prohibited
local-storage tokens: prohibited
request timeout: 10 seconds
cache posture: no-store
```

The client validates the response schema, requested session identity, event identity, evidence classes, null values for `UNAVAILABLE`, and the retrieval receipt. Authentication failure, session-identity mismatch, missing receipt, or contract-invalid output fails closed and may not silently downgrade to fixture evidence.

The prepared client does not activate an endpoint, configure a credential, change deployment state, or claim live retrieval. Endpoint implementation and authenticated deployment remain destination-controlled work.

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

## Installed Ecosystem Chat navigation

```text
assets/ecosystem-chat-hps.js
scripts/check_ecosystem_chat_navigation.py
scripts/check_ecosystem_chat_application.py
```

The already-loaded Ecosystem Chat bootstrap installs direct primary-navigation links to:

```text
ecosystem-usage.html -> Usage Ledger
ecosystem-comparison.html -> Route Comparison
```

The navigation installer runs before HPS fixture loading, does not depend on the fixture succeeding, does not grant authority, and does not alter transition hashes, provider output, receipts, custody, or evidence standing.

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
Usage retrieval receipt != Master-Records custody.
Prepared authenticated client != deployed authenticated endpoint.
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
  -> python scripts/check_ecosystem_chat_navigation.py
  -> python scripts/check_ecosystem_usage_auth_contract.py
  -> python scripts/check_ecosystem_usage_ledger.py
  -> python scripts/check_ecosystem_comparison.py
```

The authenticated retrieval checker verifies:

```text
PREPARED_NOT_DEPLOYED posture
same-origin credential isolation
no Site-configured bearer/query/local-storage token path
bounded timeout and no-store transport
session identity preservation
retrieval receipt requirement
MEASURED / CONFIGURED / DERIVED / UNAVAILABLE evidence classes
UNAVAILABLE values remain null
no silent fallback after authentication or integrity failure
retrieval grants no authority, admissibility, custody, or RECORDED status
```

The navigation checker verifies:

```text
primary navigation exists
usage target exists
comparison target exists
runtime navigation installer exists
both labels and hrefs are declared
no authority or execution marker is introduced
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

## Latest bounded task completion

```text
Task: prepare Site-owned authenticated live usage retrieval boundary
Contract commit: 48105fdf455cdba89c3904d9b325c566b7ab6701
Client commit: 8e254127dc6e3d093e1c94a887775fdad21fc033
Validator commit: 86d01352a9b14d660bf6f5e868d3278915017619
Canonical integration commit: 94067c07c581c00334ba2c468b6c796cd04417b8
State: PREPARED_NOT_DEPLOYED; current-main workflow verification pending
```

## Remaining files or modules

```text
StegVerse-Labs/Site
  -> load the authenticated client on the usage surface after an authorized endpoint exists
  -> deployed authenticated live usage retrieval
  -> live paired-result ingestion replacing configured comparison fixture
  -> public retrieval, comparison, and receipt-navigation verification

StegVerse-org/LLM-adapter
  -> automatic provider usage emission
  -> authenticated session-usage retrieval endpoint
  -> live external recursive route endpoint

StegVerse-org/core-node-runtime-demo
  -> automatic runtime usage emission
  -> live governed route endpoint

master-records
  -> custody usage and comparison events
  -> deduplication and reconstruction indexes
```

## Next task

```text
1. Verify the current-main Site workflow passes with navigation and authenticated-usage contract checks included.
2. Preserve the passing Site application validation receipt.
3. Review the current destination handoff before any LLM-adapter endpoint mutation.
4. Load the authenticated client only after an authorized endpoint and same-origin authentication path exist.
5. Preserve CONFIGURED_FIXTURE classification until live paired results are observed and validated.
6. Do not claim RECORDED until authenticated Master-Records custody and reconstructability PASS are observed.
```

## Release posture

Role descriptions, shared usage display, transition prepends, local aggregation, session filtering, JSON export, receipt navigation, governed-versus-recursive route rendering, delta rendering, fixtures, navigation, authenticated retrieval contract, fail-closed browser client, and canonical validation are installed. The authenticated retrieval surface remains `PREPARED_NOT_DEPLOYED`. Live endpoint transport, live paired results, Master-Records custody, public endpoint verification, current-main green evidence, and an observed identity-preserving RECORDED transition remain activation gates. No deployment, release, merge, credential configuration, or tag is authorized by this handoff.

## Archive readiness

This handoff preserves the provider, gateway, custody, cross-entry usage, route comparison, navigation, authenticated retrieval boundary, validation, authority boundaries, and continuation state. Earlier conversation context is not required.
