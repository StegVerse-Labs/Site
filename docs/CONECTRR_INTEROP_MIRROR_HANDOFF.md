# Conectrr Interoperability Mirror Handoff

## Source of truth

This file is the current task and continuation source of truth for the Conectrr minimum interoperable handoff evaluation within `StegVerse-Labs/Site`.

## Current goal

```text
Goal: prove the smallest interoperable discovery-to-governance handoff
Source role: Conectrr intent-first discovery and recommendation
Destination role: StegVerse independent governance evaluation
Authority effect: NONE
Status: RUNTIME_IMPORT_API_AND_PROJECTION_LOADER_IMPLEMENTED; PAGE_BINDING_AND_LIVE_CONECTRR_OUTPUT_PENDING
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
runtime loader -> imports source and decision without semantic normalization
authority effect -> none
```

`assets/ecosystem-node-views.js` now exposes `importCanonicalEvents(events)`. Imported events are cloned before admission, duplicate identifiers are rejected, unresolved parent references are rejected, and admitted records are frozen. `assets/conectrr-interop.js` loads the independent-evaluation fixture and imports the Conectrr evidence event and StegVerse decision event together while checking that the source object remains unchanged.

## User action

```text
Required now: NONE
Do not manually construct, normalize, copy, or approve a Conectrr record.
```

A real Conectrr output will eventually be needed from Conectrr or an authorized adapter, but that is an interoperability input requirement rather than a current manual repository task for the user.

## Required next work

Destination `StegVerse-Labs/Site`:

```text
Bind assets/conectrr-interop.js into ecosystem-chat.html after ecosystem-node-views.js
Bind check_conectrr_runtime_projection.py into canonical Site application validation
Add browser execution test proving both imported records render
Add browser selection test proving source/decision correlation in both directions
Add source-byte and source-hash preservation at the import boundary
Add reconstruction receipt fixture covering source plus downstream decision
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
Verify hashes, references, ordering, and reconstruction
Issue a receipt proving source and downstream records remain distinct
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
fixture coverage != live interoperability
```

## Archival readiness

This handoff and its referenced executable artifacts preserve the complete continuation state. No additional part of the conversation is required to continue the work.
