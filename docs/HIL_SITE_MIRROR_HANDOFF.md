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
Result: APPROVED_CLEAN_REBASE_AND_CONTROLLED_CYCLE_STAGING
Authority: NONE
```

## Participant approval

Sara Katpar granted named attribution, exchange reproduction, model-response description, and public-record inclusion permission. She reviewed the v0.5 Primary candidate and Site presentation and stated that everything looked good to proceed. Participant approval is complete and remains separate from technical activation, private review, publication mutation, custody, and Master Record authority.

## Participant-originated continuation

Sara Katpar independently proposed publishing a LinkedIn reflection about the exchange, the research, and the value of curiosity, and requested permission to mention and tag Rigel Randolph. The available screenshot does not show a sent response from Rigel. Reciprocal permission therefore remains pending and must not be represented as granted until evidence of the sent response exists. This event is preserved as `data/hil-traces/HIL-CONTINUATION-0001.json` and linked from `HIL-TRACE-0001`.

```text
Continuation ID: HIL-CONTINUATION-0001
Parent: HIL-TRACE-0001
Type: INDEPENDENT_PARTICIPANT_PUBLIC_REFLECTION
Authorship: participant-controlled
Publication: participant-controlled
Reciprocal permission: AWAITING_RIGEL_RESPONSE
Protocol submission: false
Directed testimonial: false
Site ingestion authority: false
Master Record authority: false
```

The prepared response is:

```text
Absolutely. You are welcome to mention me, tag me, and discuss our exchange and the research. Please write it in your own voice and present it as you believe is accurate.
```

After the response is actually sent, capture evidence of the sent message and update the reciprocal-permission state. The eventual public post, URL, and captured artifact hash remain pending participant publication and may be appended only after the public artifact exists and is independently captured.

## Participant continuation outreach trace

`data/hil-participant-traces/HIL-PARTICIPANT-TRACE-SARA-002.json` records Rigel Randolph's later message informing Sara Katpar that the prior exchange had been formalized into the paper and public replication protocol and that the dedicated Site surfaces, response schema, hash verification, receipt structure, and bounded upload gateway had been built while final public intake deployment remained incomplete.

```text
Trace ID: HIL-PARTICIPANT-TRACE-SARA-002
State: CONTACTED_AWAITING_RESPONSE
Outreach sent: ESTABLISHED
Acknowledgment received: NOT_ESTABLISHED
Prior approved scope: PRESERVED
New consent inferred: false
Technical activation authority: false
Publication authority: false
Custody authority: false
Execution authority: false
Commit: 1e307e5c8bf8c31bdfa70454d63eaff896db2852
```

This outreach does not enlarge the earlier participant approval and does not authorize activation, intake, review, publication, custody, execution, or Master Record mutation.

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

The dedicated `HIL Controlled Cycle` workflow completed successfully on the earlier LLM-adapter PR #37 head `bc25376938db2fcfca84ac75d6fc9fc8a4f1f80d`, run `30113301291`. Architecture Guard and capability-runtime also completed successfully on that head. This is CI evidence, not deployed-service restart evidence and not activation authority.

The controlled test exercises intake readiness, exact response and provenance persistence, receiver receipt v2, separate application clients over the same durable directory, authenticated `ACCEPT_PRIVATE`, private-review receipt, append-only publication, public lookup, and SQLite submission/review/publication records.

## Clean rebase onto current gateway main

PR #37 had fallen 91 commits behind `main` and became non-mergeable. The HIL changes were rebuilt as a single commit on the current `main` tree while preserving all current gateway files and reconciling the two shared files:

```text
base main: 47cfad18eb75746410e6d3d58516515aaae26be5
rebased HIL head: 336433dff29758d9581b0541daaac53b54126f30
status: ahead by 1, behind by 0
PR mergeable: true
changed files: 9
```

The reconciled `combined_gateway.py` keeps the current provider-usage custody middleware and adds HIL intake/publication routers, HIL endpoint advertisement, and the two server-only HIL authorization headers. `pyproject.toml` keeps current dependencies and adds `python-multipart` to both development and service sets.

Fresh Architecture Guard, capability-runtime, validate, and HIL Controlled Cycle runs were started automatically for the rebased head. They must complete before merge; the earlier passing run is not substituted for the new-head checks.

## Live readiness observer v2

The deployed-state observer checks:

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
1. Observe all fresh PR #37 checks for head 336433dff29758d9581b0541daaac53b54126f30.
2. Retain and repair the first failing job if any; merge only after required checks pass.
3. Install data/hil-primary-v0.5-review.pdf.b64 and verify exact bytes and SHA-256.
4. Deploy the merged gateway with durable HIL storage.
5. Configure intake, review, and publication credentials only in the authorized runtime.
6. Observe HIL-LIVE-READINESS-OBSERVATION-v2 reaching CONTROLLED_CYCLE_READY.
7. Run one controlled deployed PDF plus provenance-manifest submission.
8. Verify exact-byte and manifest persistence across an actual gateway restart.
9. Record one authenticated ACCEPT_PRIVATE decision and verify write-once behavior.
10. Record one authenticated publication decision and verify identifier uniqueness.
11. Import the first HIL-PUBLICATION-RECORD-v1 into the Site projection.
12. Build the first HIL-MASTER-RECORD-RELEASE-v1 and validate its release chain.
13. Submit the release and supporting evidence to master-records/orchestration only after authorization.
14. Open public acquisition only after the deployed controlled cycle passes.
15. Send the prepared reciprocal-permission response to Sara Katpar and preserve evidence of the sent message.
16. After Sara Katpar publishes her independent reflection, capture its public URL and artifact hash and append them to HIL-CONTINUATION-0001 without changing the parent trace.
```

## Authority boundaries

```text
participant approval != technical activation
participant request != reciprocal permission
prepared response != sent response
continuation outreach != acknowledgment
continuation outreach != new consent
participant-authored continuation != protocol-generated submission
reciprocal mention permission != editorial control
Primary hash match != proof the LLM read the Primary
prompt hash match != proof of complete instruction following
response hash match != producer identity verification
producer signature != participant publication consent
CI controlled-cycle success != live deployment
clean rebase != merge authorization
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

No HIL canonical release tag or public data-acquisition activation is authorized while the Primary artifact is absent, PR #37 is unmerged or undeployed, fresh rebased-head checks are incomplete, and no controlled deployed submission, restart, private-review, publication, Site-import, and Master Record release cycle has produced persisted evidence.

## Archive readiness

This handoff, Site issues #67, #80, and #81, LLM-adapter PR #37, the HIL pages, approved review records, `HIL-TRACE-0001`, `HIL-CONTINUATION-0001`, `HIL-PARTICIPANT-TRACE-SARA-002`, schemas, client chain builder, gateway transitions, clean rebase record, successful earlier controlled-cycle CI evidence, Site importers/builders, live observer v2, validators, and repository history preserve complete continuation state. The remaining non-repository and deployment actions are explicitly listed above; no additional conversation context is required.
