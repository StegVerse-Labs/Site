# Governed VA Claims Chat Mirror Handoff

## Identity

```text
Goal ID: SV-VA-CLAIMS-CHAT-001
Originating goal: govern the VA Claims Guide and VA Claims Chat, add ChatGPT-like private document workflows, and progress toward veteran-approved automated claim filing
Repository: StegVerse-Labs/Site
Branch: main
Canonical parent handoff: docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
Canonical issue: StegVerse-Labs/Site#113
Document workspace issue: StegVerse-Labs/Site#116
Public surface: va-claims-chat.html
Capability state: data/va-claim-assistant/chat-capability-state.json
Validator: scripts/validate_va_claims_chat_surface.py
Workflow: .github/workflows/va-claims-chat-surface.yml
```

## Active claim

```text
Task: VACC-SURFACE-001
Claimant: repository-owned workflow and Site#113 integration lane
Role: CLAIMED_FOR_INTEGRATION and MACHINE_OWNED validation
Claim created: 2026-08-02T20:40:00Z
Claim release condition: committed PASS receipt plus deployed HTTP 200 and exact repository-byte equality for the page and capability-state endpoint
Collision boundary: do not modify Site#116 document processors or represent upload, substantive interpretation, or filing as active
Next task after release: bind the governed LLM-adapter runtime and expand source-grounded routes while preserving fail-closed unsupported routes
```

## Installed implementation

```text
data/va-claim-assistant/chat-capability-state.json
commit 042d8c88506f9cc075f10862b70ca39bd1422a11

va-claims-chat.html
commit f18b8ec45f07eacb998a6c709557fcbca174c7c5

scripts/validate_va_claims_chat_surface.py
commit b24d6344601cf056e47dbe7dbd7364dad7f9affe

.github/workflows/va-claims-chat-surface.yml
commit 476ab30b99a302748e76e6d83b7b57b7f9e897f4
```

## Current capability

```text
state: SOURCE_GROUNDED_ACTIVE
current capability: SOURCE_GROUNDED_ASSISTANT
private document upload: DISABLED
automated filing: DISABLED
public upload: DISABLED
veteran submission authority: RETAINED
human review before filing: REQUIRED
authority effect: NONE
```

The surface visibly separates available, next, and future capabilities. It includes disabled upload and filing controls so future intent is preserved without implying activation.

## Validation

The deterministic validator requires:

- the current state and capability to remain source-grounded;
- private upload, public upload, and automated filing to remain false;
- veteran submission authority, human review, and fail-closed behavior to remain true;
- all authority flags to remain false;
- the page to display exact current, upcoming, filing-gate, and non-rating language;
- upload and filing controls to remain disabled.

Expected receipt:

```text
data/va-claim-assistant/chat-surface-validation.json
state = PASS
private_document_upload_enabled = false
automated_filing_enabled = false
veteran_submission_authority_preserved = true
authority_effect = false
activation_effect = false
```

Hosted workflow success, deployment, and public accessibility are not yet claimed.

## Remaining work

1. Observe and inspect the workflow-generated validation receipt.
2. Verify deployed `va-claims-chat.html` returns HTTP 200 and exactly matches repository bytes.
3. Add a governed link and capability projection to `va-disability-claim-guide.html` without rewriting its established evidence workflow inaccurately.
4. Bind the page to the governed adapter runtime when the required routes and execution receipt are available.
5. Keep document upload disabled until Site#116 proves substantive document execution, privacy, deletion, export, custody, reconstruction, and deployed runtime evidence.
6. Keep filing disabled until the filing integration contract, exact-package authorization, authorized transport, confirmation, retry, revocation, and duplicate-prevention gates pass.

## Cross-repository dependencies

```text
StegVerse-org/LLM-adapter: governed route classification, source-grounded answer generation, document-grounded generation, execution receipts
StegVerse-Labs/TVC: scoped provider and private-document capability custody
master-records/orchestration: sanitized session, package, and submission-confirmation custody and reconstruction
StegVerse-Labs/Site#116: substantive private multi-document workspace
StegVerse-Labs/Site#113: public Guide, Chat, capability projection, filing contract
```

## Archive conditions

This subordinate claim may release after validation and deployed byte equality. The broader session may archive only after every remaining Guide, Chat, document workspace, and filing requirement is completed or durably transferred to active canonical executors with machine-observable release conditions.

## Percentages

```text
developed files: 4/4
static validation path: installed
hosted validation: pending
public deployment verification: pending
runtime integration: pending
document upload activation: pending
automated filing activation: pending
```
