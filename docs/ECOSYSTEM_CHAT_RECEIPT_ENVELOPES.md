# Ecosystem Chat Receipt Envelope Previews

## Status

```text
mode: backend-shaped preview artifacts
live signatures: false
issuer verification: false
Site-issued governing receipts: false
authority receipt result: ALLOW preview
execution receipt result: DRY_RUN_ONLY preview
```

## Purpose

These envelopes define how authority and execution receipts should bind governed transitions without falsely claiming a live signature, verified issuer, or activated backend.

## Authority receipt

```text
fixtures/ecosystem-chat/authority-receipt-envelope.example.json
```

It binds:

- authority request ID
- transition type
- ALLOW result and evaluation-only scope
- policy reference and hash
- evidence references
- commit-time validity
- replay and reconstruction pointers
- supersession posture

## Execution receipt

```text
fixtures/ecosystem-chat/execution-receipt-envelope.example.json
```

It binds:

- execution request ID
- authority request ID and ALLOW result
- DRY_RUN_ONLY execution result
- commit-time validity
- zero resource use
- no state change
- no rollback performance
- authority-receipt reconstruction pointer
- replay, reconstruction, and supersession posture

## Cryptographic boundary

Both fixtures declare a canonicalization method and preview-shaped SHA-256 digest, but keep these fields null:

```text
signature_algorithm
signature
key_id
```

The preview issuer remains unverified. These envelopes are structurally cryptographic, not cryptographically proven.

## Validator

```text
python scripts/check_ecosystem_chat_receipt_envelopes.py
```

The validator confirms transition binding, preview-only digest shape, null signature fields, replayability, reconstructability, supersession posture, authority-to-execution linkage, and zero state-changing resource use.

It is included in:

```text
python scripts/run_site_task.py validate
python scripts/run_site_task.py public-guard
```

## Activation boundary

A live backend must canonicalize the receipt payload, calculate the actual digest, sign it using a governed key, identify the verified issuer and key, preserve replay and reconstruction references, and issue authority and execution receipts as distinct artifacts. Site cannot perform or claim those actions.
