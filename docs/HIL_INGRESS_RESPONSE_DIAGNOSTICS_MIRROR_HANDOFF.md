# HIL Ingress Response Diagnostics Mirror Handoff

Updated: 2026-09-04
Repository: `StegVerse-Labs/Site`
Issue: `#986`
PR: `#987`
Branch: `fix/hil-ingress-response-diagnostics-986`

## Scope

This handoff tracks the bounded diagnostic hardening for the existing HIL browser submission path after an authentic iPhone participant attempt reached local exact-byte preservation, local SHA-256 verification, provenance preservation, canonical InTr transport intent construction, and carrier-bound materialization staging, but `POST /api/hil/submissions` produced a response that the browser could not parse as the expected JSON ingress result.

## Authority constraints

This task MUST NOT create a new runtime, heartbeat, oscillator, scheduler, receiver, credential path, second user-operated machine dependency, or Site-held provider credential.

Diagnostics grant no execution, admission, custody, publication, transition, claim/fence, or consequence authority.

The submission remains `INTR_TRANSPORT_PENDING` / `NOT_YET_RECEIVED` unless and until an authentic `HIL-RECEIVER-RECEIPT-v2` is returned.

## Implemented source state

The browser client now reads the ingress response exactly once as text, classifies only bounded diagnostic facts, and then parses JSON when available.

Recorded diagnostic facts are limited to:

- HTTP status
- normalized response content type
- whether the response was redirected
- same-origin / cross-origin / unknown final URL scope
- same-origin final pathname only; query and fragment are excluded
- bounded response class: `JSON`, `NON_JSON_HTML`, `NON_JSON_TEXT`, `EMPTY`, or `OTHER`

Arbitrary response-body text is not copied into the diagnostic record.

Fail-closed semantics remain unchanged: a non-JSON/empty response cannot become a receiver receipt, and the participant record remains pending/noncustodial while the exact local packet remains available for the existing retry path.

Implementation commit: `c1f91e500eafa5a7454f34ccdc614849aee1244f`.

## Deterministic verification

Added `scripts/check_hil_ingress_response_diagnostics.py` to assert bounded diagnostic markers and reject the legacy lossy `response.json().catch(...)` fallback, arbitrary response body/text persistence markers, and URL query/fragment exposure.

The existing `scripts/check_hil_intr_submission.py` is also extended so the repository's established HIL InTr Submission Contract workflow verifies these diagnostic invariants rather than leaving the new checker disconnected from an existing contract lane.

Verification integration commits:

- `26fc660e359e262a84d3c05789afb10fc9949677` — standalone deterministic diagnostics checker
- `405d1e7463a532642d904ae09de9c9de79b003e2` — bind diagnostics to the established HIL InTr contract check

At commit `26fc660e359e262a84d3c05789afb10fc9949677`, the `HIL InTr Submission Contract` and `Canonical Generated InTr Connectors` workflows completed successfully. `Check HIL v1 Upload Surface`, `HIL Post-Submit Continuity`, and `Ecosystem Heartbeat Orchestration` reported failures and must not be represented as passing; the first two failures occurred even though this diff removed no existing contract markers and require independent reconciliation before merge. Workflow state is validation evidence only and is not runtime/custody evidence.

## Evidence boundary

A diagnostic classification only identifies where the authentic public ingress path stopped. It is not runtime execution evidence and must not be represented as StegVerse custody.

## Remaining continuation

1. Reconcile the failing `Check HIL v1 Upload Surface` and `HIL Post-Submit Continuity` validation jobs without weakening their fail-closed contracts.
2. Obtain clean source validation for PR #987.
3. Merge only after validation is clean and no duplicate ownership/collision exists.
4. Deploy through the existing Site publication path.
5. Perform one controlled retry of the already-preserved participant packet only after the diagnostic change is deployed; use the resulting bounded diagnostic or authentic receiver receipt as the next evidence.
6. Do not mark HIL activated from this diagnostic change alone.

## Upstream runtime continuation after diagnostics

The canonical HIL activation denominator remains outside this source-only diagnostic task:

- `StegVerse-Labs/.github`: authentic event consumption, ESRL `LEASE_OPEN`, Gateway READY, WorkerCoordinator real claim/fresh fence, sovereign HIL receiver READY
- `StegVerse-Labs/TVC`: authentic lifecycle receiving/admission, private review, publication, and required canonical StegGate evidence
- `StegVerse-Labs/Site`: public receiver READY, authentic `HIL-RECEIVER-RECEIPT-v2`, durable returned receipt projection, exact-byte post-restart verification
- `master-records/orchestration`: custody/reconstruction and Master Record release after authentic upstream evidence

No tag/release is authorized by this diagnostic lane.

## Archive readiness

The diagnostic implementation, verification contract, observed validation state, and next execution boundary are repository-resident. The complete prior conversation is not required to continue this lane.
