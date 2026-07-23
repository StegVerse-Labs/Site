# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public `Humans as the Interoperability Layer` experiment surface within `StegVerse-Labs/Site`. It is subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide Site authority and activation posture.

## Current goal

```text
Goal: publish one authoritative participant-facing surface that distributes the canonical Primary PDF, supplies the exact LLM invocation prompt, verifies a returned response-only PDF locally, records participant-controlled consent, prepares a hash-bound receipt, and publishes accepted results through an append-only response index and Master Record.
Primary surface: humans-as-interoperability-layer.html
Response detail surface: humans-as-interoperability-response.html?id=HIL-RESP-...
Client behavior: assets/hil-experiment.js
Response renderer: assets/hil-response.js
Experiment manifest: data/hil-experiment.json
Response projection: data/hil-responses.json
Submission schema: data/schemas/hil-submission.schema.json
Receiver receipt schema: data/schemas/hil-receiver-receipt.schema.json
Static verifier: scripts/check_hil_experiment.py
Result: BROWSER_LOCAL_INTAKE_PREVIEW
Authority: NONE
```

## Implemented

```text
Dedicated public experiment page
Canonical paper, protocol, prompt, and SHA-256 metadata display
Minimal six-step participant path
Exact one-line prompt with copy action
Response-only PDF selection
PDF extension, size, and %PDF signature checks
Browser-local SHA-256 calculation using Web Crypto
Participant identifier, contact, publication-consent, and no-edit confirmation fields
Participant-consent authority acknowledgement
Temporary HIL-INTAKE identifier generation
Downloadable JSON receipt aligned to HIL-SUBMISSION-v1
Explicit validation posture fields for PDF signature, primary reference, prompt integrity, active content, and malware scan
Fail-closed authority flags for transmission, custody, acceptance, publication, and Master Record append
Machine-readable experiment manifest
Machine-readable public response index
Dynamic response-index rendering from data/hil-responses.json
Generic public response detail surface resolved by stable HIL-RESP ID
Submission metadata JSON Schema
Receiver receipt JSON Schema
Static verifier for page, detail page, prompt, hashes, schemas, manifest, response records, duplicate IDs, and authority boundaries
HIL verifier bound into Site validate and public-guard tasks
HIL public paths registered in docs/SITE_PUBLIC_PATHS.md and check_site_public_paths.py
Initiating observation reserved as HIL-TRACE-0001
Home-page transition card and proof-status entry
Mobile-responsive layout
```

## Canonical input

```text
Filename: Humans_as_the_Interoperability_Layer_Canonical_Input_v0_4.pdf
Paper version: v0.4
Protocol version: HIL-PROTOCOL-v1.0
Prompt version: HIL-PROMPT-v1.0
Declared SHA-256: 97df3006c8d96212560c5fa970dc7bceac66bde23a8b23373491c030ccc0049d
Verified source size: 107675 bytes
Repository artifact state: PENDING INSTALLATION
```

Expected repository path:

```text
data/hil-primary-v0.4.pdf.b64
```

The page decodes the artifact in-browser, recomputes SHA-256, and blocks download if the bytes do not match the declared canonical hash. The source PDF was independently rechecked before continuation and matched the declared hash. Binary-to-repository installation remains pending.

## Current participant flow

```text
Site page
-> download and verify Primary PDF
-> participant uploads unchanged PDF to chosen LLM
-> participant supplies exact prompt
-> LLM produces response-only PDF
-> participant selects Response PDF on Site
-> browser validates and hashes file locally
-> participant supplies consent fields
-> browser generates schema-aligned receipt JSON
-> participant returns original Response PDF plus receipt through interim transport
```

The file does not leave the participant device during browser-local intake preview.

## Response publication flow

```text
received response bytes
-> receiver SHA-256
-> HIL-RECEIVER-RECEIPT-v1
-> validation / quarantine / acceptance decision
-> stable HIL-RESP identifier
-> data/hil-responses.json append
-> humans-as-interoperability-response.html?id=<HIL-RESP-ID>
-> Master Record release linkage
```

The public detail surface is a projection. It is not custody and does not edit the response artifact.

## Verification

Canonical command:

```text
python scripts/run_site_task.py validate
```

The Site task runner invokes `scripts/check_hil_experiment.py` during both `validate` and `public-guard`.

Expected current HIL output:

```text
HIL_EXPERIMENT_STATIC_VERIFICATION=PASS
HIL_PRIMARY_ARTIFACT=PENDING_INSTALLATION
HIL_PRIMARY_SHA256=97df3006c8d96212560c5fa970dc7bceac66bde23a8b23373491c030ccc0049d
HIL_PUBLIC_RESPONSE_COUNT=0
HIL_AUTHORITY=NONE
```

After `data/hil-primary-v0.4.pdf.b64` is installed and `data/hil-experiment.json` is changed to `VERIFIED`, the verifier decodes the PDF, checks `%PDF-`, recomputes SHA-256, and fails closed on mismatch.

## Required next vertical slice

```text
Install canonical Primary PDF artifact
Change manifest artifact_state to VERIFIED
Observe Site validation workflow after artifact installation
Deploy and browser-test hash-verified Primary PDF download
Build server-side upload adapter
Preserve exact uploaded bytes and receiver SHA-256
Inspect active PDF content and malware state
Issue HIL-RECEIVER-RECEIPT-v1
Create private review queue
Append accepted records without ID reuse or overwrite
Publish first response detail page from machine-readable index
Build versioned Master Record assembly workflow
Route the same intake contract into Ecosystem Chat
```

## Authority boundaries

```text
Primary metadata display != artifact availability
Primary download != participant execution
LLM-generated PDF != participant consent
browser-local validation != server validation
browser-local hash != custody
receipt preparation != submission
transport != authoritative archive
submission != acceptance
acceptance != publication
publication != endorsement
response recurrence != shared intent
Master Record inclusion != scientific proof
```

## Remaining destination work

Destination `StegVerse-Labs/Site`:

```text
data/hil-primary-v0.4.pdf.b64
server-side upload and isolated storage adapter
malware and active-content inspection
private review queue
append-only response-index mutation workflow
Master Record assembly and release workflow
browser and accessibility tests
```

Destination `master-records/orchestration` after server-side intake authorization:

```text
custody original response bytes
validate primary-document and response chain references
retain receiver receipt and reconstruction evidence
return custody and reconstruction status without granting publication authority
```

Downstream destinations after verified publication:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

## Release posture

No HIL release tag is authorized while the canonical Primary artifact is absent and no deployed browser execution has verified the hash-bound download and receipt path. The fail-closed preview may remain deployed because it claims no transmission, custody, acceptance, publication, or activation authority.

## Archive readiness

This handoff and the checked-in HIL page, response page, client renderers, manifests, schemas, validators, public-path register, and repository history preserve all continuation state. No additional conversation context is required.
