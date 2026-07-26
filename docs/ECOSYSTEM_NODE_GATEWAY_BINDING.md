# Ecosystem Node Browser Canonical Gateway Binding

## Status

Implementation contract for validating immutable upstream governed events before they enter the synchronized Conversation, Governed Record, or Split View renderers.

## Boundary

The browser may validate and render an upstream event stream. It may not repair, reorder, rehash, reidentify, authorize, admit, publish, execute, sign, or assume custody of that stream.

```text
Gateway/runtime canonical stream
        ↓
Browser SHA-256 and graph validation
        ↓
Immutable import into the existing canonical renderer
        ↓
Conversation / Governed Record / Split projections
```

## Required upstream stream envelope

```json
{
  "schema": "stegverse.canonical-event-stream.v0.1",
  "authority_effect": "NONE",
  "events": []
}
```

Every imported event must:

- retain the strict canonical event shape;
- carry a canonical `sha256:*` hash;
- declare `governed_projection.source_class` as `upstream_governed`;
- use a unique stable `event_id`;
- reference only already accepted parents and event-scoped evidence or continuity records;
- remain byte-semantically unchanged after validation.

## Preview separation

Existing Site-created preview events remain local simulation records identified by the `fnv1a32:*` fixture marker. They are not promoted into upstream governed records. Upstream events require SHA-256 validation before import.

```text
local preview != upstream governed event
validation != admissibility
rendering != custody
visibility != authority
```

## Fetch posture

The browser fetch helper uses:

- `cache: no-store`;
- omitted credentials;
- explicit JSON acceptance;
- a bounded timeout;
- fail-closed rejection of malformed responses.

A deployment may call `StegVerseCanonicalGatewayBinding.fetchAndImport(url)` only with an endpoint that returns the declared canonical stream envelope. Endpoint discovery and authorization remain separate concerns.

## Next implementation step

Connect the verified provider-neutral gateway discovery result to `fetchAndImport` using a declared canonical-event endpoint in the node advertisement. The advertisement must bind endpoint identity and must not imply execution, publication, or custody authority.
