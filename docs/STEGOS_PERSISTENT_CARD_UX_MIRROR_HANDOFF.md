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

## Initial implementation scope

Destination `StegVerse-Labs/Site`:

- `stegos-bootstrap/index.html`
- reusable same-device card-state/persistence helper under `stegos-bootstrap/`
- card-specific help pages under `stegos-bootstrap/help/`
- exact copy controls for reusable text surfaces
- automatic restoration of card data from the existing same-device journal/local state where available
- Master Records same-device completed-proof reuse before manual import

## Collision rule

Do not alter canonical Master Records validation logic or WorkerCoordinator/TVC authority semantics. Do not claim authentic runtime execution from source/UI changes. Preserve existing interaction-guard ownership and exact current-iPhone mutation fencing.

## Completion predicates

1. Every StegOS bootstrap workflow section is represented as a stateful card.
2. Card completion state deterministically maps to green/red border semantics after hydration.
3. Completed card data survives reload/revisit on the same device.
4. Reusable text surfaces expose Copy Text.
5. Dedicated help routes exist for cards needing explanation/remediation/troubleshooting.
6. SV001 completed state is restored and does not present rerun as the normal path.
7. Master Records auto-discovers same-device completed SV001 proof when available; exact manual import remains fallback.
8. No authority boundary changes.

## Remaining files/modules to install

Destination `StegVerse-Labs/Site`:

- persistent card-state helper
- bootstrap card markup/state integration
- help pages and help navigation
- validation coverage for persistence/copy/card-state semantics

## Archive readiness

Not archive-ready until the implementation, validation, and repository handoff updates for issue #1000 are complete.
