# Ecosystem Continuity Panel Mirror Handoff

Updated: 2026-09-11

```text
Parent Goal Task ID: ECOSYSTEM-CONTINUITY-EVALUATOR-001
COSV: 71000000100111
Repository: StegVerse-Labs/Site
Branch: feature/ece-continuity-panel-001
State: SOURCE_IMPLEMENTED / VALIDATION_PENDING / AUTHENTIC PROJECTION ABSENT
Authority effect: NONE_SITE_PROJECTION_ONLY
```

## Purpose

Expose a human-readable Ecosystem Continuity page without moving continuity truth into Site. The page consumes only the previously defined `stegverse.site-ecosystem-continuity-projection.v1` safe projection and remains explicitly unavailable until an authentic retained projection is materialized at the Site projection path.

## Source surfaces

```text
ecosystem-continuity.html
assets/ecosystem-continuity-panel.js
scripts/check_ecosystem_continuity_panel.py
```

## Data contract

The browser attempts one same-origin, no-store read from:

```text
data/ecosystem-continuity/current.json
```

That file is intentionally not created by this source tranche. An authentic resident ECE cycle must first produce and retain the Site-safe projection. A later bounded propagation/materialization step may place those exact safe bytes at the Site read path with provenance; source implementation must not create a synthetic current-state fixture.

Accepted input must satisfy:

```text
schema = stegverse.site-ecosystem-continuity-projection.v1
authority_effect = NONE_READ_ONLY_PROJECTION
source_available = true
continuity_state in canonical projection vocabulary
source_evaluation_id = ece_*
evaluated_at = parseable timestamp
projection_error = null
findings contain only Site-safe v1 finding fields
```

## Fail-closed behavior

The page renders `UNAVAILABLE` rather than continuity state when the projection is missing, HTTP-failed, malformed, wrong-schema, authorizing, source-unavailable, error-bearing, or contains unsafe finding fields. Browser local/session storage is not used, so a prior green projection cannot silently become the current display after the authentic source disappears.

The unavailable state explicitly states that absence of a retained projection is not evidence of either continuity or interruption.

## Authority boundary

- ECE remains continuity-evaluation truth.
- Master Records remains retained reality/custody and reconstruction authority.
- Healer remains scheduling/finding-intake/repair-dispatch owner; dispatch does not prove recovery.
- Site only renders safe retained projection bytes.
- Interlock/InTr remains governed transition authority where applicable.
- TV/TVC remains credential authority.

Site does not calculate continuity, inspect raw evidence/detail, mutate findings, dispatch repairs, certify recovery, obtain credentials, or write Master Records.

## Current evidence boundary

```text
Panel HTML/consumer source: IMPLEMENTED ON BRANCH
Panel source validator: IMPLEMENTED ON BRANCH
Authentic resident ECE schedule slot: NOT OBSERVED
Authentic retained ECE evaluation: NOT OBSERVED
Authentic Master Records ECE custody/reconstruction: NOT OBSERVED
Authentic Site-safe projection bytes: NOT OBSERVED
Current Site data/ecosystem-continuity/current.json: INTENTIONALLY NOT MATERIALIZED BY SOURCE WORK
Public continuity state: NOT CLAIMED
```

## Next

1. Obtain exact-head Site repository validation for this branch and merge only when required lanes pass.
2. Terminalize the Site work claim after merge using only repository-permitted terminalization fields.
3. Continue observing the existing authorized resident Healer reusable scheduler for an authentic `RT-ECOSYSTEM-CONTINUITY-EVALUATION-001` slot receipt.
4. Require exact linked evaluation, Master Records custody/reconstruction, Healer intake, and Site-safe projection artifacts.
5. Materialize only the exact retained Site-safe projection bytes to `data/ecosystem-continuity/current.json` through a separately evidenced bounded path.
6. Verify the public page displays that exact projection; do not infer publication/live rendering from source merge.
7. Recovery remains unverified until a later independent ECE PASS observation.
