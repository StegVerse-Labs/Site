# StegVerse Execution Boundary Audit Template

## Purpose

This template turns the StegVerse company-testbed offer into a repeatable, bounded audit format.

The audit evaluates one representative AI or agentic workflow and asks whether the downstream action has authority, admissibility, current-state validity, and receipt-verifiable evidence before it binds consequences.

## Use Boundary

This template is intended for:

```text
non-production workflow review
staging workflow review
mock workflow review
conceptual workflow review
limited advisory assessment
pilot-scoping conversation
```

This template is not intended to claim:

```text
production certification
regulatory approval
security certification
third-party endorsement
complete ecosystem deployment
```

## Audit Header

```text
Audit name:
Company / team:
Workflow owner:
Date:
Reviewer:
Confidentiality level:
Production status: production / staging / mock / conceptual
Case-study permission: named / anonymized / internal-only / undecided
```

## 1. Workflow Summary

Describe the workflow in plain language.

```text
Workflow name:
Workflow purpose:
Business or operational function:
Primary users or actors:
Systems involved:
Current maturity: concept / prototype / pilot / production-adjacent / production
```

### Summary Narrative

```text
[Write a short paragraph explaining what the workflow does and why it matters.]
```

## 2. Decision Point

Identify where an AI system, agent, model, assistant, automation, or human-AI process produces a decision, recommendation, classification, instruction, or action proposal.

```text
Decision producer:
Decision type:
Input data used:
Output produced:
Human review present: yes / no / partial / unknown
Decision confidence or scoring available: yes / no / partial / unknown
```

### Decision Description

```text
[Describe the AI or agentic decision in plain language.]
```

## 3. Execution Boundary

Identify where the decision becomes capable of binding consequences.

```text
Downstream action:
Action executor:
Trigger mechanism:
Manual or automated execution:
Reversibility: reversible / partially reversible / irreversible / unknown
Potential consequence class: low / medium / high / critical
```

### Boundary Statement

```text
The execution boundary occurs when [decision/output] causes or authorizes [downstream action].
```

## 4. Authority Assumptions

Identify the authority currently assumed before execution.

```text
Who or what is authorized to act:
Source of authority:
Authority scope:
Authority expiration or refresh rule:
Delegated authority present: yes / no / unknown
Human accountable owner:
Policy or contract reference:
```

### Authority Gap Notes

```text
[Describe any missing, implicit, stale, overbroad, or unclear authority assumptions.]
```

## 5. State Dependencies

Identify what must be true at commit time for the action to remain valid.

```text
Required current state 1:
Required current state 2:
Required current state 3:
State source systems:
State freshness requirement:
State drift risk:
State verification method:
```

### State Validity Notes

```text
[Describe whether the workflow can prove the relevant state is current at the moment of execution.]
```

## 6. Admissibility Conditions

Define the conditions that must be satisfied before the action can execute.

```text
Condition 1:
Condition 2:
Condition 3:
Condition 4:
Condition 5:
```

### Minimal Admissibility Rule

```text
The action is admissible only if current authority, current state, required evidence, and permitted action scope are all satisfied before execution.
```

## 7. Evidence Currently Available

List the evidence the organization already captures.

```text
Input log available: yes / no / partial / unknown
Decision log available: yes / no / partial / unknown
Authority record available: yes / no / partial / unknown
State snapshot available: yes / no / partial / unknown
Execution log available: yes / no / partial / unknown
Receipt or trace available: yes / no / partial / unknown
Reviewer record available: yes / no / partial / unknown
Policy reference available: yes / no / partial / unknown
```

### Evidence Notes

```text
[Describe what evidence exists today and whether it is enough to reconstruct the action later.]
```

## 8. Evidence Gaps

List missing or insufficient proof surfaces.

```text
Missing authority evidence:
Missing state evidence:
Missing decision evidence:
Missing execution evidence:
Missing reviewer evidence:
Missing policy reference:
Missing receipt fields:
Missing reconstruction fields:
```

### Gap Severity

```text
Low:
Medium:
High:
Critical:
```

## 9. Fail-Closed Conditions

Define when the system should refuse execution because authority, admissibility, state, or evidence cannot be proven.

```text
Fail closed if authority is missing: yes / no / conditional
Fail closed if state is stale: yes / no / conditional
Fail closed if evidence is missing: yes / no / conditional
Fail closed if policy reference is missing: yes / no / conditional
Fail closed if actor identity is uncertain: yes / no / conditional
Fail closed if downstream consequence class is critical: yes / no / conditional
```

### Fail-Closed Rule

```text
If the workflow cannot prove authority, admissibility, current state, and minimum receipt evidence before execution, the action should FAIL_CLOSED rather than proceed by default.
```

## 10. Receipt Fields

Define the minimum receipt fields needed for reconstruction.

```text
receipt_id:
generated_utc:
workflow_id:
decision_id:
action_id:
actor_id:
authority_source:
authority_scope:
authority_valid_at:
state_snapshot_ref:
state_valid_at:
policy_ref:
admissibility_result: ALLOW / DENY / FAIL_CLOSED
admissibility_reason:
evidence_refs:
execution_boundary:
downstream_action:
reviewer_ref:
case_study_visibility:
receipt_hash:
previous_receipt_hash:
```

## 11. Reconstruction Path

Define what a reviewer should be able to reconstruct after the event.

```text
Can reconstruct input state: yes / no / partial
Can reconstruct decision output: yes / no / partial
Can reconstruct authority basis: yes / no / partial
Can reconstruct current-state validity: yes / no / partial
Can reconstruct admissibility result: yes / no / partial
Can reconstruct execution action: yes / no / partial
Can reconstruct fail-closed reason: yes / no / partial
Can reconstruct reviewer involvement: yes / no / partial
```

### Reconstruction Notes

```text
[Describe what can and cannot be reconstructed from the available evidence.]
```

## 12. Risk Classification

Assign a preliminary risk level.

```text
Execution consequence risk: low / medium / high / critical
Authority ambiguity risk: low / medium / high / critical
State staleness risk: low / medium / high / critical
Evidence gap risk: low / medium / high / critical
Reconstruction failure risk: low / medium / high / critical
Overall audit risk: low / medium / high / critical
```

## 13. StegVerse Decision Readiness

Classify the current workflow.

```text
Current readiness: ALLOW_READY / DENY_READY / FAIL_CLOSED_REQUIRED / INSUFFICIENT_EVIDENCE
Reason:
Minimum remediation required:
```

### Classification Meanings

```text
ALLOW_READY: The workflow appears to have enough authority, state, and evidence for a controlled allow path.
DENY_READY: The workflow has enough evidence to determine that the action should not execute under stated conditions.
FAIL_CLOSED_REQUIRED: The workflow cannot prove enough to safely execute and should fail closed.
INSUFFICIENT_EVIDENCE: The audit cannot classify readiness because required information is unavailable.
```

## 14. Recommendations

List concrete next steps.

```text
Recommendation 1:
Recommendation 2:
Recommendation 3:
Recommendation 4:
Recommendation 5:
```

Recommended categories:

```text
authority model clarification
state freshness check
receipt schema addition
fail-closed trigger addition
reviewer record addition
policy reference addition
execution log hardening
reconstruction test
non-production gate prototype
```

## 15. Pilot Outcome

Record what the pilot produced.

```text
Boundary map completed: yes / no
Authority gaps identified: yes / no
State gaps identified: yes / no
Evidence gaps identified: yes / no
Fail-closed rules proposed: yes / no
Receipt fields proposed: yes / no
Reconstruction path proposed: yes / no
Company follow-up requested: yes / no
Case-study permitted: yes / no / anonymized / undecided
```

## 16. Audit Summary

```text
[Write a concise summary of the audit outcome, including whether the workflow is ready for a minimal admissibility gate, needs receipt hardening, or should fail closed until authority/state/evidence gaps are resolved.]
```

## 17. Completion Footer

```text
Audit completion: ___%
Workflow mapped: ___%
Authority/admissibility evaluated: ___%
Receipt/reconstruction evaluated: ___%
Ready for next pilot step: yes / no / conditional
```

## Archive Readiness

This template contains the minimum structure needed to perform a bounded StegVerse Execution Boundary Audit without needing prior chat context. The prior chat thread is no longer required for forward progress once this file is present in the repository.
