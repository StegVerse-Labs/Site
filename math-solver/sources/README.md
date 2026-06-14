# Math-Solver Paper Source Intake

Generated: `2026-06-14`

## Purpose

This directory defines how compiled papers and source materials enter the public math-solver adapter surface.

The goal is to prevent papers from becoming invisible authority. Papers should enter as declared sources with posture, claim limits, related formalisms, and review state.

## Canonical internal paths

```text
GCAT-BCAT-Engine/Publisher/papers
GCAT-BCAT-Engine/workflows
GCAT-BCAT-Engine/workflows/math-solver
```

These paths are referenced here as canonical internal locations for the compiled papers and workflow machinery. The Site remains a public mirror and posture surface.

## Machine-readable registry

```text
math-solver/sources/paper-sources.json
```

The registry starts empty until individual compiled papers are added as structured entries.

## Source posture classes

```text
context
solver_instruction_source
mapped_claim_support
receipt_backed_support
superseded_deprecated
```

## Intake rule

A paper may inform a solver instruction packet, but it does not become proof authority merely because it exists.

Before a paper can support a public claim, it should be mapped to:

```text
source posture
related formalism
claim limit
review state
receipt or test reference, when available
```

## Entry shape

```text
source_id
title
authors_or_source
source_path_or_reference
canonical_location
related_formalisms
posture_class
claim_limit
mapped_claims
use_in_instruction_packets
review_status
last_reviewed
notes
```

## Next stage

1. Add structured entries for the compiled papers already present under `GCAT-BCAT-Engine/Publisher/papers`.
2. Map each paper to RTG, STCM, BCAT, GCAT, CGE, Governance Testing Suite, or Math-Solver Adapter.
3. Mark which papers may be used in instruction packets.
4. Create one paper-backed RTG or STCM instruction packet.
