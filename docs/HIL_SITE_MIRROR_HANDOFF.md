# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public `Humans as the Interoperability Layer` experiment surface within `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide Site authority and activation posture.

## Current goal

```text
Goal: activate the complete provenance-bound path from verified Primary and prompt references through exact response bytes, receiver receipt, authenticated private review, append-only public publication, and later Master Record linkage.
Primary surface: humans-as-interoperability-layer.html
Response detail surface: humans-as-interoperability-response.html?id=HIL-RESP-...
Client: assets/hil-experiment.js
Experiment manifest: data/hil-experiment.json
Review state: data/hil-review-state.json
Initiating trace: data/hil-traces/HIL-TRACE-0001.json
Provenance schema: data/schemas/hil-response-provenance.schema.json
Private review schemas: data/schemas/hil-private-review-state.schema.json and hil-private-review-receipt.schema.json
Publication schema: data/schemas/hil-publication-record.schema.json
Private review contract: docs/HIL_PRIVATE_REVIEW_CONTRACT.md
Publication contract: docs/HIL_APPEND_ONLY_PUBLICATION_CONTRACT.md
Receiver gateway: StegVerse-org/LLM-adapter PR #37
Result: APPROVED_END_TO_END_STAGING
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

Participant approval is complete and remains separate from technical activation, private review, public acceptance, publication authority, and Master Record authority.

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

The Site builds `HIL-RESPONSE-PROVENANCE-v1` for every selected response PDF. It binds Primary, protocol, exact prompt, exact response bytes, model/provider declaration, generation metadata, conversation reference, and optional producer-signature state.

The browser computes the exact response PDF SHA-256 and submits the PDF plus provenance manifest only when gateway readiness reports matching Primary and prompt hashes and requires the provenance manifest. Otherwise the Site permits local manifest download but fails closed on transmission.

## Gateway intake implementation

`StegVerse-org/LLM-adapter` branch `build/hil-intake-gateway`, PR #37:

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

Tests cover exact-byte and manifest persistence, receipt v2, response-hash mismatch, wrong-Primary rejection, and active-content rejection.

## Private review transition

Authenticated endpoints:

```text
GET  /api/hil/submissions/{submission_id}/review-state
POST /api/hil/submissions/{submission_id}/review-decisions
Header: X-SteGVerse-HIL-Review-Token
Runtime secret: STEGVERSE_HIL_REVIEW_TOKEN
```

Allowed decisions are `ACCEPT_PRIVATE`, `QUARANTINE`, and `REJECT`. Review records are write-once. A decision produces `HIL-PRIVATE-REVIEW-RECEIPT-v1`. `ACCEPT_PRIVATE` does not authorize public publication.

## Append-only publication transition

Separately authenticated endpoints:

```text
GET  /api/hil/publication-readiness
GET  /api/hil/publications/{response_id}
POST /api/hil/submissions/{submission_id}/publication-decisions
Header: X-SteGVerse-HIL-Publication-Token
Runtime secret: STEGVERSE_HIL_PUBLICATION_TOKEN
```

Publication requires:

```text
private review decision = ACCEPT_PRIVATE
participant publication consent = public or anonymous
unique submission_id
unique HIL-RESP response_id
repository-relative .pdf artifact path
configured publication token
durable storage declared
```

The gateway creates `HIL-PUBLICATION-RECORD-v1`. Each accepted publication binds the Primary, response, provenance manifest, private-review receipt, public artifact path, and previous publication-record hash. Submission IDs and response IDs cannot be reused. No update or delete route exists.

Anonymous consent suppresses the public participant display name. Public projection authorization remains distinct from execution, endorsement, custody, and Master Record append.

Tests cover missing private acceptance, private-only consent rejection, successful public projection, public lookup, anonymous-name suppression, duplicate submission rejection, and response-ID reuse rejection.

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
-> authenticated reviewer records ACCEPT_PRIVATE, QUARANTINE, or REJECT
-> gateway issues HIL-PRIVATE-REVIEW-RECEIPT-v1
-> separately authenticated publication transition allocates one stable HIL-RESP ID
-> gateway emits append-only HIL-PUBLICATION-RECORD-v1
-> Site public response index and detail projection consume that record
-> Master Record linkage remains a later separately authorized transition
```

## Required next vertical slice

```text
1. Install data/hil-primary-v0.5-review.pdf.b64.
2. Change artifact_state only after repository verification of exact bytes and hash.
3. Observe CI for PR #37 and merge only after checks pass.
4. Deploy gateway with durable HIL storage.
5. Configure intake, review, and publication tokens only in the authorized runtime.
6. Observe readiness matching Primary and prompt hashes.
7. Run one controlled PDF plus provenance-manifest submission.
8. Verify exact-byte persistence, manifest persistence, receiver receipt, and restart persistence.
9. Record one authenticated ACCEPT_PRIVATE decision and verify write-once behavior.
10. Record one authenticated publication decision and verify response-ID/submission-ID uniqueness.
11. Project the first HIL-PUBLICATION-RECORD-v1 into data/hil-responses.json and the response detail page.
12. Open public acquisition only after the controlled end-to-end chain passes.
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
private acceptance != public publication
publication consent != publication mutation authority
publication record != custody
public projection authorization != endorsement
public projection authorization != Master Record append
Master Record inclusion != scientific proof
```

## Release posture

No HIL canonical release tag or public data-acquisition activation is authorized while the Primary artifact is absent from the repository, PR #37 is unmerged or undeployed, and no controlled live submission, private-review, and append-only publication cycle has produced persisted receipts and a stable public projection.

## Archive readiness

This handoff, Site issue #67, LLM-adapter PR #37, the HIL pages, approved review records, provenance/private-review/publication schemas, client chain builder, gateway intake/review/publication transitions, tests, validators, and repository history preserve complete continuation state. No additional conversation context is required.
