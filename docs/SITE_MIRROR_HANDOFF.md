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
assets/ecosystem-usage-auth-client.js
assets/ecosystem-usage-ledger.js
data/entry-point-roles.json
data/usage-session-fixture.json
data/ecosystem-usage-config.json
data/ecosystem-usage-live-contract.json
scripts/check_ecosystem_usage_auth_contract.py
scripts/check_ecosystem_usage_ledger.py
```

The usage surface preserves one session identity across entry points, deduplicates by `metric_owner + measurement_id`, preserves evidence classes, prepends usage before each transition, supports session lookup, JSON export, and receipt navigation.

The authenticated client is now loaded before the ledger renderer. Loading the client does not activate live retrieval. `data/ecosystem-usage-config.json` keeps `live_transport.enabled=false`, `usage_api_base=null`, and requires `AUTHORIZED_DEPLOYED_ENDPOINT` before activation.

## Authenticated usage retrieval boundary

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
live transport enabled: false
usage API base: null
activation prerequisite: AUTHORIZED_DEPLOYED_ENDPOINT
```

The client validates the response schema, requested session identity, event identity, evidence classes, null values for `UNAVAILABLE`, and the retrieval receipt.

Fallback behavior is separated by failure class:

```text
network unavailable -> bounded local or configured-fixture fallback may occur
authentication failure -> fail closed
session identity mismatch -> fail closed
missing retrieval receipt -> fail closed
contract-invalid output -> fail closed
```

The prepared and loaded client does not activate an endpoint, configure a credential, change deployment state, or claim live retrieval. Endpoint implementation and authenticated deployment remain destination-controlled work.

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

Positive values mean the external recursive route used more of the displayed metric.

## Authority boundary

```text
Site display != execution.
Usage retrieval != authority.
Usage event != authority.
Usage display != admissibility.
Usage retrieval receipt != Master-Records custody.
Prepared authenticated client != deployed authenticated endpoint.
Loaded authenticated client != enabled live transport.
Network fallback != live evidence.
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

The authenticated retrieval and ledger checks verify:

```text
PREPARED_NOT_DEPLOYED contract posture
authenticated client loads before ledger renderer
same-origin credential isolation
no Site-configured bearer/query/local-storage token path
bounded timeout and no-store transport
live_transport.enabled == false
usage_api_base == null
activation requires AUTHORIZED_DEPLOYED_ENDPOINT
session identity preservation
retrieval receipt requirement
MEASURED / CONFIGURED / DERIVED / UNAVAILABLE evidence classes
UNAVAILABLE values remain null
network-only bounded fallback
no fallback after authentication or integrity failure
exported state retains authority=none and custody=not-recorded-by-site
retrieval grants no authority, admissibility, custody, or RECORDED status
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
Task: integrate authenticated usage client into the public ledger without activating transport
Configuration commit: d96a8150b3c85f2d451774b14a5c4215d5c4db15
Page integration commit: 540aa3f027aa5d5a5eff1bf144259492a851ead9
Renderer integration commit: 554a70d7fcfa3fd7cc2997af2941db1027c58fd2
Validator integration commit: 4eccd604003e03ebc5646802707aec8a80fdd179
State: CLIENT_LOADED_TRANSPORT_DISABLED; current-main workflow verification pending
```

## Remaining files or modules

```text
StegVerse-Labs/Site
  -> current-main green validation receipt
  -> authorized deployed authenticated live usage endpoint configuration
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
1. Verify current-main Site workflows with authenticated-client integration included.
2. Preserve the passing Site application validation receipt.
3. Review the current LLM-adapter handoff before any endpoint mutation.
4. Implement the authenticated session-usage endpoint only under destination authority.
5. Configure usage_api_base and set live_transport.enabled=true only after deployed endpoint and same-origin authentication evidence exist.
6. Preserve CONFIGURED_FIXTURE classification until live paired results are observed and validated.
7. Do not claim RECORDED until authenticated Master-Records custody and reconstructability PASS are observed.
```

## Release posture

Role descriptions, shared usage display, transition prepends, local aggregation, session filtering, JSON export, receipt navigation, governed-versus-recursive route rendering, delta rendering, fixtures, navigation, authenticated retrieval contract, loaded fail-closed browser client, disabled activation configuration, and canonical validation are installed. The authenticated retrieval surface remains `PREPARED_NOT_DEPLOYED` and `CLIENT_LOADED_TRANSPORT_DISABLED`. Live endpoint transport, live paired results, Master-Records custody, public endpoint verification, current-main green evidence, and an observed identity-preserving RECORDED transition remain activation gates. No deployment, release, merge, credential configuration, or tag is authorized by this handoff.

## Archive readiness

This handoff preserves the provider, gateway, custody, cross-entry usage, route comparison, navigation, authenticated retrieval integration, disabled activation posture, validation, authority boundaries, and continuation state. Earlier conversation context is not required.
