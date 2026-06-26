# Site TT Code Representation Mirror

## Assumptions

1. `Admissible-Existence/TT` is the canonical source for Transition Table element identity, registry structure, code references, receipt schemas, fixtures, generated status, and propagation bundles.
2. `StegVerse-Labs/Site` is a public display and ingestion surface. It must not redefine TT semantics.
3. Default handlers are executable fail-closed code surfaces, not completed element-specific governance logic.
4. Any path displayed here without a leading period for iOS compatibility is noted as such.

## Done Definition

This mirror is done when Site can publicly describe the TT code-representation contract, point downstream readers to canonical TT artifacts, and preserve the rule that missing code representation fails closed.

## Mirror Boundary

```text
Admissible-Existence/TT -> canonical transition-element source
StegVerse-Labs/Site -> public mirror and ingestion surface
admissibility-wiki -> explanatory mirror and external-framework crosswalk surface
SPE / SDK -> execution and packaging consumers
```

Site does not become the source of truth for transition-element semantics.

## Canonical TT Artifacts

The TT propagation bundle identifies the canonical artifact set.

```text
dist/transition-element-propagation-bundle.manifest.json
```

The bundle is generated in TT by:

```bash
python scripts/build_transition_element_propagation_bundle.py
```

The Site mirror should consume that bundle or a downstream copy of it rather than maintain a manual copy list.

## Required Element Fields

Each mirrored transition element should preserve these fields from TT:

```text
transition_id
transition_name
transition_family
canonical_status
code_ref
code_strategy
implementation_status
fixture_ref
receipt_schema_ref
allowed_results
propagation_status
```

## Fail-Closed Rule

If Site displays, indexes, or routes a transition element whose canonical TT registry entry lacks a valid `code_ref`, `fixture_ref`, or `receipt_schema_ref`, the mirrored status must mark the element as not operational and downstream evaluators should return `FAIL_CLOSED`.

## Public Meaning

A rendered transition element page or status card proves only that Site has mirrored the current TT record.

It does not prove:

```text
execution authority
commit-time standing
policy validity
delegation validity
evidence sufficiency
recoverability sufficiency
```

Those remain SPE and governance-evaluation concerns.

## iOS Path Note

The workflow path is displayed without the leading period for iOS compatibility:

```text
github/workflows/transition-element-code-validation.yml
```

The canonical TT repository path begins with a leading period.

## Current Build Posture

```text
Admissible-Existence - 92%complete
TT - 86%complete
TT - 86%complete TO GOAL ACTIVATION
```

Site propagation has begun as a public mirror contract. The remaining Site work is to consume a generated TT bundle and render element status from canonical data rather than static text.
