# Governed Admissibility Tester Output Examples

Generated: `2026-06-14`

## Purpose

This directory contains example tester-output packets for discipline-facing governed admissibility review.

These examples show output shape only. They do not certify domain correctness, proof closure, medical correctness, legal correctness, financial suitability, engineering safety, or any other professional result.

## Files

| File | Discipline | Purpose |
|---|---|---|
| `ai-llm-output-example.tester-output.json` | AI / LLM systems | Shows how a model response proposed as a public governance claim may be limited to research-note posture. |
| `math-formal-methods-example.tester-output.json` | Mathematics / formal methods | Shows how a solver artifact proposed as formalism support may require receipt and replay before stronger posture. |

## Reusable template

```text
applicability/tester-output.template.json
```

## Tester return shape

```text
Discipline
Test object
Recommended route
Declared intent
Authority source
Evidence posture
Replay posture
Consequence level
Decision
Allowed next state
Required follow-up
Claim limit
```

## Boundary

The examples are static scaffolds. They are not test results from real discipline testers.
