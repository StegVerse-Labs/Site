# StegMusic Song Reference Builder

## Purpose

The song-reference builder converts heterogeneous source records and computed musical analysis into one governed song evidence unit.

```text
source-native records
-> normalized source records
-> preserved gaps and substitutions
-> historical, audience, place, musical, and performance maps
-> rights posture
-> confidence and conflicts
-> frozen song reference
```

## Source preservation

Each source record retains:

```text
source identity and priority
availability state
retrieval time
response hash
provenance path
adopted fields
missing fields
source-native record
mapping confidence
uncertainty
```

Supported field states are:

```text
AVAILABLE
ABSENT
UNKNOWN
RESTRICTED
CONFLICTED
SECONDARY_DERIVED
```

`SECONDARY_DERIVED` never replaces the primary source's original absence, restriction, conflict, or uncertainty.

## Confidence

Confidence is derived from source priority and availability posture, then reduced by unresolved conflicts and uncertainty.

Confidence is an aid to composition review. It is not truth, permission, cultural ownership, or authority.

## Rights and access

The builder separates:

```text
source access posture
composition use posture
authorized audio custody
restrictions and evidence references
```

A source can be openly accessible while still allowing reference only. A source can also be lawfully held while composition use remains prohibited.

The runtime rejects any record claiming authorized source-audio custody while its composition-use posture is `PROHIBITED`.

## Composition eligibility

Derived-analysis eligibility requires:

```text
composition_use_posture = ALLOW_DERIVED_ANALYSIS
builder hash present
source records present
no rights blocker
```

`ALLOW_REFERENCE_ONLY` permits contextual lookup but not derived generative analysis.

`REQUIRES_REVIEW`, `PROHIBITED`, and `UNKNOWN` remain blocked from autonomous composition use.

## Hash and immutability

Every completed song reference receives a SHA-256 builder hash and is frozen against in-memory mutation.

The hash covers the normalized evidence state, not the original external service or source file unless its own hash is separately preserved.

## Boundaries

```text
song reference != source recording
confidence != correctness
access != permission
reference eligibility != synthesis authorization
statistical similarity != cultural legitimacy
builder hash != rights grant
Site fixture != production activation
```

## Canonical files

- `data/stegmusic/song-reference.schema.v1.json`
- `assets/stegmusic-song-reference-builder.js`
- `scripts/check_stegmusic_song_reference_builder.py`
