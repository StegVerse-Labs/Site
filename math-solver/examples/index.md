# Math-Solver Example Packet Lifecycles

Generated: `2026-06-14`

## Purpose

This directory contains public example packet lifecycles for the StegVerse math-solver adapter.

These examples show the adapter shape only. They do not assert that a real solver run occurred, and they do not create proof authority.

## Current examples

| Example | Instruction | Artifact return | Admissibility result | Posture |
|---|---|---|---|---|
| RTG observer-window sketch | `rtg-observer-window.instruction.json` | `rtg-observer-window.artifact-return.json` | `rtg-observer-window.admissibility-result.json` | RESEARCH_NOTE |

## Lifecycle

```text
instruction packet
→ artifact return
→ admissibility result
→ allowed public posture
```

## Boundary

The current RTG observer-window example is a static packet lifecycle. It is not a proof artifact, not a solver result, and not a claim of mathematical closure.

## Next stage

1. Add structured paper/source entries.
2. Create one paper-backed instruction packet.
3. Route a real solver task only after sources, claim limits, and authority posture are declared.
4. Attach receipts when a governed adapter authority exists.
