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
Result: SITE_AUTOMATED_ACTIVATION_CONSUMPTION_INSTALLED_LIVE_VERIFIED_RECEIPT_PENDING
```

## Active workflows

```text
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
.github/workflows/ecosystem-chat-activation-retention.yml
```

The iOS validation mirror remains `iosnoperiod/github/workflows/validate.yml`.
No additional workflow is required for destination receipt ingestion.

## Current architecture

```text
StegVerse-org/LLM-adapter live governed gateway
-> provider response
-> provider usage local persistence
-> authenticated provider-usage Master-Records custody
-> transition Master-Records custody
-> reconstruction PASS for both custody chains
-> retained adapter VERIFIED activation receipt
-> automatic Site receipt acquisition and validation
-> Site activation-state recomputation
-> downstream propagation packet
```

## Destination evidence consumer

Installed:

```text
scripts/acquire_ecosystem_chat_live_activation_receipt.py
scripts/acquire_external_framework_catalog.py
scripts/check_ecosystem_chat_activation_receipt_import.py
scripts/update_ecosystem_chat_activation_state.py
docs/ECOSYSTEM_CHAT_ACTIVATION_MIRROR_HANDOFF.md
```

Generated state:

```text
data/ecosystem-chat-destination-activation-receipt.json
data/ecosystem-chat-destination-activation-import-status.json
data/ecosystem-chat-activation-state.json
data/ecosystem-chat-activation-propagation.json
```

The existing scheduled Site task runner invokes external catalog synchronization, which
also acquires the retained adapter activation receipt. No browser credential, copy/paste,
or manually executed verification command is required.

## Fail-closed destination gates

The Site no longer hard-codes destination gates to false. It computes them from a
canonical, hash-verified adapter receipt:

```text
destination_current_main_validation
same_origin_authenticated_deployment
retrieval_receipt_validation
master_records_custody
reconstructability_pass
```

Receipt acceptance requires a real provider response, non-custodial local usage,
provider-usage custody, transition custody, reconstruction PASS for both chains, exact
identity preservation, no blockers, and all authority flags false.

Missing evidence remains pending. Invalid, conflicting, or authority-escalating evidence
is rejected and cannot activate the Site.

## Site-local gates

The following remain independently required:

```text
site_current_main_validation
public_route_verification
mutation_required_disabled
site_activation_evidence
```

Only when every local and destination gate is true does the state become:

```text
ACTIVATION_COMPLETE
```

## Downstream propagation

The activation-state writer generates:

```text
data/ecosystem-chat-activation-propagation.json
```

Before completion:

```text
state: PENDING_ACTIVATION_EVIDENCE
```

After completion:

```text
state: READY_FOR_DOWNSTREAM_INGESTION
```

Destinations:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

The packet is non-authorizing and is not custody, publication authority, release
authority, or activation authority.

## Current evidence state

```text
Site destination receipt importer: INSTALLED
Receipt canonical hash verification: INSTALLED
Authority-escalation guards: INSTALLED
Destination gate computation: INSTALLED
Downstream propagation packet writer: INSTALLED
Canonical Site validation binding: INSTALLED
Scheduled import path: INSTALLED
Adapter retained VERIFIED activation receipt: NOT YET OBSERVED
Site imported verified destination receipt: NOT YET OBSERVED
Site activation state ACTIVATION_COMPLETE: NOT YET OBSERVED
Downstream ingestion: NOT YET OBSERVED
```

## Current blocker

```text
StegVerse-org/LLM-adapter/receipts/ecosystem-chat-live-activation.verified.json
has not yet been retained on current main.
```

The adapter workflow owns live observation and first verified receipt retention. The Site
workflow owns automatic acquisition, validation, activation-state recomputation, Pages
publication, and downstream propagation-packet generation after the receipt appears.

## Remaining work

```text
StegVerse-org/LLM-adapter
  -> complete current-main validation
  -> deploy current source through existing autoDeploy
  -> run scheduled live activation verification
  -> retain the first VERIFIED activation receipt

master-records/orchestration
  -> deploy provider-usage custody route
  -> return authenticated provider-usage and transition custody receipts
  -> return reconstruction PASS evidence

StegVerse-Labs/Site
  -> automatically import the retained adapter receipt
  -> recompute local and destination activation gates
  -> repair only an exact rejected receipt gate or failing Site validator
  -> publish ACTIVATION_COMPLETE only when every gate passes
  -> generate READY_FOR_DOWNSTREAM_INGESTION propagation state

Downstream repositories
  -> ingest the propagation packet after it becomes ready
  -> preserve non-authorizing boundaries
  -> update documentation and publication surfaces only from verified evidence
```

## Authority boundary

```text
Site display != execution.
Provider output != authority.
Usage retrieval != authority.
Usage measurement != admissibility.
Local persistence != custody.
Submission != custody.
Imported receipt != deployment authority.
Propagation packet != publication authority.
Reconstruction PASS != execution authority.
No release tag is authorized before all validation and live-evidence gates pass.
```

## Release posture

Repository-local automation for acquisition, validation, activation-state computation,
and propagation packaging is installed. Live deployed evidence and downstream ingestion
remain pending. No tag or release is authorized.

## Archive readiness

This handoff, `docs/ECOSYSTEM_CHAT_ACTIVATION_MIRROR_HANDOFF.md`, the adapter and
Master-Records handoffs, generated machine-readable state, workflows, and repository
history preserve all continuation state. Earlier conversation context is not required.
