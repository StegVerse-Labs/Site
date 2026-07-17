# Ecosystem Chat Activation Mirror Handoff

## Source of truth

This file is the activation-evidence continuation source for `StegVerse-Labs/Site`.
The repository-wide source remains `docs/SITE_MIRROR_HANDOFF.md`.

## Active goal

```text
Goal: automatically consume verified adapter and Master-Records evidence, complete Site activation gates, and generate downstream propagation state
Result: AUTOMATED_EVIDENCE_CONSUMPTION_INSTALLED_VERIFIED_SOURCE_RECEIPT_PENDING
Manual user action required: false
```

## Installed path

```text
StegVerse-org/LLM-adapter
receipts/ecosystem-chat-live-activation.verified.json
-> scripts/acquire_ecosystem_chat_live_activation_receipt.py
-> data/ecosystem-chat-destination-activation-receipt.json
-> data/ecosystem-chat-destination-activation-import-status.json
-> scripts/update_ecosystem_chat_activation_state.py
-> data/ecosystem-chat-activation-state.json
-> data/ecosystem-chat-activation-propagation.json
```

The acquisition runs as part of the existing scheduled Site synchronization through
`scripts/acquire_external_framework_catalog.py`. No new workflow or browser credential
is required.

## Fail-closed acceptance

A source receipt is accepted only when all of the following hold:

```text
schema = stegverse.ecosystem_chat.live_activation.v1
state = VERIFIED
blockers = []
result_sha256 matches canonical receipt content
authority_granted = false
publication_authorized = false
repository_mutation_authorized = false
gateway health = ok
gateway storage durable = true
governed provider enabled = true
transition submission enabled = true
real provider used = true
local usage custody = false
provider-usage custody = true
provider-usage reconstructability = PASS
provider-usage authority = false
transition custody = RECORDED
transition reconstructability = PASS
```

A missing receipt remains `PENDING_SOURCE_RECEIPT`. Invalid or authority-escalating
evidence becomes `REJECTED_SOURCE_RECEIPT` and fails validation.

## Site activation gates

The Site activation state now computes destination gates from imported evidence rather
than permanently setting them to false:

```text
destination_current_main_validation
same_origin_authenticated_deployment
retrieval_receipt_validation
master_records_custody
reconstructability_pass
```

Local Site gates remain independently required:

```text
site_current_main_validation
public_route_verification
mutation_required_disabled
site_activation_evidence
```

Only when every gate is true does the state become `ACTIVATION_COMPLETE`.

## Downstream propagation

`data/ecosystem-chat-activation-propagation.json` is generated on every state rebuild.
It remains `PENDING_ACTIVATION_EVIDENCE` until activation is complete, then becomes
`READY_FOR_DOWNSTREAM_INGESTION` for:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

The packet is non-authorizing and never constitutes custody, release authority,
publication authority, or activation authority.

## Current blocker

```text
The adapter's retained VERIFIED live-activation receipt has not yet been observed at
receipts/ecosystem-chat-live-activation.verified.json.
```

The existing adapter workflow owns production observation and first-receipt retention.
The existing Site schedule owns import, state recomputation, and propagation packet
generation after that receipt appears.

## Next task

```text
1. Observe the first retained adapter VERIFIED receipt automatically.
2. Let the Site scheduled synchronization import and validate it.
3. Repair only an exact rejected evidence gate or Site validation failure.
4. When Site state becomes ACTIVATION_COMPLETE, let downstream consumers ingest the generated propagation packet.
5. Tag or release only after repository validation, retained live evidence, Site activation, and required downstream updates are all verified.
```

## Archive readiness

This handoff, the Site mirror handoff, adapter handoff, Master-Records provider-usage
handoff, generated state files, and workflow evidence preserve all continuation state.
No prior conversation is required.
