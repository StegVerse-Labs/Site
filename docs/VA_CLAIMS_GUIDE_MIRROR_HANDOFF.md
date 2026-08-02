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
validation claim: MACHINE_OWNED
validation owner: .github/workflows/va-claims-guide-surface.yml
claim release condition: committed PASS receipt plus deployed page HTTP 200 and exact deployed-to-repository byte equality
collision boundary: do not enable private document upload or automated filing from Guide text or fixture evidence
```

## Completed work

```text
Governed Guide rewrite: f790b3864ba0ecc5f016211f110bc7389515b479
Guide validator: c448467b5c81687f8bf5b4960a907771a0b04adf
Guide workflow: f3f08f77e8c7b2fbb55aaba6662f644b308690bb
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

## Validation commands

```bash
python scripts/validate_va_governed_product_goals.py
python scripts/validate_va_claims_chat_surface.py
python scripts/validate_va_claims_guide_surface.py
```

## Remaining exact tasks

1. Observe `data/va-claim-assistant/guide-surface-validation.json` with `state = PASS`.
2. Observe deployed `va-disability-claim-guide.html` returning HTTP 200.
3. Verify deployed Guide bytes equal the repository bytes.
4. Preserve the current capability state until document-aware execution and custody are proven.
5. Transfer runtime expansion to the governed Claims Chat owner.
6. Transfer private upload and multi-document analysis to `StegVerse-Labs/Site#116`.
7. Keep automated filing inactive until an authorized filing integration and all filing gates verify.

## Cross-repository dependencies

```text
Governed Chat runtime: StegVerse-org/LLM-adapter
Private document workspace: StegVerse-Labs/Site#116
Capability custody: StegVerse-Labs/TVC
Derived-record and submission custody: master-records/orchestration
Public projection and filing contract: StegVerse-Labs/Site#113
```

## Authority boundary

The Guide has no adjudication, representation, legal-opinion, medical-opinion, rating, signature, credential, filing, publication, or activation authority. It may describe future capabilities only as unavailable targets until their exact receipts and deployment observations pass.

## Session consolidation

`MERGED INTO: StegVerse-Labs/Site#113 and docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`

The Guide-specific requirements are durable. This session retains a distinct observation and integration role until Guide validation/deployment is observed and the remaining governed Chat, document workspace, filing contract, and Ecosystem Chat requirements are completed or transferred to verified active executors.
