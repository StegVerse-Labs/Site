# HIL Append-Only Publication Contract

## Purpose

This contract defines the only supported transition from a privately reviewed HIL submission to a public `HIL-RESP` projection.

## Preconditions

A publication mutation is admissible only when all of the following are true:

```text
submission exists
Primary / protocol / prompt / response provenance chain verified
private review record exists
private review decision = ACCEPT_PRIVATE
participant publication consent = public or anonymous
publication token configured in the authorized runtime
response_id matches ^HIL-RESP-[A-Z0-9-]+$
artifact path is repository-relative and ends in .pdf
submission_id has never been published
response_id has never been allocated
```

## Endpoint

```text
POST /api/hil/submissions/{submission_id}/publication-decisions
Header: X-SteGVerse-HIL-Publication-Token
```

The publication token is sourced only from `STEGVERSE_HIL_PUBLICATION_TOKEN`. It must never be sent to the participant browser, stored in Site JavaScript, written into receipts, or committed to the repository.

Public lookup is separate and read-only:

```text
GET /api/hil/publications/{response_id}
```

## Append-only guarantees

```text
one submission_id -> at most one publication record
one response_id -> at most one submission
no update endpoint
no delete endpoint
no response_id reuse
no replacement of prior publication record
previous_publication_sha256 links accepted records in insertion order
```

A duplicate submission or reused response ID fails with conflict. A later correction must be a separately governed superseding record, not an overwrite.

## Publication record

The gateway emits `HIL-PUBLICATION-RECORD-v1`, binding:

```text
publication_id
response_id
submission_id
published_at
publisher
participant display posture
publication consent
artifact path
Primary SHA-256
response SHA-256
provenance-manifest SHA-256
chain-validation state
private-review ID
private-review receipt SHA-256
previous publication SHA-256
publication-record SHA-256
```

Anonymous consent suppresses the participant display name even when a name was supplied during intake.

## Authority boundary

```text
ACCEPT_PRIVATE != public publication
publication consent != publication mutation authority
publication token != execution authority
public projection authorized != endorsement
public projection authorized != Master Record append
publication record != custody of original bytes
publication record != scientific validation
```

The publication record authorizes only the bounded public projection represented by its response ID and artifact path. Execution, endorsement, and Master Record append remain false.
