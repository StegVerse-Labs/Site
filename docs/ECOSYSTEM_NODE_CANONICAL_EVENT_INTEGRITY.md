# Ecosystem Node Canonical Event Integrity

## Goal

Move the synchronized Conversation, Governed Record, and Split View contract from browser-only correlation markers toward deterministic, fail-closed canonical records.

This layer validates records for rendering. It does not create execution authority, admissibility, publication authority, custody, release authority, or actor standing.

## Integrity path

```text
governed gateway/runtime event
→ canonical event schema
→ canonical SHA-256 verification
→ stable event-ID graph validation
→ Site rendering eligibility
→ Conversation / Governed Record / Split projections
```

## Required guarantees

Every accepted event must contain:

- one stable `event_id`;
- an RFC3339-compatible timestamp;
- actor type and identity reference;
- one supported event type;
- human and governed projection objects;
- unique policy, evidence, artifact, and continuity references;
- a canonical `sha256:` event digest.

A stream fails closed when it contains:

- duplicate event identifiers;
- hash drift;
- missing required fields or unexpected top-level fields;
- a parent reference that is unresolved or appears only later in the stream;
- unresolved event-scoped evidence or continuity references;
- duplicate references.

## Canonical hashing

The digest is calculated over sorted, compact UTF-8 JSON with the event `hash` field set to an empty string.

```text
sha256(canonical_json(event_with_empty_hash))
```

The resulting value is represented as:

```text
sha256:<64 lowercase hexadecimal characters>
```

This replaces the browser preview's non-cryptographic `fnv1a32:*` marker for governed records received from upstream. A valid digest is integrity evidence only; it is not a signature, custody receipt, admissibility result, or authority grant.

## Correlation boundary

```text
correlation == stable_event_id_only
text_matching == prohibited
view_selection_mutates_event_stream == false
projection_visibility_changes_authority == false
```

Parent, evidence, and continuity relationships are evaluated from explicit identifiers. Similar or identical text never establishes correspondence.

## Current implementation

```text
schemas/ecosystem-node-canonical-event.schema.json
fixtures/ecosystem-node-canonical-events.json
scripts/validate_ecosystem_node_canonical_events.py
tests/test_ecosystem_node_canonical_events.py
.github/workflows/validate-ecosystem-node-canonical-events.yml
```

## Next integration step

The Site browser renderer should accept gateway/runtime records only through an integrity adapter that:

1. validates this schema;
2. verifies canonical SHA-256 hashes;
3. validates event order and graph references;
4. rejects duplicate or unresolved identifiers;
5. freezes accepted records before projection;
6. keeps locally constructed preview records explicitly separate from upstream governed records.
