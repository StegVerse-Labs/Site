# HIL TVC/Vercel Mirror Handoff

Updated: 2026-07-31
Repository: `StegVerse-Labs/Site`
Branch: `main`

## Scope and authority

This is the canonical Site handoff for the provider-neutral HIL activation path. Live repository state, Git history, Vercel project/deployment evidence, direct runtime observations, TVC receipts, and genuine participant artifacts are authoritative. Endpoint availability alone grants no custody, participant-readiness, publication, release, or Master Record authority.

## Selected architecture

```text
Connected Vercel Site project
  -> public stegverse.org/api/hil/* diagnostic ingress
GitHub-native participant return
  -> authenticated source object or attachment
StegVerse-Labs/TVC
  -> commit-pinned package authority
  -> exact-byte verification
  -> deterministic chunking and reconstruction
  -> scoped execution and lifecycle receipts
CGE/downstream governance
  -> admissibility, review, publication, release
```

The former Cloudflare secret-dependent path is not selected. `StegVerse-org/TV` remains the private ephemeral token-distribution path and is not the public HIL receiver.

## Canonical identities

```text
Primary version: v1.1
Primary SHA-256: a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462
Protocol: HIL-PROTOCOL-v1.1
Prompt: HIL-PROMPT-v1.1
Prompt SHA-256: cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c
```

## Vercel project evidence

```text
team: team_tb2tGtHkSFhg5cpTMCvAhQJi
project: site
project id: prj_xHOgZyCUzb37Zs7gyYVPCMb2OIl8
production domain: stegverse.org
framework: null
node version: 22.x
latest observed production deployment: dpl_8UwhvCtqe9pquQd1tXY9ue4JejBF
state: READY
source commit: ecae84bd80a99a3dddee3c245e492f833a8111e4
aliases: stegverse.org, site-henna-gamma.vercel.app, site-rigel-randolphs-projects.vercel.app, site-git-main-rigel-randolphs-projects.vercel.app
```

The deployment is stale relative to current Site `main`. Git commits made during this session did not produce a newly listed deployment. A direct deployment attempt through the connected Vercel control returned an input-contract error requiring deployment name, target, and files; no deployment was created and no production alias changed.

## Implemented Site diagnostic surface

The following isolated Vercel-compatible Node functions were committed without changing unrelated routes:

```text
336c0c0f6b55c3c0e5b68f3a680f250688340dc3  api/hil/probes.js
38b68d4e13cd041c1ad7e572bed9123b78b08586  api/hil/readiness.js
32de0cf89cf819149fd739e9a808922a99117f88  api/hil/submissions/validate.js
```

Intended contracts:

```text
GET /api/hil/probes
  receiver_mode: DIAGNOSTIC
  durable_submission: false
  exact_byte_retrieval: false
  publication_authorized: false
  canonical identities included

GET /api/hil/readiness
  state: DIAGNOSTIC
  participant_ready: false
  upload_button_authorized: false
  release_authorized: false
  explicit blocking dependencies

POST /api/hil/submissions/validate
  validates required source-object/provenance/hash/model/provider/consent fields
  rejects Primary or Prompt mismatch
  rejects malformed response SHA-256
  rejects unsupported consent and premature receipt state
  accepted_for_custody: false
```

These functions deliberately do not claim durable custody or exact-byte retrieval.

## Current production state

```text
new Vercel deployment from current main: not observed
production source commit current: false
/api/hil/probes current production result: not proven changed; prior production was 404
/api/hil/readiness current production result: not proven changed; prior production was 404
participant_ready: false
upload_button_authorized: false
durable_submission: false
exact_byte_retrieval: false
publication_authorized: false
release_authorized: false
```

## Participant and model invariants

```text
Claude Opus 5 / Anthropic: MODEL_REQUEST_INITIATED_RESPONSE_NOT_RECEIVED
ChatGPT Medium 5.6 / OpenAI: MODEL_REQUEST_INITIATED_RESPONSE_NOT_RECEIVED
response PDFs: 0
response packages: 0
participant acknowledgments: 0
receiver receipts: 0
```

No genuine participant PDF or provenance package was discovered or created. These values must remain unchanged.

## GitHub-native participant return contract

The selected transport must be an authenticated GitHub source object that preserves the PDF and provenance JSON and yields a reconstructable repository, issue, pull-request, discussion, or release-asset identity. The machine-readable intake must bind:

```text
response_pdf
provenance_manifest
primary_sha256
prompt_sha256
response_sha256
model
provider
optional participant_identity
publication_consent
receipt_state
source_object_identity
immutable_or_reconstructable_git_reference
```

No synthetic participant object is authorized.

## TVC work remaining

Destination: `StegVerse-Labs/TVC`

- register a commit-pinned HIL package for the Site ingress implementation;
- bind allowed paths and expected source hashes;
- add bounded tasks through the existing dispatcher for source verification, source-object retrieval, exact-byte PDF hashing, provenance validation, identity-chain validation, deterministic chunking, chunk hashing, reconstruction, reconstructed-hash comparison, receipt generation, lifecycle enforcement, and activation-readiness summary;
- implement fail-closed positive and negative validators;
- define a truthful GitHub-source-object/TVC-reconstruction custody identity only after direct validation passes.

## Release posture

No tag or release is authorized. Diagnostic ingress code is committed but not proven deployed. Genuine participant receipt, exact-byte reconstruction, custody receipt, private review, governed publication, participant-readiness authorization, Master Record creation, and downstream verification remain absent.

## Exact next action

Use the connected Vercel control plane to create a production deployment from current `StegVerse-Labs/Site/main` or restore Git-triggered deployment for the current branch without user-managed secrets. Preserve deployment ID, source commit, build logs, aliases, runtime responses, and redeployment persistence. Then register the exact deployed Site commit in TVC before implementing the source-object verifier.

## Archive readiness

This handoff contains the complete current implementation, provider evidence, unchanged participant state, exact deployment block, and next execution path. The prior thread is not required to continue.
