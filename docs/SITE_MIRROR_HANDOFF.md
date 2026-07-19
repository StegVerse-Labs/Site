# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: fully functional governed Ecosystem Chat request-response, provider, persistence, custody, reconstruction, immutable receipt, Site activation, and downstream propagation path
Primary surface: ecosystem-chat.html
Usage surface: ecosystem-usage.html
Comparison surface: ecosystem-comparison.html
Operational projection: governed-transitions.html
Result: ACTIVATION_PENDING_RUNTIME_EVIDENCE
Manual user action required: false
```

## Required vertical slice

```text
real request
-> governed provider response
-> provider usage persistence
-> authenticated provider-usage Master-Records custody
-> transition custody
-> reconstruction PASS for both chains
-> immutable adapter VERIFIED receipt with zero blockers
-> automatic Site acquisition and validation
-> Site ACTIVATION_COMPLETE
-> hash-bound downstream propagation
-> verified downstream ingestion
```

## Authoritative owners

```text
Runtime gateway and activation evidence: StegVerse-org/LLM-adapter
Custody and reconstruction: existing Master-Records implementation referenced by adapter evidence
Site activation projection: StegVerse-Labs/Site
Publication projection: GCAT-BCAT-Engine/Publisher
Admissibility projection: StegVerse-Labs/admissibility-wiki
Guardian projection: StegVerse-002/stegguardian-wiki
```

## Existing components reused

Adapter:

```text
.github/workflows/ecosystem-chat-live-activation.yml
scripts/verify_live_ecosystem_chat_activation.py
scripts/write_live_activation_status.py
reports/ecosystem-chat-live-activation-status.json
receipts/ecosystem-chat-live-activation.latest.json
receipts/ecosystem-chat-live-activation.verified.json when VERIFIED
```

Site:

```text
.github/workflows/ecosystem-chat-activation-retention.yml
scripts/watch_ecosystem_chat_adapter_monitor.py
scripts/acquire_ecosystem_chat_live_activation_receipt.py
scripts/check_ecosystem_chat_activation_receipt_import.py
scripts/import_ecosystem_chat_external_activation_states.py
scripts/update_ecosystem_chat_activation_state.py
```

Site-generated state:

```text
data/ecosystem-chat-adapter-monitor-watch.json
data/ecosystem-chat-destination-activation-receipt.json when VERIFIED
data/ecosystem-chat-destination-activation-import-status.json
data/ecosystem-chat-activation-state.json
data/ecosystem-chat-activation-propagation.json
```

## Heartbeat boundary

The StegVerse runtime heartbeat is not defined, generated, scheduled, or authorized by GitHub Actions.

```text
GitHub Actions cron != runtime heartbeat
workflow execution record != runtime heartbeat
CI status file != runtime heartbeat
repository commit frequency != runtime heartbeat
Site evidence watcher != runtime heartbeat watchdog
```

The adapter intentionally removed the former CI-derived activation heartbeat writer, report, scheduler-status report, and related workflow steps. Site does not fetch or require those removed artifacts.

`scripts/watch_ecosystem_chat_adapter_monitor.py` observes only:

```text
reports/ecosystem-chat-live-activation-status.json
receipts/ecosystem-chat-live-activation.verified.json when present
```

This watcher is an activation-evidence consumer. It does not determine heartbeat cadence, continuity, authority, or existence.

## Current exact evidence posture

```text
Site acquisition and activation-state consumers: IMPLEMENTED
Site heartbeat-boundary repair: INTEGRATED
Adapter live verifier: IMPLEMENTED
Adapter automation contract heartbeat alignment: IMPLEMENTED on main
Adapter validation after contract repair: EXECUTION PENDING
Current real provider request/response: NOT YET VERIFIED
Provider-usage custody: NOT YET VERIFIED
Provider-usage reconstruction: NOT YET VERIFIED
Transition custody: NOT YET VERIFIED
Transition reconstruction: NOT YET VERIFIED
Adapter immutable VERIFIED receipt: NOT YET OBSERVED
Site ACTIVATION_COMPLETE: NOT YET OBSERVED
Downstream verified ingestion: NOT YET OBSERVED
Manual user action required: false
```

Current stable adapter status remains `PENDING` with blocker `live_activation_observation_not_yet_recorded`. This is a runtime-evidence blocker, not a heartbeat blocker.

## Verified receipt gates

The immutable adapter receipt is accepted only when:

```text
state = VERIFIED
blockers = []
canonical receipt hash valid
gateway health OK
durable storage
governed provider enabled
real provider use
local usage remains non-custodial
provider-usage custody RECORDED
provider-usage reconstructability PASS
transition custody RECORDED
transition reconstructability PASS
all authority flags false
```

Invalid, conflicting, stale, or authority-escalating evidence is rejected.

## Site-local completion and downstream propagation

Site publishes `ACTIVATION_COMPLETE` only when every local and destination gate is true. Until then:

```text
data/ecosystem-chat-activation-propagation.json
state: PENDING_ACTIVATION_EVIDENCE
```

After machine-verified completion:

```text
state: READY_FOR_DOWNSTREAM_INGESTION
```

Canonical destinations:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

A propagation packet is not custody, activation authority, publication authority, execution authority, admissibility, or release authority.

## Progress accounting

Three measures must remain separate:

```text
Implementation coverage: required code and integrations exist
Runtime gate completion: gates passed by a current real execution
Evidence state: DESIGNED / IMPLEMENTED / INTEGRATED / EXECUTED / VERIFIED / DEPLOYED / LIVE / PROPAGATED
```

Documentation, handoffs, status files, CI schedules, installed workflows, pending imports, and monitors do not increase runtime gate completion.

The Site repository may have high implementation coverage while the end-to-end activation slice remains unverified. Percentages must describe which measure they represent and must not imply verified runtime completion.

## Machine-owned continuation

```text
1. Adapter validation runs with the heartbeat-corrected automation contract.
2. The existing live verifier executes gateway, provider, persistence, custody, identity, and reconstruction checks.
3. The exact runtime blockers are written to stable semantic status.
4. The first zero-blocker VERIFIED result is retained immutably.
5. Site imports and validates pending or VERIFIED evidence automatically.
6. Site recomputes activation and propagation state.
7. Publisher and both wiki consumers ingest the Site projection automatically.
8. Release readiness remains fail-closed until downstream verified evidence exists.
```

No browser credential, copy/paste, workflow dispatch, artifact download, screenshot confirmation, receipt construction, blocker transcription, credential copying, or manual publication task is required.

## Authority boundary

```text
Site display != execution
provider output != authority
usage retrieval != authority
usage measurement != admissibility
local persistence != custody
submission != custody
pending status != activation
CI execution != runtime heartbeat
CI evidence watcher != heartbeat authority
imported verified receipt != deployment authority
propagation packet != publication authority
reconstruction PASS != execution authority
Site autonomy runtime PASS != Ecosystem Chat activation
Site autonomy completion evidence != release authority
```

## Current blocker and next executable step

```text
Blocker: current live activation result has not yet been executed and retained after automation-contract alignment
Owner: StegVerse-org/LLM-adapter
Next step: allow the existing validate and live-activation workflows to execute from commit 7c26041eeeb7f165583308efaedd59e1d17a8c92, inspect the first exact runtime result, and repair only that failing boundary
Manual user action required: false
```

## Release posture

No tag or release is authorized. Existing acquisition, validation, activation-state computation, propagation packaging, retention, custody checks, reconstruction checks, and downstream consumers are retained. Remaining conditions are a current real runtime execution, immutable VERIFIED receipt publication, Site activation completion, and verified downstream ingestion.

## Archive readiness

This handoff, the paired build-goal and active-building records, adapter stable status, immutable receipt path, Site machine-readable state, and repository history preserve all continuation state without requiring conversation context.
