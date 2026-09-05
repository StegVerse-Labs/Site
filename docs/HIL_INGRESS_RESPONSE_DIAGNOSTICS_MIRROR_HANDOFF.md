# HIL Ingress Response Diagnostics Mirror Handoff

Updated: 2026-09-05
Repository: `StegVerse-Labs/Site`
Primary issue: `#986` / merged PR `#987`
Receipt retry successor issue: `#1006`
Active branch: `fix/hil-receipt-retry-diagnostics-1006`

## Scope

This handoff tracks bounded diagnostic hardening for both HIL participant ingress paths:

1. the initial browser submission path in `assets/hil-direct-upload-v1.js`;
2. the persisted participant-record retry path in `hil-receipt.html`.

An authentic iPhone participant attempt preserved exact response bytes, SHA-256, provenance, the canonical InTr transport intent, and carrier-bound materialization staging, but `POST /api/hil/submissions` returned a response that could not be accepted as the expected JSON ingress result.

## Authority constraints

This task MUST NOT create a new runtime, heartbeat, oscillator, scheduler, receiver, credential path, second user-operated machine dependency, or Site-held provider credential.

Diagnostics grant no execution, admission, custody, publication, transition, claim/fence, or consequence authority.

The submission remains `INTR_TRANSPORT_PENDING` / `NOT_YET_RECEIVED` unless and until an authentic `HIL-RECEIVER-RECEIPT-v2` is returned and validated.

Credential authority remains `TV/TVC`. GitHub token runtime authority remains `NONE`.

## Initial submission diagnostic state — merged

PR #987 hardened `assets/hil-direct-upload-v1.js` so the browser reads the ingress response exactly once as text, classifies only bounded diagnostic facts, and then parses JSON when appropriate.

Recorded diagnostic facts are limited to:

- HTTP status
- normalized response content type
- whether the response was redirected
- same-origin / cross-origin / unknown final URL scope
- same-origin final pathname only; query and fragment are excluded
- bounded response class: `JSON`, `NON_JSON_HTML`, `NON_JSON_TEXT`, `EMPTY`, or `OTHER`

Arbitrary response-body text is not copied into the diagnostic record.

Fail-closed semantics remain unchanged: a non-JSON/empty response cannot become a receiver receipt, and the participant record remains pending/noncustodial while the exact local packet remains available for retry.

PR #987 merged as `3aaba426550b73e201c4641e9b242eb479547253`.

## Receipt retry gap discovered from authentic participant evidence

A later iPhone attempt at `2026-09-05T01:49:16.221Z` remained `INTR_TRANSPORT_PENDING` / `NOT_YET_RECEIVED` with exact response SHA-256:

`98410c4a2343952d4b72b09ee7ce7719c828b4975ef5d3107365e49182d63662`

The receipt page still displayed only `invalid_ingress_response`. Source inspection showed that `hil-receipt.html` retained the legacy lossy retry fallback even though the initial submit client had already been hardened. This is the basis of Site #1006.

## Receipt retry repair — source implementation

The `hil-receipt.html` retry path now applies the same bounded response-observation contract:

- `normalizeContentType(value)`
- `classifyIngressResponse(contentType,text)`
- `ingressResponseDiagnostic(response,contentType,responseClass)`
- `parseIngressResponse(response)` reads the response body exactly once with `response.text()`
- invalid/non-JSON results retain only bounded diagnostic facts
- `last_ingress_diagnostic` is stored on the participant-device record for inspection
- no arbitrary response body is stored
- no query string or URL fragment is retained
- the visible retry status includes only bounded status/class/content-type/redirect/scope/path facts
- `INTR_TRANSPORT_PENDING` remains explicit until an authentic receiver receipt validates

## Transport identity continuity

Receipt retry continues the exact stored transport intent rather than minting a new operation when one is already present.

The repair binds retry verification to:

- `record.intr_transport_intent`
- the stored `intent.operation_id`
- deterministic reconstruction with `buildTransportIntent(actual, provenance, originalOperationId)`
- exact canonical equality between the reconstructed and stored intent
- explicit failure if the operation identity changes

A repeated response SHA-256 alone is not treated as proof of transport identity continuity.

## Deterministic verification

`scripts/check_hil_intr_submission.py` now verifies both initial-submit and receipt-retry diagnostic surfaces. The checker rejects:

- the legacy `response.json().catch(...)` invalid-ingress fallback in either governed participant ingress path
- arbitrary `response_body` / `response_text` persistence markers
- `finalUrl.search` or `finalUrl.hash` exposure
- receipt retry source lacking bounded diagnostic markers
- receipt retry source lacking stored operation-id continuity checks

The established HIL contract remains submission-triggered Universal Interlock/InTr transport:

- `DEVICE_SYSTEM / Site:HIL`
- `STEGOS_ECOSYSTEM / HIL:Ingress`
- `HIL:Ingress -> HIL:Custody`
- `HIL:Custody -> TVC:HIL-Lifecycle`
- `always_on_application_receiver_required = false`
- `second_user_device_required = false`
- `exact_packet_transport_retry_allowed = true`
- `blind_consequence_retry_allowed = false`

## Evidence boundary

A diagnostic classification identifies where the authentic public ingress path stopped. It is not runtime execution evidence and must not be represented as StegVerse custody.

Source merge or CI validation is not public deployment proof. Public deployment is not receiver custody proof. Receiver custody is not TVC lifecycle admission or publication authority.

## Remaining continuation

1. Observe exact-head validation for Site #1006.
2. Reconcile any concrete validation failure without weakening fail-closed authority/custody boundaries.
3. Merge only after the HIL InTr Submission Contract, HIL upload surface, Site orchestration, and applicable bootstrap checks are clean.
4. Terminalize the #1006 work claim with authentic merge evidence.
5. Verify the repaired `hil-receipt.html` is the published public version.
6. Perform one controlled retry of the already-preserved participant packet only after publication verification.
7. Use the returned bounded diagnostic or authentic `HIL-RECEIVER-RECEIPT-v2` as the next runtime evidence.
8. Do not mark HIL activated from this diagnostic change alone.

## Upstream runtime continuation after diagnostics

The canonical HIL activation denominator remains outside this source-only diagnostic task:

- `StegVerse-Labs/.github`: authentic event consumption, ESRL `LEASE_OPEN`, Gateway READY, WorkerCoordinator real claim/fresh fence, sovereign HIL receiver READY
- `StegVerse-Labs/TVC`: authentic lifecycle receiving/admission, private review, publication, and required canonical StegGate evidence
- `StegVerse-Labs/Site`: public receiver READY, authentic `HIL-RECEIVER-RECEIPT-v2`, durable returned receipt projection, exact-byte post-restart verification
- `master-records/orchestration`: custody/reconstruction and Master Record release after authentic upstream evidence

No tag/release is authorized by this diagnostic lane before publication verification and the authentic runtime evidence predicates applicable to the larger HIL lifecycle.

## Archive readiness

The #986 implementation, #987 merge, #1006 successor repair, active ownership claim, authority boundary, exact transport-identity requirement, and next execution boundary are repository-resident. The complete prior conversation is not required to continue this lane.
