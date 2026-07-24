# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public `Humans as the Interoperability Layer` experiment surface within `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide Site authority and activation posture.

## Current goal

```text
Goal: activate the complete provenance-bound path from verified Primary and prompt references through exact response bytes, receiver receipt, authenticated private review, append-only public publication, Site projection, and hash-chained Master Record release.
Primary surface: humans-as-interoperability-layer.html
Response detail: humans-as-interoperability-response.html?id=HIL-RESP-...
Client: assets/hil-experiment.js
Experiment manifest: data/hil-experiment.json
Public response index: data/hil-responses.json
Master Record index: data/hil-master-records.json
Provenance schema: data/schemas/hil-response-provenance.schema.json
Publication schema: data/schemas/hil-publication-record.schema.json
Master Record schema: data/schemas/hil-master-record-release.schema.json
Publication importer: scripts/import_hil_publication.py
Master Record builder: scripts/build_hil_master_record.py
Receiver gateway: StegVerse-org/LLM-adapter PR #37
Result: APPROVED_MASTER_RECORD_STAGING
Authority: NONE
```

## Participant approval

Sara Katpar granted named attribution, exchange reproduction, model-response description, and public-record inclusion permission. She reviewed the v0.5 Primary candidate and Site presentation and stated that everything looked good to proceed. Participant approval is complete and remains separate from technical activation, private review, publication mutation, custody, and Master Record authority.

## Primary and prompt chain

```text
Primary version: v0.5
Primary SHA-256: 52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946
Primary repository path: data/hil-primary-v0.5-review.pdf.b64
Primary artifact state: PENDING_INSTALLATION
Protocol: HIL-PROTOCOL-v1.0
Prompt: HIL-PROMPT-v1.0
Prompt SHA-256: 0ebe215318b4eeeb8ed6422e0954372c314fadc8fac9254e452bc7670a1b9922
```

## Implemented end-to-end application path

```text
Site verifies Primary identity and exact prompt
-> browser hashes response PDF
-> browser creates HIL-RESPONSE-PROVENANCE-v1
-> gateway verifies Primary, prompt, response, and optional signature state
-> gateway preserves exact PDF bytes and normalized provenance manifest
-> gateway issues HIL-RECEIVER-RECEIPT-v2
-> authenticated reviewer records ACCEPT_PRIVATE, QUARANTINE, or REJECT
-> gateway issues HIL-PRIVATE-REVIEW-RECEIPT-v1
-> separately authenticated publisher allocates one stable HIL-RESP ID
-> gateway emits HIL-PUBLICATION-RECORD-v1
-> Site importer validates hash continuity and appends the public projection
-> deterministic builder emits HIL-MASTER-RECORD-RELEASE-v1
```

## Append-only publication

Publication requires `ACCEPT_PRIVATE`, public or anonymous participant consent, unique submission and response identifiers, a repository-relative PDF artifact path, durable storage, and a separate publication credential. Anonymous publication suppresses the participant display name. No update or delete route exists.

## Master Record release staging

The Site now includes:

```text
data/schemas/hil-master-record-release.schema.json
data/hil-master-records.json
scripts/build_hil_master_record.py
docs/HIL_MASTER_RECORD_RELEASE_CONTRACT.md
```

The builder validates the ordered response publication chain, binds response/provenance/private-review/publication hashes, binds the previous Master Record release hash, and computes a canonical release SHA-256. Default execution is dry-run. Repository mutation requires explicit `--apply`. The Site Master Record index does not claim custody and does not replace `master-records/orchestration`.

## Required next vertical slice

```text
1. Install data/hil-primary-v0.5-review.pdf.b64.
2. Change artifact_state only after repository verification of exact bytes and hash.
3. Observe CI for PR #37 and merge only after checks pass.
4. Deploy the gateway with durable HIL storage.
5. Configure intake, review, and publication credentials only in the authorized runtime.
6. Observe readiness matching Primary and prompt hashes.
7. Run one controlled PDF plus provenance-manifest submission.
8. Verify exact-byte and manifest persistence across restart.
9. Record one authenticated ACCEPT_PRIVATE decision and verify write-once behavior.
10. Record one authenticated publication decision and verify identifier uniqueness.
11. Import the first HIL-PUBLICATION-RECORD-v1 into the Site projection.
12. Build the first HIL-MASTER-RECORD-RELEASE-v1 and validate its release chain.
13. Submit the release and supporting evidence to master-records/orchestration only after authorization.
14. Open public acquisition only after the controlled cycle passes.
```

## Authority boundaries

```text
participant approval != technical activation
Primary hash match != proof the LLM read the Primary
prompt hash match != proof of complete instruction following
response hash match != producer identity verification
producer signature != participant publication consent
receiver receipt != private review decision
private acceptance != public publication
publication record != original-byte custody
public projection != endorsement
Master Record release != custody
Master Record release != execution authority
Master Record release != scientific proof
Site index != master-records/orchestration
```

## Release posture

No HIL canonical release tag or public data-acquisition activation is authorized while the Primary artifact is absent, PR #37 is unmerged or undeployed, and no controlled live submission, private-review, publication, Site-import, and Master Record release cycle has produced persisted evidence.

## Archive readiness

This handoff, Site issue #67, LLM-adapter PR #37, the HIL pages, approved review records, provenance/private-review/publication/Master-Record schemas, client chain builder, gateway transitions, Site importers/builders, validators, and repository history preserve complete continuation state. No additional conversation context is required.
