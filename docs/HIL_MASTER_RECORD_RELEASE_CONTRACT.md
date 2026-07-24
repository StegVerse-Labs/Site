# HIL Master Record Release Contract

## Purpose

A HIL Master Record release is a deterministic, hash-bound snapshot of the already-published HIL response projection. It does not custody original response bytes, authorize publication, execute artifacts, endorse conclusions, or establish scientific proof.

## Source chain

```text
verified Primary and prompt
-> exact response PDF hash
-> provenance manifest hash
-> receiver receipt
-> authenticated private review receipt
-> append-only publication record
-> Site public response projection
-> HIL-MASTER-RECORD-RELEASE-v1
```

Only records already present in `data/hil-responses.json` may enter a Site Master Record release.

## Release content

Each release binds:

```text
release_id
created_at
Primary version and SHA-256
ordered public response records
response, provenance, private-review, and publication hashes
artifact paths
previous publication hashes
previous Master Record release hash
release SHA-256
```

## Deterministic builder

```text
python scripts/build_hil_master_record.py
```

The default mode validates and prints a candidate release without modifying repository state.

Mutation requires explicit authorization:

```text
python scripts/build_hil_master_record.py --apply
```

## Append-only behavior

- release identifiers cannot be reused;
- the response publication chain must be continuous;
- the release points to the previous release hash;
- no update or delete operation exists in the builder;
- response artifacts must use repository-relative PDF paths;
- an empty first release is permitted as a structural proof, but grants no activation or custody authority.

## Authority boundary

```text
Master Record release != original-byte custody
Master Record release != publication authority
Master Record release != execution authority
Master Record release != endorsement
Master Record release != scientific proof
Site index != master-records/orchestration custody
```

A later authorized transfer to `master-records/orchestration` may preserve the release and supporting evidence and return custody or reconstruction status. That downstream status must not be inferred from the Site release alone.
