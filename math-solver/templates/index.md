# Math-Solver Packet Templates

Generated: `2026-06-14`

## Purpose

These templates define the first governed packet shapes for the StegVerse math-solver adapter.

The adapter does not ask a solver or model to act with free-form authority. It routes work through declared packets, bounded returns, and admissibility decisions.

## Templates

| Template | Path | Purpose |
|---|---|---|
| Instruction Packet | `instruction-packet.template.json` | Declares what a solver/model is allowed to attempt. |
| Artifact Return | `artifact-return.template.json` | Declares what the solver/model returned and what claim is attempted. |
| Admissibility Result | `admissibility-result.template.json` | Declares what the returned artifact is allowed to become. |

## Chain

```text
instruction_packet
→ artifact_return
→ admissibility_result
→ receipt / replay posture
→ next admissible instruction
```

## Boundary

These templates are public adapter scaffolds. They do not create proof authority until connected to receipt-backed tests, formalism authority, or governed review.
