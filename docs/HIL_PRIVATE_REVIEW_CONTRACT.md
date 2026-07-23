# HIL Private Review Contract

## Purpose

After the gateway verifies and preserves a response PDF and its `HIL-RESPONSE-PROVENANCE-v1` manifest, the submission enters a private review queue. Private review decides only whether the retained submission is suitable for private acceptance, quarantine, or rejection.

It does not publish the response, assign a public `HIL-RESP` identifier, append a Master Record, or grant execution authority.

## Endpoints

```text
GET  /api/hil/submissions/{submission_id}/review-state
POST /api/hil/submissions/{submission_id}/review-decisions
```

Both endpoints require the server-side header:

```text
X-SteGVerse-HIL-Review-Token
```

The token is supplied from `STEGVERSE_HIL_REVIEW_TOKEN`. It must never be embedded in Site JavaScript, HTML, repository data, receipts, or browser storage.

## Review decisions

```text
ACCEPT_PRIVATE
QUARANTINE
REJECT
```

`ACCEPT_PRIVATE` means the submission may remain in the governed private research corpus. It is not public acceptance and does not authorize publication.

`QUARANTINE` preserves the record as a rejected or unresolved input requiring separate remediation or investigation.

`REJECT` records that the submission should not advance through the experiment path.

Only one private review decision is admitted for a submission. A second decision attempt fails closed rather than overwriting the first review record.

## Review-state disclosure

The review-state endpoint returns submission metadata, hashes, chain-validation state, and any recorded review receipt. It does not expose:

```text
original PDF bytes
server storage paths
review token
participant contact secrets
publication authority
```

## Receipt

A decision produces `HIL-PRIVATE-REVIEW-RECEIPT-v1`, validated by:

```text
data/schemas/hil-private-review-receipt.schema.json
```

The receipt contains the stable submission reference, reviewer, timestamp, decision, notes, canonical receipt hash, and fail-closed authority flags.

## Transition boundary

```text
receiver receipt              != private review decision
private acceptance            != public acceptance
private acceptance            != publication
quarantine                    != deletion
review receipt                != Master Record append
review token possession       != repository mutation authority
```

Public publication requires a separate authorized transition that validates participant consent, private review state, stable response ID allocation, artifact custody, and append-only public-index mutation.
