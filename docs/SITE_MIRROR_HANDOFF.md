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
Result: ACTIVATION_PENDING_AUTHORIZED_REAL_PROVIDER_AND_PERSISTENT_ENDPOINT
Manual user action required for routine repository work: false
```

## Required vertical slice

```text
real request
-> governed real-provider response
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
Runtime gateway, canonical StegDeploy runtime, provider broker, portable-node runtime, and activation evidence: StegVerse-org/LLM-adapter
Custody and reconstruction: master-records/orchestration
Site activation projection: StegVerse-Labs/Site
Publication projection: GCAT-BCAT-Engine/Publisher
Admissibility projection: StegVerse-Labs/admissibility-wiki
Guardian projection: StegVerse-002/stegguardian-wiki
```

## Canonical components

Adapter runtime and evidence:

```text
Dockerfile
compose.stegdeploy.yaml
scripts/container-entrypoint.sh
scripts/stegdeploy_bootstrap.py
.github/workflows/stegdeploy-image.yml
.github/workflows/ecosystem-chat-live-activation.yml
.github/workflows/validate.yml
llm_adapter/combined_gateway.py
llm_adapter/governed_provider.py
llm_adapter/master_records_client.py
llm_adapter/transition_store.py
scripts/verify_live_ecosystem_chat_activation.py
scripts/write_live_activation_status.py
scripts/check_stegdeploy_image_receipt_retention.py
scripts/write_provider_readiness_status.py
receipts/stegdeploy-image-publication.json
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
scripts/sync_ecosystem_chat_custody_state.py
```

## Current verified evidence posture

```text
Canonical provider-neutral StegDeploy runtime: IMPLEMENTED and MERGED
Canonical image build and publication: VERIFIED
Repository-retained image publication receipt: VERIFIED
Published image digest: sha256:71a77c2b10762fa070f01ad2f2314b9f7989f62821e972f75f2a0991b237936e
Canonical package anonymous pull compatibility: NOT VERIFIED
Portable-node health-bound advertisement: IMPLEMENTED and MERGED
Site portable-node discovery and local runtime binding: VERIFIED
Governed gateway request with deterministic provider fallback: VERIFIED
Local transition persistence: VERIFIED
Authenticated transition custody: VERIFIED
Transition reconstruction: VERIFIED
Real governed provider response: NOT VERIFIED
Provider-usage persistence from real provider use: NOT VERIFIED
Provider-usage custody: NOT VERIFIED
Provider-usage reconstruction: NOT VERIFIED
Adapter immutable zero-blocker VERIFIED receipt: NOT OBSERVED
Site ACTIVATION_COMPLETE: NOT OBSERVED
Downstream verified ingestion: NOT OBSERVED
```

Custody and reconstruction were verified through `master-records/orchestration` Runtime Evidence Validation run `29865690620`, merge `421da84784888e3dc9bb98a7b2b47a1518f0eee0`, with authenticated custody `RECORDED` and reconstruction `PASS`. Provider execution remained disabled during that run.

## Canonical image publication evidence

The canonical image workflow successfully retained:

```text
receipt: receipts/stegdeploy-image-publication.json
source commit: e1628dcd5635b1e3f0d7f7fabed3ba616b4951f5
retention commit: fdaf8568c18c4546a76cf08462f53a551b1d1fc4
publication run: 29859044640
image: ghcr.io/stegverse-org/llm-adapter
digest: sha256:71a77c2b10762fa070f01ad2f2314b9f7989f62821e972f75f2a0991b237936e
package visibility asserted: false
authority effect: IMAGE_PUBLICATION_ONLY
```

```text
publication receipt retention != package visibility
package visibility != deployment authority
container publication != live deployment
```

## Provider readiness boundary

The governed provider now requires every configuration gate to pass before any network call:

```text
STEGVERSE_PROVIDER_ENABLED=true
STEGVERSE_PROVIDER_ENDPOINT uses HTTPS
endpoint hostname exists
STEGVERSE_PROVIDER_ALLOWED_HOSTS is non-empty
endpoint hostname is explicitly included in STEGVERSE_PROVIDER_ALLOWED_HOSTS
STEGVERSE_PROVIDER_TOKEN is configured
STEGVERSE_PROVIDER_MODEL is configured
cost, quota, input, and output limits pass
```

An empty hostname allowlist is fail-closed. Earlier behavior that allowed any HTTPS hostname when the allowlist was empty has been removed.

Provider readiness implementation:

```text
StegVerse-org/LLM-adapter@15172dc2e69a604a4b419b8098911a97ab38488b explicit allowlist and readiness contract
StegVerse-org/LLM-adapter@7999fbfe3824cee63d6db13e493314f1133d44c5 provider readiness and fail-closed tests
StegVerse-org/LLM-adapter@be94e104e8ae44953c2044a7b84dbdfabe82f45a secret-free readiness status writer
StegVerse-org/LLM-adapter@091e0789140ce7c1376f1a911382c252a0dd310b canonical provider-boundary verification
```

Readiness status is configuration evidence only:

```text
credential value retained = false
provider contact attempted = false
provider response verified = false
custody verified by readiness status = false
authority granted = false
execution authority = false
activation authority = false
```

## Verified activation receipt gates

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

Invalid, conflicting, stale, simulated, or authority-escalating evidence is rejected.

## Site-local completion and downstream propagation

Until all activation gates pass:

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
1. StegVerse-org/LLM-adapter issue #18 owns the remaining live-provider and persistent-endpoint path.
2. Reuse the canonical StegDeploy runtime and governed provider broker.
3. Supply an already-authorized real-provider HTTPS endpoint, explicit hostname allowlist, credential, model, and bounded cost policy only through an authorized runtime environment.
4. Run scripts/write_provider_readiness_status.py and retain the exact secret-free blocker set.
5. When readiness is READY, execute one governed request through the existing gateway and verified custody path.
6. Retain the first exact provider, usage-persistence, provider-usage custody, reconstruction, or activation-receipt failure.
7. Expose a persistent authorized endpoint and point the existing live verifier at it.
8. Site imports and validates the first zero-blocker immutable VERIFIED receipt automatically.
9. Site recomputes activation and propagation state.
10. Publisher and both wiki consumers ingest the Site projection automatically.
11. Release readiness remains fail-closed until downstream verified evidence exists.
```

No browser credential, copy/paste, workflow dispatch, artifact download, image build, node installation, node start, screenshot confirmation, receipt construction, blocker transcription, or manual publication task is assigned to the user.

## Authority boundary

```text
Site display != execution
provider readiness != provider authorization
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

The Site includes an operator-local convenience surface:

```text
chat-session-launcher.html
docs/CHATGPT_SESSION_LAUNCHER.md
scripts/check_chat_session_launcher.py
```

It stores a validated `https://chatgpt.com/c/<conversation-id>` URL in browser local storage only and does not inject prompts, transmit the private identifier, authenticate ChatGPT, grant Site execution authority, create custody, or produce activation evidence.

## Current blocker and next executable step

```text
Blocker: no repository evidence establishes an authorized real-provider HTTPS endpoint, explicit hostname allowlist, credential, model, and bounded cost policy in a persistent authorized runtime environment
Owner: StegVerse-org/LLM-adapter issue #18
Next step: produce the secret-free provider readiness status from the authorized runtime; when READY, execute one real governed provider request through the already-verified transition custody and reconstruction path and retain the first exact downstream failure
Manual user action required for routine repository work: false
```

## Release posture

No tag or release is authorized. Remaining conditions are authorized real-provider execution, provider-usage persistence and custody, provider-usage reconstruction, persistent endpoint verification, immutable zero-blocker activation receipt publication, Site activation completion, and verified downstream ingestion.

## Archive readiness

This handoff, the active build-goal records, custody cycle record, adapter issue #18, canonical image publication receipt, provider readiness contract, immutable activation receipt paths, Site machine-readable state, and repository history preserve all continuation state without requiring conversation context.
