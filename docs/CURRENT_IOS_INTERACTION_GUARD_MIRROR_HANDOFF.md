# Current iOS Interaction Guard Mirror Handoff

Updated: 2026-09-04
Repository: `StegVerse-Labs/Site`
Issue: #991
Canonical coordinator: `StegVerse-Labs/.github#922`

## Purpose

Make the organization-level current-iPhone interaction serialization physically enforceable in the StegOS bootstrap UI. This prevents independent chat sessions or stale page scripts from exposing competing state-changing controls on the same physical iPhone.

## Current canonical posture

The organization queue is `HOLD_UI_ORCHESTRATION_CONFLICT`. No current-iPhone state mutation is admitted. The Site projection must therefore default all mutation controls to disabled/read-only and expose only read-only journal/evidence operations.

## Authority boundary

This guard is a UI serialization mechanism only. It grants no WorkerCoordinator, InTr, TV/TVC, HB, custody, execution, publication, activation, claim/fence, receiving, routing, or credential authority.

Credential authority remains `TV/TVC`.
GitHub token runtime authority remains `NONE`.
No second user-operated machine is required.

## Required UI contract

1. `stegos-bootstrap/current-ios-interaction-manifest.json` is the Site projection of the canonical organization queue.
2. Missing, malformed, unsupported, or HOLD manifest state fails closed.
3. Every state-mutating control is disabled in static HTML before JavaScript runs.
4. Mutation-associated input fields are read-only unless their exact action is admitted.
5. The guard re-applies disabled/read-only state when other scripts attempt to change controls.
6. At most one exact mutation control may be enabled when the manifest is `ADMITTED_SINGLE_ACTION`.
7. An admitted action is locally single-consumption: one click may dispatch it, then the UI returns to local fail-closed until a new manifest/action is observed.
8. Read-only `Replay Local Journal`, `Show Evidence Bundle`, and evidence-copy operations remain separate.
9. Stale session instructions cannot override the manifest.
10. Source merge or validation does not prove public propagation or device enforcement.

## Incident basis

The current-iPhone page was observed showing the protected SV001 repeat-checkout denial while the Master Records input contained JavaScript module text and the custody surface returned an `Invalid JSON` parse error. That parse failure does not prove custody or journal mutation. It demonstrates that repo-level instruction serialization without page-level enforcement is insufficient.

## Completion predicates for #991

- current-main bootstrap loads the guard;
- all mutation controls default disabled;
- guarded inputs default read-only;
- a visible coordinator state/action panel is present;
- HOLD manifest permits zero mutation controls;
- guard blocks stale re-enable attempts and duplicate action dispatch;
- bounded source validator passes;
- merge completed;
- public/device observation remains a separate post-merge predicate.
