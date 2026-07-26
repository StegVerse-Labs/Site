# HIL Master Record Release Contract

## Purpose

A HIL Master Record release is a deterministic, hash-bound record of one already-published HIL v1.1 response. It does not custody original response bytes, authorize publication, execute artifacts, endorse conclusions, or establish scientific proof.

## Source chain

```text
canonical v1.1 Primary and prompt
-> exact response PDF hash
-> VERIFIED receiver receipt
-> authenticated ACCEPT_PRIVATE review
-> separately authenticated append-only publication
-> Site public response projection
-> HIL-MASTER-RECORD-RELEASE-v1
```

Only records already present in `data/hil-responses.json` may enter a Site Master Record release.

## Release content

Each release binds:

```text
release_id
created_at
canonical v1.1 Primary and prompt hashes
one public response identifier and exact byte hash
receiver receipt and VERIFIED state
authenticated private-review receipt
authenticated append-only publication receipt
previous Master Record release hash
canonical release-payload SHA-256
explicit false authority claims
```

Release files are stored under:

```text
data/hil-master-record-releases/<release_id>.json
```

The index stores only the release identifier, governed path, release payload hash, and current chain tip.

## Deterministic builder

```text
python scripts/build_hil_master_record.py
```

The default mode validates and prints a candidate release without modifying repository state. It requires at least one governed public response.

Mutation requires explicit authorization:

```text
python scripts/build_hil_master_record.py --apply
```

An optional response may be selected explicitly:

```text
python scripts/build_hil_master_record.py --response-id <response_id>
```

## Canonicalization

The release payload hash is computed over the release object without `release_payload_sha256`, using:

```text
sorted JSON keys
compact separators
UTF-8
one trailing newline
SHA-256
```

## Append-only behavior

- release identifiers cannot be reused;
- each release is written as a new file;
- the release points to the previous release payload hash;
- the index chain tip must equal the final release hash;
- response bytes must match the receiver receipt;
- no release is permitted without a real governed response;
- no update or delete operation exists in the builder.

## Validation

```text
python scripts/check_hil_master_record_release.py
```

The verifier rejects:

- any Primary or prompt identity other than canonical v1.1;
- response and receiver-receipt hash disagreement;
- a receiver receipt that is not `VERIFIED`;
- missing or unauthenticated `ACCEPT_PRIVATE` review;
- missing, unauthenticated, or mutable publication;
- a broken previous-release link;
- a release payload hash mismatch;
- a release outside the governed release directory;
- any custody, execution, mutation, endorsement, or scientific-proof authority escalation.

## Authority boundary

```text
receiver receipt != private acceptance
private acceptance != publication
publication != Master Record release
Master Record release != original-byte custody
Master Record release != publication authority
Master Record release != execution authority
Master Record release != endorsement
Master Record release != scientific proof
Site index != master-records/orchestration custody
validated release != authorized downstream append
```

A later authorized transfer to `master-records/orchestration` may preserve the release and supporting evidence and return custody or reconstruction status. That downstream status must not be inferred from the Site release alone.

## Current state

The v1.1 schema, deterministic builder, fail-closed verifier, and CI workflow are implemented. The release index remains empty until a real controlled response completes receipt verification, private review, append-only publication, and Site import.
