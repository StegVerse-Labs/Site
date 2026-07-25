# HIL First Master Record Release Preparation

Version: `HIL-FIRST-MASTER-RECORD-PREPARATION-v1`

## Purpose

This document binds the final preparation boundary between an authorized external HIL controlled cycle and the first `HIL-MASTER-RECORD-RELEASE-v1` candidate.

A successful GitHub-hosted process-restart cycle proves runtime behavior. It does not establish an authorized external deployment, Site publication authority, Master Record append authority, or orchestration submission authority.

## Required order

```text
authorized external deployment observation
→ externally produced receiver receipt
→ actual restart and persistence proof
→ authenticated ACCEPT_PRIVATE
→ separately authenticated publication record
→ stable public lookup
→ governed Site import
→ first release readiness ledger becomes READY_FOR_DRY_RUN
→ deterministic Master Record release candidate
→ independent validation
→ separate release authorization
→ separate orchestration-submission authorization
```

## Readiness ledger

The machine-readable gate is:

```text
data/hil-first-release-readiness.json
```

The ledger must remain `WAITING_FOR_AUTHORIZED_EXTERNAL_CYCLE` until all required external-cycle and Site-import inputs are established. Missing evidence may not be replaced by fixture values, CI observations, screenshots, inferred identifiers, or manually typed hashes.

## Candidate generation boundary

The existing deterministic builder may be used only in dry-run mode until the readiness ledger records all required inputs. Candidate generation does not itself authorize release or mutation.

The candidate must bind:

- stable `HIL-RESP` identifier;
- response PDF SHA-256;
- provenance SHA-256;
- receiver receipt hash or governed reference;
- private-review receipt SHA-256;
- publication-record SHA-256;
- previous release hash, or `null` for the first release;
- canonical release SHA-256.

## Authority separation

```text
process-cycle proof != external deployment
external deployment != Site import
Site import != Master Record release
release candidate != release authorization
release authorization != orchestration submission authorization
orchestration submission != public acquisition authorization
```

Every authorization remains false in the readiness ledger until separately recorded by the authority that owns that transition.

## Verification

```bash
python scripts/check_hil_first_release_readiness.py
```

The validator fails closed if incomplete inputs are represented as release-ready, if a candidate is claimed without evidence, or if any authority flag is enabled in the preparation ledger.
