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
Workflow: .github/workflows/va-claims-guide-surface.yml
```

## Claim

```text
implementation claim: RELEASED_COMPLETE_FOR_REPOSITORY_SURFACE
repository validation claim: RELEASED_COMPLETE
repository validation evidence: data/va-claim-assistant/guide-surface-validation.json state PASS
remaining observation claim: MACHINE_OWNED_DEPLOYMENT_OBSERVATION
observation owner: .github/workflows/va-claims-guide-surface.yml and Site deployment control
observation release condition: deployed page HTTP 200 and exact deployed-to-repository byte equality
collision boundary: do not enable private document upload or automated filing from Guide text or fixture evidence
```

## Completed work

```text
Governed Guide rewrite: f790b3864ba0ecc5f016211f110bc7389515b479
Guide validator: c448467b5c81687f8bf5b4960a907771a0b04adf
Guide workflow: f3f08f77e8c7b2fbb55aaba6662f644b308690bb
Validator contract repair: 72391f5ad049493b1414b494afaad39fdc438fa1
Guide validation receipt: data/va-claim-assistant/guide-surface-validation.json state PASS schema 1.0.1
Claims Chat validation receipt: data/va-claim-assistant/chat-surface-validation.json state PASS
Product goals validation receipt: data/va-claim-assistant/governed-product-goals-validation.json state PASS
```

The Guide now:

- identifies itself as governed;
- links the native Governed VA Claims Chat;
- displays `SOURCE_GROUNDED_ASSISTANT` as the current capability;
- keeps private document upload and automated filing disabled;
- establishes the document-workspace roadmap;
- establishes veteran-approved automated filing gates;
- preserves veteran control of material facts, claimed conditions, package authorization, signature, and submission;
- prohibits submission while any applicable filing gate remains unmet.

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

Repository validation is complete. Deployment and byte equality remain a separate evidence level.

## Validation commands

```bash
python scripts/validate_va_governed_product_goals.py
python scripts/validate_va_claims_chat_surface.py
python scripts/validate_va_claims_guide_surface.py
```

## Remaining exact tasks

1. Observe deployed `va-disability-claim-guide.html` returning HTTP 200.
2. Verify deployed Guide bytes equal the repository bytes.
3. Preserve the current capability state until document-aware execution and custody are proven.
4. Continue runtime expansion under `StegVerse-org/LLM-adapter#90` and `docs/VA_CLAIMS_CHAT_RUNTIME_MIRROR_HANDOFF.md`.
5. Continue private upload and multi-document analysis under `StegVerse-Labs/Site#116`.
6. Keep automated filing inactive until an authorized filing integration and all filing gates verify.

## Cross-repository dependencies

```text
Governed Chat runtime: StegVerse-org/LLM-adapter#90
Runtime contract: StegVerse-org/LLM-adapter/docs/VA_CLAIMS_CHAT_RUNTIME_MIRROR_HANDOFF.md
Private document workspace: StegVerse-Labs/Site#116
Capability custody: StegVerse-Labs/TVC
Derived-record and submission custody: master-records/orchestration
Public projection and filing contract: StegVerse-Labs/Site#113
```

## Authority boundary

The Guide has no adjudication, representation, legal-opinion, medical-opinion, rating, signature, credential, filing, publication, or activation authority. It may describe future capabilities only as unavailable targets until their exact receipts and deployment observations pass.

## Session consolidation

`MERGED INTO: StegVerse-Labs/Site#113 and docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`

The Guide-specific implementation and repository validation requirements are durable and complete. No chat history is required to reproduce them. The remaining Guide work is deployment observation owned by repository automation and Site deployment controls.
