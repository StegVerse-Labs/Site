# Ecosystem Continuity Site Projection Mirror Handoff

Updated: 2026-09-11

```text
Parent Goal Task ID: ECOSYSTEM-CONTINUITY-EVALUATOR-001
COSV: 71000000100111
Repository: StegVerse-Labs/Site
Branch: feature/ece-continuity-site-projection-001
State: SOURCE_IMPLEMENTATION
Authority effect: NONE_READ_ONLY_PROJECTION
```

## Purpose

Consume the canonical `stegverse.ecosystem-continuity-evaluation.v1` artifact without re-evaluating continuity, minting health, or exposing sensitive diagnostic material.

## Invariants

- Site is projection-only; `.github` ECE remains continuity evaluation source.
- Invalid/missing source fails closed to `INDETERMINATE`/unavailable.
- `FAIL`, `NOT_OBSERVED`, `STALE`, `UNKNOWN`, `UNREACHABLE`, and `PROBE_REQUIRED` remain distinct.
- v1 excludes raw evidence locators, free-form diagnostic detail, remediation class, credentials, private KV paths, tokens, callback query material, and sensitive infrastructure identifiers.
- Site does not mark recovery independently and does not mutate ECE or Healer state.

## Source

```text
scripts/project_ecosystem_continuity.py
tests/test_ecosystem_continuity_projection.py
```

Expected future retained projection path:

```text
data/ecosystem-continuity-latest.json
```

That path is not claimed live until an authentic retained ECE evaluation is available and the projection has executed against it.

## Next

Validate this source on exact head, merge only after repository checks pass, then add the user-facing continuity panel against the retained projection. No synthetic green fixture may be published as current ecosystem state.
