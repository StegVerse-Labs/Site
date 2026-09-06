# StegOS Persistent Card UX Mirror Handoff

Updated: 2026-09-05
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

UI persistence, card coloring, copy controls, help pages, and offline caching create no execution, custody, lease, credential, admission, publication, activation, or sovereign authority. Canonical runtime and Master Records validators remain unchanged.

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
  - source validator covers helper loading, red/green contract, copy controls, help pages, same-device persistence, SV001 terminal behavior, authority boundary markers, and explicit offline-shell completeness.

Direct repository reads after the writes confirm the updated bootstrap references `persistent-card-ux.js`, starts SV001 in `CHECKING_DEVICE_HISTORY`, and starts Master Records in `CHECKING_SAME_DEVICE_PROOF`.

## Important legacy-evidence boundary

The persistence layer retains exact completed output from this point forward. A completed SV001 cycle that predates this UI persistence layer may be discoverable as terminal from the existing local journal/metadata even when the complete proof object itself was not previously stored as a UI snapshot.

In that legacy case:

```text
SV001 terminal state -> retained / rerun prohibited
exact full proof snapshot -> may be absent
Master Records manual exact-proof import -> allowed fallback
```

Do not synthesize missing immutable proof fields. Any future recovery from older journal data must be hash-verifiable against the already-recorded immutable receipt hash before it may replace manual import.

## Machine preflight and README completeness — 2026-09-05

Before the offline-shell continuation was mutated, the current canonical state was reconciled against this handoff, the Master Records task `MR-STEGVERSE001-BOUNDED-AUTONOMY-001`, current Site claim state, and cross-task coordination. The result was `REUSE_OR_EXTEND_EXISTING`: continue this existing #1000 capability and do not create a duplicate task.

Durable preflight evidence: Site issue #1000 comment `5555874931`.

README impact determination:

```text
readme_impact_required: true
material_function_change: true
readme_path: README.md
readme_updated_in_change_set: true
reason: explicit offline capability and service-worker cache refresh behavior change materially
```

`README.md` is therefore part of the same change set and documents the offline operational-card capability, cache-generation semantics, same-device proof reuse, terminal-SV001 rule, and non-authority boundary.

## Explicit offline-shell continuation — 2026-09-05

The existing #1000 implementation has now been installed into the explicit StegOS service-worker shell on branch `continue/site1000-offline-shell`.

Source facts:

```text
predecessor service-worker blob: 048ae96f211e28314fa91c6a34cbc29ec13a2a26
predecessor cache: stegos-web-bootstrap-v10
current branch service-worker blob: 9fdb5a580002c3a881f1523938ab1c0bcb127546
current branch cache: stegos-web-bootstrap-v11
persistent-card-ux.js: EXPLICIT_SHELL_ASSET
all eleven help routes: EXPLICIT_SHELL_ASSETS
```

The legacy exact-identity StegOS projection validator admits only the exact new service-worker blob `9fdb5a580002c3a881f1523938ab1c0bcb127546`; no wildcard, prefix, or semantic-equivalence admission was added.

A bounded validation-only workflow, `.github/workflows/validate-stegos-persistent-card-ux.yml`, executes the existing #1000 source validator and the legacy exact-projection validator without credentials, repository writeback, schedule, deployment, or runtime authority.

This source change does not prove that any deployed/current iPhone has installed v11, does not establish Master Records custody, and does not establish SV002 disposition.

## Collision rule

Do not alter canonical Master Records validation logic or WorkerCoordinator/TVC authority semantics. Do not claim authentic runtime execution from source/UI/cache changes. Preserve existing interaction-guard ownership and exact current-iPhone mutation fencing. The shared `.github/workflows/validate.yml` is not modified by this continuation.

## Completion predicates

1. Every StegOS bootstrap workflow section is represented as a stateful card. **SOURCE IMPLEMENTED.**
2. Card completion state deterministically maps to green/red border semantics after hydration. **SOURCE IMPLEMENTED.**
3. Completed card data survives reload/revisit on the same device. **SOURCE IMPLEMENTED; LIVE BROWSER REVISIT PROOF PENDING.**
4. Reusable text surfaces expose Copy Text. **SOURCE IMPLEMENTED.**
5. Dedicated help routes exist for cards needing explanation/remediation/troubleshooting. **SOURCE IMPLEMENTED.**
6. SV001 completed state is restored and does not present rerun as the normal path. **SOURCE IMPLEMENTED; LIVE SAME-DEVICE PROOF PENDING.**
7. Master Records auto-discovers same-device completed SV001 proof when available; exact manual import remains fallback. **SOURCE IMPLEMENTED; LIVE SAME-DEVICE PROOF PENDING.**
8. Persistent-card helper and all eleven help routes are explicit service-worker shell assets. **SOURCE IMPLEMENTED; VALIDATION PENDING.**
9. Exact v11 service-worker successor is admitted without widening exact-identity validation. **SOURCE IMPLEMENTED; VALIDATION PENDING.**
10. README completeness accompanies the material offline-capability change. **SOURCE IMPLEMENTED; VALIDATION PENDING.**
11. No authority boundary changes. **VERIFIED BY SOURCE INSPECTION; VALIDATION PENDING.**

## Remaining files/modules to install or verify

Destination `StegVerse-Labs/Site`:

- execute `scripts/validate_stegos_persistent_card_ux.py` and exact StegOS projection validation in repository validation;
- merge the validated offline-shell continuation and release its active claim;
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

Issue #1000 is not archive-ready. Offline-shell source installation is implemented but repository validation/merge and deployed same-device browser predicates remain open. Authentic Master Records custody/reconstruction and SV002 disposition are separate runtime predicates and are not inferred here.
