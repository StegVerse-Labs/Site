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

## Ecosystem Chat governed request path

```text
create canonical SITE_INPUT identity
-> submit to governed gateway
-> validate identity-preserving response
-> display governed provider posture or deterministic fallback
-> display final response receipt
-> display SQLite persistence and restart durability
-> display custody queue and Master-Records state
-> inspect the same transition in governed-transitions.html
```

## Shared entry-point role and usage surface

Installed:

```text
ecosystem-usage.html
assets/ecosystem-usage-ledger.js
data/entry-point-roles.json
data/usage-session-fixture.json
scripts/check_ecosystem_usage_ledger.py
scripts/check_ecosystem_chat_application.py invokes the usage-ledger checker
```

The page gives easily identified primary and related role descriptions for:

```text
StegVerse SDK
  -> developer-native programmatic testing, integration, and observation

StegVerse LLM Adapter
  -> machine-readable translation and external interoperability

StegVerse Ecosystem Chat
  -> universal browser-based governed conversation, discovery, development, testing, and orchestration
```

Every displayed transition begins with a usage prepend containing the preserved session and transition identity, origin and participating entry points, measurement owners, receipt references, and evidence-classified metrics.

## Cross-entry usage proof path

```text
SDK / LLM Adapter / Ecosystem Chat / runtime event
-> validate one session identity
-> preserve transition lineage
-> deduplicate metric_owner + measurement_id
-> retain MEASURED / CONFIGURED / DERIVED / UNAVAILABLE classification
-> aggregate evidence-separated session usage
-> prepend usage metadata before transition content
-> render shared session timeline
```

The browser reads `stegverse.transitionUsageEvents.v1` from local storage when a synchronized entry point has supplied a session ledger. It uses the configured fixture only when no synchronized local session exists.

## Usage ownership boundary

```text
Ecosystem Chat owns browser interaction and presentation measurements.
SDK owns SDK validation and orchestration measurements.
LLM Adapter owns provider, token, and translation measurements.
Runtime owns node, execution, closure, receipt, and runtime-storage measurements.
Master-Records owns custody and persistence measurements.
```

The Site does not re-own or duplicate measurements. Deduplication is based on the stable pair:

```text
metric_owner + measurement_id
```

## Evidence and authority boundary

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
```

## Existing provider and custody display

The Site already displays provider source, status, name, model, provider receipt, estimated provider cost, deterministic fallback, lifecycle, final receipt, custody queue, custody receipt, Master-Records reference, and reconstruction posture.

Relevant surfaces:

```text
assets/ecosystem-chat-transition-identity.js
assets/ecosystem-chat-gateway-health.js
assets/governed-transitions-live-custody.js
ecosystem-chat.html
governed-transitions.html
scripts/check_ecosystem_chat_gateway_activation.py
scripts/check_governed_transition_observatory.py
```

## Validation surface

The existing `Site Bootstrap Validate` workflow now reaches the usage-ledger checker through:

```text
python scripts/check_ecosystem_chat_application.py
  -> python scripts/check_ecosystem_usage_ledger.py
```

The checker verifies:

```text
public usage page and renderer exist
SDK / LLM Adapter / Ecosystem Chat roles are declared
fixture spans browser, SDK, adapter, and runtime owners
one session identity is preserved
measurement identities are unique per owner
evidence classes remain valid
UNAVAILABLE values remain null
transition usage prepend is rendered
usage does not claim authority or alter transition output
```

## Remaining files or modules

```text
StegVerse-Labs/Site
  -> link Ecosystem Usage Ledger prominently from Ecosystem Chat and primary navigation
  -> ingest live gateway usage events instead of fixture fallback
  -> render governed-vs-recursive paired output and delta bars
  -> add session filtering, export, and receipt navigation

StegVerse-org/LLM-adapter
  -> automatically emit provider usage during the live provider lifecycle
  -> expose authenticated session-usage retrieval

StegVerse-org/core-node-runtime-demo
  -> automatically emit runtime usage during governed execution

master-records
  -> custody usage events, deduplication index, and session reconstruction pointers
```

## Release posture

Role descriptions, the shared usage page, transition prepend rendering, local cross-entry aggregation, deduplication, fixtures, and validation are installed. Live event transport, Master-Records custody, public endpoint verification, current-main green evidence, and an observed identity-preserving RECORDED transition remain activation gates. No release tag is authorized.

## Archive readiness

This handoff preserves the provider, gateway, custody, cross-entry role, usage-ledger, validation, authority-boundary, and continuation state. Earlier conversation context is not required.
