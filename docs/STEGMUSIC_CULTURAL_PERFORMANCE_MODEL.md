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

A performer may move among melody, rhythm, drone, counterline, percussive emphasis, rest, repair, and re-entry. A musical role may transfer among available instruments without resetting the tune.

## Ensemble state

Each simulated circle maintains participants, age and experience profiles, available instruments, instrument condition, role assignments, shared phrase familiarity, rhythmic anchor, current leader, handoff readiness, and repair state.

Differences in skill should create coherent variation rather than random error. A less experienced player may simplify a phrase, enter late, follow another player, or inherit only part of a role.

## Universal string-component dependency

All tensioned strings and string-like musical elements use `data/stegmusic/string-component-standard.v1.json` and `assets/stegmusic-string-physics.js`.

```text
one canonical string state
+ instrument-specific adapter
+ performer or tool interaction
= instrument-specific sound and failure behavior
```

The shared attributes include construction, geometry, tension, tuning, attachment, environment, use, wear, fatigue, damage, acoustics, failure, repair, retension, and re-entry. Instrument adapters may extend this state but may not redefine canonical fields.

This applies across plucked, bowed, struck, sympathetic, experimental, and repair/test contexts. Shared attributes do not mean that a fiddle string, piano string, banjo string, bow-hair bundle, and test-rig line sound or behave identically.

## Physical instrument model

Each instrument retains its own adapter and body state while consuming the standard string-component state. Physical state influences timbre, tuning drift, attack, decay, resonance, and failure probability.

## String-failure model

A string break under high stress and quick play is not a fixed sound effect. The event may include a sharp crack, brief pitch instability, loss of the intended note, loose-string motion, contact noise, the next attack landing on absence, and sympathetic ringing.

Failure probability rises from physical state while the exact bar, measure, beat, gesture, and failure site remain stochastic.

```text
predictable pressure envelope
+ uncertain exact failure time
+ instrument-specific break acoustics
+ ensemble recovery behavior
```

## Continuity after failure

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

## Composition engine requirements

The synthesis engine requires an ensemble role graph, performer-role assignments, standardized component condition state, instrument adapters, handoff rules, dropout recovery, phrase memory, rhythmic anchor, variation inheritance, repair and re-entry, and room/proximity modeling.

A phrase must be represented as something several performers partially know and can preserve, not as a permanent clip owned by one track.

## Cultural lineage model

Subcultures are modeled as linked nodes rather than flat tags. Nodes may represent regional traditions, instruments, techniques, rhythmic patterns, cadences, production methods, historical influences, and community functions.

Edges may include originated_from, influenced_by, shares_instrument_with, shares_cadence_with, adapted_technique_from, regional_variant_of, merged_with, reacted_against, and commercialized_as.

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

```text
instrumental emotional navigation first
-> context-sensitive transition learning
-> cultural performance modeling
-> controlled mood-direction testing
-> later lyrical interpretation
```

Traditional holiday music may be treated as a separately labeled exception. General lyrical interpretation remains deferred.

## Personalization boundary

StegDJ combines cultural-performance structure with the active user's voluntary choices, replay, completion, skip, stop, familiarity tolerance, novelty tolerance, transition acceptance, session intent, and contextual emotional direction.

```text
familiar enough to be emotionally credible
novel enough to be personally meaningful
different enough to remain an original composition
```

No identifiable protected melody, lyric, hook, chorus line, arrangement, or artist voice may be reproduced without the required rights.

## Sensory fidelity benchmark

The engineering objective is perceptual deception of the senses during a controlled blind evaluation.

```text
blind sensory exposure
-> independent judgment
-> forced human-or-StegDJ classification
-> provenance disclosure
-> method and evidence inspection
```

Qualified musicians familiar with the selected tradition evaluate instrument realism, ensemble interaction, role circulation, handoff credibility, historical plausibility, timing variation, failure and recovery, room interaction, cultural authenticity, emotional credibility, and mechanical-generation artifacts.

A successful result approaches chance-level origin classification while maintaining high cultural-authenticity ratings.

> I would not have believed it if I had not heard it for myself.

## Governed event model

Candidate event types include cultural_profile_selected, ensemble_circle_created, performer_role_assigned, instrument_handoff_started, instrument_handoff_completed, role_substitution_started, instrument_condition_changed, string_failure_occurred, ensemble_recovery_started, repair_started, repair_completed, instrument_reentry_started, instrument_reentry_completed, cultural_fidelity_evaluated, blind_origin_classification_recorded, and provenance_disclosed.

Each event preserves observations, derived interpretation, confidence, uncertainty, profile scope, evidence references, and authority=`none` for Site fixtures.

## Authority boundaries

```text
cultural profile != cultural ownership
instrument sample != authentic performance
shared string schema != identical instrument behavior
historical influence != unrestricted reproduction right
blind sensory test != permission to misrepresent provenance after disclosure
perceptual indistinguishability != factual identity
simulated failure != historical event evidence
Site fixture != production activation
```

## Internal testing gate

The slice is not internally complete until testers can select a cultural profile; inspect performers, roles, instruments, adapters, and component condition; hear role circulation; observe stochastic failure; hear ensemble compensation; observe repair and imperfect re-entry; compare human and StegDJ examples blindly; inspect provenance after classification; and verify profile and rights boundaries.

## Destination

Primary destination: `StegVerse-Labs/Site` for public mirror, browser fixture, validation, and evidence presentation.

Later production destinations include the StegDJ composition engine, rights-resolution service, Master Records custody, blind-test evaluation service, and internal patent packet.
