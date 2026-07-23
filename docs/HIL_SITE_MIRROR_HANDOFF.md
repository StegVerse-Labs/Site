# Humans as the Interoperability Layer — Site Handoff

## Source of truth

This document owns continuation for the public `Humans as the Interoperability Layer` experiment surface within `StegVerse-Labs/Site`. It is subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide Site authority and activation posture.

## Current goal

```text
Goal: publish one authoritative participant-facing surface that distributes the canonical Primary PDF, supplies the exact LLM invocation prompt, verifies a returned response-only PDF locally, records participant-controlled consent, prepares a hash-bound receipt, and publishes accepted results through an append-only response index and Master Record.
Primary surface: humans-as-interoperability-layer.html
Client behavior: assets/hil-experiment.js
Experiment manifest: data/hil-experiment.json
Response projection: data/hil-responses.json
Submission schema: data/schemas/hil-submission.schema.json
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
Machine-readable empty public response index
Dynamic response-index rendering from data/hil-responses.json
Submission metadata JSON Schema
Static source verifier for page, prompt, hash, schema, manifest, response index, and authority boundaries
Empty public response-index state
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
Repository artifact state: PENDING INSTALLATION
```

The page expects the canonical artifact as base64 text at:

```text
data/hil-primary-v0.4.pdf.b64
```

The download path decodes the artifact in-browser, recomputes SHA-256, and blocks download if the bytes do not match the declared canonical hash. The source artifact available to the build session was independently verified at 106 KiB with the declared SHA-256. The artifact is not yet installed because the repository write connector accepts UTF-8 text and the binary-to-base64 transfer remains pending.

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
-> participant returns original Response PDF plus receipt through LinkedIn DM
```

The file does not leave the participant device during browser-local intake preview.

## Machine-readable state

### `data/hil-experiment.json`

Owns the canonical paper identity, prompt, protocol, artifact state, transport posture, public-record state, and fail-closed authority flags.

### `data/hil-responses.json`

Owns the public response projection. It begins empty and retains `HIL-TRACE-0001` separately as a pre-protocol observational trace pending attribution consent.

### `data/schemas/hil-submission.schema.json`

Defines the submission lifecycle:

```text
BROWSER_LOCAL_PREPARED_NOT_SUBMITTED
RECEIVED_PENDING_VALIDATION
INCOMPLETE
QUARANTINED
ACCEPTED_PRIVATE
ACCEPTED_FOR_PUBLICATION
PUBLISHED
WITHDRAWN
```

It separates browser-declared, participant-controlled, receiver-verified, and publication-authority fields.

## Verification

Run:

```text
python scripts/check_hil_experiment.py
```

Expected while the Primary artifact remains absent:

```text
HIL_EXPERIMENT_STATIC_VERIFICATION=PASS
HIL_PRIMARY_ARTIFACT=PENDING_INSTALLATION
HIL_PRIMARY_SHA256=97df3006c8d96212560c5fa970dc7bceac66bde23a8b23373491c030ccc0049d
HIL_PUBLIC_RESPONSE_COUNT=0
HIL_AUTHORITY=NONE
```

After `data/hil-primary-v0.4.pdf.b64` is installed and the manifest artifact state is changed to `VERIFIED`, the same verifier decodes the PDF, checks the `%PDF-` signature, recomputes SHA-256, and fails closed on mismatch.

## Required next vertical slice

```text
Install canonical Primary PDF artifact at the expected path
Change data/hil-experiment.json primary_document.artifact_state to VERIFIED
Bind scripts/check_hil_experiment.py into the canonical Site validation workflow
Deploy page and observe Primary PDF hash-verified download
Add server upload endpoint with PDF validation, isolated storage, malware scanning, rate limiting, and receipt issuance
Preserve exact uploaded bytes and calculate receiver-verified SHA-256
Create private review queue
Create receiver receipt schema
Create stable HIL-RESP identifiers
Publish accepted response artifact pages
Generate append-only Master Record editions with previous-release hash
Route the same endpoint into Ecosystem Chat when governed intake becomes available
```

## Authority boundaries

```text
Primary metadata display != artifact availability
Primary download != participant execution
LLM-generated PDF != participant consent
browser-local validation != server validation
browser-local hash != custody
receipt preparation != submission
LinkedIn transport != authoritative archive
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
canonical Site validation workflow binding
server-side upload and storage adapter
malware and active-content inspection
receiver receipt schema
review queue
public response detail route
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

No release tag is authorized for the HIL experiment surface while the canonical Primary artifact is absent and no deployed browser execution has verified the hash-bound download and receipt path. The page may remain merged as a fail-closed preview because it explicitly disclaims transmission, custody, publication, and activation.

## Archive readiness

This handoff, `humans-as-interoperability-layer.html`, `assets/hil-experiment.js`, `data/hil-experiment.json`, `data/hil-responses.json`, `data/schemas/hil-submission.schema.json`, `scripts/check_hil_experiment.py`, the canonical artifact metadata, and repository commits preserve the complete continuation state. No additional conversation context is required.
