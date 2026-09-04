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

At commit `7ed2d8b5ce226250bec1cba005f7cd7f367d68b9`, the `HIL InTr Submission Contract` and `Canonical Generated InTr Connectors` workflows completed successfully.

The two HIL source-check failures at that head were reconciled to exact causes rather than treated as implementation failures:

- `Check HIL v1 Upload Surface` failed only because its page-copy assertion still required the removed phrase `Submit the single Response PDF`. The stepped page retains the structural `response-file` input and `Submit Response Packet`; commit `21369df3689785db2a4d07ab39335ae34d95a241` changes the checker to the stable structural marker and current verified-result wording without weakening any transport, identity, custody, credential, or authority invariant.
- `HIL Post-Submit Continuity` failed only because its participant-flow assertion required `exact submission-result packet` while the current stepped page says `verified submission-result packet`. Commit `f91bc730f17e5a6e0732ae1b0c4e4eaddfcb9728` reconciles that copy assertion and leaves every fail-closed result, worker, receiver-discovery, credential, and authority check intact.

The Site handoff/bootstrap/heartbeat reconciliation failures at the earlier head were caused by this PR branch having no active pre-work claim. Commit `bfd5e6ec088253e6ce9a849f45749115d87aab29` adds the branch-scoped active claim at `data/session-work-claims.d/site-hil-ingress-response-diagnostics-986.json`, with an isolated diagnostic dependency surface and explicit collision boundaries. This claim does not acquire runtime, receiver, TVC, or consequence authority.

Validation after the latest reconciliation head must be observed before merge. Workflow state is validation evidence only and is not runtime/custody evidence.

## Evidence boundary

A diagnostic classification only identifies where the authentic public ingress path stopped. It is not runtime execution evidence and must not be represented as StegVerse custody.

## Remaining continuation

1. Observe the exact-head validation runs after the checker and claim reconciliation commits.
2. If any validation still fails, reconcile the concrete failure without weakening fail-closed authority/custody boundaries.
3. Merge PR #987 only after clean source validation and collision/ownership validation.
4. Terminalize the branch pre-work claim with authentic merge evidence.
5. Deploy through the existing Site publication path and verify the diagnostic client is the published version.
6. Perform one controlled retry of the already-preserved participant packet only after deployment; use the resulting bounded diagnostic or authentic receiver receipt as the next evidence.
7. Do not mark HIL activated from this diagnostic change alone.

## Upstream runtime continuation after diagnostics

The canonical HIL activation denominator remains outside this source-only diagnostic task:

- `StegVerse-Labs/.github`: authentic event consumption, ESRL `LEASE_OPEN`, Gateway READY, WorkerCoordinator real claim/fresh fence, sovereign HIL receiver READY
- `StegVerse-Labs/TVC`: authentic lifecycle receiving/admission, private review, publication, and required canonical StegGate evidence
- `StegVerse-Labs/Site`: public receiver READY, authentic `HIL-RECEIVER-RECEIPT-v2`, durable returned receipt projection, exact-byte post-restart verification
- `master-records/orchestration`: custody/reconstruction and Master Record release after authentic upstream evidence

No tag/release is authorized by this diagnostic lane before merge, publication verification, and the authentic runtime evidence predicates applicable to the larger HIL lifecycle.

## Archive readiness

The diagnostic implementation, active ownership claim, verification reconciliation, evidence boundary, and next execution boundary are repository-resident. The complete prior conversation is not required to continue this lane.
