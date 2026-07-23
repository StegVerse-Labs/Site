# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public `Humans as the Interoperability Layer` experiment surface within `StegVerse-Labs/Site`. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide Site authority and activation posture.

## Current goal

```text
Goal: complete Sara Katpar's prepublication review, install the verified v0.5 Primary artifact, prove the live Site and bounded intake path, and then open serious public data acquisition without collapsing review, custody, acceptance, publication, or Master Record authority.
Primary surface: humans-as-interoperability-layer.html
Response detail surface: humans-as-interoperability-response.html?id=HIL-RESP-...
Client behavior: assets/hil-experiment.js
Response renderer: assets/hil-response.js
Experiment manifest: data/hil-experiment.json
Initiating trace: data/hil-traces/HIL-TRACE-0001.json
Response projection: data/hil-responses.json
Submission schema: data/schemas/hil-submission.schema.json
Receiver receipt schema: data/schemas/hil-receiver-receipt.schema.json
Static verifier: scripts/check_hil_experiment.py
Live observer: scripts/check_hil_live_readiness.py
Live workflow: .github/workflows/check-hil-live-readiness.yml
Result: PREPUBLICATION_REVIEW
Authority: NONE
```

## Implemented

```text
Dedicated public experiment page
Named HIL-TRACE-0001 presentation for Sara Katpar
Recorded attribution, reproduction, model-response description, and public-record inclusion permission
Explicit prepublication review requirement and presentation-approval boundary
v0.5 review-candidate metadata and SHA-256 display
Exact one-line invocation prompt
Response-only PDF selection
Browser-local PDF signature, size, and SHA-256 validation
Participant identifier and publication-consent fields
Browser-local fallback receipt
Bounded gateway readiness and multipart submission wiring
Receiver-receipt display and download path
Machine-readable experiment manifest
Machine-readable initiating-trace record
Machine-readable public response index
Generic public response detail surface resolved by stable HIL-RESP ID
Submission and receiver-receipt JSON Schemas
Static verifier bound into Site validate and public-guard tasks
Public-path registration
Scheduled live Site and gateway readiness observation
Mobile-responsive layout
Durable Site issue #67
Bounded gateway implementation in StegVerse-org/LLM-adapter PR #37
```

## v0.5 review artifact

```text
Filename: Humans_as_the_Interoperability_Layer_Primary_Review_Candidate_v0_5.pdf
Paper version: v0.5
Protocol version: HIL-PROTOCOL-v1.0
Prompt version: HIL-PROMPT-v1.0
SHA-256: 52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946
Verified size: 109210 bytes
Repository artifact state: PENDING INSTALLATION
Review state: SARA_REVIEW_PENDING
Canonical-public state: NOT YET CANONICAL
```

Expected repository path:

```text
data/hil-primary-v0.5-review.pdf.b64
```

The Site must decode the artifact, check `%PDF-`, recompute SHA-256, and fail closed if the bytes do not match. The locally generated source has been independently checked against the hash above. Repository transfer remains the immediate artifact blocker.

## HIL-TRACE-0001 consent state

```text
Participant: Sara Katpar
Classification: PRE_PROTOCOL_OBSERVATIONAL_TRACE
Attribution permission: GRANTED
Exchange reproduction permission: GRANTED
Model-response description permission: GRANTED
Public-record inclusion permission: GRANTED
Prepublication review requested: YES
Final presentation approval: PENDING
Publication state: REVIEW_PENDING
```

Permission does not substitute for the requested review. The public Site may show the review-gated presentation, but final canonical publication remains blocked until Sara has reviewed the relevant section, Primary PDF, and Site presentation.

## Current review flow

```text
Sara receives v0.5 review PDF
-> Sara reviews HIL-TRACE-0001 wording and broader presentation
-> corrections are recorded without rewriting the original exchange
-> final presentation approval is recorded
-> approved v0.5 canonical PDF is generated
-> canonical hash is frozen
-> Site artifact is installed and verified
-> controlled end-to-end response submission is performed
-> public acquisition may open only after observed success
```

## Future participant flow

```text
Site page
-> hash-verified Primary PDF download
-> unchanged PDF submitted to participant-selected LLM
-> exact prompt supplied
-> response-only PDF returned
-> browser validates locally
-> governed gateway receives exact bytes when READY
-> receiver SHA-256 and HIL-RECEIVER-RECEIPT-v1 issued
-> private review / quarantine / acceptance decision
-> stable HIL-RESP identifier assigned
-> public response projection
-> versioned Master Record linkage
```

## Live verification

Static repository validation:

```text
python scripts/run_site_task.py validate
```

Direct live observation:

```text
python scripts/check_hil_live_readiness.py
```

The live observer checks:

```text
GitHub Pages HIL URL is reachable
v0.5 prepublication review markers are deployed
Sara Katpar and HIL-TRACE-0001 are visible
review permission remains distinct from final presentation approval
gateway readiness endpoint is reachable
gateway Primary hash matches the current review artifact before upload can be considered ready
publication and activation authority remain false
```

The scheduled workflow runs every six hours and on relevant Site changes. Its observation is evidence only; it cannot activate intake or authorize publication.

## Required next vertical slice

```text
Install data/hil-primary-v0.5-review.pdf.b64
Change artifact_state only after repository verifier confirms the exact hash
Observe live GitHub Pages deployment of the review presentation
Merge and deploy LLM-adapter PR #37
Configure durable HIL storage and enable bounded intake
Update gateway Primary hash from v0.4 to the approved v0.5 hash
Run one controlled exact-byte upload and receiver-receipt cycle
Verify persistence across gateway restart
Provide Sara the deployed review URL and review PDF
Record corrections and final presentation approval
Generate final canonical v0.5 artifact and hash
Open serious public acquisition only after the controlled cycle passes
```

## Authority boundaries

```text
permission granted != final presentation approval
review PDF != canonical public input
Primary metadata display != artifact availability
Primary download != participant execution
LLM-generated PDF != participant consent
browser-local validation != receiver validation
browser-local hash != custody
receiver receipt != acceptance
submission != publication
publication != endorsement
response recurrence != shared intent
Master Record inclusion != scientific proof
live observation != activation authority
```

## Remaining destination work

Destination `StegVerse-Labs/Site`:

```text
data/hil-primary-v0.5-review.pdf.b64
review artifact hash verification
live workflow evidence review
browser and accessibility tests
append-only response-index mutation workflow
Master Record assembly and release workflow
```

Destination `StegVerse-org/LLM-adapter`:

```text
merge PR #37
deploy HIL readiness and submission routes
durable exact-byte storage
active-content and malware posture
receiver receipt persistence
restart proof
```

Destination `master-records/orchestration` after server-side authorization:

```text
custody original response bytes
validate Primary and response-chain references
retain receiver receipts and reconstruction evidence
return custody status without granting publication authority
```

## Release posture

No HIL canonical release tag or public data-acquisition activation is authorized while Sara's presentation review is pending, the v0.5 artifact is absent from the repository, the gateway remains unmerged or undeployed, and no controlled live upload has produced a verified receiver receipt.

## Archive readiness

This handoff, Site issue #67, LLM-adapter PR #37, the HIL public pages, trace record, manifests, schemas, validators, live observer, workflow, and generated v0.5 artifact metadata preserve the complete continuation state. No additional conversation context is required.
