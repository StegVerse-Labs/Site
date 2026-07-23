# StegMusic Song Reference Builder

The builder converts heterogeneous source records and computed analysis into one governed song evidence unit.

```text
source-native records
-> normalized source records
-> preserved gaps and substitutions
-> historical, audience, place, musical, and performance maps
-> rights posture
-> confidence and conflicts
-> frozen song reference
```

Each source retains identity, priority, availability state, retrieval time, response hash, provenance path, adopted and missing fields, source-native record, mapping confidence, and uncertainty.

Supported states:

```text
AVAILABLE
ABSENT
UNKNOWN
RESTRICTED
CONFLICTED
SECONDARY_DERIVED
```

`SECONDARY_DERIVED` never erases the primary source's original gap.

The builder separates source access, composition use, audio custody, restrictions, and evidence references. `ALLOW_REFERENCE_ONLY` permits contextual lookup but not derived generative analysis. `REQUIRES_REVIEW`, `PROHIBITED`, and `UNKNOWN` remain blocked from autonomous composition use.

Derived-analysis eligibility requires:

```text
composition_use_posture = ALLOW_DERIVED_ANALYSIS
builder hash present
source records present
no rights blocker
```

Every completed record receives a SHA-256 builder hash and is frozen against in-memory mutation.

```text
song reference != source recording
confidence != correctness
access != permission
reference eligibility != synthesis authorization
statistical similarity != cultural legitimacy
builder hash != rights grant
Site fixture != production activation
```

Canonical files:
- `data/stegmusic/song-reference.schema.v1.json`
- `assets/stegmusic-song-reference-builder.js`
- `scripts/check_stegmusic_song_reference_builder.py`
