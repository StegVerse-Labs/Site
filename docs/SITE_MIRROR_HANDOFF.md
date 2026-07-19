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

No additional destination-ingestion workflow is required.

## Current architecture

```text
StegVerse-org/LLM-adapter live governed gateway
-> provider response
-> provider usage local persistence
-> authenticated provider-usage Master-Records custody
-> transition Master-Records custody
-> reconstruction PASS for both chains
-> adapter stable semantic blocker status while pending
-> adapter immutable VERIFIED activation receipt after all gates pass
-> automatic Site acquisition and validation
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

The scheduled Site path first seeks the immutable adapter receipt:

```text
https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/receipts/ecosystem-chat-live-activation.verified.json
```

Until that receipt exists, it imports and validates the adapter's stable blocker status:

```text
https://raw.githubusercontent.com/StegVerse-org/LLM-adapter/main/reports/ecosystem-chat-live-activation-status.json
```

The pending status is accepted only when its repository identity, schema, canonical hash, blocker list, manual-action boundary, and all authority flags validate. Pending status cannot activate Site.

The first stable blocker status has now been observed and imported by Site. The accepted source state is `PENDING`, its canonical status hash is `9a3cbb86725b3fefbe028f548abeb7ed1af865e2759e45f1a1c4a817f6fee14a`, and the exact blocker is `live_activation_observation_not_yet_recorded`.

This removes the need to inspect expiring workflow artifacts merely to determine why activation remains pending.

## Retention self-healing path

The retention workflow now independently reacquires and validates the immutable receipt or stable blocker status before every activation-state rebuild. Artifact downloads are supplemental rather than a prerequisite for destination-state continuity.

The workflow must persist and cross-check:

```text
data/ecosystem-chat-destination-activation-import-status.json
data/ecosystem-chat-destination-activation-receipt.json when present
data/ecosystem-chat-activation-state.json
data/ecosystem-chat-activation-propagation.json
```

The consistency gate requires the imported destination state to be reflected in the rebuilt Site gates, requires the propagation packet to bind the current state hash, and refuses a pending source that lacks an exact blocker. This repairs the previously observed stale projection in which the validated pending import existed while `data/ecosystem-chat-activation-state.json` still reported that no destination state had been imported.

## Verified receipt gates

The immutable verified receipt remains the only destination activation input. Acceptance requires:

```text
state = VERIFIED
blockers = []
canonical receipt hash valid
gateway health OK
durable storage
governed provider enabled
real provider use
local usage non-custodial
provider-usage custody RECORDED
provider-usage reconstructability PASS
transition custody RECORDED
transition reconstructability PASS
all authority flags false
```

Invalid, conflicting, or authority-escalating evidence is rejected.

## Site-local gates

```text
site_current_main_validation
public_route_verification
mutation_required_disabled
site_activation_evidence
```

Only when every local and destination gate is true does Site publish:

```text
ACTIVATION_COMPLETE
```

## Downstream propagation

Site generates:

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

Canonical destinations:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

The packet is not custody, activation authority, publication authority, execution authority, or release authority.

## Current evidence state

```text
Site verified-receipt importer: INSTALLED
Site pending semantic-status importer: INSTALLED
Pending status canonical hash verification: INSTALLED
Verified receipt canonical hash verification: INSTALLED
Authority-escalation guards: INSTALLED
Destination gate computation: INSTALLED
Downstream propagation packet writer: INSTALLED
Canonical Site validation binding: INSTALLED
Scheduled import path: INSTALLED
Retention independent source reacquisition: INSTALLED
Retention cross-artifact consistency gate: INSTALLED
Site autonomy strict completion evidence: INSTALLED
Site autonomy strict completion evidence validation: INSTALLED
Adapter first stable blocker state: OBSERVED_AND_VALIDATED
Adapter pending source state: PENDING
Adapter exact blocker: live_activation_observation_not_yet_recorded
Adapter immutable VERIFIED activation receipt: NOT YET OBSERVED
Site ACTIVATION_COMPLETE: NOT YET OBSERVED
Downstream verified ingestion: NOT YET OBSERVED
```

## Site autonomy evidence advancement

The public autonomy runtime has produced a current PASS receipt for all seven required checks, including both mobile flows. Site now persists the strict classifier input at:

```text
data/autonomy/completion-evidence.json
```

The receipt binds `StegVerse-Labs/Site` to objective `site-public-autonomy-observability`, records the observed public user outcome, names GitHub Actions as the machine verifier, declares zero critical blockers for that bounded objective, rejects manual completion dependency, and links the public runtime evidence surfaces.

`.github/workflows/autonomy-telemetry.yml` now validates this receipt before enumeration and includes it in persisted autonomy state. The next public autonomy cycle must therefore classify Site as `OPERATIONALLY_COMPLETE`, increase `valid_completion_evidence` from zero to at least one, and retain automatic freshness downgrade when the receipt becomes older than 30 days.

This bounded Site autonomy completion evidence does not complete Ecosystem Chat activation, authorize release, or grant authority to any downstream repository.

## Machine-owned continuation

```text
1. Adapter scheduled verification has written a stable semantic blocker state while pending.
2. Site scheduled acquisition has imported and validated that pending state automatically.
3. Site retention independently reacquires source evidence and rebuilds a hash-bound activation projection.
4. Exact blockers propagate through Site state without granting activation.
5. Site public autonomy cycle validates and consumes data/autonomy/completion-evidence.json.
6. Adapter must execute and record the live activation observation, then retain the first immutable VERIFIED receipt after every live gate passes.
7. Site imports and validates that receipt automatically.
8. Site recomputes local and destination activation gates.
9. Site publishes ACTIVATION_COMPLETE only when every gate passes.
10. Publisher and both wiki consumers ingest the ready propagation packet automatically.
11. Release readiness remains fail-closed until downstream public evidence is observed.
```

No browser credential, copy/paste, workflow dispatch, artifact download, manually executed verifier, or manual blocker transcription is required.

## Exact remaining blocker and owner

```text
Blocker: live_activation_observation_not_yet_recorded
Owner: StegVerse-org/LLM-adapter
Required durable evidence: reports/ecosystem-chat-live-activation-status.json must advance from PENDING only after gateway health, durable storage, governed provider use, provider-usage custody and reconstruction, transition custody and reconstruction, and all fail-closed authority checks pass.
Completion artifact: receipts/ecosystem-chat-live-activation.verified.json
Site action after publication: automatic acquisition, canonical-hash validation, gate recomputation, and propagation packet update.
Manual user action required: false
```

## Authority boundary

```text
Site display != execution
provider output != authority
usage retrieval != authority
usage measurement != admissibility
local persistence != custody
submission != custody
pending status != activation
imported verified receipt != deployment authority
propagation packet != publication authority
reconstruction PASS != execution authority
Site autonomy runtime PASS != Ecosystem Chat activation
Site autonomy completion evidence != release authority
```

## Release posture

Repository-local automation for pending-status acquisition, verified-receipt acquisition, validation, activation-state computation, propagation packaging, independent retention reacquisition, cross-artifact consistency validation, strict Site autonomy evidence persistence, and evidence validation is installed. The first stable pending blocker and the Site autonomy seven-check runtime PASS have been observed and validated. Live Ecosystem Chat activation observation, immutable verified receipt publication, Site activation completion, and downstream verified ingestion remain pending. No tag or release is authorized.

## Archive readiness

This handoff, `docs/ECOSYSTEM_CHAT_ACTIVATION_MIRROR_HANDOFF.md`, the adapter and Master-Records handoffs, generated machine-readable state, workflows, strict Site autonomy completion evidence, and repository history preserve all continuation state. This workstream should remain active until the adapter records live activation evidence or publishes the immutable verified receipt, Site recomputes its activation state, and any exact repository-owned failure is repaired.
