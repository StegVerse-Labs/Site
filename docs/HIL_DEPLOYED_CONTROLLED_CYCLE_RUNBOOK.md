# HIL Deployed Controlled-Cycle Runbook

Version: `HIL-DEPLOYED-CONTROLLED-CYCLE-RUNBOOK-v1.1`

## Purpose

This runbook governs the first live `Humans as the Interoperability Layer` controlled cycle after Primary installation. It converts the remaining activation gates into an ordered evidence-producing procedure without granting execution, review, publication, or Master Record authority.

## Preconditions

- Canonical Primary is installed at `data/HIL_Canonical_Paper_v1_1.pdf`.
- Installed Primary size is `87271` bytes.
- Primary version is `v1.1`.
- Primary SHA-256 is `a7b1c62e336b4e244ecf7fdcd10af195401f6c44328de32615b073d2a5c3c462`.
- Prompt SHA-256 is `cdff8d2266bb3eefbb6e5d28d9adc548e6c8dfc039debd72fe404f1d0249912c`.
- Protocol is `HIL-PROTOCOL-v1.1`.
- Prompt contract is `HIL-PROMPT-v1.1`.
- Provenance schema is `HIL-RESPONSE-PROVENANCE-v1.1`.
- Receiver receipt schema is `HIL-RECEIVER-RECEIPT-v2`.
- Gateway source is `StegVerse-org/LLM-adapter` and the deployed commit must be recorded exactly.
- The bounded repository-local persisted cycle has passed, but that result is not external deployment evidence.
- Public acquisition remains disabled.

## Required runtime separation

The authorized runtime must configure distinct credentials for intake, private review, and publication. No credential may silently satisfy another role. Credential values must never be committed to this repository. Evidence may record only redacted identifiers or irreversible fingerprints.

## Evidence packet

All observations for the first cycle must be assembled in `data/hil-deployed-controlled-cycle-evidence.json`.

The packet must conform to `HIL-DEPLOYED-CONTROLLED-CYCLE-EVIDENCE-v1`, bind the exact HIL v1.1 contract, and remain `INCOMPLETE` until every required observation is independently supported.

## Ordered procedure

### 1. Deploy the unchanged OCI runtime

Record the provider, service identifier, exact deployed source commit, deployment time, conforming public HTTPS base URL, and evidence proving the running revision. The deployment must use durable external storage. A GitHub-hosted ephemeral cycle does not satisfy this gate.

### 2. Establish durable storage

Record storage class `EXTERNAL_DURABLE_SERVICE`, a non-secret storage locator fingerprint, and the provider declaration or configuration evidence. Ephemeral filesystem-only storage is inadmissible.

### 3. Establish credential separation

Record three distinct redacted credential references or fingerprints. Do not record secret material.

### 4. Observe live readiness

Run the origin-bound HTTPS probe and preserve `HIL-HTTPS-RECEIVER-PROBE-v1`.

Required state: `READY`.

Readiness must bind the exact HIL v1.1 Primary hash, prompt hash, protocol, prompt version, provenance schema, PDF-only intake, size limit, optional participant metadata, and all non-authority declarations.

### 5. Submit one controlled response

Submit one response PDF and its provenance manifest through `/api/hil/submissions`.

Preserve the exact response SHA-256, provenance-manifest SHA-256, submission identifier, `HIL-RECEIVER-RECEIPT-v2`, receiver receipt SHA-256, and gateway-recorded storage references.

### 6. Perform an actual service restart or replacement

Record the pre-restart service instance identifier, restart request evidence, post-restart instance identifier, and restart completion time.

A new in-process client, test process, or CI-only restart does not satisfy this gate.

### 7. Prove persistence after restart

Retrieve the submission after restart and independently verify that the response bytes and provenance manifest retain their original hashes, the submission identity is unchanged, and no record was rewritten into a new success state.

### 8. Record private review

Using only the private-review credential, record one write-once `ACCEPT_PRIVATE` decision. Preserve `HIL-PRIVATE-REVIEW-RECEIPT-v1` and its SHA-256. A second terminal decision attempt must fail closed or return the immutable existing decision.

### 9. Record append-only publication

Using only the publication credential, publish the accepted submission. Preserve `HIL-PUBLICATION-RECORD-v1`, a stable unique `HIL-RESP` identifier, publication-record SHA-256, public lookup URL, and evidence that no update or delete mutation route is available.

### 10. Import the public projection

Validate and append the publication to `data/hil-responses.json` using the governed importer. Preserve importer output and resulting Site commit.

### 11. Build the first Master Record release

Generate and validate `HIL-MASTER-RECORD-RELEASE-v1`. Default operation remains dry-run. Mutation requires explicit authorization.

### 12. Submit to orchestration only under separate authority

Submission to `master-records/orchestration` is not implied by successful release construction. Record the separate authorization reference before mutation.

### 13. Activation decision

Public acquisition may open only when the evidence packet is `COMPLETE`, activation-state validation passes, restart persistence is established, review and publication separation are established, Site import and Master Record release are established, and release authority is separately granted where required.

## Failure posture

Any mismatch, missing observation, duplicate identity, credential-role overlap, restart-persistence failure, stale contract version, ephemeral deployment scope, or hash discontinuity leaves the packet incomplete and public acquisition disabled. Failed evidence must be retained rather than rewritten or omitted.

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
