# Mapping-to-Instruction Generation

Generated: `2026-06-14`

## Purpose

This directory defines how a reviewed source-to-instruction mapping may become a governed math-solver instruction packet.

The generation step does not create proof authority. It preserves source posture, claim limits, review requirements, and admissibility target while producing a bounded instruction packet.

## Files

| File | Purpose |
|---|---|
| `mapping-to-instruction.template.json` | Reusable generation record template. |
| `examples/rtg-stcm-placeholder.generated-instruction.json` | Placeholder generated instruction packet. |
| `examples/rtg-stcm-placeholder.generated-artifact-return.json` | Placeholder artifact return from the generated instruction. |
| `examples/rtg-stcm-placeholder.generated-admissibility-result.json` | Placeholder admissibility result for the generated lifecycle. |

## Chain

```text
paper/source entry
→ source-to-instruction mapping
→ mapping-to-instruction generation
→ governed instruction packet
→ artifact return
→ admissibility result
```

## Boundary

The current generated lifecycle is a placeholder. It does not assert source import, solver execution, proof, final equations, or production authority.

## Current placeholder lifecycle

```text
rtg-stcm-placeholder.generated-instruction.json
→ rtg-stcm-placeholder.generated-artifact-return.json
→ rtg-stcm-placeholder.generated-admissibility-result.json
```

## Next stage

1. Import a real compiled paper entry.
2. Create a real source-to-instruction mapping.
3. Generate one paper-backed instruction packet.
4. Preserve source posture and claim limits until receipt-backed review exists.
