# Legacy Aggregate Claim Terminalization Mirror Handoff

Updated: 2026-09-03
Repository: `StegVerse-Labs/Site`
Issue: #970

## Purpose

Provide a fail-closed migration path for legacy active claims that still live only in `data/session-work-claims.json` after their underlying work has already completed and merged.

The migration uses a terminalization tombstone stored under `data/session-work-claims.d/`. A tombstone does not replace claim ownership. It may only apply terminal/release metadata to an existing active aggregate claim while inheriting every protected ownership, dependency, handoff, credential, and authority field from that aggregate source.

## Allowed terminalization tombstone fields

Required:

- `claim_id`
- `terminalization_override_of: "canonical_registry"`
- terminal `state`
- positive integer `pull_request`
- non-empty `release_commit`
- non-empty `claim_released_at`

Optional:

- `archive_eligible`

No task, branch, role, dependency surface, claimed path, handoff, credential, authority, activation, or other protected field may be supplied by the tombstone.

## Fail-closed rules

A tombstone is invalid unless its target exists in the canonical aggregate registry and is currently active. Unknown targets, duplicate tombstones, active-to-active changes, missing release evidence, protected-field injection, authority widening, or activation widening fail closed.

The existing full-fragment claim path and the existing #611 terminalization-only mutation path remain unchanged.

## Initial migration target

After this control repair merges, terminalize `SITE-STEGOS-CURRENT-IPHONE-VALIDATOR-949-20260903` using its already-observed completion evidence:

```text
issue: Site #949 CLOSED / completed
pull request: #950
release commit: d4013fbae31aa455a5cf50d73e9e4d9fd0aee261
```

Only after that stale ownership is released may Site #965 reacquire `site:stegos-bootstrap-validator` and merge the exact post-custody successor allowlist.

## Authority

Authority effect: NONE.
Activation effect: NONE.
Credential authority remains TV/TVC.
GitHub token runtime authority remains NONE.
This migration creates no generic claim override mechanism.
