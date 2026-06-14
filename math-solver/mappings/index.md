# Source-to-Instruction Mappings

Generated: `2026-06-14`

## Purpose

This directory defines how a declared source becomes eligible to inform a math-solver instruction packet.

A paper or source does not automatically become instruction authority. It must be mapped with source posture, related formalism, allowed use, disallowed use, claim limit, review requirement, and admissibility target.

## Files

| File | Purpose |
|---|---|
| `source-to-instruction.template.json` | Reusable mapping template. |
| `examples/rtg-stcm-placeholder.mapping.json` | Placeholder mapping example for RTG/STCM source intake. |

## Mapping chain

```text
paper/source entry
→ source-to-instruction mapping
→ governed instruction packet
→ artifact return
→ admissibility result
```

## Boundary

The current example is a placeholder. It does not assert that a compiled paper has been imported, reviewed, mapped, or accepted as evidence.

## Next stage

1. Import real compiled paper entries into `math-solver/sources/paper-sources.json`.
2. Create one mapping for a real paper.
3. Generate one paper-backed instruction packet from that mapping.
4. Preserve claim limits until receipt-backed review exists.
