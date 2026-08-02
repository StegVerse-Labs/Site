# VA Filing Integration Mirror Handoff

## Identity

```text
Task ID: VAFI-CONTRACT-001
Originating goal: work toward automated VA claim filing from veteran-uploaded documents while preserving veteran authority and governed evidence boundaries
Repository: StegVerse-Labs/Site
Branch: main
Canonical parent: docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
Canonical issue: StegVerse-Labs/Site#113
Document workspace dependency: StegVerse-Labs/Site#116
Contract: data/va-claim-assistant/filing-integration-contract.json
Validator: scripts/validate_va_filing_integration_contract.py
Workflow: .github/workflows/va-filing-integration-contract.yml
Receipt: data/va-claim-assistant/filing-integration-contract-validation.json
```

## Claim

```text
role: INTEGRATION_CONTRACT_AND_VALIDATION
claim state: MACHINE_OWNED_VALIDATION
claim created: 2026-08-02T21:28:00Z
release condition: committed PASS receipt and accepted transfer into Site#113, Site#116, TVC, Master Records, and an admitted transport implementation lane
collision boundary: no credential collection, browser automation, signature, submission transport, claim submission, or filing activation
```

## Installed contract

The contract establishes a governed progression from derived evidence to a veteran-approved filing package:

```text
DRAFT_PACKAGE
→ VETERAN_REVIEW_REQUIRED
→ PREFLIGHT_REQUIRED
→ EXACT_PACKAGE_AUTHORIZATION_REQUIRED
→ TRANSPORT_ADMISSION_REQUIRED
→ READY_FOR_VETERAN_APPROVED_SUBMISSION
→ SUBMISSION_IN_PROGRESS
→ SUBMITTED_CONFIRMATION_PENDING_CUSTODY
→ SUBMITTED_CONFIRMED
```

It also defines fail-closed `BLOCKED`, `REVOKED`, `PARTIAL_FAILURE_REVIEW_REQUIRED`, and `DUPLICATE_PREVENTED` states.

## Veteran authority boundary

The veteran must:

- confirm every material fact;
- select every claimed condition;
- review contradictions, unfavorable evidence, and missing evidence;
- approve forms and supporting statements;
- authorize the exact package hash;
- provide a valid signature or separately valid delegation;
- retain the ability to revoke before submission.

The assistant may not sign, select claimed conditions, confirm facts, collect VA credentials, or submit through unadmitted browser automation.

## Transport boundary

```text
active transport: none
submission enabled: false
allowed future transport classes:
- AUTHORIZED_VA_INTEGRATION
- AUTHORIZED_ACCREDITED_REPRESENTATIVE_INTEGRATION
```

Any transport requires a scoped and expiring TVC capability receipt, revocation support, custody, reconstruction, duplicate prevention, and exact-package hash matching.

## Package and execution controls

Required package evidence includes:

- veteran identity reference;
- veteran-selected claimed conditions;
- veteran-confirmed material facts;
- evidence index and source hashes;
- page anchors;
- separately labeled inference;
- contradictions and unfavorable evidence;
- missing evidence;
- current form and rule versions;
- package SHA-256 and change log.

Submission requires idempotency, commit-time authorization validity, duplicate prevention, partial-failure stop, state reconstruction before retry, and retained submission confirmation.

## Machine-owned validation

```text
workflow: .github/workflows/va-filing-integration-contract.yml
trigger: owned-path push, every six hours, or workflow dispatch
success: PASS receipt with submission disabled, transport absent, veteran authority preserved, exact-package authorization required, duplicate prevention required, and reconstruction PASS required
```

## Cross-repository continuation

```text
Site#113:
package contract, public status, veteran review and authorization surfaces

Site#116:
derived evidence, document hashes, page anchors, contradictions, missing evidence, and review packet export

LLM-adapter#90:
governed conversational preparation using sanitized derived context only

TVC:
future scoped transport and credential capability custody

master-records/orchestration:
package, authorization, transport-admission, attempt, confirmation, and reconstruction custody
```

## Transfer

```text
MERGED INTO: StegVerse-Labs/Site#113
MERGED INTO: StegVerse-Labs/Site#116
```

The contract does not create an admitted transport lane. Once the PASS receipt exists, this bounded contract task may be released while actual filing remains blocked on an authorized transport and all exact-package evidence gates.

## Archive conditions

This subordinate task is archive-safe after its PASS receipt is committed and the canonical issues record acceptance. The broader session remains active while substantive document execution, route generators, transport admission, submission confirmation, and Ecosystem Chat activation remain incomplete.
