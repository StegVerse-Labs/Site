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
Validation workflow: .github/workflows/va-claims-chat-surface.yml
Deployment observer: .github/workflows/va-governed-surfaces-deployment.yml
Deployment receipt: data/va-claim-assistant/governed-surfaces-deployment.json
```

## Active claim

```text
Task: VACC-SURFACE-001
Claimant: Site#113 integration lane and repository-owned deployment observer
Role: CLAIMED_FOR_INTEGRATION and MACHINE_OWNED_DEPLOYMENT_OBSERVATION
Claim release condition: committed PASS repository receipt plus deployed HTTP 200 and exact repository-byte equality for the page and capability endpoint
Collision boundary: read-only production observation; do not modify Site#116 processors or represent upload, substantive interpretation, or filing as active
Next task after release: bind deployed governed adapter runtime and expand routes while preserving fail-closed unsupported routes
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

scripts/observe_va_governed_surfaces.py
commit 6c696f59023722b7241263e487beecd3722222ba

.github/workflows/va-governed-surfaces-deployment.yml
commit 6ecbcc68d006d6795318d5ac1119ec55aa88b1ab
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

## Validation and deployment evidence

Repository validation is complete through:

```text
data/va-claim-assistant/chat-surface-validation.json
state = PASS
private_document_upload_enabled = false
automated_filing_enabled = false
veteran_submission_authority_preserved = true
authority_effect = false
activation_effect = false
```

Deployment remains separate. It is verified only when:

```text
data/va-claim-assistant/governed-surfaces-deployment.json
state = VERIFIED
surfaces.chat.http_status = 200
surfaces.chat.byte_equal = true
surfaces.capability.http_status = 200
surfaces.capability.byte_equal = true
```

The observer runs on owned-path pushes, every six hours, or workflow dispatch. It does not deploy or mutate production.

## Remaining work

1. Observe the deployment receipt.
2. If `BLOCKED`, repair only the first retained Chat or capability deployment blocker.
3. Bind the page to the governed adapter runtime when required routes and execution receipts are available.
4. Keep document upload disabled until Site#116 proves substantive document execution, privacy, deletion, export, custody, reconstruction, and deployed runtime evidence.
5. Keep filing disabled until the filing contract, exact-package authorization, admitted transport, confirmation, retry, revocation, and duplicate-prevention gates pass.

## Cross-repository dependencies

```text
StegVerse-org/LLM-adapter#90: governed route generation and execution receipts
StegVerse-Labs/TVC: scoped provider and private-document capability custody
master-records/orchestration: sanitized session, package, and submission-confirmation custody
StegVerse-Labs/Site#116: substantive private multi-document workspace
StegVerse-Labs/Site#113: public Guide, Chat, capability projection, filing contract
```

## Archive conditions

This subordinate claim releases after the committed deployment receipt proves HTTP 200 and byte equality. The broader session remains active while route expansion, document workspace, admitted filing transport, and Ecosystem Chat activation remain incomplete.
