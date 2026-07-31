# HIL Ephemeral Order Execution Integration Handoff

Updated: 2026-07-31
Repository: `StegVerse-Labs/Site`
Branch: `main`

## Authority

Read in this order before continuing:

1. `docs/CROSS_SESSION_EXECUTION_HANDOFF_PROTOCOL.md`
2. `docs/SITE_MIRROR_HANDOFF.md`
3. `docs/HIL_MIRROR_HANDOFF.md`
4. `docs/HIL_SITE_MIRROR_HANDOFF.md`
5. `StegVerse-Labs/TVC/TVC_MIRROR_HANDOFF.md`
6. `StegVerse-Labs/TVC/docs/HIL_TVC_MIRROR_HANDOFF.md`
7. `StegVerse-Labs/TVC/docs/PROVIDER_AGNOSTIC_EPHEMERAL_ORDER_EXECUTION_CONTRACT.md`
8. this handoff

Repository state, committed artifacts, direct provider evidence, and normalized receipts supersede chat history.

This handoff grants no execution, publication, release, certification, or deployment authority.

## Decision

The HIL participant upload must activate provider-agnostic, order-born ephemeral execution.

Site owns public ingress and participant-facing status projection. TVC owns the canonical order, exact-byte verification, provider-conformance, receipt, and lifecycle contracts. A cloud platform, device, operating system, repository host, or conversational session may execute an order but may not define its meaning.

## Canonical flow

```text
participant presses Upload Response Packet
-> Site accepts exact bytes or immutable source-object reference
-> Site emits intake receipt
-> Site creates or proposes root order
-> admitted order selects a conforming provider
-> provider creates one ephemeral execution construct
-> bounded task executes
-> outputs and normalized receipts are verified
-> temporary execution state is destroyed
-> order status is projected to the participant
-> downstream orders require separate admission
```

## Required public interfaces

```text
POST /api/hil/response-packets
GET /api/hil/orders/{order_id}
GET /api/hil/orders/{order_id}/receipts
```

The upload response must return `202 Accepted` after durable intake and root-order creation or proposal. It must not wait for complete downstream execution.

Example response:

```json
{
  "packet_id": "hil-pkt-...",
  "order_id": "ord-root-...",
  "status": "accepted",
  "intake_receipt_ref": "...",
  "status_url": "/api/hil/orders/ord-root-..."
}
```

## Site responsibilities

Site must:

1. authenticate the participant or apply an explicit permitted anonymous posture;
2. validate the response-packet envelope;
3. preserve exact bytes or an immutable authenticated source-object reference;
4. calculate and record SHA-256 and exact byte size;
5. issue packet and root-order identifiers;
6. bind the root order to the canonical TVC order schema and protocol version;
7. avoid embedding provider-specific execution semantics in the public API;
8. project lifecycle states and receipt references;
9. permit the client to disconnect after acceptance;
10. preserve unrelated `stegverse.org` routes and services.

Site must not:

- claim TVC verification before a valid TVC receipt exists;
- claim exact-byte reconstruction before reconstruction evidence exists;
- claim worker destruction when provider destruction evidence is absent;
- infer success from a missing result;
- grant publication, release, certification, or execution authority;
- require a continuously running conversational session or human continuation action.

## Root-order contents

The root order must minimally bind:

```text
packet ID
participant/source posture
exact input object reference
SHA-256
byte size
media type
Primary identity
prompt identity
provenance identity
required task graph
required capabilities
network policy
resource limits
expiry
idempotency key
admission policy reference
expected receipt classes
```

## Initial subordinate orders

```text
verify source identity or source-object authority
verify exact input hash and size
validate response-packet manifest
verify commit-pinned TVC package authority
deterministically chunk and reconstruct
compare reconstructed and submitted exact bytes
evaluate lifecycle and admissibility posture
aggregate execution and destruction receipts
propose private review or publication work when separately authorized
```

Each subordinate task is its own order or policy-bound node. A worker may propose downstream work but may not self-authorize it.

## Lifecycle projection

Site may project these normalized states:

```text
PROPOSED
VALIDATED
ADMITTED
DENIED
INDETERMINATE
BLOCKED_DEPENDENCY
EXECUTING
OUTPUTS_PENDING_VERIFICATION
RECEIPT_COMMITTED
DESTRUCTION_PENDING_VERIFICATION
COMPLETE
RETRYABLE
FAILED
EXPIRED
SUPERSEDED
MANUAL_REVIEW_REQUIRED
```

Participant-facing wording must preserve the difference between packet acceptance, execution, verification, admissibility, review, publication, and release.

## Current state

```text
canonical TVC contract committed: true
TVC implementation schemas: false
TVC order admission engine: false
provider adapter conformance: false
Site root-order endpoint: not verified
Site status endpoint: not verified
upload-triggered ephemeral execution: not verified
normalized receipt projection: not verified
worker destruction evidence: not verified
production readiness: false
release authority: false
```

## Required implementation artifacts

Destination: `StegVerse-Labs/Site`

```text
api/hil/response-packets.* or equivalent framework route
api/hil/orders/[order_id].* or equivalent framework route
api/hil/orders/[order_id]/receipts.* or equivalent framework route
schemas/hil-response-packet-intake.schema.json
schemas/hil-root-order-projection.schema.json
lib/hil/order-client.*
lib/hil/order-status-projection.*
tests/hil/ephemeral-order-ingress.*
data/hil-ephemeral-order-integration-latest.json
```

The actual paths may follow the connected Vercel project framework, but the external contract must remain provider neutral.

## Required integration tests

```text
SITE-EO-01 valid packet -> 202 and intake receipt
SITE-EO-02 malformed envelope -> DENY
SITE-EO-03 exact-byte hash mismatch -> DENY
SITE-EO-04 duplicate idempotency key -> same accepted order or explicit duplicate denial
SITE-EO-05 client disconnect after 202 -> work continues
SITE-EO-06 missing TVC dependency -> BLOCKED_DEPENDENCY
SITE-EO-07 provider change -> canonical status unchanged
SITE-EO-08 missing execution receipt -> not COMPLETE
SITE-EO-09 missing destruction evidence under required policy -> not COMPLETE
SITE-EO-10 complete verified lifecycle -> COMPLETE
```

## Continuation path

1. Read the TVC contract and its specific mirror handoff.
2. Implement the TVC schemas, admission engine, receipt contracts, and first provider adapter.
3. Inspect the connected Vercel Site project and current framework routing.
4. Add the three public interfaces without changing unrelated routes.
5. Bind Site root orders to commit-pinned TVC schemas and package authority.
6. Execute SITE-EO-01 through SITE-EO-10.
7. Prove one upload continues after client disconnection and produces execution plus destruction receipts.
8. Preserve exact provider and deployment evidence.
9. Update this handoff, `docs/HIL_SITE_MIRROR_HANDOFF.md`, `docs/HIL_MIRROR_HANDOFF.md`, and machine-readable HIL state.
10. Do not tag, release, publish, or claim participant readiness until all required gates pass.

## Downstream destinations

After independently verified implementation and authorization:

```text
Admissible-Existence/AE or CGE authority surface
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
HIL Master Record authority
```

## Release posture

```text
contract integration posture: DOCUMENTED
live Site implementation: NOT ESTABLISHED
live TVC execution: NOT ESTABLISHED
provider conformance: NOT ESTABLISHED
participant readiness: false
publication authority: false
release authority: false
```

## Archive readiness

This handoff and the canonical TVC contract contain the complete implementation boundary. No additional part of the prior conversational thread is required to continue, and the complete thread is ready for archiving.
