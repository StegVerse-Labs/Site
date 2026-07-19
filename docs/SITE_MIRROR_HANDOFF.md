# Site Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for `StegVerse-Labs/Site`.

## Current goal

```text
Goal: fully functional governed Ecosystem Chat request-response, provider, custody, comparison, usage, and downstream propagation path
Primary surface: ecosystem-chat.html
Usage surface: ecosystem-usage.html
Comparison surface: ecosystem-comparison.html
Operational projection: governed-transitions.html
Result: SITE_STABLE_BLOCKER_PROPAGATION_OBSERVED_ACTIVATION_PENDING
Manual user action required: false
```

## Active workflows

```text
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
.github/workflows/ecosystem-chat-activation-retention.yml
.github/workflows/autonomy-telemetry.yml
iosnoperiod/github/workflows/validate.yml
```

## Governed activation path

```text
StegVerse-org/LLM-adapter live governed gateway
-> provider response
-> provider usage persistence
-> authenticated provider-usage Master-Records custody
-> transition custody
-> reconstruction PASS for both chains
-> adapter stable semantic blocker status while pending
-> adapter immutable VERIFIED activation receipt after all gates pass
-> automatic Site acquisition and validation
-> Site activation-state recomputation
-> downstream propagation packet
```

## Site evidence consumers

Installed:

```text
scripts/acquire_ecosystem_chat_live_activation_receipt.py
scripts/check_ecosystem_chat_activation_receipt_import.py
scripts/import_ecosystem_chat_external_activation_states.py
scripts/update_ecosystem_chat_activation_state.py
scripts/watch_ecosystem_chat_adapter_monitor.py
```

Generated state:

```text
data/ecosystem-chat-destination-activation-receipt.json when VERIFIED
data/ecosystem-chat-destination-activation-import-status.json
data/ecosystem-chat-adapter-monitor-watch.json
data/ecosystem-chat-activation-state.json
data/ecosystem-chat-activation-propagation.json
```

## Adapter monitor watchdog

The adapter's semantic activation status is intentionally timestamp-free, so unchanged status alone cannot prove that its activation workflow executed. The adapter now publishes:

```text
reports/ecosystem-chat-live-activation-monitor.json
reports/ecosystem-chat-activation-scheduler-status.json
```

Site independently fetches and validates these records through `scripts/watch_ecosystem_chat_adapter_monitor.py`.

`.github/workflows/ecosystem-chat-activation-retention.yml` now:

```text
runs hourly at minute 11
runs after Site Task Runner
self-starts when its watchdog implementation changes
fetches adapter monitor and scheduler status
validates canonical monitor hashing
records exact execution-observation blockers
reacquires pending or VERIFIED activation evidence
rebuilds activation and propagation state
persists all changed records automatically
```

This removes workflow-run inspection, artifact inspection, and blocker transcription as manual tasks.

## Current exact evidence posture

```text
Site autonomy runtime: 7 of 7 required checks PASS
Site strict operational completion evidence: VALID
Adapter stable pending status: OBSERVED_AND_VALIDATED
Adapter semantic blocker: live_activation_observation_not_yet_recorded
Adapter scheduler evidence blocker: github_actions_execution_not_observed_for_self_starting_activation_monitor
Adapter monitor heartbeat blocker: live_activation_monitor_run_not_yet_recorded
Adapter immutable VERIFIED activation receipt: NOT YET OBSERVED
Site ACTIVATION_COMPLETE: NOT YET OBSERVED
Downstream verified ingestion: NOT YET OBSERVED
Manual user action required: false
```

The scheduler and heartbeat blockers are execution-evidence blockers, not proof that GitHub Actions is disabled. Site will continue observing them automatically and replace them with the exact runtime result when the adapter publishes a monitor run.

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

All three destinations have autonomous fail-closed consumers. A propagation packet is not custody, activation authority, publication authority, execution authority, admissibility, or release authority.

## Machine-owned continuation

```text
1. Site's hourly watchdog observes adapter scheduling and heartbeat evidence.
2. Adapter's 15-minute bounded verifier continues probing gateway, provider, custody, identity, and reconstruction.
3. Exact monitor or runtime blockers replace generic missing-observation state automatically.
4. Adapter retains the first immutable VERIFIED receipt only with zero blockers.
5. Site imports and validates pending or VERIFIED state automatically.
6. Site recomputes activation and propagation state.
7. Publisher and both wiki consumers ingest the Site projection automatically.
8. Release readiness remains fail-closed until downstream public evidence exists.
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
monitor heartbeat != activation
scheduler status != execution authority
imported verified receipt != deployment authority
propagation packet != publication authority
reconstruction PASS != execution authority
Site autonomy runtime PASS != Ecosystem Chat activation
Site autonomy completion evidence != release authority
```

## Release posture

No tag or release is authorized. Repository-local acquisition, validation, activation-state computation, propagation packaging, retention, cross-artifact consistency checks, strict Site autonomy evidence, adapter scheduler watching, and downstream consumers are installed. Remaining conditions are observed adapter runtime evidence, immutable VERIFIED receipt publication, Site activation completion, and verified downstream ingestion.

## Archive readiness

This workstream remains active. The exact current blocker is durably observable without conversation context, and Site now owns an independent machine-scheduled watchdog for adapter workflow silence and runtime evidence.
