# HIL v1.0 Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for the `Humans as the Interoperability Layer` v1.0 Site activation path in `StegVerse-Labs/Site`.

## Canonical release recovered

The complete HIL v1.0 release set has been recovered outside the repository and verified against its release manifest.

```text
Canonical PDF: HIL_Canonical_Paper_v1_0.pdf
Size: 85084 bytes
SHA-256: e7a86cf05323d8352cfa188e0bff1c35fdb15f9fac6af91ca62b6a126ac4e68f
Status: CANONICAL INPUT · v1.0 · DO NOT ALTER
```

Associated release artifacts:

```text
HIL_Canonical_Paper_v1_0.docx
HIL_Experiment_Protocol_v1_0.pdf
HIL_Experiment_Protocol_v1_0.docx
HIL_Governance_Specification_v1_0.pdf
HIL_Governance_Specification_v1_0.docx
HIL_Master_Record_Release_v1_0.template.json
release-manifest.json
README.md
```

## Current deployed mismatch

The current Site still exposes the v0.5 prepublication review candidate through:

```text
humans-as-interoperability-layer.html
assets/hil-experiment.js
data/hil-primary-v0.5-review.pdf.b64
```

Current deployed v0.5 identity:

```text
Filename: Humans_as_the_Interoperability_Layer_Primary_Review_Candidate_v0_5.pdf
Size: 109210 bytes
SHA-256: 52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946
```

The v0.5 artifact must remain available as a superseded source-review artifact, but it must no longer be presented as the active canonical experiment input after v1.0 activation.

## Required Site update

1. Install the exact `HIL_Canonical_Paper_v1_0.pdf` bytes in a Site-served location.
2. Verify the installed bytes against SHA-256 `e7a86cf05323d8352cfa188e0bff1c35fdb15f9fac6af91ca62b6a126ac4e68f`.
3. Update `assets/hil-experiment.js`:
   - version `v1.0`;
   - canonical PDF filename;
   - canonical PDF hash;
   - canonical prompt text and prompt hash;
   - active artifact path.
4. Update `humans-as-interoperability-layer.html`:
   - replace v0.5 review-candidate labels with canonical v1.0 labels;
   - display the full canonical prompt from page 4 of the paper;
   - identify the v0.5 PDF as the verified source-review predecessor;
   - preserve Sara Katpar's approved HIL-TRACE-0001 attribution and review status;
   - clarify that response generation is not submission;
   - direct participants to return the response through the governed Site intake.
5. Update the gateway readiness contract to require the v1.0 Primary hash and the exact v1.0 prompt hash.
6. Run one operator pilot using the exact v1.0 PDF and canonical prompt.
7. Preserve exact response bytes, provenance manifest, receiver receipt, review receipt, publication record, and reconstruction evidence.
8. Only after a complete successful cycle, identify the result as the first fully tested operator example.

## Fail-closed activation boundary

```text
v1.0 document recovered != Site installed
Site metadata updated != canonical bytes installed
canonical bytes installed != gateway chain ready
response generated != response submitted
response submitted != receiver receipt
receiver receipt != review approval
review approval != publication authority
publication != Master Record release
```

## Current status

```text
Canonical v1.0 release recovered: VERIFIED
Release-manifest match: VERIFIED
Canonical PDF repository installation: NOT VERIFIED
Site active Primary: v0.5 REVIEW CANDIDATE
Gateway v1.0 readiness: NOT VERIFIED
First valid v1.0 operator cycle: NOT RUN
Activation state: PENDING_CANONICAL_ARTIFACT_INSTALLATION
```

## Installation note

A direct attempt to add a text-encoded canonical artifact was rejected and reverted because exact byte identity could not be guaranteed through the available text-only repository write path. No invalid v1.0 artifact remains in the repository. Installation must preserve the exact 85,084 PDF bytes and verify the canonical SHA-256 before Site metadata is switched.

## Downstream destinations after verified activation

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

No downstream destination may ingest or publish v1.0 as active until the Site verifies the installed canonical bytes and completes the governed operator cycle.
