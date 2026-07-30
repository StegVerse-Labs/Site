# HIL Participant Readiness Gate

Status: Normative

Protocol: `HIL-PROTOCOL-v1.1`

Test case: `HIL-E2E-001`

## Rule

A deployment MUST NOT be described as **participant-ready**, **uploadable**, or **operational** solely because source code exists, bindings respond, or `/api/hil/readiness` returns `READY`.

Participant readiness is established only after the production receiver completes the canonical synthetic response-packet cycle against the currently deployed version:

1. construct the canonical synthetic PDF and provenance manifest;
2. submit them through the public production submission endpoint;
3. receive a governed receiver receipt;
4. retrieve submission status;
5. retrieve the exact stored PDF bytes;
6. verify original, receipt, status, and retrieved SHA-256 values;
7. verify exact binary equality and byte length;
8. verify review remains pending and publication remains unauthorized;
9. preserve the complete evidence package.

## Canonical synthetic fixture

The fixture MUST declare:

- `test_case_id`: `HIL-E2E-001`
- `artifact_type`: `HIL_TEST_RESPONSE_PACKET`
- `participant_type`: `SYNTHETIC_VALIDATION_ACTOR`
- `participant_identifier`: `CONTROLLED-INFRASTRUCTURE-CYCLE`
- `model`: `SYNTHETIC-INFRASTRUCTURE-FIXTURE`
- `research_data`: `false`
- `publication_consent`: `NOT_APPLICABLE_SYNTHETIC`
- `authority_effect`: `false`

The PDF itself MUST visibly state that it is synthetic infrastructure evidence and is not participant research, a review determination, a publication candidate, or a Master Record.

## Required positive assertions

The acceptance cycle MUST verify:

- HTTP submission result is `200` or `201`;
- a non-empty `submission_id` exists;
- a non-empty `receipt_id` exists;
- `chain_validation_state` is `PRIMARY_PROMPT_RESPONSE_CHAIN_VERIFIED`;
- `custody_state` is `EXACT_BYTES_PERSISTED`;
- `custody_backend` is `portable-sqlite-chunks-v1`;
- `registry_state` is `RECORDED`;
- `review_state` is `PENDING`;
- `publication_state` is `NOT_AUTHORIZED`;
- status is `ACCEPTED`;
- stored byte length equals original byte length;
- original bytes equal retrieved bytes exactly;
- original SHA-256 equals provenance, receipt, status, and retrieved SHA-256.

## Required negative assertions

The production endpoint MUST reject, deterministically:

- missing provenance manifest;
- non-PDF extension;
- invalid PDF signature;
- wrong response hash in provenance;
- wrong Primary hash;
- wrong prompt hash.

A negative-case failure blocks participant readiness even if the positive cycle passes.

## Operational states

The following meanings are distinct:

- `CONFIGURED`: deployment configuration exists.
- `RUNTIME_READY`: bindings and storage probes pass.
- `UPLOAD_PATH_VERIFIED`: canonical packet was accepted by production.
- `CUSTODY_VERIFIED`: exact bytes were retrieved and matched.
- `NEGATIVE_CASES_VERIFIED`: malformed packets were rejected as specified.
- `PARTICIPANT_READY`: all required gates passed for the deployed version.

`/api/hil/readiness` reports runtime readiness. The controlled-cycle evidence establishes participant readiness.

## Evidence package

The workflow artifact MUST retain:

- readiness JSON and response headers;
- original synthetic PDF;
- provenance manifest;
- submission HTTP status;
- receiver receipt;
- submission status;
- retrieved PDF;
- retrieval headers;
- controlled-cycle verifier output;
- negative-case results;
- evidence manifest containing byte lengths and SHA-256 values.

## Authority boundary

Passing this gate proves only that the governed receiver can accept, preserve, receipt, and return a conforming response packet while rejecting specified malformed packets.

It does not grant review approval, publication authority, endorsement, execution authority, or Master Record inclusion.
