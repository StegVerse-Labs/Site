# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public `Humans as the Interoperability Layer` experiment surface within `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide Site authority and activation posture.

## Current goal

```text
Goal: activate the complete provenance-bound path from verified Primary and prompt references through exact response bytes, receiver receipt, authenticated private review, append-only public publication, Site projection, hash-chained Master Record release, and machine-observed deployed readiness.
Primary surface: humans-as-interoperability-layer.html
Response detail: humans-as-interoperability-response.html?id=HIL-RESP-...
Client: assets/hil-experiment.js
Experiment manifest: data/hil-experiment.json
Public response index: data/hil-responses.json
Master Record index: data/hil-master-records.json
Live observer: scripts/check_hil_live_readiness.py
Live workflow: .github/workflows/check-hil-live-readiness.yml
Receiver gateway: StegVerse-org/LLM-adapter PR #37
Controlled-cycle workflow: StegVerse-org/LLM-adapter/.github/workflows/hil-controlled-cycle.yml
Result: APPROVED_CONTROLLED_CYCLE_PASS_LIVE_STAGING
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

## Implemented application path

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

## Controlled-cycle CI evidence

The dedicated `HIL Controlled Cycle` workflow completed successfully on LLM-adapter PR #37 head `bc25376938db2fcfca84ac75d6fc9fc8a4f1f80d`, run `30113301291`. Architecture Guard and capability-runtime also completed successfully on that head. The general `validate` workflow was still in progress when this record was updated.

The controlled test exercises intake readiness, exact response and provenance persistence, receiver receipt v2, separate application clients over the same durable directory, authenticated `ACCEPT_PRIVATE`, private-review receipt, append-only publication, public lookup, and SQLite submission/review/publication records. This is CI evidence, not deployed-service restart evidence and not activation authority.

## Live readiness observer v2

The deployed-state observer now checks:

```text
approved Site markers
Primary base64 artifact availability and exact decoded SHA-256
gateway intake readiness
gateway Primary and prompt hashes
required provenance manifest
private-review configuration presence
publication readiness
append-only publication declaration
execution/publication/Master Record authority boundaries
```

It emits `HIL-LIVE-READINESS-OBSERVATION-v2` and reports `CONTROLLED_CYCLE_READY` only when all deployed prerequisites match. The scheduled workflow stores structured JSON as an artifact and workflow summary. Observation grants no activation, publication, execution, or Master Record authority.

## Append-only publication and Master Record staging

Publication requires `ACCEPT_PRIVATE`, public or anonymous participant consent, unique submission and response identifiers, a repository-relative PDF artifact path, durable storage, and a separate publication credential. No update or delete route exists.

The Site Master Record builder validates the ordered publication chain, binds response/provenance/private-review/publication hashes, binds the previous release hash, and computes a canonical release SHA-256. Default operation is dry-run; mutation requires explicit `--apply`. The Site index does not claim original-byte custody and does not replace `master-records/orchestration`.

## Required next vertical slice

```text
1. Observe completion of the remaining PR #37 validate workflow; retain any failure evidence and merge only after all required checks pass.
2. Install data/hil-primary-v0.5-review.pdf.b64 and verify exact bytes and SHA-256.
3. Deploy the merged gateway with durable HIL storage.
4. Configure intake, review, and publication credentials only in the authorized runtime.
5. Observe HIL-LIVE-READINESS-OBSERVATION-v2 reaching CONTROLLED_CYCLE_READY.
6. Run one controlled deployed PDF plus provenance-manifest submission.
7. Verify exact-byte and manifest persistence across an actual gateway restart.
8. Record one authenticated ACCEPT_PRIVATE decision and verify write-once behavior.
9. Record one authenticated publication decision and verify identifier uniqueness.
10. Import the first HIL-PUBLICATION-RECORD-v1 into the Site projection.
11. Build the first HIL-MASTER-RECORD-RELEASE-v1 and validate its release chain.
12. Submit the release and supporting evidence to master-records/orchestration only after authorization.
13. Open public acquisition only after the deployed controlled cycle passes.
```

## Authority boundaries

```text
participant approval != technical activation
Primary hash match != proof the LLM read the Primary
prompt hash match != proof of complete instruction following
response hash match != producer identity verification
producer signature != participant publication consent
CI controlled-cycle success != live deployment
new TestClient != actual service restart
live readiness observation != activation authority
receiver receipt != private review decision
private acceptance != public publication
publication record != original-byte custody
public projection != endorsement
Master Record release != custody
Site index != master-records/orchestration
```

## Release posture

No HIL canonical release tag or public data-acquisition activation is authorized while the Primary artifact is absent, PR #37 is unmerged or undeployed, and no controlled deployed submission, restart, private-review, publication, Site-import, and Master Record release cycle has produced persisted evidence.

## Archive readiness

This handoff, Site issue #67, LLM-adapter PR #37, the HIL pages, approved review records, schemas, client chain builder, gateway transitions, successful controlled-cycle CI evidence, Site importers/builders, live observer v2, validators, and repository history preserve complete continuation state. No additional conversation context is required.
