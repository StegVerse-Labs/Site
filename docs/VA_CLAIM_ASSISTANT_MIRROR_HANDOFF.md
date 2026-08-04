# VA Claim Assistant Mirror Handoff

## Identity and authority

```text
Goal ID: SV-VA-CLAIM-ASSISTANT-001
Adjacent goal ID: SV-VA-GUIDED-CARDS-001
Originating session goal: make the VA claims guide understandable to veterans and family members with little knowledge of VA.gov, Login.gov, ID.me, Blue Button, or AI tools
Repository: StegVerse-Labs/Site
Branch: main
Canonical issue: StegVerse-Labs/Site#113
Substantive document-aware owner: StegVerse-Labs/Site#116
Canonical handoff: docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
Repository handoff: docs/SITE_MIRROR_HANDOFF.md
```

This is the canonical VA Claim Assistant handoff. `docs/SITE_MIRROR_HANDOFF.md` and `data/site-orchestration-state.json` remain authoritative for repository collision control. No guide, chat, workflow, receipt, or validation result grants authority to adjudicate, represent, diagnose, rate, sign, or file a claim.

## Current capability

```text
state: SOURCE_GROUNDED_ACTIVE_WITH_GUIDED_CARD_TEST
current public capability: SOURCE_GROUNDED_ASSISTANT
public test: VETERAN_CONFIRMED_GUIDED_CARDS
next activation target: DOCUMENT_AWARE_ASSISTANT
final target: GOVERNED_CLAIM_SESSION
private document upload: DISABLED
automated claim filing: DISABLED
submission authority: VETERAN RETAINED
authority effect: NONE
```

## Authoritative surfaces and automation

```text
Comprehensive guide: va-disability-claim-guide.html
Guided cards: va-claims-guided-workflow.html
Claims Chat: va-claims-chat.html
Static surface validator: scripts/validate_va_claims_guide_surface.py
Interaction/accessibility contract test: scripts/test_va_guided_workflow_contract.py
Validation workflow: .github/workflows/va-guided-workflow-validation.yml
Surface receipt: data/va-claim-assistant/guide-surface-validation.json
Guided contract receipt: data/va-claim-assistant/guided-workflow-contract-validation.json
```

## Session execution inventory

| Task ID | Requirement | Location | Owner / claim | Completion | Validation / evidence | Next executable action |
|---|---|---|---|---|---|---|
| SV-VA-GC-001 | Link the old guide to a simpler test workflow at the top | `va-disability-claim-guide.html` | RELEASED_COMPLETE | Implemented | commit `832eaed986a0551e50613b80e017fd96ef1604d3` | machine validation and deployment observation |
| SV-VA-GC-002 | One major access/download task per card with a visible flow | `va-claims-guided-workflow.html` | RELEASED_COMPLETE | Six cards implemented | commit `8e631ff625af935d65bed3afc5657c641b2c33ee` | browser/deployment observation |
| SV-VA-GC-003 | Plain-language Login.gov, ID.me, VA.gov, and Blue Button explanations | Guided page and Chat | RELEASED_COMPLETE | Implemented | commits `8e631ff625af935d65bed3afc5657c641b2c33ee`, `15669e0bee12ef68e4d4a7fcdc236189600d3077` | maintain against official-source changes |
| SV-VA-GC-004 | Claims Chat optional card walkthrough | `va-claims-chat.html` | RELEASED_COMPLETE | Implemented | commit `15669e0bee12ef68e4d4a7fcdc236189600d3077` | browser/deployment observation |
| SV-VA-GC-005 | Require confirmation before card transition | Guided page and Chat | RELEASED_COMPLETE | Implemented | source validator commit `783660e3865a886c11fc3f2a4963d967699c4086`; contract test commit `9cafcba71de237078e106f725c0553b4ed59e62a` | inspect hosted workflow jobs, logs, and receipts |
| SV-VA-GC-006 | Keep reference and guided experiences separate | Three public surfaces | RELEASED_COMPLETE | Integrated | links and distinct surfaces committed | deployed route verification |
| SV-VA-GC-007 | Add accessible purpose-built visual illustrations | `assets/va-claims-guided/` plus card markup | UNCLAIMED | Missing | none | verify current official screens, then create dated non-authority-labelled illustrations |
| SV-VA-GC-008 | Automate interaction, mobile, and accessibility contract checks | `scripts/test_va_guided_workflow_contract.py`, `.github/workflows/va-guided-workflow-validation.yml` | MACHINE_OWNED_VALIDATION | Implemented | commits `9cafcba71de237078e106f725c0553b4ed59e62a`, `fb020b9116b5a547e6701ba5e6ead3770bebed59`; hosted result not surfaced by connector | GitHub Actions executes on matching push/PR/dispatch and uploads both receipts |
| SV-VA-GC-009 | Observe deployed public HTTP behavior | Site deployment observer | MACHINE_OWNED / BLOCKED | Not observed | no route observation for current bytes | release when all three routes return expected content and deployed-byte equality is verified |

## Guided workflow contract

```text
Guide page != guided workflow
Guided workflow != claim filing
Chat explanation != card completion
Generic "done" != confirmation of all required tasks
Card completion requires veteran confirmation of every task
Current-card help may explain, simplify, repeat, or troubleshoot
Next card remains unavailable until current completion criteria pass
Private credentials and one-time security codes must never be requested
Medical records must not be posted publicly
```

Card sequence:

```text
1. Get ready
2. Choose Login.gov or ID.me
3. Create or verify the secure account
4. Sign in to VA.gov
5. Download VA medical records / Blue Button records
6. Preserve the original and continue to evidence gathering
```

## Claims, convergence, and collision boundaries

```text
Guide/Guided/Chat implementation: RELEASED_COMPLETE
Static and contract validation: MACHINE_OWNED by .github/workflows/va-guided-workflow-validation.yml
Substantive document-aware implementation: CLAIMED_FOR_IMPLEMENTATION under Site#116
Automated filing requirements: CLAIMED_FOR_REQUIREMENTS under Site#113
Deployment observation: MACHINE_OWNED by Site deployment controls
Visual illustration task: UNCLAIMED
```

This work does not modify or compete with Site#116 substantive private-document interpretation, TVC execution, or Master Records custody. Private upload and automated filing remain fail-closed.

`MERGED INTO: StegVerse-Labs/Site/docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`

Transferred session requirements:

- novice-first prerequisite orientation;
- separate comprehensive and guided experiences;
- one goal and visible flow per card;
- direct official links;
- optional Claims Chat walkthrough;
- explicit veteran confirmation before transition;
- browser-local resume point;
- credential and sensitive-record warnings;
- deterministic validation automation;
- future accessible illustration obligation.

## Validation status

```text
File presence: VERIFIED
Three-surface link integration: VERIFIED BY SOURCE
Static surface validator: IMPLEMENTED
Interaction/accessibility contract test: IMPLEMENTED
Dedicated GitHub Actions workflow: IMPLEMENTED
Push-triggered hosted workflow run: NOT OBSERVED through available connector lookup
Workflow jobs/logs/artifacts: NOT INSPECTED
Browser interaction execution: NOT OBSERVED
Mobile device execution: NOT OBSERVED
Public deployment: NOT OBSERVED FOR CURRENT BYTES
Governed activation effect: NONE
```

The workflow runs both validators and uploads deterministic receipt files as `va-guided-workflow-validation-receipts`. Missing receipts fail the job. The available commit-run connector returned no pull-request-triggered run for commit `fb020b9116b5a547e6701ba5e6ead3770bebed59`; this is recorded as absent observation, not failure or success.

## Machine-owned continuation

```text
Owner repository: StegVerse-Labs/Site
Trigger: push to main, pull request affecting the VA surfaces/tests, or workflow_dispatch
Workflow: .github/workflows/va-guided-workflow-validation.yml
Inputs: three VA HTML surfaces and two Python validators
Outputs: guide-surface-validation.json and guided-workflow-contract-validation.json
Success state: both scripts exit zero and both receipts upload
Failure state: validator error or missing receipt fails closed
Next task after success: inspect run, jobs, logs, artifacts, then record observation here
Deployment release condition: all three public routes match repository bytes and expected guided behavior
```

## Exact incomplete work

1. `assets/va-claims-guided/`: create accessible, dated, non-misleading illustrations after current official VA/Login.gov/ID.me screens are verified.
2. `.github/workflows/va-guided-workflow-validation.yml`: obtain and inspect a hosted run, its job steps, logs, and uploaded receipt artifact.
3. Site deployment observer: verify `va-disability-claim-guide.html`, `va-claims-guided-workflow.html`, and `va-claims-chat.html` against current repository bytes.
4. Site#116: retain sole ownership of substantive document interpretation and derived-record custody.
5. Site#113: retain automated filing as inactive until exact-package authorization, signature, authorized transport, confirmation, custody, reconstruction, revocation, retry, and duplicate-prevention gates verify.

## Release and propagation posture

No release or tag is authorized for this milestone while hosted validation, browser execution, current-byte deployment observation, and accessible visuals remain unverified. No propagation to Publisher, admissibility-wiki, stegguardian-wiki, or Master Records is required for this presentation-only guided-card test unless a later governed contract explicitly requires it.

## Archive conditions and completion measures

All unique session requirements are installed or durably assigned here. Continuation no longer depends on undocumented conversation state. Remaining execution is repository-native or assigned to exact durable owners.

```text
task completion: 7/9
required developed files: 6/7
scaffolding or stubs: 0
missing required component: 1 (accessible visual asset set)
validation implementation: 2/2
hosted validation observation: 0/1
integration among Guide/Guided/Chat: 3/3
public deployment observation: 0/3 routes
session requirement transfer: 9/9
```
