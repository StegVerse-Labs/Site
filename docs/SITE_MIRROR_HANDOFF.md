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
Result: ACTIVATION_PENDING_LIVE_MACHINE_EXECUTION
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
Runtime gateway, canonical StegDeploy runtime, portable-node runtime, and activation evidence: StegVerse-org/LLM-adapter
Custody and reconstruction: existing Master-Records implementation referenced by adapter evidence
Site activation projection: StegVerse-Labs/Site
Publication projection: GCAT-BCAT-Engine/Publisher
Admissibility projection: StegVerse-Labs/admissibility-wiki
Guardian projection: StegVerse-002/stegguardian-wiki
```

## Canonical existing components reused

Adapter runtime and evidence:

```text
Dockerfile
compose.stegdeploy.yaml
scripts/container-entrypoint.sh
scripts/stegdeploy_bootstrap.py
.github/workflows/stegdeploy-image.yml
llm_adapter/node_bootstrap.py
llm_adapter/node_service.py
.github/workflows/ecosystem-chat-live-activation.yml
.github/workflows/validate.yml
scripts/verify_live_ecosystem_chat_activation.py
scripts/write_live_activation_status.py
scripts/check_stegdeploy_image_receipt_retention.py
reports/ecosystem-chat-live-activation-status.json
receipts/stegdeploy-image-publication.json after successful publication retention
receipts/ecosystem-chat-live-activation.latest.json
receipts/ecosystem-chat-live-activation.verified.json when VERIFIED
```

Site activation consumers:

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

## Non-canonical overlapping packaging retained pending approval

```text
Dockerfile.portable-node
.github/workflows/publish-portable-node-image.yml
```

These files overlap the canonical StegDeploy packaging from merged adapter PR #14. They are not designated canonical and must not be removed, replaced, or consolidated without an explicit removal proposal and approval.

## Heartbeat boundary

The StegVerse runtime heartbeat is not defined, generated, scheduled, or authorized by GitHub Actions, container publication, portable-node process supervision, or Site evidence consumers.

```text
GitHub Actions cron != runtime heartbeat
workflow execution record != runtime heartbeat
container image publication != runtime heartbeat
portable-node supervisor != runtime heartbeat
repository commit frequency != runtime heartbeat
Site evidence watcher != runtime heartbeat watchdog
```

The adapter's live verifier and Site watcher consume activation evidence only. They do not determine heartbeat cadence, continuity, authority, or existence.

## Current exact evidence posture

```text
Canonical provider-neutral StegDeploy runtime: IMPLEMENTED and MERGED
Portable-node zero-touch bootstrap: IMPLEMENTED and MERGED
Portable-node autonomous lifecycle: IMPLEMENTED and MERGED
Portable-node autostart: IMPLEMENTED and MERGED
Portable-node authorized external binding: IMPLEMENTED
Portable-node authorized environment preservation: IMPLEMENTED
Adapter live verifier: IMPLEMENTED
Validation-owned evidence retention: IMPLEMENTED
Canonical image publication receipt repository retention: IMPLEMENTED; FIRST RETAINED RECEIPT NOT YET OBSERVED
Canonical package anonymous pull compatibility: NOT VERIFIED
Current real provider request/response: NOT VERIFIED
Provider-usage custody: NOT VERIFIED
Provider-usage reconstruction: NOT VERIFIED
Transition custody: NOT VERIFIED
Transition reconstruction: NOT VERIFIED
Adapter immutable VERIFIED receipt: NOT OBSERVED
Site ACTIVATION_COMPLETE: NOT OBSERVED
Downstream verified ingestion: NOT OBSERVED
Manual user action required: false
```

The retained stable adapter status remains `PENDING` with blocker `live_activation_observation_not_yet_recorded`. The last deployed endpoint evidence remains HTTP 404 with `x-render-routing: no-server`, confirming that the configured Render hostname has no attached application server.

The repository now has a canonical Render-independent deployment contract, but no connected authorized machine executor has run:

```text
python scripts/stegdeploy_bootstrap.py deploy
```

with authorized provider and Master-Records environment and exposed the resulting endpoint for verification.

## Canonical image publication receipt retention

The canonical image publication workflow now retains a hash-bound publication receipt in the adapter repository after a successful publication run:

```text
StegVerse-org/LLM-adapter@6a1bd64a93a0ac4c83debe68d17be5b37de8daff workflow retention
StegVerse-org/LLM-adapter@78ba620da51dbcc1d2f03381648961d26dbe0fa6 retention validator
StegVerse-org/LLM-adapter@b376d5b24ebec25b5615cba1d0cdc65634193c08 canonical validation binding
```

Receipt boundary:

```text
repository-retained digest discovery = enabled after successful publication run
package visibility asserted = false
anonymous pull authorization asserted = false
provider credentials embedded = false
Master-Records credentials embedded = false
authority effect = IMAGE_PUBLICATION_ONLY
persistent deployment authority = false
activation evidence = false
```

This repairs the prior condition where the canonical publication receipt existed only as a temporary workflow artifact. It does not prove that `ghcr.io/stegverse-org/llm-adapter:main` is publicly pullable, and it does not satisfy persistent host, provider, custody, reconstruction, activation, or downstream-ingestion gates.

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

## Machine-owned continuation

```text
1. StegVerse-org/LLM-adapter issue #18 owns deployment recovery.
2. Reuse the canonical StegDeploy runtime before any new deployment architecture.
3. Observe the first successful canonical image publication run and repository-retained publication receipt.
4. Treat package visibility separately; do not infer anonymous pull authorization from publication or receipt retention.
5. Connect an already-authorized machine executor to scripts/stegdeploy_bootstrap.py deploy.
6. Supply provider and Master-Records configuration only through the authorized runtime environment.
7. Expose the resulting gateway endpoint.
8. Point the existing live verifier at that endpoint.
9. Retain the exact semantic blocker or first zero-blocker VERIFIED receipt automatically.
10. Site imports and validates the receipt automatically.
11. Site recomputes activation and propagation state.
12. Publisher and both wiki consumers ingest the Site projection automatically.
13. Release readiness remains fail-closed until downstream verified evidence exists.
```

No browser credential, copy/paste, workflow dispatch, artifact download, image build, node installation, node start, screenshot confirmation, receipt construction, blocker transcription, credential copying, or manual publication task is assigned to the user.

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
container publication != live deployment
portable-node supervision != heartbeat authority
imported verified receipt != deployment authority
propagation packet != publication authority
reconstruction PASS != execution authority
Site autonomy runtime PASS != Ecosystem Chat activation
Site autonomy completion evidence != release authority
publication receipt retention != package visibility
package visibility != deployment authority
```

## Browser-local ChatGPT session continuation

The Site now includes an operator-local convenience surface for reopening one specific existing web ChatGPT conversation:

```text
chat-session-launcher.html
docs/CHATGPT_SESSION_LAUNCHER.md
scripts/check_chat_session_launcher.py
```

Implementation commits:

```text
9d01610a54960fcefb74e2c98a6f252c7b6bfc53 launcher page
81f3e739cd3db58e67d8c0310dfa5e9b61443a8a launcher contract
5f782e2bed3d6d1f865b3936aa925302ffaddb1d launcher static validator
449a277a915d2fabca6a86091a21e5ac6c971942 canonical application-validator integration
153658d3775aa30074af4ac180925ecff8454e59 navigation integration
34654a9be3cd072fa68dd260b59356afd9ab7fcf navigation and handoff validation
```

Launcher boundary:

```text
private conversation URL storage = browser localStorage only
accepted target = https://chatgpt.com/c/<conversation-id>
query and fragment retention = false
repository persistence = false
StegVerse transmission = false
prompt injection or submission = false
ChatGPT authentication authority = false
Site execution authority = false
custody = none
activation evidence = none
```

This launcher does not replace, advance, or satisfy the governed Ecosystem Chat provider, persistence, custody, reconstruction, immutable receipt, activation, or downstream propagation gates. It is independently useful operator continuation scaffolding with a complete page, contract, and static validator.

## Current blocker and next executable step

```text
Blocker: no connected authorized machine executor has launched the canonical StegDeploy runtime and exposed a live endpoint; the configured Render hostname still returns x-render-routing: no-server
Owner: StegVerse-org/LLM-adapter issue #18
Next step: observe the first repository-retained canonical image publication receipt, then execute the canonical StegDeploy bootstrap on an already-authorized persistent machine runtime, supply authorized provider and Master-Records environment, expose the endpoint, and allow the existing verifier and retention path to proceed automatically
Manual user action required: false
```

## Release posture

No tag or release is authorized. Existing deployment packaging, image publication receipt retention, acquisition, validation, activation-state computation, propagation packaging, retention, custody checks, reconstruction checks, downstream consumers, and browser-local session continuation are retained. Remaining conditions are first retained image-publication evidence, persistent live machine execution, a current real runtime result, immutable VERIFIED receipt publication, Site activation completion, and verified downstream ingestion.

## Archive readiness

This handoff, the paired build-goal and active-building records, adapter issue #18, stable adapter status, canonical image publication receipt path, immutable activation receipt path, Site machine-readable state, launcher implementation contract, canonical launcher validation, and repository history preserve all continuation state without requiring conversation context.
