# HIL v1 Upload Mirror Handoff

Status: RELEASE-CRITICAL — PROVIDER-NEUTRAL EXACT-BYTE RECEIVER IMPLEMENTED; DEPLOYED READY OBSERVATION PENDING
Repository: StegVerse-Labs/Site
Date: 2026-07-29
Goal: Make the public HIL response upload path seamless and ready for launch while preserving exact-byte provenance, fail-closed authority boundaries, and device/platform independence.

## Source-of-truth relationship

This handoff governs the canonical v1 upload-surface tranche. It remains subordinate to `docs/SITE_MIRROR_HANDOFF.md` for ecosystem-wide Site authority and to `docs/HIL_SITE_MIRROR_HANDOFF.md` for the full HIL review, publication, and Master Record lifecycle.

## Immediate architecture correction — 2026-07-29

The deployed Worker previously made Cloudflare R2 (`HIL_SUBMISSIONS`) a mandatory readiness condition. That contradicted the platform-agnostic objective and forced an unnecessary subscription dependency.

Commit `b459ad44ed8e5fa9c6a980c8460617695b4b9b07` removes the mandatory R2 dependency.

The receiver now uses the already-bound SQL-compatible registry (`HIL_REGISTRY`) for both:

- submission/receipt/provenance metadata; and
- exact response-PDF bytes stored as independently hashed, ordered chunks.

The custody contract is identified as `portable-sqlite-chunks-v1`. The schema and receipt semantics do not require Cloudflare R2. The same tables and behavior can be implemented by another SQLite-compatible runtime without changing the participant protocol.

## Exact-byte custody behavior

1. The browser validates and hashes the response PDF locally.
2. The Worker validates the Primary → prompt → response chain.
3. The Worker divides the exact PDF bytes into 192 KiB chunks.
4. Each chunk is Base64 encoded for portable SQL storage and individually SHA-256 hashed.
5. Chunks are stored in `hil_submission_chunks` keyed by `submission_id` and `chunk_index`.
6. Submission, receipt, provenance, chunk count, size, and backend identity are stored in `hil_submissions`.
7. The Worker reconstructs the bytes immediately after persistence.
8. The reconstructed byte length and SHA-256 must match the uploaded PDF or the submission is deleted and rejected.
9. `GET /api/hil/submissions/{submission_id}/content` reconstructs and returns the exact PDF with `x-content-sha256`.

## Readiness contract

`READY` now requires:

```text
HIL_REGISTRY query succeeds
+ schema can be created/read
+ chunk custody table can be queried
```

It no longer requires:

```text
HIL_SUBMISSIONS
Cloudflare R2
an R2 subscription
any named object-storage vendor
```

## Canonical v1.1 chain

- Primary file: `HIL_Canonical_Paper_v1_1.pdf`
- Primary SHA-256: `a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462`
- Prompt version: `HIL-PROMPT-v1.1`
- Prompt SHA-256: `cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c`
- Provenance schema: `HIL-RESPONSE-PROVENANCE-v1.1`
- Receipt schema: `HIL-RECEIVER-RECEIPT-v2`

## Seamless upload behavior

The participant:

1. drops or selects one response-only PDF;
2. enters model, provider, consent, and confirmations;
3. presses `Submit response PDF` once;
4. receives local PDF validation and SHA-256 hashing;
5. receives automatic provenance-manifest construction;
6. uploads the exact PDF plus manifest after readiness passes;
7. receives the receiver receipt in the same surface;
8. may download provenance and receipt records without rebuilding either artifact.

## Fail-closed behavior

- Registry/custody schema unavailable: receiver reports `DEGRADED` and upload stays disabled.
- Timeout before receipt: no successful submission is claimed.
- Primary or prompt mismatch: submission is rejected.
- Missing consent or confirmations: upload is rejected locally.
- Invalid, empty, oversized, non-PDF, or signature-mismatched file: upload is rejected locally.
- Chunk write, reconstruction, byte-length, or SHA-256 failure: stored state is deleted and submission fails.
- Receiver receipt does not grant review, publication, endorsement, execution, admissibility, or Master Record authority.

## Remaining release-critical work

1. Observe the Cloudflare deployment containing commit `b459ad44ed8e5fa9c6a980c8460617695b4b9b07`.
2. Observe `GET /api/hil/readiness` return HTTP 200 and `state: READY` using `portable-sqlite-chunks-v1`.
3. Execute one deployed controlled PDF submission and retain the receiver receipt.
4. Retrieve `/api/hil/submissions/{submission_id}/content` and verify exact byte length and SHA-256.
5. Redeploy or restart the Worker and repeat status/content verification.
6. Complete authenticated private review and append-only publication for the first response.
7. Import the first public response into the Site index.
8. Build and validate the first chained HIL Master Record release.
9. Verify release projections in Publisher, admissibility-wiki, and stegguardian-wiki.

## Authority

```text
Site code merged != deployed Site
configured D1 binding != successful readiness probe
readiness response != submission
receiver receipt != private acceptance
private acceptance != public publication
publication != endorsement
Site projection != original-byte Master Records custody
Master Record release != scientific proof
```

## Archival continuity

The provider-neutral receiver correction, exact-byte chunk custody contract, commit, remaining deployment observations, launch boundaries, and downstream obligations are represented here. Complete thread is ready for archiving without any additional part of the thread needed to continue.