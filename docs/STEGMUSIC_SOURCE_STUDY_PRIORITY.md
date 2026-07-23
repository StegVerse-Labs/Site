# StegMusic Source Study Priority and Gap Map

## Purpose

This document governs how StegDJ studies external music compendiums, records what each source provides, identifies what is distinctly unavailable, and resolves missing information through secondary sources without collapsing disagreement or provenance.

The study order is based on contribution to culturally credible original composition, not database size.

## Priority order

### 1. Global Jukebox

Primary role: cultural and social performance grammar.

Available:

- individual performance coding;
- Cantometrics and related performing-arts datasets;
- ensemble organization;
- leader/group relationships;
- rhythmic and melodic coordination;
- ornamentation, phrasing, vocal and instrumental organization;
- society, geography, language, and social-context links;
- downloadable coded data.

Distinctly unavailable or insufficient:

- current broad commercial catalog identity;
- dense modern audio features;
- note-level score alignment;
- physical instrument/tool condition;
- stochastic failure, repair, and re-entry;
- modern rights posture;
- continuously updated recording coverage.

Secondary-source substitutions:

- MusicBrainz for stable work/recording/person/place identity;
- Dunya/CompMusic for tradition-specific computational analysis;
- AcousticBrainz or StegDJ extraction for signal features;
- Library of Congress for early recording context and intended audience;
- StegMusic component standards for physical state and failure.

Store from study:

- normalized cultural-performance variables;
- source-code definitions and version;
- society/place/language crosswalks;
- confidence and coder-disagreement notes;
- mappings from coded traits to StegDJ performance-grammar candidates.

Near-real-time access:

- discovery of additional records and updated documentation;
- never depend on an uncaptured live response during composition.

### 2. Dunya / CompMusic

Primary role: culture-specific computational musicology.

Available:

- tradition-specific corpora;
- recordings and scores where permitted;
- metadata and computed analysis;
- tonic, tempo, section, phrase, and score-performance methods;
- culturally specialized schemas and algorithms;
- evidence that one universal Western analysis is inadequate.

Distinctly unavailable or insufficient:

- comprehensive global genre coverage;
- Appalachian, Red Dirt, blues/gospel, ska/reggae/dub, grunge, and alternative-rock coverage as one integrated corpus;
- broad audience modeling;
- physical component degradation and repair;
- unrestricted source-audio access for every corpus.

Secondary-source substitutions:

- Global Jukebox for comparative social-performance structure;
- MusicBrainz for shared external identity;
- Library of Congress and later tradition-specific archives for uncovered American traditions;
- StegDJ-built corpora for uncovered domains.

Store from study:

- cultural adapter definitions;
- analysis-method versions;
- tonic, phrase, section, ornament, and score-performance representations;
- access restrictions and permitted-use posture;
- mappings between tradition-specific fields and shared StegMusic records.

Near-real-time access:

- metadata and computed files available through supported interfaces;
- authorized audio only when access and rights permit;
- freeze any returned material that changes composition.

### 3. MusicBrainz

Primary role: canonical external identity and relationship backbone.

Available:

- works;
- recordings;
- releases;
- artists and contributors;
- instruments;
- places and events;
- labels;
- relationship graphs;
- web service and database dumps;
- persistent MusicBrainz identifiers.

Distinctly unavailable or insufficient:

- detailed signal analysis;
- cultural-performance grammar;
- listener/audience response;
- microtiming and performer gesture;
- physical instrument state;
- synthesis permission or rights determination.

Secondary-source substitutions:

- AcousticBrainz or StegDJ extraction for signal features;
- Global Jukebox and Dunya for cultural structure;
- DOREMUS for richer work/expression/performance/publication semantics;
- rights-specific evidence sources for legal posture.

Store from study:

- external IDs and crosswalk confidence;
- work/recording/release distinctions;
- relationship snapshots used by a composition;
- retrieved-at time and response hash;
- unresolved identity conflicts.

Near-real-time access:

- identity resolution and relationship refresh;
- obey service rate limits;
- freeze every result that materially influences generation.

### 4. AcousticBrainz

Primary role: reusable recording-level acoustic-feature precedent.

Available:

- low-level acoustic JSON;
- high-level inferred JSON;
- MusicBrainz recording-ID indexing;
- spectral, tonal, rhythmic, loudness, dynamics, key, scale, mood, and genre-related values;
- downloadable historical dumps;
- similarity methods.

Distinctly unavailable or insufficient:

- new submissions after discontinuation;
- current complete catalog coverage;
- cultural and historical explanation;
- performer-role circulation;
- audience and social function;
- physical causality and repair;
- authoritative truth for inferred mood or genre.

Secondary-source substitutions:

- StegDJ extraction for new recordings;
- MusicBrainz for current identity;
- Global Jukebox and Dunya for cultural interpretation;
- song/corpus records for role and historical context.

Store from study:

- compatible low-level feature definitions;
- extractor and model versions;
- recording ID and duplicate-submission identity;
- raw derived values used in training or comparison;
- uncertainty and known bias notes.

Near-real-time access:

- retrieval of existing historical records only;
- prefer durable local snapshots for reproducibility.

### 5. Library of Congress National Jukebox

Primary role: early historical recordings, audience, place, market, and recording technology.

Available:

- recording-level metadata;
- date, location, matrix, take, catalog, label, contributors, groups, language, category, and target audience;
- streaming collection;
- a downloadable exploratory package containing metadata and audio for a rights-scoped subset;
- early acoustic-recording context.

Distinctly unavailable or insufficient:

- fine-grained genre vocabulary;
- mathematical performance maps;
- performer-role and microtiming annotation;
- broad noncommercial family/field-performance coverage;
- automatic permission for every reuse.

Secondary-source substitutions:

- Global Jukebox for social and noncommercial performance structure;
- StegDJ signal extraction for mathematical features;
- MusicBrainz for identity crosswalks;
- RISM for earlier written sources;
- source-specific rights review for reuse.

Store from study:

- item and take identity;
- date/place/audience/market context;
- recording-technology profile;
- source and rights statement;
- audio or derived features only when lawfully permitted;
- historical terminology preserved with an explicit interpretation warning.

Near-real-time access:

- collection discovery and item metadata through Library interfaces;
- freeze queried item records used by composition.

### 6. DOREMUS

Primary role: semantic ontology for works, expressions, performances, recordings, publications, and derivations.

Available:

- linked-data ontology;
- work/performance/publication distinctions;
- casting, medium, key, genre, tempo, style, derivation, and harmonic-structure concepts;
- SPARQL endpoint and example queries.

Distinctly unavailable or insufficient:

- low-level audio features;
- detailed gesture and microtiming;
- informal oral transmission;
- social audience behavior;
- physical component condition;
- real-time composition constraints.

Secondary-source substitutions:

- MusicBrainz for broader public identities;
- Dunya and Global Jukebox for performance behavior;
- RISM for source provenance;
- StegMusic schemas for physical execution and generation receipts.

Store from study:

- adopted ontology terms and exact mappings;
- work/expression/performance/recording distinctions;
- derivation and intended-versus-realized instrumentation relations;
- ontology version and unsupported concepts.

Near-real-time access:

- semantic discovery through SPARQL;
- cache and hash any query result used in generation.

### 7. RISM

Primary role: historical written-source provenance and incipit relationships.

Available:

- manuscripts, printed editions, libretti, and theoretical writings;
- source dating, location, holding institution, and provenance;
- instrumentation and source descriptions;
- musical incipits;
- JSON-LD resource API and data services.

Distinctly unavailable or insufficient:

- realized sound for most records;
- audience reaction;
- microtiming and improvisation;
- recording acoustics;
- performer-role behavior;
- comprehensive modern popular and vernacular coverage.

Secondary-source substitutions:

- DOREMUS for semantic work/performance relations;
- MusicBrainz for modern identities;
- Library of Congress for historical recordings;
- Dunya or StegDJ analysis for realized performance.

Store from study:

- source IDs, dates, places, holdings, instrumentation, incipits, and variant relations;
- provenance and uncertainty;
- clear separation between written source and performed evidence.

Near-real-time access:

- source discovery and incipit search;
- freeze records used to condition a composition.

### 8. Million Song Dataset

Primary role: large-scale MIR method and statistical-baseline study.

Available:

- metadata and derived analysis for one million tracks;
- segments, pitch, timbre, sections, beats, tempo, meter, loudness, similarity, tags, and year;
- complementary listener, lyric-derived, cover-song, and tag datasets;
- established research benchmarks.

Distinctly unavailable or insufficient:

- source audio in the core dataset;
- current continuously maintained coverage;
- deep cultural context;
- physical instrument state;
- social-performance grammar;
- dependable full-dataset availability through every formerly documented channel.

Secondary-source substitutions:

- AcousticBrainz for open song-level JSON precedent;
- StegDJ extraction for current recordings;
- MusicBrainz for identity repair;
- Global Jukebox, Dunya, LOC, and RISM for cultural/historical meaning.

Store from study:

- adopted feature definitions and benchmark methods;
- dataset/version identifiers;
- experiment splits and evaluation results;
- no assumption that legacy access remains available.

Near-real-time access:

- none required for composition;
- use local/batch study copies or documented subsets.

## Cross-source missing-information rule

For every requested field:

```text
query highest-priority authoritative source
-> record AVAILABLE, ABSENT, UNKNOWN, RESTRICTED, or CONFLICTED
-> if not AVAILABLE, query approved secondary source
-> preserve both source identities and retrieval evidence
-> never overwrite the primary-source absence
-> mark the adopted value as SECONDARY_DERIVED
-> freeze the result if it influences composition
```

An unavailable field is evidence about the source and remains part of the record even when another source supplies the value.

## Composition benefit classes

Study results support:

1. identity and version resolution;
2. musical segmentation and feature extraction;
3. cultural-performance grammar;
4. historical, geographic, audience, and technology conditioning;
5. statistical distinction among common, rare-valid, regional, period-specific, performer-specific, recording-specific, transitional, and accidental behavior;
6. evidence-backed explanation of every generated choice.

## Durable-storage rule

Store any information that:

- materially changes a generated result;
- may change or disappear upstream;
- is expensive or impossible to recompute;
- is needed for replay, audit, comparison, attribution, rights review, or challenge;
- resolves a conflict among sources;
- defines a culture-specific adapter or corpus distribution.

## Composition-time-access rule

Access close to composition time only when the information is:

- discovery-oriented;
- likely to improve or expand upstream;
- not already required as a stable corpus primitive;
- available through an authorized interface;
- captured and frozen before it affects the generated result.

## Governing distinction

```text
songs and performances are evidence units
corpora are derived statistical maps
genres are navigational summaries
external sources are evidence providers
StegDJ is the governed synthesis and reconstruction layer
```
