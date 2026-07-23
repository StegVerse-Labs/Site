# StegMusic Cultural Performance Model

## Purpose

StegDJ must learn historically grounded instrumental traditions as living social performance systems, not as flat genre labels or collections of instrument samples.

The first scoped implementation domain is lyrics-free Appalachian circle performance. Broader genre competence should be derived from deeply modeled subcultures, instruments, techniques, histories, social structures, and performance recovery patterns.

## Core principle

```text
learn culture deeply enough to understand the sound
rather than learning the sound superficially and assigning it a culture
```

A generated performance is not culturally credible merely because it contains a banjo, fiddle, mandolin, guitar, dulcimer, or modal melody. Credibility depends on how performers share, transfer, preserve, repair, and recover the tune.

## Appalachian circle model

The canonical performance unit is a family or neighborhood circle in which several participants of different ages and skill levels sustain one tune together.

The model must represent:

```text
shared tune memory
rotating performers
instrument handoff
role handoff
skill and age variation
instrument wear and repair
continuous performance through interruption
leader mobility
collective recovery
```

The tune belongs to the circle rather than to one permanent lead performer.

## Role separation

StegDJ must treat these as separate state dimensions:

```text
musical role != instrument != performer
```

A performer may move among melody, rhythm, drone, counterline, percussive emphasis, rest, repair, and re-entry. A musical role may transfer from fiddle to mandolin, banjo, guitar, dulcimer, or another available instrument without resetting the tune.

## Ensemble state

Each simulated circle maintains:

```text
participants
age and experience profiles
available instruments
instrument condition
current role assignments
shared phrase familiarity
rhythmic anchor
current leader
handoff readiness
repair state
```

Differences in skill should create coherent variation rather than random error. A less experienced player may simplify a phrase, enter late, follow another player, or inherit only part of a role.

## Physical instrument model

Each instrument must have a physical state, including:

```text
string age
string tension
tuning stability
material wear
attack intensity
bow or picking pressure
repetition rate
prior damage
temperature and environmental effects
```

Physical state influences timbre, tuning drift, attack, decay, resonance, and failure probability.

## String-failure model

A string break under high stress and quick play is not a fixed sound effect. The event may include:

```text
sharp metallic crack
brief unstable pitch rise or chirp
loss of the intended note
loose-string rattle or whip
contact noise against the instrument
next attack landing on absence
sympathetic ringing from remaining strings
```

Failure probability may rise with physical stress but the exact bar, measure, beat, and gesture must remain stochastic.

```text
predictable pressure envelope
+ uncertain exact failure time
+ instrument-specific break acoustics
+ ensemble recovery behavior
```

A break should not always occur at a bar line or phrase boundary.

## Continuity after failure

The break is only the beginning of the event. The performance must propagate its consequences:

```text
string failure mid-gesture
-> expected note fractures
-> player adapts or drops out
-> nearby roles widen
-> rhythm and tune identity continue
-> another performer absorbs part of the missing function
-> repair or substitution occurs during performance
-> repaired instrument re-enters imperfectly
```

The tune proves itself by continuing through disruption.

```text
continuity is demonstrated by successful role recovery,
not by pretending disruption never occurred
```

## Composition engine requirements

The synthesis engine requires more than samples or MIDI patterns. It needs:

```text
ensemble role graph
performer-role assignments
instrument-condition state
handoff rules
dropout recovery rules
phrase-memory model
shared rhythmic anchor
variation inheritance
repair and re-entry events
room and proximity model
```

A phrase must be represented as something several performers partially know and can preserve, not as a permanent clip owned by one track.

## Cultural lineage model

Subcultures are modeled as linked nodes rather than flat tags.

Nodes may represent:

```text
regional tradition
instrument
playing technique
rhythmic pattern
cadence
production method
historical influence
community function
```

Edges may include:

```text
originated_from
influenced_by
shares_instrument_with
shares_cadence_with
adapted_technique_from
regional_variant_of
merged_with
reacted_against
commercialized_as
```

Broad categories such as country, rock, blues, gospel, ska, reggae, grunge, and alternative rock are derived from overlaps among deeply grounded traditions.

## Development domains

Initial high-resolution instrumental domains:

```text
Appalachian family and neighborhood circle traditions
Texas and Red Dirt country instrumental language
blues and gospel-derived harmonic systems
Jamaican ska, rocksteady, reggae, and dub lineages
alternative rock and grunge production structures
```

Each domain must produce instrument, technique, rhythm, cadence, form, production, lineage, uncertainty, and permitted-synthesis records.

## Instrumental-first boundary

The primary learning environment is lyrics-free music.

```text
instrumental emotional navigation first
-> context-sensitive transition learning
-> cultural performance modeling
-> controlled mood-direction testing
-> later lyrical interpretation
```

Traditional holiday music may be treated as a separately labeled exception, with explicit cultural and emotional posture. General lyric, dialect, language, history, dialogue, and semantic modeling remain deferred.

## Personalization boundary

StegDJ should combine cultural-performance structure with the active user's learned emotional map, including:

```text
voluntary choice
replay
completion
skip
stop
familiarity tolerance
novelty tolerance
transition acceptance
current session intent
contextual emotional direction and intensity
```

The result should preserve cultural structure while changing the composition for the user.

```text
familiar enough to be emotionally credible
novel enough to be personally meaningful
different enough to remain an original composition
```

No identifiable protected melody, lyric, hook, chorus line, arrangement, or artist voice may be reproduced without the required rights.

## Sensory fidelity benchmark

The engineering objective is perceptual deception of the senses during a controlled blind evaluation.

```text
indistinguishable in musical credibility
but never falsely represented in origin after disclosure
```

The benchmark sequence is:

```text
blind sensory exposure
-> independent judgment
-> forced human-or-StegDJ classification
-> provenance disclosure
-> method and evidence inspection
```

Qualified musicians familiar with the selected tradition should evaluate:

```text
instrument realism
ensemble interaction
role circulation
handoff credibility
historical plausibility
timing variation
failure and recovery behavior
room interaction
cultural authenticity
emotional credibility
mechanical-generation artifacts
```

A successful result approaches chance-level origin classification while maintaining high cultural-authenticity ratings.

The purpose of the blind phase is to test the same skills standard humans have long used when evaluating unknown performers:

> I would not have believed it if I had not heard it for myself.

## Governed event model

Candidate event types:

```text
cultural_profile_selected
ensemble_circle_created
performer_role_assigned
instrument_handoff_started
instrument_handoff_completed
role_substitution_started
instrument_condition_changed
string_failure_occurred
ensemble_recovery_started
repair_started
repair_completed
instrument_reentry_started
instrument_reentry_completed
cultural_fidelity_evaluated
blind_origin_classification_recorded
provenance_disclosed
```

Each event should preserve direct observations, derived interpretation, confidence, uncertainty, profile scope, evidence references, and authority=`none` for Site fixtures.

## Authority boundaries

```text
cultural profile != cultural ownership
instrument sample != authentic performance
historical influence != unrestricted reproduction right
blind sensory test != permission to misrepresent provenance
perceptual indistinguishability != factual identity
user response != universal preference truth
simulated failure != historical event evidence
Site fixture != production activation
```

## Internal testing gate

The cultural-performance slice is not internally complete until testers can:

```text
select an instrumental cultural profile
inspect performers, roles, instruments, and condition state
hear role circulation and handoff
observe stochastic failure outside fixed bar placement
hear ensemble compensation and uninterrupted tune identity
observe repair and imperfect re-entry
compare human and StegDJ examples in a blind test
inspect provenance after classification
verify that generated output remains profile-scoped and rights-bounded
```

## Destination

Primary destination: `StegVerse-Labs/Site` for public mirror, browser fixture, validation, and evidence presentation.

Later production destinations include the StegDJ composition engine, rights-resolution service, Master Records custody, blind-test evaluation service, and internal patent packet.
