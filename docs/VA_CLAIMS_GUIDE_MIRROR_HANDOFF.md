# Governed VA Claims Guide Mirror Handoff

## Identity

```text
Task ID: VACG-SURFACE-001
Originating goal: govern the VA Claims Guide and establish its goals as part of the governed VA product family
Repository: StegVerse-Labs/Site
Branch: main
Canonical parent: docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
Canonical issue: StegVerse-Labs/Site#113
Public surface: va-disability-claim-guide.html
Capability state: data/va-claim-assistant/chat-capability-state.json
Validator: scripts/validate_va_claims_guide_surface.py
Validation workflow: .github/workflows/va-claims-guide-surface.yml
Deployment observer: .github/workflows/va-governed-surfaces-deployment.yml
Deployment receipt: data/va-claim-assistant/governed-surfaces-deployment.json
```

## Claim

```text
implementation claim: RELEASED_COMPLETE_FOR_REPOSITORY_SURFACE
repository validation claim: RELEASED_COMPLETE
repository validation evidence: data/va-claim-assistant/guide-surface-validation.json state PASS
remaining observation claim: MACHINE_OWNED_DEPLOYMENT_OBSERVATION
observation owner: .github/workflows/va-governed-surfaces-deployment.yml
observation cadence: owned-path push, every six hours, or workflow dispatch
observation release condition: guide HTTP 200 and exact deployed-to-repository SHA-256 equality in the committed deployment receipt
collision boundary: read-only production observation; do not modify HIL deployment files or enable private document upload or automated filing
```

## Completed work

```text
Governed Guide rewrite: f790b3864ba0ecc5f016211f110bc7389515b479
Guide validator: c448467b5c81687f8bf5b4960a907771a0b04adf
Guide workflow: f3f08f77e8c7b2fbb55aaba6662f644b308690bb
Validator contract repair: 72391f5ad049493b1414b494afaad39fdc438fa1
Guide validation receipt: data/va-claim-assistant/guide-surface-validation.json state PASS schema 1.0.1
Deployment observer script: 6c696f59023722b7241263e487beecd3722222ba
Deployment observer workflow: 6ecbcc68d006d6795318d5ac1119ec55aa88b1ab
Claims Chat validation receipt: data/va-claim-assistant/chat-surface-validation.json state PASS
Product goals validation receipt: data/va-claim-assistant/governed-product-goals-validation.json state PASS
```

The Guide identifies itself as governed, links the native Governed VA Claims Chat, displays `SOURCE_GROUNDED_ASSISTANT`, keeps private document upload and automated filing disabled, establishes the document-workspace roadmap and veteran-approved filing gates, and preserves veteran control of facts, claimed conditions, package authorization, signature, and submission.

## Validation result

```text
state: PASS
private_document_upload_enabled: false
automated_filing_enabled: false
veteran_submission_authority_preserved: true
human_review_required_before_filing: true
fail_closed_when_evidence_or_authority_missing: true
authority_effect: false
activation_effect: false
```

Repository validation is complete. Deployment is verified only when `data/va-claim-assistant/governed-surfaces-deployment.json` records `state = VERIFIED`, Guide HTTP 200, and byte equality.

## Remaining exact tasks

1. Observe the machine-owned deployment receipt.
2. If `BLOCKED`, repair only the first retained Guide deployment blocker.
3. Preserve the current capability until document-aware execution and custody are proven.
4. Continue runtime expansion under `StegVerse-org/LLM-adapter#90`.
5. Continue private upload and multi-document analysis under `StegVerse-Labs/Site#116`.
6. Keep filing inactive until an authorized transport and every filing gate verify.

## Cross-repository dependencies

```text
Governed Chat runtime: StegVerse-org/LLM-adapter#90
Private document workspace: StegVerse-Labs/Site#116
Capability custody: StegVerse-Labs/TVC
Derived-record and submission custody: master-records/orchestration
Public projection and filing contract: StegVerse-Labs/Site#113
```

## Authority and session boundary

The Guide has no adjudication, representation, legal-opinion, medical-opinion, rating, signature, credential, filing, publication, or activation authority.

`MERGED INTO: StegVerse-Labs/Site#113 and docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`

The Guide implementation and repository validation are durable and complete. Its only remaining claim is machine-owned deployment observation.
