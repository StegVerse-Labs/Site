# HIL Deployed Controlled-Cycle Runbook

Version: `HIL-DEPLOYED-CONTROLLED-CYCLE-RUNBOOK-v1.0`

## Purpose

This runbook governs the first live `Humans as the Interoperability Layer` controlled cycle after Primary installation. It converts the remaining activation gates into an ordered evidence-producing procedure without granting execution, review, publication, or Master Record authority.

## Preconditions

- Canonical Primary is installed and verified at `data/hil-primary-v0.5-review.pdf.b64`.
- Decoded Primary size is `109210` bytes.
- Primary SHA-256 is `52102cccb9ba9016c76434a64e22031b6a8c3edd3b8806e7b664e609216b2946`.
- Gateway source is `StegVerse-org/LLM-adapter` at or after merge commit `b2e612dd74d311e0cbe66cd1c1d4758bff129fd4`.
- Controlled-cycle CI has passed.
- Public acquisition remains disabled.

## Required runtime separation

The authorized runtime must configure distinct credentials for:

1. intake;
2. private review;
3. publication.

No credential may silently satisfy another role. Credential values must never be committed to this repository. Evidence may record only redacted identifiers or irreversible fingerprints.

## Evidence packet

All observations for the first cycle must be assembled in:

`data/hil-deployed-controlled-cycle-evidence.json`

The packet must conform to `HIL-DEPLOYED-CONTROLLED-CYCLE-EVIDENCE-v1` and remain `INCOMPLETE` until every required observation is independently supported.

## Ordered procedure

### 1. Deploy the merged gateway

Record:

- deployment provider and service identifier;
- deployed source commit;
- deployment time;
- gateway base URL;
- evidence reference proving the running revision.

The deployed source commit must be equal to or descend from the minimum merged HIL commit.

### 2. Establish durable storage

Record the configured storage class and a non-secret storage locator fingerprint. Ephemeral filesystem-only storage is inadmissible.

### 3. Establish credential separation

Record three distinct redacted credential references or fingerprints. Do not record secret material.

### 4. Observe live readiness

Run the live observer and preserve `HIL-LIVE-READINESS-OBSERVATION-v2`.

Required state:

`CONTROLLED_CYCLE_READY`

Readiness must bind the canonical Primary hash, prompt hash, durable-storage declaration, provenance requirement, private-review configuration, and append-only publication posture.

### 5. Submit one controlled response

Submit one response PDF and its provenance manifest through `/api/hil/submissions`.

Preserve:

- exact submitted response SHA-256;
- provenance-manifest SHA-256;
- submission identifier;
- `HIL-RECEIVER-RECEIPT-v2`;
- receiver receipt SHA-256;
- gateway-recorded storage references.

### 6. Perform an actual service restart

Record the pre-restart service instance identifier, restart request evidence, post-restart instance identifier, and restart completion time.

A new in-process client, test process, or redeploy without persistence verification does not satisfy this gate.

### 7. Prove persistence after restart

Retrieve the submission after restart and independently verify:

- response bytes still hash to the original response SHA-256;
- the stored provenance manifest still hashes to the original manifest SHA-256;
- submission identity is unchanged;
- no record was rewritten into a new success state.

### 8. Record private review

Using only the private-review credential, record one write-once `ACCEPT_PRIVATE` decision.

Preserve `HIL-PRIVATE-REVIEW-RECEIPT-v1` and its SHA-256. A second terminal decision attempt must fail closed or return the immutable existing decision.

### 9. Record append-only publication

Using only the publication credential, publish the accepted submission.

Preserve:

- `HIL-PUBLICATION-RECORD-v1`;
- stable unique `HIL-RESP` identifier;
- publication-record SHA-256;
- public lookup URL;
- evidence that no update or delete mutation route is available.

### 10. Import the public projection

Validate and append the publication to `data/hil-responses.json` using the governed importer. Preserve importer output and resulting Site commit.

### 11. Build the first Master Record release

Generate and validate `HIL-MASTER-RECORD-RELEASE-v1`. Default operation remains dry-run. Mutation requires explicit authorization.

### 12. Submit to orchestration only under separate authority

Submission to `master-records/orchestration` is not implied by successful release construction. Record the separate authorization reference before mutation.

### 13. Activation decision

Public acquisition may open only when:

- the evidence packet is `COMPLETE`;
- the activation-state validator passes;
- restart persistence is established;
- review and publication separation are established;
- Site import and Master Record release are established;
- release authority is separately granted where required.

## Failure posture

Any mismatch, missing observation, duplicate identity, credential-role overlap, restart-persistence failure, or hash discontinuity leaves the packet incomplete and public acquisition disabled. Failed evidence must be retained rather than rewritten or omitted.

## Authority boundaries

```text
runbook != execution authority
readiness != activation authority
receiver receipt != acceptance
ACCEPT_PRIVATE != publication
publication != endorsement
Site import != original-byte custody
Master Record build != orchestration authority
complete evidence packet != automatic public activation
```
