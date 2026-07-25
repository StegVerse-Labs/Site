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
Receiver gateway: StegVerse-org/LLM-adapter main @ c50d9148aa91a8e04eb7e5b3c6a2da4e9a1293ed
Controlled-cycle workflow: StegVerse-org/LLM-adapter/.github/workflows/hil-controlled-cycle.yml
Portable-runtime workflow: StegVerse-org/LLM-adapter/.github/workflows/platform-agnostic-runtime.yml
Result: PRIMARY_INSTALLED_GATEWAY_MERGED_PORTABLE_RUNTIME_STAGED_LIVE_ACTIVATION_PENDING
Authority: NONE
```

## Participant approval

Sara Katpar granted named attribution, exchange reproduction, model-response description, and public-record inclusion permission. She reviewed the v0.5 Primary candidate and Site presentation and stated that everything looked good to proceed. Participant approval is complete and remains separate from technical activation, private review, publication mutation, custody, and Master Record authority.

## Participant-originated continuation

Sara Katpar independently proposed publishing a LinkedIn reflection about the exchange, the research, and the value of curiosity, and requested permission to mention and tag Rigel Randolph. Rigel sent affirmative permission on 2026-07-25 at 8:37 a.m. as shown in the supplied LinkedIn screenshot. The sent-message transcript and evidentiary conclusion are preserved in `data/hil-traces/HIL-CONTINUATION-0001-PERMISSION-EVIDENCE.md`; the governed continuation state is preserved in `data/hil-traces/HIL-CONTINUATION-0001.json` and linked from `HIL-TRACE-0001`.

```text
Continuation ID: HIL-CONTINUATION-0001
Parent: HIL-TRACE-0001
Type: INDEPENDENT_PARTICIPANT_PUBLIC_REFLECTION
Authorship: participant-controlled
Publication: participant-controlled
Reciprocal permission: APPROVED_SENT_AND_EVIDENCED
Permission sent: 2026-07-25 08:37 local / 2026-07-25T13:37:00Z
Protocol submission: false
Directed testimonial: false
Site ingestion authority: false
Master Record authority: false
```

The permission allows Sara Katpar to mention and tag Rigel Randolph and discuss the exchange and research. It does not impose prepublication review or editorial control. The eventual public post, URL, and captured artifact hash remain pending participant publication and may be appended only after the public artifact exists and is independently captured.

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
Primary artifact state: VERIFIED_INSTALLED
Primary Git blob SHA: 5db09a3819ca68192071810e11c80ef0382f4ad4
Installation manifest commit: b150b813cce5d019172d75688aa3ac67bf7637ed
Installation receipt commit: d1a4a18fccf8c125cfb167469f1bcaccc62634d1
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

All fresh rebased-head checks completed successfully for `336433dff29758d9581b0541daaac53b54126f30` before merge:

```text
Architecture Guard: success — run 30127608884
HIL Controlled Cycle: success — run 30127608787
capability-runtime: success — run 30127609107
validate: success — run 30127608720
```

The controlled test exercises intake readiness, exact response and provenance persistence, receiver receipt v2, separate application clients over the same durable directory, authenticated `ACCEPT_PRIVATE`, private-review receipt, append-only publication, public lookup, and SQLite submission/review/publication records. This is CI evidence, not deployed-service restart evidence and not activation authority.

## Gateway merge

PR #37 was squash-merged after all fresh checks passed.

```text
PR: StegVerse-org/LLM-adapter#37
rebased head: 336433dff29758d9581b0541daaac53b54126f30
merge commit: b2e612dd74d311e0cbe66cd1c1d4758bff129fd4
merged: true
merge method: squash
```

## Platform-agnostic runtime package

The gateway now has a provider-neutral runtime tranche:

```text
Dockerfile: existing OCI image contract
entrypoint persistence correction: 68dcc4cb318cd77eeb859e94aa80cc46687abea3
compose.yaml: 5ad890b97cc6ef60cf67f47e2f532c0392bfb34f
example environment: 721013a131005bc98957d8152524c2f751d422ce
runtime specification: d85fca64cac34b8c763a0d21562812d61e514811
OCI portability workflow: c50d9148aa91a8e04eb7e5b3c6a2da4e9a1293ed
```

The entrypoint now maps `STEGVERSE_HIL_DATA_DIR` beneath the common durable volume. The compose contract provides a named durable volume, configurable port, separated review and publication secrets, health checks, and no provider-specific application dependency. The workflow builds the OCI image, verifies readiness and canonical hashes, replaces the container, and checks mounted-state persistence. Workflow execution evidence remains pending observation.

Render is not an architectural dependency, default target, or accepted deployment assumption. Historical Render-specific records are historical evidence only.

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
1. Observe the Platform-Agnostic Runtime workflow for c50d9148aa91a8e04eb7e5b3c6a2da4e9a1293ed and repair any failing job.
2. Select or provision any conforming OCI/process runtime without changing application code.
3. Deploy LLM-adapter main at or after c50d9148aa91a8e04eb7e5b3c6a2da4e9a1293ed with a durable mounted volume.
4. Inject distinct private-review and publication credentials only through the runtime secret boundary.
5. Provide HTTPS termination or a documented reverse-proxy boundary.
6. Observe HIL-LIVE-READINESS-OBSERVATION-v2 reaching CONTROLLED_CYCLE_READY.
7. Run one controlled deployed PDF plus provenance-manifest submission.
8. Replace or restart the service and verify exact-byte and manifest persistence.
9. Record one authenticated ACCEPT_PRIVATE decision and verify write-once behavior.
10. Record one authenticated publication decision and verify identifier uniqueness.
11. Import the first HIL-PUBLICATION-RECORD-v1 into the Site projection.
12. Build the first HIL-MASTER-RECORD-RELEASE-v1 and validate its release chain.
13. Submit the release and supporting evidence to master-records/orchestration only after authorization.
14. Open public acquisition only after the deployed controlled cycle passes.
15. After Sara Katpar publishes her independent reflection, capture its public URL and artifact hash and append them to HIL-CONTINUATION-0001 without changing the parent trace.
```

## Authority boundaries

```text
participant approval != technical activation
participant request != reciprocal permission
prepared response != sent response
sent reciprocal permission != editorial control
continuation outreach != acknowledgment
continuation outreach != new consent
participant-authored continuation != protocol-generated submission
reciprocal mention permission != Site publication authority
Primary hash match != proof the LLM read the Primary
prompt hash match != proof of complete instruction following
response hash match != producer identity verification
producer signature != participant publication consent
CI controlled-cycle success != live deployment
OCI image build != live deployment
mounted-volume test != production custody
merged gateway != deployed gateway
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

No HIL canonical release tag or public data-acquisition activation is authorized while the portable-runtime workflow is unobserved, the gateway is not evidenced as deployed through the provider-neutral contract with durable storage, credentials are not configured in an authorized runtime, and no controlled deployed submission, restart, private-review, publication, Site-import, and Master Record release cycle has produced persisted evidence.

## Archive readiness

This handoff, Site issues #67, #80, and #81, LLM-adapter issue #41, merged PR #37, the installed Primary artifact and receipt, the HIL pages, approved review records, participant traces, schemas, client chain builder, gateway transitions, controlled-cycle evidence, provider-neutral Docker/Compose/runtime specification, portability workflow, Site importers/builders, live observer v2, validators, and repository history preserve complete continuation state. The remaining workflow observation, runtime deployment, credential, controlled-cycle, publication, and Master Record actions are explicitly listed above; no additional conversation context is required.
