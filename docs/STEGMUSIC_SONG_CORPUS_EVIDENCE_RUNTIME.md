# StegMusic Song and Corpus Evidence Runtime

The song builder converts source-native observations into one governed song evidence unit. It preserves priority, gaps, restrictions, conflicts, secondary derivations, rights posture, confidence, source hashes, and provenance.

The corpus builder aggregates eligible song references without flattening them into a genre stereotype.

```text
source observations
-> governed song references
-> weighted corpus membership
-> distributions and variant clusters
-> rare-valid and transitional evidence
-> composition constraints
-> governed corpus reference
```

## Membership

Each song reference receives an explicit membership reason and weight. References that are unavailable for derived analysis remain visible with zero generation weight instead of disappearing.

## Distributions

Corpus distributions are weighted by governed membership. A distribution describes observed evidence; it is not a mandatory compositional formula.

## Variant clusters

Historical and regional groupings remain separately inspectable. Later adapters may add audience, setting, technology, performer, instrumentation, and transitional clusters without replacing the underlying song records.

## Outliers

Low-weight valid members may be classified `RARE_VALID` and retained for generation. Rights-blocked or invalid records are classified `EXCLUDED`. Transitional evidence must remain representable rather than being averaged away.

## Constraints

The runtime emits:

- variable ranges;
- rare-but-valid evidence;
- prohibited copying rules;
- rights constraints;
- uncertainty-review constraints.

## Boundaries

```text
corpus frequency != compositional requirement
outlier != error
rare != inadmissible
cluster != culture
confidence != correctness
membership != permission
builder hash != rights grant
Site runtime != production synthesis activation
```

Canonical files:

- `assets/stegmusic-song-reference-builder.js`
- `assets/stegmusic-corpus-reference-builder.js`
- `data/stegmusic/song-reference.schema.v1.json`
- `data/stegmusic/corpus-reference.schema.v1.json`
- `scripts/check_stegmusic_song_corpus_builders.py`
