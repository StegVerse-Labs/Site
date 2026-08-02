# HIL Runtime Path Reconciliation

Updated: 2026-08-02T04:18:00-05:00
Repository: `StegVerse-Labs/Site`
Branch: `main`
Goal ID: `HIL-LIFECYCLE-ACTIVATION-001`

## Purpose

Resolve the durable conflict between the legacy Cloudflare/D1 HIL deployment handoffs and the provider-neutral Site/Vercel + TVC architecture without erasing historical evidence or allowing a secret-bound path to halt development.

## Authoritative records read

- `docs/HIL_MIRROR_HANDOFF.md`
- `docs/HIL_SITE_MIRROR_HANDOFF.md`
- `StegVerse-Labs/TVC/docs/HIL_TVC_MIRROR_HANDOFF.md`
- `StegVerse-Labs/StegCore/docs/HIL_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md`

## Determination

The Cloudflare deployment attempt is valid historical evidence:

- run `30573565667` failed before Wrangler or Cloudflare provider invocation;
- the three required Actions values were empty;
- public `/api/hil/probes` and `/api/hil/readiness` returned GitHub Pages 404;
- no production receiver, route, D1 binding, custody, or readiness was proven.

That path is now classified:

```text
claim state: SUPERSEDED_FOR_ACTIVE_IMPLEMENTATION
completion state: FAILED_BEFORE_PROVIDER_INVOCATION
preservation state: RETAIN_HISTORICAL_EVIDENCE
retry authority: NOT_GRANTED_BY_THIS_RECORD
```

The active implementation path is:

```text
StegVerse-Labs/Site connected hosted runtime
→ public stegverse.org/api/hil/* ingress
→ participant remains on StegVerse surfaces
→ exact response bytes and provenance enter a governed internal transport
→ StegVerse-Labs/TVC verifies package, source object, exact bytes, chunking, reconstruction, and private-review contract
→ master-records/orchestration validates a candidate only
→ StegVerse-Labs/StegCore validates cross-repository lifecycle consistency
```

The active path is provider-neutral at the contract boundary. A specific deployment provider may be used only when directly available through connected deployment controls and verified by runtime evidence. No user-managed secret becomes an unspecified external task.

## Participant boundary

Participants must not be sent to GitHub. GitHub may be used internally for repository-native transport, workflow execution, immutable object references, and receipts only.

The participant experience remains owned by:

- `https://stegverse.org/hil-study-launch.html`
- `https://stegverse.org/hil-managed-return.html`
- `https://stegverse.org/hil/upload/` when a verified hosted receiver is ready
- Site lifecycle receipt and projection surfaces owned by issue `StegVerse-Labs/Site#67`

## Active owner and exact tasks

### Hosted runtime implementation

Owner: `StegVerse-Labs/Site#81`

1. Inspect the connected Site deployment control plane and identify the currently authoritative production project.
2. Install or bind `/api/hil/probes`, `/api/hil/readiness`, and the bounded upload/receipt routes without altering unrelated routes.
3. Verify exact Primary v1.1 and Prompt v1.1 identities in readiness output.
4. Execute `HIL-E2E-001` through the hosted route.
5. Persist receiver, exact-byte retrieval, negative-case, and restart/redeployment receipts.
6. Set participant readiness only from validated source evidence.

### Participant lifecycle projection

Owner: `StegVerse-Labs/Site#67`

1. Validate TVC lifecycle projection receipts with `scripts/validate_hil_lifecycle_projection.py`.
2. Reject `contract_test_only` receipts as real review, publication, release, or activation evidence.
3. Display validated lifecycle state without claiming custody of original bytes.
4. Import the Master Record validation-only receipt and StegCore activation receipt when available.

## Internal observation and non-halting rule

No unresolved item is classified as external.

When the hosted deployment control plane is unavailable or a route is not live, Site#81 must emit one of:

- `RETRY` with the exact failed observation;
- `REVIEW_REQUIRED` with the named StegVerse authority boundary and required input;
- `FAILED` with logs and receipt;
- `CLAIMED` with a fresh claim expiration;
- `SUPERSEDED` when another verified runtime path replaces it.

The repository-native coordinator at `StegVerse-Labs/StegCore#41` owns next-action selection and stale-claim release.

## Canonical continuation

MERGED INTO: `StegVerse-Labs/StegCore/docs/HIL_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md`

Site-specific work continues in `StegVerse-Labs/Site#81` and `StegVerse-Labs/Site#67`. The originating session is not required to remember or restate this runtime-path decision.

## Validation and release boundary

File presence and route code do not prove deployment. Activation requires direct hosted runtime observation, controlled-cycle evidence, exact-byte custody proof, restart/redeployment persistence, authenticated private review, separate publication, Site projection, Master Record validation, and a bounded StegCore activation receipt.

No publication, release, tag, or downstream propagation is authorized by this reconciliation record.
