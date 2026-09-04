# StegOS Persistent Card UX Mirror Handoff

Updated: 2026-09-04
Repository: StegVerse-Labs/Site
Issue: #1000
Goal: SITE-STEGOS-PERSISTENT-CARD-UX-1000

## Source of truth

This file is the bounded continuation record for Site issue #1000. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`. The completed SV001 custody authority boundary remains `docs/MR_SV001_CURRENT_IPHONE_CUSTODY_MIRROR_HANDOFF.md`.

## Objective

Establish a reusable same-device operational-card UX contract, beginning with `stegos-bootstrap/`.

Required behavior:

```text
logical workflow section -> card
completed card -> green border
incomplete/blocked card -> red border
hydrating card -> neutral temporary state only
completed device-local data -> restored on later visits to this device
reusable text/input/output -> adjacent Copy Text control
purpose/remediation/troubleshooting needed -> dedicated per-card help page
same-device evidence exists -> automatic reuse before manual import
manual paste/import -> fallback/recovery path
```

## Authority boundary

UI persistence, card coloring, copy controls, and help pages create no execution, custody, lease, credential, admission, publication, activation, or sovereign authority. Canonical runtime and Master Records validators remain unchanged.

The previously completed StegVerse-001 bounded-autonomy cycle is terminal and MUST NOT be rerun merely to satisfy Master Records custody.

## Implemented source state — 2026-09-04

Destination `StegVerse-Labs/Site`:

- `stegos-bootstrap/index.html`
  - loads the persistent card UX layer;
  - replaces stale SV001 `READY_WHEN_NODE_ESTABLISHED` presentation with device-history discovery;
  - makes same-device Master Records proof discovery the normal path;
  - retains manual exact-proof import as fallback;
  - prevents normal SV001 rerun once the card state is terminal.
- `stegos-bootstrap/persistent-card-ux.js`
  - uses the existing same-device IndexedDB store;
  - persists per-card snapshots under `ui-card-state:*`;
  - restores completed card data on revisit;
  - applies green borders to completed cards and red borders to incomplete/blocked cards;
  - installs `Copy Text` controls on reusable textarea/pre output surfaces;
  - adds per-card purpose/remediation/troubleshooting links;
  - scans local metadata/journal state for terminal SV001 execution;
  - reuses an exact retained full SV001 proof for the Master Records card when present;
  - preserves `authority_effect: NONE` for UI persistence state.
- `stegos-bootstrap/help/*.html`
  - dedicated pages now exist for all eleven StegOS bootstrap cards.
- `scripts/validate_stegos_persistent_card_ux.py`
  - source validator covers helper loading, red/green contract, copy controls, help pages, same-device persistence, SV001 terminal behavior, and authority boundary markers.

Direct repository reads after the writes confirm the updated bootstrap references `persistent-card-ux.js`, starts SV001 in `CHECKING_DEVICE_HISTORY`, and starts Master Records in `CHECKING_SAME_DEVICE_PROOF`.

## Important legacy-evidence boundary

The new persistence layer retains exact completed output from this point forward. A completed SV001 cycle that predates this UI persistence layer may be discoverable as terminal from the existing local journal/metadata even when the complete proof object itself was not previously stored as a UI snapshot.

In that legacy case:

```text
SV001 terminal state -> retained / rerun prohibited
exact full proof snapshot -> may be absent
Master Records manual exact-proof import -> allowed fallback
```

Do not synthesize missing immutable proof fields. Any future recovery from older journal data must be hash-verifiable against the already-recorded immutable receipt hash before it may replace manual import.

## Collision rule

Do not alter canonical Master Records validation logic or WorkerCoordinator/TVC authority semantics. Do not claim authentic runtime execution from source/UI changes. Preserve existing interaction-guard ownership and exact current-iPhone mutation fencing.

## Completion predicates

1. Every StegOS bootstrap workflow section is represented as a stateful card. SOURCE IMPLEMENTED.
2. Card completion state deterministically maps to green/red border semantics after hydration. SOURCE IMPLEMENTED.
3. Completed card data survives reload/revisit on the same device. SOURCE IMPLEMENTED; LIVE BROWSER REVISIT PROOF PENDING.
4. Reusable text surfaces expose Copy Text. SOURCE IMPLEMENTED.
5. Dedicated help routes exist for cards needing explanation/remediation/troubleshooting. SOURCE IMPLEMENTED.
6. SV001 completed state is restored and does not present rerun as the normal path. SOURCE IMPLEMENTED; LIVE SAME-DEVICE PROOF PENDING.
7. Master Records auto-discovers same-device completed SV001 proof when available; exact manual import remains fallback. SOURCE IMPLEMENTED; LIVE SAME-DEVICE PROOF PENDING.
8. No authority boundary changes. VERIFIED BY SOURCE INSPECTION.

## Remaining files/modules to install or verify

Destination `StegVerse-Labs/Site`:

- add `persistent-card-ux.js` and the help routes to the explicit offline-shell/service-worker cache manifest;
- execute `scripts/validate_stegos_persistent_card_ux.py` in repository validation;
- observe one deployed iPhone reload/revisit showing persisted completed-card data;
- observe green/red border transitions in the deployed browser;
- observe Copy Text on generated outputs in the deployed browser;
- observe per-card help navigation in the deployed browser;
- verify terminal SV001 remains non-runnable after interaction-guard hydration;
- verify Master Records auto-fills from an exact same-device persisted SV001 proof when one is present;
- optionally implement hash-verifiable recovery of the legacy pre-persistence cycle receipt from retained journal data instead of requiring one-time manual import;
- after the StegOS pattern is browser-validated, roll the same reusable card contract across other operational Site workflow pages rather than reimplementing it independently.

Downstream only after this UI contract is validated and when the relevant release/propagation gate is reached:

- `StegVerse-Labs/Sit`
- `GCAT-BCAT-Engine/Publisher`
- `StegVerse-Labs/admissibility-wiki`
- `StegVerse-002/stegguardian-wiki`

## Archive readiness

Source implementation is materially advanced but issue #1000 is not archive-ready because deployed same-device browser validation and explicit offline-shell cache installation remain open.
