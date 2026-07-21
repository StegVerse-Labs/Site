# Ecosystem Node Canonical Event Mapping Contract

## Status

Initial interface-shell contract for `StegVerse-Labs/Site/ecosystem-chat.html`.

This contract defines synchronized projections. It does not grant execution, publication, admissibility, custody, or release authority.

## Authority model

```text
Canonical governed event stream
├── Conversation renderer
├── Governed-record renderer
└── Split-view correlation layer
```

Neither visible pane is authoritative. The canonical event structure is authoritative.

Changing a view MUST NOT create, remove, reorder, or mutate canonical events. Hiding governance complexity MUST NOT disable governance.

## Minimum canonical event

```json
{
  "event_id": "stable-unique-id",
  "parent_event_id": null,
  "timestamp": "RFC3339",
  "actor": {},
  "event_type": "message|decision|execution|receipt|policy|evidence",
  "human_projection": {},
  "governed_projection": {},
  "policy_refs": [],
  "evidence_refs": [],
  "artifact_refs": [],
  "continuity_refs": [],
  "hash": ""
}
```

## Mapping invariants

1. Every conversation event has exactly one stable `event_id`.
2. Every rendered governed record uses the same `event_id`; correlation never uses text matching.
3. Governance-only events may omit a conversation rendering.
4. Human-readable, formatted governed, and raw JSON/JSONL outputs resolve to the same canonical object.
5. Role-based disclosure and redaction are projection policies; they do not rewrite the underlying event identity.
6. Exports preserve event order, parent links, evidence links, continuity links, and hashes.
7. Replay consumers must reject duplicate event identifiers and unresolved mandatory parent references.
8. The initial browser hash is a non-cryptographic fixture marker (`fnv1a32:*`), not a signature or custody proof. Production records require canonical cryptographic hashing and signature verification upstream.

## Initial renderer modes

- `conversation`: human-facing messages, notices, artifacts, attachments, and summaries.
- `governed`: formatted technical inspection or raw JSONL.
- `split`: synchronized panes with stable-ID selection correlation.

## Disclosure extension points

Future renderers may filter or redact fields using:

```json
{
  "viewer_role": "public|operator|technical|legal|executive|auditor",
  "locale": "BCP47-language-tag",
  "disclosure_policy_refs": [],
  "redaction_receipt_refs": []
}
```

A redacted renderer must retain `event_id`, ordering, permitted chain references, and an explicit redaction marker.

## Future governed fields

The `governed_projection` object is intentionally extensible for model/provider identifiers, policy/delegation references, evidence and artifact hashes, admissibility, execution requests/results, confidence, uncertainty, correspondence, receipts, signatures, quarantine, refusal, override, and recovery events.

## Production next step

Move canonical event creation to the governed gateway/runtime so the browser receives immutable canonical records rather than constructing preview records from rendered DOM events. The Site renderer should then validate schema, hash, disclosure policy, and correlation integrity before display.
