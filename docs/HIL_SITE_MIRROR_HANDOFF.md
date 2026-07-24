# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public `Humans as the Interoperability Layer` experiment surface within `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide Site authority and activation posture.

## Current goal

```text
Goal: activate the complete provenance-bound path from verified Primary and prompt references through exact response bytes, receiver receipt, authenticated private review, append-only public publication, Site projection, hash-chained Master Record release, and one machine-observed controlled cycle.
Primary surface: humans-as-interoperability-layer.html
Response detail: humans-as-interoperability-response.html?id=HIL-RESP-...
Client: assets/hil-experiment.js
Experiment manifest: data/hil-experiment.json
Public response index: data/hil-responses.json
Master Record index: data/hil-master-records.json
Publication importer: scripts/import_hil_publication.py
Master Record builder: scripts/build_hil_master_record.py
Receiver gateway: StegVerse-org/LLM-adapter PR #37
Controlled-cycle workflow: StegVerse-org/LLM-adapter/.github/workflows/hil-controlled-cycle.yml
Result: APPROVED_CONTROLLED_CYCLE_CI_STAGING
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

## Controlled-cycle CI

PR #37 now contains `tests/test_hil_controlled_cycle.py` and `.github/workflows/hil-controlled-cycle.yml`.

The controlled test executes:

```text
READY observation
-> response PDF plus provenance submission
-> receiver receipt v2
-> new client process boundary
-> authenticated review-state lookup
-> ACCEPT_PRIVATE decision
-> private-review receipt
-> authenticated append-only publication
-> public publication lookup through a third client
-> exact PDF and provenance persistence checks
-> SQLite submission/review/publication row checks
```

The workflow runs the complete HIL test set on Python 3.11 and emits an observation-only `HIL-CONTROLLED-CYCLE-CI-v1` artifact. The artifact grants no deployment, publication, or Master Record authority.

Current observation at the latest PR head: HIL Controlled Cycle, validate, capability-runtime, and Architecture Guard workflow runs were queued. No successful CI conclusion has yet been observed, so merge and activation remain blocked.

## Append-only publication and Master Record staging

Publication requires `ACCEPT_PRIVATE`, public or anonymous participant consent, unique submission and response identifiers, a repository-relative PDF artifact path, durable storage, and a separate publication credential. No update or delete route exists.

The Site Master Record builder validates the ordered publication chain, binds response/provenance/private-review/publication hashes, binds the previous release hash, and computes a canonical release SHA-256. Default operation is dry-run; mutation requires explicit `--apply`. The Site index does not claim original-byte custody and does not replace `master-records/orchestration`.

## Required next vertical slice

```text
1. Observe the new PR #37 workflow conclusions and retain the first failing job/log if any.
2. Resolve any CI failure or branch conflict; merge only after checks pass.
3. Install data/hil-primary-v0.5-review.pdf.b64 and verify exact bytes and SHA-256.
4. Deploy the merged gateway with durable HIL storage.
5. Configure intake, review, and publication credentials only in the authorized runtime.
6. Observe readiness matching Primary and prompt hashes.
7. Run one controlled live PDF plus provenance-manifest submission.
8. Verify exact-byte and manifest persistence across an actual gateway restart.
9. Record one authenticated ACCEPT_PRIVATE decision and verify write-once behavior.
10. Record one authenticated publication decision and verify identifier uniqueness.
11. Import the first HIL-PUBLICATION-RECORD-v1 into the Site projection.
12. Build the first HIL-MASTER-RECORD-RELEASE-v1 and validate its release chain.
13. Submit the release and supporting evidence to master-records/orchestration only after authorization.
14. Open public acquisition only after the controlled live cycle passes.
```

## Authority boundaries

```text
participant approval != technical activation
Primary hash match != proof the LLM read the Primary
prompt hash match != proof of complete instruction following
response hash match != producer identity verification
producer signature != participant publication consent
CI test pass != live deployment
new TestClient != actual service restart
receiver receipt != private review decision
private acceptance != public publication
publication record != original-byte custody
public projection != endorsement
Master Record release != custody
Master Record release != execution authority
Site index != master-records/orchestration
```

## Release posture

No HIL canonical release tag or public data-acquisition activation is authorized while the Primary artifact is absent, PR #37 is unmerged or undeployed, CI has not been observed successful, and no controlled live submission, restart, private-review, publication, Site-import, and Master Record release cycle has produced persisted evidence.

## Archive readiness

This handoff, Site issue #67, LLM-adapter PR #37, the HIL pages, approved review records, provenance/private-review/publication/Master-Record schemas, client chain builder, gateway transitions, controlled-cycle workflow and tests, Site importers/builders, validators, and repository history preserve complete continuation state. No additional conversation context is required.
