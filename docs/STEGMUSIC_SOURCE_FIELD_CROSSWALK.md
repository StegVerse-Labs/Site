# StegMusic Source Field Crosswalk

## Purpose

This crosswalk maps eight external music compendiums into the canonical StegMusic song, corpus, and frozen-evidence records.

The crosswalk does not assume that similarly named fields mean the same thing. Every adopted value preserves its source-native form, normalized form, mapping confidence, uncertainty, and availability state.

## Canonical field groups

```text
work identity
recording identity
release or source identity
performer identity
instrument identity
place
date or historical period
audience
social function
musical structure
pitch and tuning
rhythm and microtiming
timbre and acoustics
ensemble and role grammar
historical lineage
physical component state
rights and access
```

## Source roles

### Global Jukebox

Best direct contribution: social function, place, historical context, ensemble organization, leader/group relationships, and performance grammar.

Major gaps: current catalog identity, dense signal analysis, physical instrument condition, and current rights posture.

### Dunya / CompMusic

Best direct contribution: culture-specific musical structure, pitch systems, tuning, phrase and section analysis, timing, and computed performance representations.

Major gaps: broad global coverage, target StegDJ traditions not already represented, physical degradation, and unrestricted source-audio access.

### MusicBrainz

Best direct contribution: work, recording, release, performer, instrument, place, event, and relationship identity.

Major gaps: acoustic detail, cultural grammar, audience, microtiming, physical component state, and synthesis permission.

### AcousticBrainz

Best direct contribution: recording-indexed tonal, rhythmic, spectral, timbral, loudness, and structural features.

Major gaps: current ingestion, cultural context, role behavior, audience, physical causality, and rights determination.

### Library of Congress National Jukebox

Best direct contribution: historical recording, take, label, contributor, date, place, audience or market, recording technology, and source-specific rights statements.

Major gaps: detailed mathematical performance mapping, role grammar, microtiming annotation, and physical component state.

### DOREMUS

Best direct contribution: semantic distinctions among work, expression, performance, recording, publication, casting, derivation, and intended instrumentation.

Major gaps: low-level audio, gesture, audience, oral transmission, and physical component state.

### RISM

Best direct contribution: written-source identity, manuscript and edition provenance, place, date, instrumentation, incipits, holdings, and historical variation.

Major gaps: realized sound, recording identity, audience response, microtiming, and performance-role behavior.

### Million Song Dataset

Best direct contribution: large-scale recording features, structural segments, pitch, timbre, rhythm, loudness, year, similarity, and benchmark methodology.

Major gaps: source audio, current maintenance, deep cultural context, audience, social function, and physical performance state.

## Gap substitution

For each field:

```text
query the highest-priority source assigned to that field
-> preserve direct, partial, absent, unknown, restricted, or conflicted state
-> consult the approved secondary source when necessary
-> preserve both provenance paths
-> mark the adopted fallback SECONDARY_DERIVED
-> freeze it before composition influence
```

A secondary source does not correct or erase the primary source's absence.

## Mapping confidence

Every normalized field must record one of:

```text
EXACT
HIGH_CONFIDENCE
PARTIAL
INTERPRETIVE
UNRESOLVED
```

`EXACT` is reserved for stable identifiers or semantically equivalent fields. Cultural, historical, genre, mood, and audience mappings should rarely be assumed exact without supporting evidence.

## Composition use

The crosswalk supports:

```text
identity resolution
historical and geographic conditioning
audience and social-function selection
song-level mathematical mapping
corpus construction
culture-specific performance grammar
rights and access review
source conflict detection
frozen evidence creation
composition receipt generation
```

## Machine-readable record

`data/stegmusic/source-field-crosswalk.v1.json`

## Boundaries

```text
field-name similarity != semantic equivalence
source presence != correctness
source absence != evidence of nonexistence
secondary derivation != primary correction
catalog identity != cultural truth
rights statement != synthesis authorization unless explicitly established
Site fixture != production activation
```
