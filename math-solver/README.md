# StegVerse Math-Solver Governance Adapter

Generated: `2026-06-14`

## Purpose

The Math-Solver Governance Adapter is the public Site layer for describing how StegVerse can govern solver or model actions during formalism development.

The adapter is meant to prevent free-form model authority. A solver or model should not simply generate claims. It should receive a declared instruction packet, return a bounded artifact, and have that artifact classified before it becomes a claim, receipt, or next instruction.

## Boundary

```text
Site         = public mirror
Math-Solver  = adapter concept / research-note posture
STCM         = conservation and replay continuity rule
RTG          = candidate geometry / formalism target
CGE          = future decision and enforcement manager
Proof        = formalism-tests or future adapter authority with receipts
```

The public math-solver pages do not claim solver correctness, completed proof, external verification, or production authority.

## Canonical internal paths

```text
GCAT-BCAT-Engine/Publisher/papers
GCAT-BCAT-Engine/workflows
GCAT-BCAT-Engine/workflows/math-solver
```

The Site references these paths as source posture and workflow context. The Site does not become the authority for those internal sources.

## Governed action chain

```text
formalism state
→ governed instruction packet
→ solver or model task
→ returned artifact
→ claim/cost confirmation
→ receipt or replay posture
→ next admissible instruction
```

## Public pages

| Page | Purpose |
|---|---|
| `math-solver/index.html` | Public posture page for the adapter concept. |
| `math-solver/papers.html` | Public posture page for papers and formalism sources. |
| `math-solver/adapter-manifest.json` | Machine-readable adapter manifest. |
| `math-solver/sources/README.md` | Paper/source intake rules. |
| `math-solver/sources/paper-sources.json` | Machine-readable paper/source registry scaffold. |
| `math-solver/templates/index.md` | Packet template index. |
| `math-solver/examples/index.md` | Example packet lifecycle index. |

## Current posture

```text
Claim id: MATH-SOLVER-ADAPTER-001
Posture: RESEARCH_NOTE
Status: published as public adapter concept only
```

## Source intake

Compiled papers and source material should enter through:

```text
math-solver/sources/paper-sources.json
```

A source entry should declare title, source, canonical location, related formalisms, posture class, claim limit, mapped claims, review status, and whether it may be used in instruction packets.

## Packet templates

The first public packet templates are now present:

| Packet | Path | Purpose |
|---|---|---|
| instruction_packet | `math-solver/templates/instruction-packet.template.json` | Declares what the solver/model is allowed to attempt. |
| artifact_return | `math-solver/templates/artifact-return.template.json` | Declares what the solver/model returned and what claim is attempted. |
| admissibility_result | `math-solver/templates/admissibility-result.template.json` | Declares what the returned artifact is allowed to become. |

## Example lifecycle

The first static example lifecycle is present:

| Example | Instruction | Artifact return | Admissibility result | Posture |
|---|---|---|---|---|
| RTG observer-window sketch | `math-solver/examples/rtg-observer-window.instruction.json` | `math-solver/examples/rtg-observer-window.artifact-return.json` | `math-solver/examples/rtg-observer-window.admissibility-result.json` | RESEARCH_NOTE |

This example is not a real solver run and does not assert proof. It exists to show the governed packet lifecycle.

## Packet boundary

The adapter supports three packet classes:

```text
instruction_packet
artifact_return
admissibility_result
```

### instruction_packet

Declares what the solver/model is allowed to attempt.

Suggested fields:

```text
schema
packet_id
formalism_id
task_type
declared_goal
allowed_operations
source_context
expected_artifact
claim_limit
review_requirement
created_at
```

### artifact_return

Declares what the solver/model returned and what claim, if any, is being attempted.

Suggested fields:

```text
schema
packet_id
artifact_id
artifact_type
summary
claim_made
claim_posture
cost_or_effort_note
open_gaps
returned_at
```

### admissibility_result

Declares whether the artifact can become a public claim, a next instruction, or only a draft/research note.

Suggested fields:

```text
schema
packet_id
decision
posture
reason
allowed_next_state
receipt_reference
```

## Papers and source posture

Papers and compiled sources should be added as structured entries. A paper should not be treated as proof authority merely because it exists. Each paper needs a posture:

```text
context
solver instruction source
mapped claim support
receipt-backed support
superseded / deprecated
```

## Next stage

1. Add structured entries for the compiled papers from `GCAT-BCAT-Engine/Publisher/papers`.
2. Map papers to RTG, STCM, math-solver adapter, or other formalism targets.
3. Create one paper-backed instruction packet.
4. Add receipt-backed adapter tests once the authority repo exists.
