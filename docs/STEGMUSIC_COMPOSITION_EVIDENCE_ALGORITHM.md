# StegMusic Composition Evidence Algorithm

## Purpose

This algorithm defines how StegDJ selects, studies, freezes, normalizes, and applies external musical evidence to produce an original, culturally grounded, physically credible, rights-bounded composition.

## Inputs

```text
user profile scope
session intent
cultural scope
historical scope
place and audience scope
instrument and tool availability
rights constraints
novelty and familiarity targets
source-study priority registry
stored song and corpus records
```

## Source resolution algorithm

For each required field or evidence class:

```text
1. identify the highest-priority source assigned to the field
2. query or load the source through an authorized interface
3. classify the response:
   AVAILABLE
   ABSENT
   UNKNOWN
   RESTRICTED
   CONFLICTED
4. preserve the primary response and retrieval evidence
5. when not AVAILABLE, query the approved secondary source
6. preserve the secondary response separately
7. record why the secondary value was adopted
8. freeze any value that can affect composition
9. reject unsupported values rather than silently inferring them
```

Absence is not overwritten. A field supplied by another source is marked `SECONDARY_DERIVED` and linked to the unresolved primary-source state.

## Evidence freezing

Every composition-affecting external result becomes a frozen evidence object containing:

```text
evidence_id
source_name
source_record_id
source_priority
retrieval_time
source_version_or_snapshot
request_or_query_hash
response_hash
availability_state
rights_and_access_posture
normalized_fields
confidence
uncertainty
conflicts
secondary_source_links
```

No live result may influence synthesis without entering the frozen evidence set.

## Identity resolution

```text
resolve work identity
-> resolve recording/performance identity
-> resolve release, source, take, edition, or manuscript identity
-> connect people, ensembles, instruments, places, and events
-> preserve unresolved duplicate or conflict candidates
```

MusicBrainz is the preferred public identity backbone where a reliable match exists. DOREMUS and RISM distinctions may refine work, expression, performance, publication, and source relationships.

## Song-level mathematical mapping

Each evidence song or performance is normalized into a song reference containing:

```text
identity and provenance
date, period, place, audience, and function
performers, instruments, tools, and roles
sections and phrase graph
pitch, interval, tuning, and cadence distributions
rhythm, meter, tempo, onset, and microtiming distributions
dynamics, articulation, spectral, timbral, and room features
role-transition and interaction matrices
variation, interruption, failure, repair, and recovery events
historical and cultural lineage edges
rights and permitted-use posture
source confidence and uncertainty
```

A source field is never promoted from inferred to observed without evidence.

## Corpus derivation

Related song records are grouped by explicit conditioning dimensions rather than broad genre alone:

```text
tradition
region
historical period
community or scene
audience and social function
performance setting
recording technology
instrument and tool availability
```

For each corpus, derive:

```text
common patterns
rare but valid patterns
regional variants
period variants
community variants
performer-specific behavior
recording-specific artifacts
outliers
transitional forms
cross-tradition influences
```

The corpus stores distributions and clusters, not only averages.

## Composition plan

```text
1. select cultural, historical, audience, and place scope
2. load the relevant stored corpus distributions
3. retrieve and freeze missing current identity or contextual evidence
4. select several song-level evidence records without copying a protected expression
5. separate invariant grammar from variable expression
6. select a valid original path through the distributions
7. instantiate performers, instruments, tools, component states, and room state
8. assign musical roles independently of performers and instruments
9. compose original phrases, transitions, and form
10. apply culture-specific performance grammar
11. apply physical excitation, coupling, wear, variation, failure, repair, and recovery
12. evaluate similarity and protected-expression risk
13. run cultural, acoustic, and sensory-fidelity checks
14. emit audio plus a complete governed composition receipt
```

## Store versus query decision

For every candidate datum, calculate a storage posture from these factors:

```text
composition influence
upstream volatility
recomputation cost
replay necessity
rights sensitivity
conflict relevance
corpus reuse value
```

Required posture:

```text
STORE when any replay, audit, source-loss, conflict, or expensive-recompute risk is material
QUERY when data is discovery-oriented, current, replaceable, and not yet composition-affecting
FREEZE_AFTER_QUERY whenever a query result changes selection, constraints, or generated output
```

## Near-real-time lookup classes

Suitable close-to-composition lookups include:

```text
current work and recording identity
new releases or newly linked performances
current source availability
new historical-source discoveries
current collection metadata
newly available tradition-specific analysis
rights or access posture requiring current verification
```

Unsuitable live dependencies include:

```text
core cultural grammar
validated corpus distributions
feature-extraction definitions
source conflict decisions
physical component models
previous composition receipts
```

Those must be stored and versioned.

## Conflict handling

When sources disagree:

```text
preserve every claim
rank source authority by field, not globally
record time and version
separate observation from interpretation
avoid forced collapse
select a working value only with stated rationale
carry unresolved conflict into uncertainty and composition constraints
```

## Rights and originality gate

Before synthesis:

```text
confirm permitted evidence use
exclude unauthorized source audio or protected material
prevent identifiable melody, hook, arrangement, lyric, or artist-voice reproduction
measure similarity at phrase, contour, rhythm, harmony, timbre, and arrangement levels
retain influence and exclusion evidence
```

Access to a recording does not establish derivative-use permission.

## Sensory-fidelity evaluation

The generated composition is evaluated for:

```text
instrument and tool realism
performance-practice credibility
ensemble interaction
historical and regional plausibility
variation and microtiming
failure and recovery consequences
room and recording behavior
cultural credibility
mechanical-generation artifacts
```

Blind human-versus-StegDJ classification occurs before provenance disclosure in controlled evaluation. Provenance is disclosed afterward.

## Composition receipt

The final governed record must include:

```text
composition_id
profile and session scope
intent
selected cultural, historical, audience, and place conditions
frozen evidence set
song and corpus references
source gaps and secondary substitutions
selected distributions and random seeds
performer-role graph
instrument and tool component states
failure, repair, recalibration, and recovery events
rights and originality decisions
model and extractor versions
output artifact hashes
evaluation results
confidence and uncertainty
provenance disclosure state
authority boundaries
```

## Authority boundary

```text
source availability != permission
catalog identity != cultural truth
statistical frequency != compositional requirement
secondary substitution != primary-source correction
similarity score != legal determination
cultural credibility != cultural ownership
blind perceptual success != factual human origin
Site fixture != production activation
```
