# Company Testbed Mirror Handoff

## Purpose

This file is the current task source of truth for `StegVerse-Labs/Site` company-testbed, LinkedIn outreach, and execution-boundary pilot-readiness work.

It does not replace `docs/SITE_MIRROR_HANDOFF.md`, which remains authoritative for Site activation and Publisher-to-Site paper-display work.

## Current Goal

```text
Goal: Company testbed discovery and execution-boundary pilot readiness
Repository: StegVerse-Labs/Site
Activation state: ready_for_external_testbed_outreach
Release state: current_main_validation_pending
Workflow target: exactly two operational workflows
```

## External-Facing Thesis

```text
Before an AI or agentic system turns a decision into action, can it prove that the action is still authorized, admissible, state-valid, and receipt-verifiable?
```

Core failure framing:

```text
AI governance becomes a policy document while execution remains probabilistic.
```

Governance must bind the point where a decision becomes capable of producing consequence, not merely document intent upstream or review outputs afterward.

## Commit-Time Rule

```text
1. Determine whether the actor has valid authority for this exact action.
2. Determine whether the resulting transition is admissible for the latest valid system state.
3. ALLOW only when both pass.
4. DENY when either is known to fail.
5. FAIL_CLOSED when either cannot be proven sufficiently.
```

Authority inherited from design-time or earlier context is not presumed durable.

A valid actor may propose an inadmissible transition. An admissible transition may be proposed by an unauthorized actor. Both conditions must hold at the governed point of irreversibility.

## Current Pilot Offer

```text
StegVerse Execution Boundary Audit
```

Bounded first engagement:

```text
One organization or lab.
One non-production workflow.
One decision path.
One governed point of irreversibility.
One receipt trail.
One reconstruction report.
```

## Built Artifact Set

```text
docs/COMPANY_TESTBED_MIRROR_HANDOFF.md
docs/STEGVERSE_EXECUTION_BOUNDARY_TESTBED_README.md
docs/STEGVERSE_EXECUTION_BOUNDARY_AUDIT_TEMPLATE.md
docs/STEGVERSE_EXECUTION_BOUNDARY_INTAKE_QUESTIONNAIRE.md
docs/STEGVERSE_EXECUTION_BOUNDARY_SAMPLE_AUDIT.md
docs/STEGVERSE_COMPANY_TESTBED_TARGET_LIST_TEMPLATE.md
scripts/check_site_company_testbed_artifacts.py
scripts/test_site_company_testbed_artifacts.py
scripts/check_site_workflow_inventory.py
```

## Latest Build Progression

```text
Commit: 55ec8ec98e5d3a016e63cb6f18671ac789e88cd5
Result: completed synthetic fail-closed treasury concurrency audit

Commit: 8bec43dbd47c0e178374bac7c918dbc2b6096498
Result: added governed company-testbed target-list template

Commit: 6846ac6f6f8255f7f1c8971b4a4117f77ad86d70
Result: added fail-closed company-testbed artifact validator

Commit: ec4333667778bddd57b5c4c1020ef1efb55f1502
Result: aligned validator integration contract with the existing workflow-inventory path

Commit: ca6f271cd39cae5f8a612a1a932d44258a29d88d
Result: bound company-testbed validation into the existing canonical Site validation path without adding a workflow

Commit: ba5c1fbd75f9d9e593204388492784c7efecefe6
Result: added six adversarial regression cases for the company-testbed validator

Commit: 674e4c58ef23f276dae8a966217551b7990f0587
Result: bound company-testbed adversarial tests into the canonical workflow-inventory validation path without adding a workflow
```

## Sample Audit Evidence Boundary

The completed synthetic sample demonstrates:

```text
synthetic treasury-payment agent workflow
valid actor identity, delegation, approval, scope, and authority
USD 4,000 proposed payment against an initial USD 10,000 balance
USD 5,000 required minimum liquidity reserve
a concurrent USD 3,000 payment before commit
latest-state reprojection to a prohibited USD 3,000 balance
authority_result: PASS
state_freshness_result: FAIL
admissibility_result: FAIL
recoverability_result: FAIL
final_decision: FAIL_CLOSED
execution_attempted: false
mutation_committed: false
local reconstructability: PASS
replayability: PASS
cryptographic verifiability: PARTIAL
```

No real company, account, payment rail, credential, personal data, endorsement, deployment, external custody, or third-party assurance is represented.

## Target-List Governance Boundary

The target-list template records only public-source research, fit hypotheses, permission state, confidentiality state, and the next permitted action.

It explicitly prohibits treating a research candidate as a partner, customer, adopter, endorser, validator, certified entity, deployment, integration, or paid pilot.

Permitted default claim:

```text
Prospective research candidate identified from public information.
```

## Validation Integration

The company-testbed validator is fail-closed and checks:

```text
required artifact presence
minimum content completeness
commit-time authority and admissibility language
sample FAIL_CLOSED result
execution_attempted: false
mutation_committed: false
target-list permission and claim boundaries
forbidden unsupported positive claims
exactly two operational workflows
binding through scripts/check_site_workflow_inventory.py
```

The adversarial regression script verifies that validation rejects:

```text
missing required fail-closed results
unsupported deployment claims
a third workflow file
removal of canonical validator binding
truncated required artifacts
```

It also verifies that a complete bounded fixture passes. The tests have no mutation, deployment, custody, release, or authority effect.

The existing `scripts/run_site_task.py` invokes `scripts/check_site_workflow_inventory.py` in both the validation and public-guard paths. The workflow inventory now invokes both the company-testbed validator and its adversarial tests. No third workflow was added.

## Current Completion State

```text
Positioning thesis: built
Pilot scope: built
Target sectors and roles: built
Outreach language and boundary: built
Testbed README: built
Operational audit template: built
Intake questionnaire: built
Synthetic completed sample audit: built
Governed target-list template: built
Artifact-set validator: built
Adversarial validator regression tests: built
Validation integration in existing workflow architecture: built
Repository current-main validation: pending observation
External populated target list: pending
Outbound messages: pending
External company conversation: pending
External workflow audit: pending
Case study or pilot evidence: pending
```

## Remaining Files Or Modules

```text
StegVerse-Labs/Site
  -> observe current-main validation containing scripts/test_site_company_testbed_artifacts.py
  -> confirm the baseline and all six adversarial cases execute successfully
  -> repair only the next exact failure without removing checks
  -> record a successful company-testbed artifact validation result
  -> create bounded release notes only after validation passes
  -> verify explicit release authority before any tag
  -> optional public landing-page copy only when Site routing is authorized

master-records/orchestration
  -> future custody schema for completed audit receipts and reconstruction evidence

GCAT-BCAT-Engine/Publisher
  -> future publication packet only after an audit or formal research artifact is release-ready

admissibility-wiki
  -> future terminology page for governed point of irreversibility, authority validity, transition admissibility, and aggregate-state admissibility

stegguardian-wiki
  -> future operator escalation, refusal, retry, and fail-closed response guidance
```

These are continuation candidates, not claims that cross-repository installation is currently authorized.

## Next Task

```text
1. Observe current-main workflow validation after commit 674e4c58ef23f276dae8a966217551b7990f0587.
2. Confirm scripts/test_site_company_testbed_artifacts.py reports all six cases PASS.
3. Confirm the company-testbed validator executes through the canonical validation path.
4. Repair only the exact failing assertion if validation fails.
5. Record the first successful current-main validation evidence.
6. Reassess release readiness.
7. Do not tag unless validation passes and release authority is explicit.
```

## LinkedIn And External Dialogue Continuity

External dialogue may test terminology and discover suitable non-production workflows. It does not establish technical validation, partnership, adoption, endorsement, or execution authority.

Preferred external question:

```text
Where does your governance live relative to where your system acts?
```

Preferred technical follow-up:

```text
At the point where a decision becomes capable of binding consequence, what current authority, state, policy, admissibility, evidence, and receipt conditions must pass before commit?
```

## IP And Attribution Hygiene

```text
For clarity and attribution, the work proposed by StegVerse is its commit-time admissibility and execution-boundary model, including governance-state evaluation, authority validation, fail-closed execution semantics, and receipt-based reconstruction.
```

Do not publish confidential third-party information, imply approval, or associate an organization with StegVerse without permission.

## Release Posture

The complete documentation, validator, and adversarial-test surface is built, but release tagging is not yet authorized.

Release requires:

```text
successful current-main artifact-set and adversarial-test validation
no unresolved internal inconsistencies
explicit release authority
bounded release notes
verification that no production, custody, certification, adoption, partnership, or endorsement claim is implied
```

When release-ready, create a follow-up task to assess updates for:

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
admissibility-wiki
stegguardian-wiki
```

## Ownership And Pending Validation

```text
StegVerse-Labs/Site owns the current documentation build and validation path.
External organizations own permission to inspect, describe, or publish their workflows.
Destination repositories own later custody, publication, terminology, or operator-guidance integration.
No external validation, custody, adoption, partnership, endorsement, or certification is completed evidence.
```

## Archive Readiness

This handoff preserves the active goal, decisions, built artifacts, commits, remaining work, blockers, ownership, release posture, external-dialogue framing, claim limits, pending validation, and exact permitted continuation scope. Earlier conversation context is not required for forward progress.