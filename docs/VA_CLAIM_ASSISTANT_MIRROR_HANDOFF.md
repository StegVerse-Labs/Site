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

This file is the canonical VA Claim Assistant handoff. The Site-wide orchestrator remains authoritative for repository collision control. No authority is granted to adjudicate, represent, diagnose, rate, sign, or file a claim.

## Current capability

```text
state: SOURCE_GROUNDED_ACTIVE_WITH_GUIDED_CARD_TEST
current public capability: SOURCE_GROUNDED_ASSISTANT
new public test: VETERAN_CONFIRMED_GUIDED_CARDS
next activation target: DOCUMENT_AWARE_ASSISTANT
final target: GOVERNED_CLAIM_SESSION
private document upload: DISABLED
automated claim filing: DISABLED
submission authority: VETERAN RETAINED
authority effect: NONE
```

## Session goal inventory

| Task ID | Goal | Destination | Claim state | Completion | Validation | Integration | Evidence / next action |
|---|---|---|---|---|---|---|---|
| SV-VA-GC-001 | Link the existing guide to a simpler tested workflow at the top of the page | `va-disability-claim-guide.html` | COMPLETE | Implemented | validator updated; hosted run pending | Linked to guided page and chat | commits `832eaed986a0551e50613b80e017fd96ef1604d3`, `783660e3865a886c11fc3f2a4963d967699c4086` |
| SV-VA-GC-002 | Present each major access/download task as its own card/page section with a visible flow | `va-claims-guided-workflow.html` | COMPLETE | Six cards implemented | validator updated; browser execution pending | Linked from Guide and Chat | commit `8e631ff625af935d65bed3afc5657c641b2c33ee` |
| SV-VA-GC-003 | Explain Login.gov, ID.me, VA.gov sign-in, and Blue Button in plain language | `va-claims-guided-workflow.html`, `va-claims-chat.html` | COMPLETE | Implemented with official links | static validator updated | shared card vocabulary | commits `8e631ff625af935d65bed3afc5657c641b2c33ee`, `15669e0bee12ef68e4d4a7fcdc236189600d3077` |
| SV-VA-GC-004 | Allow Claims Chat to walk a veteran through cards when preferred | `va-claims-chat.html` | COMPLETE | Guided mode implemented | static validator updated; interaction test pending | query-string card entry and shared sequence | commit `15669e0bee12ef68e4d4a7fcdc236189600d3077` |
| SV-VA-GC-005 | Prevent movement to the next card until current tasks are confirmed | Guided page and chat | COMPLETE | Page lock and chat confirmation gate implemented | source validation pending hosted observation | veteran confirmation retained | commits `8e631ff625af935d65bed3afc5657c641b2c33ee`, `15669e0bee12ef68e4d4a7fcdc236189600d3077` |
| SV-VA-GC-006 | Keep the comprehensive reference guide separate from the guided experience | Guide, guided page, chat | COMPLETE | Three distinct surfaces | links statically validated | integrated navigation | all three surface commits above |
| SV-VA-GC-007 | Add screenshots or purpose-built visual illustrations for key steps | `assets/va-claims-guided/` and card markup | UNCLAIMED | Missing | Not validated | Not integrated | create accessible, non-misleading visuals after current VA/Login.gov screens are verified |
| SV-VA-GC-008 | Run browser interaction and mobile accessibility tests | test/workflow location to be installed under `scripts/` and `.github/workflows/` | UNCLAIMED | Missing | Not run | Not integrated | deterministic card-lock, resume, keyboard, screen-reader, and mobile checks |
| SV-VA-GC-009 | Observe deployed public HTTP behavior | Site deployment observer | MACHINE_OWNED / BLOCKED | Repository commits present | deployment observation absent | public activation not proven | release condition: deployed bytes equal commits and three routes return expected content |

## Product surfaces

1. `GOVERNED_VA_CLAIMS_GUIDE` — comprehensive reference page.
2. `VETERAN_CONFIRMED_GUIDED_CARDS` — simpler card-by-card workflow with one goal, flow, links, checklist, and veteran confirmation per card.
3. `GOVERNED_VA_CLAIMS_CHAT` — source-grounded question mode plus optional guided-card mode.
4. `PRIVATE_CLAIM_DOCUMENT_WORKSPACE` — remains owned by Site#116 and is not activated by this work.
5. `VETERAN_APPROVED_AUTOMATED_CLAIM_FILING` — future staged target under Site#113; inactive.

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

Current card sequence:

```text
1. Get ready
2. Choose Login.gov or ID.me
3. Create or verify the secure account
4. Sign in to VA.gov
5. Download VA medical records / Blue Button records
6. Preserve the original and continue to evidence gathering
```

## Existing verified chains retained

```text
Source-grounded answer chain: COMPLETE
Bounded document-fixture chain: VERIFIED_BOUNDED_FIXTURE_ONLY
Substantive private-document interpretation: NOT VERIFIED
Public private-document upload: DISABLED
Automated filing: DISABLED
```

Canonical prior evidence remains in:

```text
data/va-claim-assistant/activation-gates.json
data/va-claim-assistant/governed-product-goals.json
data/va-claim-assistant/document-evidence-validation-receipt.json
data/va-claim-assistant/private-document-runtime-receipt.json
```

## Claims and convergence

```text
Guide/Chat guided-card implementation: RELEASED_COMPLETE by this session
Guide/Chat deterministic static validation: CLAIMED_FOR_VALIDATION by repository workflow
Substantive document-aware implementation: CLAIMED_FOR_IMPLEMENTATION under Site#116
Automated filing requirements: CLAIMED_FOR_REQUIREMENTS under Site#113
Deployment observation: MACHINE_OWNED by Site deployment controls
```

No work in this session modifies or competes with the Site#116 substantive-document execution lane.

`MERGED INTO: StegVerse-Labs/Site/docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`

Transferred requirements:

- novice-first language and prerequisite orientation;
- separate comprehensive and guided experiences;
- one card per goal with visible flow;
- direct official links for Login.gov, ID.me, VA.gov, and medical-record download;
- Claims Chat walkthrough mode;
- explicit veteran confirmation before card transition;
- persistent resume point in the browser;
- credential and sensitive-record warnings;
- future screenshot/illustration and accessibility test obligations.

## Validation and automation

```text
Validator: scripts/validate_va_claims_guide_surface.py
Receipt: data/va-claim-assistant/guide-surface-validation.json
Existing workflow: .github/workflows/va-governed-product-goals.yml and/or current VA guide validation workflow
Static validator commit: 783660e3865a886c11fc3f2a4963d967699c4086
Hosted workflow result for this change set: NOT YET OBSERVED
Browser interaction result: NOT YET OBSERVED
Deployment result: NOT YET OBSERVED
```

The validator now checks all three surfaces, six-card coverage, official links, the page-level next-card lock, the chat confirmation boundary, credential warnings, and inactive upload/filing controls.

## Exact remaining tasks

1. Add current, accessible step illustrations or screenshots under `assets/va-claims-guided/`, with source date and non-authority labels.
2. Add deterministic browser tests for checkbox gating, back navigation, resume state, chat guided entry, generic `done` rejection, and explicit completion transition.
3. Add mobile and accessibility checks for keyboard operation, visible focus, labels, readable diagrams, and screen-reader order.
4. Observe the repository workflow for commit `783660e3865a886c11fc3f2a4963d967699c4086`; inspect jobs, logs, and receipt artifact.
5. Observe deployed routes for `va-disability-claim-guide.html`, `va-claims-guided-workflow.html`, and `va-claims-chat.html`; verify repository-byte equality where available.
6. Preserve Site#116 as the sole owner of substantive private-document interpretation and derived-record custody.
7. Keep automated filing inactive until the exact-package, signature, authorized transport, confirmation, custody, reconstruction, revocation, retry, and duplicate-prevention gates verify.

## Archive conditions

This session's unique requirements are now durably transferred to this handoff and installed in production files. The session may be archived once validation/deployment observation is assigned to an active durable machine owner without relying on undocumented chat state. Current repository workflows and this handoff contain the continuation requirements; the remaining work does not require the conversation text.

## Completion measures

```text
task completion: 6/9
required developed files for current guided-card milestone: 4/4
scaffolding or stubs in current milestone: 0
missing adjacent required components: 2 (visual assets; browser/accessibility tests)
static validation implementation: 1/1
hosted validation observation: 0/1
integration among Guide/Guided/Chat: 3/3
public deployment observation: 0/3 routes
session requirement transfer: 9/9
```
