# StegVerse Execution Boundary Intake Questionnaire

## Purpose

This questionnaire helps identify one suitable non-production AI or agentic workflow for a bounded StegVerse Execution Boundary Audit.

It is designed to avoid production credentials, sensitive operational data, invasive access, and unsupported claims.

## Intake Boundary

```text
One organization or lab.
One representative workflow.
One decision path.
One governed point of irreversibility.
One bounded pilot question.
```

Submitting this questionnaire does not authorize production access, integration, deployment, publication, endorsement, or use of confidential information outside the agreed pilot boundary.

## 1. Organization And Contact Boundary

```yaml
organization_or_lab: ""
team_or_unit: ""
primary_contact_name: ""
primary_contact_role: ""
preferred_contact_method: ""
technical_contact_name: ""
legal_or_compliance_contact_needed: true | false | unknown
```

## 2. Workflow Summary

```text
Workflow name:

What does the workflow do?

Why is it useful or important?

Who currently uses or reviews its outputs?

Current maturity:
conceptual / mock / prototype / staging / non-production pilot / production-adjacent
```

## 3. Decision Producer

Identify what produces the recommendation, classification, plan, instruction, or proposed action.

```yaml
decision_producer_type: model | agent | assistant | automation | human_ai_process | other
decision_producer_name: ""
decision_output_type: ""
model_or_system_version_known: true | false | partial
human_review_present: true | false | conditional
```

Questions:

1. What inputs are used?
2. What output is produced?
3. Is the output advisory, preparatory, executable, or already binding?
4. Can the decision be logged or replayed in a non-production setting?

## 4. Downstream Action

Describe what may happen after the decision is produced.

```text
Downstream action:

Target system, account, record, resource, or environment:

Who or what performs the action:

Is execution manual, automated, or mixed?

Potential consequence if the action executes:
```

Consequence categories:

```text
money
identity or access
records or data
infrastructure
eligibility or benefits
healthcare or safety
compliance
publication or public trust
other
```

## 5. Governed Point Of Irreversibility

Identify the final boundary where the proposed action becomes capable of binding real consequences.

```text
The action becomes real when:
```

```yaml
boundary_component: ""
commit_operation: ""
reversibility: reversible | compensatable | partially_irreversible | irreversible | unknown
current_gate_or_approval: ""
```

## 6. Authority Source And Scope

The audit evaluates whether the actor has valid authority at commit time.

```text
Who or what is currently allowed to act?

What is the source of that authority?

What action scope is permitted?

Are there amount, resource, role, geography, channel, rail, or time limits?

Are delegation or approval chains involved?

How can authority be revoked or expire?
```

```yaml
authority_documented: true | false | partial
authority_machine_legible: true | false | partial
revocation_state_available: true | false | partial
authority_version_available: true | false | partial
```

## 7. Resulting-State Admissibility

The audit also evaluates whether the resulting state transition is permitted for the current system state.

```text
What must be true immediately before the action?

What state would change if the action commits?

What limits or invariants must remain true afterward?

Could two individually valid actions combine into an invalid result?

What state change between evaluation and commit would invalidate the action?

What recoverability or future-governability condition must be preserved?
```

## 8. Current-State Dependencies

List the facts that must still be current when execution is attempted.

| Required state | Current source | Freshness requirement | What happens if stale or unavailable? |
|---|---|---|---|
|  |  |  |  |

Examples:

```text
policy version
account balance
identity status
consent state
approval status
risk score
inventory
patient status
resource lock
rate or spending limit
prior transaction state
recoverability margin
```

## 9. Known Failure Modes

```text
What can currently go wrong?

Has an action ever executed with stale state, missing approval, unclear authority, or incomplete evidence?

Could the system act twice, race another action, or exceed an aggregate limit?

What does the workflow do when required information is missing?

What should always cause refusal or escalation?
```

## 10. Evidence Currently Available

Mark each item.

```text
Input record: yes / no / partial / unknown
Decision record: yes / no / partial / unknown
Actor identity record: yes / no / partial / unknown
Authority record: yes / no / partial / unknown
Delegation or approval record: yes / no / partial / unknown
Policy version: yes / no / partial / unknown
Current-state snapshot: yes / no / partial / unknown
Admissibility or invariant result: yes / no / partial / unknown
Execution result: yes / no / partial / unknown
Receipt or trace: yes / no / partial / unknown
Custody record: yes / no / partial / unknown
Reconstruction report: yes / no / partial / unknown
```

Available artifacts may be described without attaching sensitive data during initial qualification.

## 11. Evidence And Access Restrictions

```text
What information cannot be shared?

Can synthetic or anonymized data be used?

Can screenshots, schema fragments, pseudocode, or redacted traces be used?

Are production credentials excluded? yes / no

Is repository access excluded? yes / no / undecided

Is live system access excluded? yes / no / undecided

Are there contractual, regulatory, privacy, export, or data-residency restrictions?
```

## 12. Desired Safe Behavior

```text
What should happen when authority is valid and the transition is admissible?

What should happen when authority fails?

What should happen when the transition is inadmissible?

What should happen when evidence is incomplete or stale?

Who should receive an escalation?

Should retries be allowed, and under what conditions?
```

## 13. Pilot Usefulness Criteria

Select the outcomes that would make the pilot useful.

```text
[ ] Identify the governed point of irreversibility.
[ ] Clarify actor authority and scope.
[ ] Identify state dependencies and freshness requirements.
[ ] Define resulting-state admissibility conditions.
[ ] Identify race or aggregate-state risks.
[ ] Define fail-closed conditions.
[ ] Produce a proposed receipt field set.
[ ] Identify evidence and custody gaps.
[ ] Define an independent reconstruction path.
[ ] Produce a short technical memo.
[ ] Produce a reusable internal checklist.
[ ] Determine whether a prototype gate is justified.
```

Additional success criteria:

```text

```

## 14. Confidentiality And Attribution

```yaml
confidentiality_preference: public | anonymized | confidential | undecided
organization_name_may_be_used: true | false | undecided
contact_name_may_be_used: true | false | undecided
workflow_may_be_described_publicly: true | false | anonymized_only | undecided
technical_artifacts_may_be_quoted: true | false | with_approval | undecided
```

Attribution boundary:

```text
For clarity and attribution, the work proposed by StegVerse is its commit-time admissibility / execution-boundary model, including governance-state evaluation, authority validation, fail-closed execution semantics, and receipt-based reconstruction.
```

## 15. Case-Study Permission

```text
No case study.
Internal-only case study.
Anonymized public case study after approval.
Named public case study after approval.
Undecided until the audit is complete.
```

No public claim or publication is permitted unless the selected option and review conditions are recorded in writing.

## 16. Qualification Result

Completed by StegVerse after review.

```yaml
workflow_fit: strong | possible | weak | not_suitable
non_production_scope_available: true | false | unknown
governed_boundary_identifiable: true | false | unknown
authority_question_present: true | false | unknown
state_transition_question_present: true | false | unknown
evidence_available: sufficient | partial | insufficient | unknown
confidentiality_boundary_clear: true | false | partial
recommended_next_step: schedule_scoping_call | request_more_information | prepare_mock_audit | decline | defer
```

Qualification notes:

```text

```

## 17. Minimum Acceptance Rule

A workflow is suitable for the first StegVerse testbed when:

```text
1. it can be represented without production credentials or prohibited data;
2. a decision can influence a downstream action;
3. a governed point of irreversibility can be identified;
4. both actor authority and resulting-state admissibility can be evaluated;
5. at least partial evidence can be inspected or represented synthetically;
6. the organization agrees to the confidentiality and claims boundary;
7. and the audit can remain non-production and non-invasive.
```

## 18. Next Step After Acceptance

```text
1. Assign an audit_id.
2. Copy the qualified workflow into docs/STEGVERSE_EXECUTION_BOUNDARY_AUDIT_TEMPLATE.md or an approved private equivalent.
3. Confirm scope, evidence, confidentiality, and case-study permissions in writing.
4. Perform the audit without production mutation authority.
5. Return a bounded result, receipt recommendation, reconstruction path, and remediation list.
```

## Archive Readiness

This questionnaire preserves the minimum intake, qualification, confidentiality, and continuation information needed to begin a bounded Execution Boundary Audit without relying on prior conversation context.