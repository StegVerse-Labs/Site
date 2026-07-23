# Conectrr Interoperability Mirror Handoff

## Source of truth

This file is the current task and continuation source of truth for the Conectrr minimum interoperable handoff evaluation within `StegVerse-Labs/Site`.

## Current goal

```text
Goal: prove the smallest interoperable discovery-to-governance handoff
Source role: Conectrr intent-first discovery and recommendation
Destination role: StegVerse independent governance evaluation
Authority effect: NONE
Status: PAGE_RUNTIME_BROWSER_CORRELATION_EXPORT_REPLAY_DEPLOYED_PUBLICATION_AND_ADAPTER_CONFORMANCE_IMPLEMENTED; LIVE_CONECTRR_OUTPUT_PENDING
```

## Accepted principle

The handoff preserves only the structured context required for a downstream system to independently understand, evaluate, reconstruct, and build upon a recommendation. Overreach and under-specification both fail.

## Implemented artifacts

```text
docs/CONECTRR_MINIMUM_INTEROPERABLE_HANDOFF.md
data/conectrr-minimum-handoff.fixture.json
scripts/check_conectrr_minimum_handoff.py
data/conectrr-boundary-failure-matrix.fixture.json
scripts/check_conectrr_boundary_failure_matrix.py
data/conectrr-independent-evaluation.fixture.json
scripts/check_conectrr_independent_evaluation.py
assets/ecosystem-node-views.js
assets/conectrr-interop.js
scripts/check_conectrr_runtime_projection.py
scripts/check_conectrr_browser_projection.py
scripts/check_conectrr_export_replay.py
scripts/check_conectrr_source_preservation.py
data/conectrr-reconstruction-receipt.fixture.json
scripts/check_conectrr_reconstruction_receipt.py
scripts/check_conectrr_live_routes.py
.github/workflows/conectrr-live-verification.yml
data/conectrr-adapter-conformance.fixture.json
scripts/check_conectrr_adapter_conformance.py
docs/CONECTRR_INTEROP_MIRROR_HANDOFF.md
```

## Verified behavior

```text
minimum valid handoff -> PASS
all declared boundary-overreach classes -> FAIL
all declared under-specification classes -> FAIL
Conectrr source -> evidence event
StegVerse result -> separate decision event
downstream disagreement -> preserved
source mutation -> fail-closed
JSON and JSONL -> distinct source and decision records
canonical import -> clone, validate references, deep-freeze
runtime loader -> loaded after canonical API initialization
browser render -> source and decision both required
browser correlation -> source-to-decision and decision-to-source required
browser export replay -> JSON and JSONL retain both records and their references
canonical source bytes -> stable across import serialization
canonical source SHA-256 -> stable across import serialization
reconstruction receipt -> source and downstream decision reconstructed distinctly
deployed publication workflow -> public runtime assets and observation contract checked after Site Task Runner
adapter conformance -> raw source bytes and semantics preserved without normalization
live-output claim -> false until genuine Conectrr output exists
authority effect -> none
```

`assets/ecosystem-node-views.js` exposes `importCanonicalEvents(events)` and loads `assets/conectrr-interop.js` only after the canonical event API exists. Imported events are cloned before admission, duplicate identifiers are rejected, unresolved parent references are rejected, and admitted records are frozen.

`assets/conectrr-interop.js` loads the independent-evaluation fixture, imports the Conectrr evidence event and StegVerse decision event together, requires both governed records to render, executes bidirectional selection checks using stable event identifiers, and replays the browser-loaded stream through JSON and JSONL. It publishes `data-conectrr-interop="loaded"`, `data-conectrr-browser-test="pass"`, and `data-conectrr-export-replay="pass"` only after the corresponding checks succeed and fails closed otherwise.

`check_conectrr_runtime_projection.py` is bound into canonical Site application validation. It invokes the browser projection, export replay, and adapter conformance validators and requires the deployed-publication verifier and workflow to exist.

`check_conectrr_source_preservation.py` independently canonicalizes the source record before and after import serialization and requires byte equality, SHA-256 equality, semantic equality, and retention of the source-declared hash marker.

`check_conectrr_reconstruction_receipt.py` verifies source-before-decision ordering, stable reference resolution, distinct identities, preserved disagreement, matching source hash, source-byte hash presence, and zero authority effect.

`check_conectrr_live_routes.py` and `.github/workflows/conectrr-live-verification.yml` verify that Pages publishes the canonical runtime, loader, fixture, and observation contract after deployment. This is deployed-publication evidence, not proof that a remote browser executed the fixture and not proof of live external interoperability.

`check_conectrr_adapter_conformance.py` verifies a fixture-only adapter envelope preserves canonical source bytes, digest, semantics, boundary flags, and zero-authority posture. The adapter fixture remains explicitly unauthorized and does not claim live output verification.

## User action

```text
Required now: NONE
Do not manually construct, normalize, copy, approve, or hash a Conectrr record.
```

A real Conectrr output will eventually be needed from Conectrr or an authorized adapter. That is an interoperability input requirement rather than a current manual repository task for the user.

## Required next work

Destination `StegVerse-Labs/Site`:

```text
Observe the first successful Conectrr Live Verification workflow report after Pages propagation
Add an actual remote-browser execution runner for the three runtime dataset markers
Replace fixture source_bytes_hash marker with the exact real-source digest when live output exists
Substitute a genuine Conectrr output into the adapter conformance path without semantic normalization
Generate a live reconstruction receipt from the genuine source and independent downstream decision
```

Destination `Conectrr` or authorized adapter:

```text
Emit the minimum handoff schema directly
Provide stable handoff and source-record identifiers
Populate intent, criteria, constraints, reasoning, evidence, alternatives, confidence, uncertainty, and unresolved dependencies
Keep consent, authority, admissibility, commitment, and execution flags false
Provide one real output fixture for reciprocal evaluation
```

Destination `master-records/orchestration` after live output exists:

```text
Custody the unmodified source handoff
Custody the independent StegVerse decision
Verify hashes, references, ordering, export replay, and reconstruction
Issue a receipt proving source and downstream records remain distinct
```

Downstream publication destinations after verified activation:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
StegVerse-Labs/Site
```

## Pass condition

StegVerse must independently determine what Conectrr recommended, why, from what evidence, with what uncertainty, what remained unresolved, what Conectrr lacked standing to decide, what downstream decision was reached, and whether it agreed or disagreed. The original Conectrr record must remain unchanged.

## Authority boundary

```text
recommendation != consent
recommendation != authority
recommendation != admissibility
recommendation != commitment
recommendation != execution
source import != semantic normalization
record correlation != record merger
downstream disagreement != source mutation
runtime projection != custody
browser fixture PASS != live external interoperability
deployed publication PASS != remote browser execution
adapter fixture conformance != adapter authorization
reconstruction receipt != approval
fixture hash marker != live cryptographic evidence
```

## Archival readiness

This handoff and its referenced executable artifacts preserve the complete continuation state. No additional part of the conversation is required to continue the work.
