# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public `Humans as the Interoperability Layer` experiment surface within `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide Site authority and activation posture.

## Current goal

```text
Goal: activate a provenance-bound artifact-submission path from verified Primary and prompt references through exact response bytes, receiver receipt, authenticated private review, and later append-only publication.
Primary surface: humans-as-interoperability-layer.html
Response detail surface: humans-as-interoperability-response.html?id=HIL-RESP-...
Client: assets/hil-experiment.js
Experiment manifest: data/hil-experiment.json
Review state: data/hil-review-state.json
Initiating trace: data/hil-traces/HIL-TRACE-0001.json
Provenance schema: data/schemas/hil-response-provenance.schema.json
Private review schema: data/schemas/hil-private-review-receipt.schema.json
Private review contract: docs/HIL_PRIVATE_REVIEW_CONTRACT.md
Receiver gateway: StegVerse-org/LLM-adapter PR #37
Result: APPROVED_CHAIN_AND_PRIVATE_REVIEW_STAGING
Authority: NONE
```

## Participant approval

```text
Participant: Sara Katpar
Named attribution: GRANTED
Exchange reproduction: GRANTED
Model-response description: GRANTED
Public record inclusion: GRANTED
Primary PDF review: APPROVED
Site presentation review: APPROVED
Final presentation approval: APPROVED
Approval evidence: LinkedIn direct-message screenshots, 2026-07-23
Technical activation: NOT YET PROVEN BY LIVE MACHINE EVIDENCE
```

Participant approval is complete and remains separate from technical activation, private review, public acceptance, and publication authority.

## Primary and prompt chain

```text
Primary version: v0.5
Primary filename: Humans_as_the_Interoperability_Layer_Primary_Review_Candidate_v0_5.pdf
Primary SHA-256: 52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946
Primary size: 109210 bytes
Primary repository path: data/hil-primary-v0.5-review.pdf.b64
Primary artifact state: PENDING_INSTALLATION
Protocol: HIL-PROTOCOL-v1.0
Prompt: HIL-PROMPT-v1.0
Prompt SHA-256: 0ebe215318b4eeeb8ed6422e0954372c314fadc8fac9254e452bc7670a1b9922
```

## Implemented artifact-submission chain

The Site builds `HIL-RESPONSE-PROVENANCE-v1` for every selected response PDF. It binds:

```text
primary_version
primary_sha256
protocol_version
prompt_version
prompt_sha256
response_sha256
model
provider
generated_at
conversation_reference
producer_signature.state
producer_signature.scheme
producer_signature.value
producer_signature.key_id
```

The browser computes the exact response PDF SHA-256 and submits the PDF plus provenance manifest only when gateway readiness reports matching Primary and prompt hashes and requires the provenance manifest. Otherwise the Site permits local manifest download but fails closed on transmission.

## Gateway implementation

`StegVerse-org/LLM-adapter` branch `build/hil-intake-gateway`, PR #37 now:

```text
requires response_pdf and provenance_manifest
checks PDF MIME and %PDF- signature
rejects active-content markers
checks Primary version and SHA-256
checks protocol and prompt versions
checks exact prompt SHA-256
checks response_sha256 against exact uploaded bytes
requires model and provider declarations
records optional producer-signature state without inventing verification
preserves exact PDF bytes and normalized provenance JSON separately
stores chain-validation state in SQLite
issues HIL-RECEIVER-RECEIPT-v2
keeps acceptance, publication, execution, and Master Record authority false
```

Updated tests now cover exact-byte and manifest persistence, receipt v2, response-hash mismatch, wrong-Primary rejection, and active-content rejection. PR #37 returned to mergeable state after the tests were aligned with the provenance-bound API.

## Private review transition

The gateway now also provides authenticated private review endpoints:

```text
GET  /api/hil/submissions/{submission_id}/review-state
POST /api/hil/submissions/{submission_id}/review-decisions
```

They require `X-SteGVerse-HIL-Review-Token`, sourced only from server-side `STEGVERSE_HIL_REVIEW_TOKEN`.

Allowed decisions:

```text
ACCEPT_PRIVATE
QUARANTINE
REJECT
```

The review-state endpoint exposes hashes and validation metadata but not stored artifact bytes or storage paths. A decision produces `HIL-PRIVATE-REVIEW-RECEIPT-v1`. Review records are write-once for each submission; later attempts fail with conflict rather than overwrite the first decision.

`ACCEPT_PRIVATE` does not authorize public acceptance, publication, execution, or Master Record append.

## Current participant path

```text
Site downloads and verifies Primary PDF
-> participant submits unchanged Primary to selected LLM
-> participant uses exact prompt
-> participant receives response-only PDF
-> browser validates PDF and computes response hash
-> browser builds HIL-RESPONSE-PROVENANCE-v1
-> gateway readiness must match Primary and prompt hashes
-> gateway receives exact PDF bytes plus provenance manifest
-> gateway recomputes and validates the chain
-> gateway preserves both artifacts
-> gateway issues HIL-RECEIVER-RECEIPT-v2
-> authenticated private reviewer records ACCEPT_PRIVATE, QUARANTINE, or REJECT
-> gateway issues HIL-PRIVATE-REVIEW-RECEIPT-v1
-> separate authorized publication transition may allocate HIL-RESP and append the public index
```

## Required next vertical slice

```text
1. Install data/hil-primary-v0.5-review.pdf.b64.
2. Change artifact_state only after repository verification of exact bytes and hash.
3. Observe CI for PR #37 and merge after checks pass.
4. Deploy gateway with durable HIL storage.
5. Configure STEGVERSE_HIL_INTAKE_ENABLED=true and STEGVERSE_HIL_REVIEW_TOKEN only in the authorized runtime.
6. Observe readiness matching Primary and prompt hashes.
7. Run one controlled PDF plus provenance-manifest submission.
8. Verify exact-byte persistence, manifest persistence, receiver receipt, and restart persistence.
9. Record one authenticated private review decision and verify write-once behavior.
10. Build the separately authorized append-only publication transition.
11. Open public acquisition only after the controlled chain and private review cycle pass.
```

## Authority boundaries

```text
participant approval != technical activation
Primary hash match != proof the LLM read the Primary
prompt hash match != proof of complete instruction following
response hash match != producer identity verification
producer signature != participant publication consent
browser validation != receiver validation
receiver receipt != private review decision
private acceptance != public acceptance
private acceptance != publication
review receipt != Master Record append
submission != publication
publication != endorsement
Master Record inclusion != scientific proof
```

## Release posture

No HIL canonical release tag or public data-acquisition activation is authorized while the Primary artifact is absent from the repository, PR #37 is unmerged or undeployed, and no controlled live provenance-chain submission plus authenticated private review has produced persisted receipts.

## Archive readiness

This handoff, Site issue #67, LLM-adapter PR #37, the HIL pages, approved review records, provenance and private-review schemas, client chain builder, gateway validator, review transition, manifests, validators, and repository history preserve complete continuation state. No additional conversation context is required.
