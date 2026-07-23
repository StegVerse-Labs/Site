# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public `Humans as the Interoperability Layer` experiment surface within `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide Site authority and activation posture.

## Current goal

```text
Goal: finish the artifact-submission path with fail-closed Primary -> protocol -> exact prompt -> response hash -> optional producer-signature validation, preserve exact bytes and the provenance manifest, issue a receiver receipt, and open public acquisition only after one controlled live chain passes.
Primary surface: humans-as-interoperability-layer.html
Response detail surface: humans-as-interoperability-response.html?id=HIL-RESP-...
Client: assets/hil-experiment.js
Experiment manifest: data/hil-experiment.json
Review state: data/hil-review-state.json
Initiating trace: data/hil-traces/HIL-TRACE-0001.json
Provenance schema: data/schemas/hil-response-provenance.schema.json
Receiver gateway: StegVerse-org/LLM-adapter PR #37
Result: APPROVED_CHAIN_INTAKE_STAGING
Authority: NONE
```

## Participant review state

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
Technical activation: NOT YET APPROVED BY MACHINE EVIDENCE
```

Sara stated that the updated Primary Review Candidate and Site presentation looked good and that everything looked good to proceed. Participant presentation approval is now recorded separately from technical activation and publication authority.

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

The Site now builds `HIL-RESPONSE-PROVENANCE-v1` for every selected response PDF. The manifest binds:

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

The browser computes the exact response PDF SHA-256 and creates the provenance manifest. It submits the PDF and manifest only when gateway readiness reports:

```text
state = READY
primary_sha256 = current Site Primary hash
prompt_sha256 = current Site prompt hash
provenance_manifest_required = true
```

Otherwise the Site permits local provenance-manifest download but fails closed on transmission.

## Gateway implementation

`StegVerse-org/LLM-adapter` branch `build/hil-intake-gateway`, PR #37 now:

```text
requires response_pdf and provenance_manifest
checks PDF MIME and %PDF- signature
rejects active-content markers
checks Primary version and SHA-256
checks protocol and prompt versions
checks exact prompt SHA-256
checks provenance response_sha256 against exact uploaded bytes
requires model and provider declarations
records optional producer-signature state without inventing verification
preserves exact PDF bytes and normalized provenance JSON separately
stores chain-validation state in SQLite
issues HIL-RECEIVER-RECEIPT-v2
keeps acceptance, publication, execution, and Master Record authority false
```

Chain states:

```text
PRIMARY_PROMPT_RESPONSE_CHAIN_VERIFIED
PRIMARY_PROMPT_RESPONSE_SIGNATURE_CHAIN_VERIFIED
```

A verified producer signature strengthens the chain but does not grant consent, acceptance, publication, or execution authority.

## Current participant flow

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
-> private review / quarantine / acceptance remains separate
-> accepted record receives stable HIL-RESP identifier
-> public response projection and Master Record linkage remain separate authorized transitions
```

## Required next vertical slice

```text
1. Install data/hil-primary-v0.5-review.pdf.b64.
2. Change artifact_state only after repository verifier confirms exact bytes and hash.
3. Merge PR #37 after CI and review.
4. Deploy gateway with durable HIL storage.
5. Enable STEGVERSE_HIL_INTAKE_ENABLED=true only with durable storage declared.
6. Observe gateway readiness matching Primary and prompt hashes.
7. Run one controlled PDF plus provenance-manifest submission.
8. Verify exact-byte persistence, manifest persistence, receiver receipt, and restart persistence.
9. Add private review/quarantine transition and append-only accepted-response publication.
10. Open public acquisition only after the controlled chain passes.
```

## Authority boundaries

```text
participant review approval != technical activation
Primary hash match != proof the LLM read the Primary
prompt hash match != proof of complete instruction following
response hash match != producer identity verification
producer signature != participant publication consent
browser validation != receiver validation
receiver receipt != acceptance
submission != publication
publication != endorsement
Master Record inclusion != scientific proof
live observation != activation authority
```

## Release posture

No HIL canonical release tag or public data-acquisition activation is authorized while the Primary artifact is absent from the repository, PR #37 is unmerged or undeployed, and no controlled live provenance-chain submission has produced a persisted receiver receipt.

## Archive readiness

This handoff, Site issue #67, LLM-adapter PR #37, the HIL pages, approved review records, provenance schema, client chain builder, gateway validator, manifests, validators, and repository history preserve complete continuation state. No additional conversation context is required.
