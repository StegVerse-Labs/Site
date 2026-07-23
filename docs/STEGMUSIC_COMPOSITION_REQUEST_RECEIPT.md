# StegMusic Composition Request and Receipt

## Purpose

This record pair binds frozen musical evidence to an authorized composition attempt and preserves the complete result afterward.

```text
frozen evidence packet
-> governed composition request
-> rights and execution gate
-> composition execution
-> governed composition receipt
```

## Composition request

The request defines the active profile and consent scope, session intent, cultural and historical posture, audience and place conditioning, novelty and familiarity targets, instrument and tool availability, rights constraints, required song and corpus references, and the final execution gate.

Execution is blocked unless:

```text
evidence_frozen = true
rights_gate_passed = true
composition_may_execute = true
blockers = []
```

The request must prohibit protected-expression copying and artist-voice imitation. Source audio use is limited to `NONE` or `AUTHORIZED_ONLY`.

## Composition receipt

The receipt preserves:

```text
composition and request identity
frozen evidence packet identity
song and corpus references
selected cultural, historical, audience, place, and intent conditions
model and extractor versions
random seeds and selected distributions
composition-plan hash
performer-role graph and handoffs
instrument and tool initial/final state hashes
failure, substitution, repair, recalibration, re-entry, and recovery events
rights and originality decision
evaluation results
artifact hashes and storage references
confidence, uncertainty, and conflicts
provenance disclosure
receipt hash
```

Rights and originality decisions are limited to:

```text
ALLOW
DENY
ESCALATE
```

Generated origin must be disclosed after any controlled blind evaluation.

## Replay boundary

A receipt is reconstructable only when its frozen evidence packet, song and corpus references, model versions, random seeds, selected distributions, component states, event references, and artifact hashes remain available.

The receipt does not claim that reconstruction will reproduce analog playback conditions perfectly. It preserves the governed inputs and execution state required to explain and test the composition.

## Authority boundaries

```text
valid schema != execution authorization
source availability != permission
rights score != legal determination
ALLOW decision != cultural ownership
blind-test success != human origin
receipt existence != audio quality
Site fixture != production synthesis activation
```

## Canonical files

- `data/stegmusic/composition-request.schema.v1.json`
- `data/stegmusic/composition-receipt.schema.v1.json`
- `scripts/check_stegmusic_composition_request_receipt.py`
