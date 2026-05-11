# Theorem Proof Map

## Purpose

This file maps DCF theorem candidates to executable proof artifacts.

## Current artifacts

```text
reports/sample_receipts.jsonl
reports/continuation_report.md
tests/expected_outcomes.json
src/validate_expected_outcomes.py
tests/compound_cases.json
src/compound_continuation_gate.py
reports/compound_receipts.jsonl
reports/compound_continuation_report.md
tools/tasks/formalism_tests_tasks.json
tools/rules/runtime_artifact_rules.json
tools/apply_runtime_artifact_rules.py
tools/run_declared_tasks.py
```

## Current workflow evidence

The declared-task workflow now runs:

```text
archive_runtime_artifacts
continuation_gate
compound_continuation_gate
```

The Stage 3 compound continuation gate generated:

```text
reports/compound_receipts.jsonl
reports/compound_continuation_report.md
```

## Mapping

| Theorem | Current evidence | Status |
|---|---|---|
| Representation Non-Consequence | Indirect; same datum remains role-dependent until continuation. Stage 2 demonstrates that content alone does not determine continuation admissibility. | Partially covered |
| Role Non-Transfer | Same patient-risk datum produces ALLOW, ALLOW_WITH_SIGNOFF, and FAIL_CLOSED across roles. | Covered |
| Continuation Capacity | Insufficient capacity cases fail closed. | Covered |
| Fail-Closed Basis Requirement | Missing required block basis fails closed. | Covered |
| Local-Composite Non-Equivalence | Stage 3 compound-local-001: local ALLOW + local ALLOW fails closed because composite consequence mass exceeds legitimacy capacity. | Covered |
| Commit-Time Sufficiency | Stage 3 drift-commit-001: pre-commit state differs from commit state, producing FAIL_CLOSED due to commit-time state drift. | Covered |
| Replay Non-Reversal | Stage 3 replay-non-reversal-001: replay may reconstruct receipt state but may not reverse consequence. | Covered |
| Inference-Window Collapse | Stage 3 inference-collapse-001: inference window collapsed below continuation threshold, producing FAIL_CLOSED. | Covered |
| Recoverability Floor | Stage 3 recoverability-floor-001: recoverability score below required floor, producing FAIL_CLOSED. | Covered |
| Role-Transition Dependence | Covered by role comparison and same-data continuation decisions. | Covered |
| Compound Continuation Positive Control | Stage 3 compound-allow-001: compound continuation remains within capacity and recoverability bounds, producing ALLOW. | Covered |

## Stage 2 proof surface

```text
same data ≠ same continuation admissibility
```

Stage 2 demonstrates that a datum can be safe as an informational note, conditional as a clinician recommendation, and inadmissible as autonomous actuation.

The governance claim is that continuation admissibility cannot attach only to data content. It must attach to the role and transition through which the data seeks continuation into consequence.

## Stage 3 proof surface

```text
local allow + local allow does not imply composite allow
pre-commit allow does not imply commit-time allow after state drift
replay can reconstruct consequence state but cannot reverse consequence
recoverability and inference-window floors are admissibility conditions
```

Stage 3 extends continuation testing beyond role comparison into compound and temporal admissibility.

The new receipt set demonstrates that local admissibility does not compose automatically into global admissibility. A transition may fail closed because:

```text
composite consequence mass exceeds legitimacy capacity
commit-time state drift occurred
the inference window collapsed
recoverability fell below the required floor
replay was incorrectly treated as reversal
```

## Covered theorem group

```text
Role Non-Transfer
Continuation Capacity
Fail-Closed Basis Requirement
Local-Composite Non-Equivalence
Commit-Time Sufficiency
Replay Non-Reversal
Inference-Window Collapse
Recoverability Floor
Role-Transition Dependence
Compound Continuation Positive Control
```

## Partially covered theorem group

```text
Representation Non-Consequence
```

Representation Non-Consequence remains partially covered because current evidence still reaches it indirectly through role-dependent continuation. A direct proof should show that representation alone has no consequence-bearing status until it is bound to a transition role and continuation path.

## Next proof upgrades

```text
direct representation non-consequence receipts
multi-body boundary-dynamics receipts
system-coherence failure receipts
purpose-convergence failure receipts
governed boundary reset receipts
governed boundary evolution receipts
```

## Next integration target

The next proof layer should connect DCF Stage 3 to:

```text
Multi-Body Admissibility
System-Coherent Boundary Dynamics
Purpose-Convergence Test
Degraded-Authority Recoverability Test
Governed Boundary Reset
Governed Boundary Evolution
```

## Current interpretation

The DCF proof surface has now moved from same-data role dependence into compound and temporal admissibility.

This supports the broader StegVerse claim:

```text
Admissibility is not local boundary compliance.
Admissibility is recoverable convergence across coherent, evolving, coupled boundary fields.
```
