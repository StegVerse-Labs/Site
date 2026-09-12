# Ecosystem Continuity Current Materializer Mirror Handoff

Updated: 2026-09-12

```text
Goal Task ID: SITE-ECE-CURRENT-PROJECTION-MATERIALIZER-001
Parent Task ID: ECOSYSTEM-CONTINUITY-EVALUATOR-001
COSV: 71000000102000
Repository: StegVerse-Labs/Site
State: SOURCE IMPLEMENTED / VALIDATION PENDING
Authority effect: NONE_COPY_ONLY
GitHub runtime authority: NONE
```

## Purpose

Provide the bounded last-mile copy from an already-retained Site-safe ECE projection to the served Site data namespace expected by `ecosystem-continuity.html`.

## Source

```text
scripts/materialize_ecosystem_continuity_current.py
tests/test_ecosystem_continuity_materializer.py
```

## Contract

The materializer requires a completed `stegverse.healer-ecosystem-continuity-cycle/v1` receipt, an exact projection path matching `site_projection_ref`, and byte-for-byte SHA-256 equality with `site_projection_sha256`. It validates the safe projection schema/authority contract and atomically copies the exact input bytes to `<served-site-root>/data/ecosystem-continuity/current.json`.

It emits `stegverse.site-ecosystem-continuity-materialization-receipt.v1` with `authority_effect=NONE_COPY_ONLY`, `continuity_recalculated=false`, `live_publication_observed=false`, and `recovery_verified=false`.

## Trust boundaries

- The materializer never calculates or changes continuity.
- The SDK/ECE/Master Records chain remains upstream authority for the retained state.
- Source repository writeback is forbidden when the source root is supplied.
- A materialization receipt does not prove the public page was reachable or rendered the bytes.
- Missing/mismatched receipt, reference, hash, schema, authority, or unsafe finding fields fail closed.
- No checked-in `data/ecosystem-continuity/current.json` is created by source work.

## Next

Pass exact-head Site validation and merge. Then bind the existing resident Healer ECE cycle to invoke this materializer against the existing served Site runtime root. Authentic materialization/public rendering remains unproven until retained runtime evidence exists.
