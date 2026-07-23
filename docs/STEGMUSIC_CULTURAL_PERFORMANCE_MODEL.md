# StegMusic Cultural Performance Model

## Purpose

StegDJ must learn historically grounded instrumental traditions as living social performance systems, not as flat genre labels or sample collections.

The first scoped implementation domain is lyrics-free Appalachian circle performance. Broader genre competence should be derived from deeply modeled subcultures, instruments, tools, techniques, histories, social structures, and recovery patterns.

## Core principle

```text
learn culture deeply enough to understand the sound
rather than learning the sound superficially and assigning it a culture
```

A generated performance is not culturally credible merely because it contains a banjo, fiddle, mandolin, guitar, dulcimer, horn, reed, drum, percussion sample, or modal melody. Credibility depends on how performers share, transfer, preserve, repair, and recover the tune through the physical capabilities and limitations of their instruments and tools.

## Appalachian circle model

The canonical performance unit is a family or neighborhood circle in which several participants of different ages and skill levels sustain one tune together.

The model includes shared tune memory, rotating performers, instrument handoff, role handoff, skill and age variation, instrument wear and repair, continuous performance through interruption, leader mobility, and collective recovery.

The tune belongs to the circle rather than to one permanent lead performer.

## Role separation

```text
musical role != instrument != performer
```

A performer may move among melody, rhythm, drone, counterline, percussive emphasis, rest, repair, and re-entry. A role may transfer among strings, horns, winds, reeds, percussion, electroacoustic instruments, and available tools without resetting the tune.

## Ensemble state

Each simulated circle maintains participants, age and experience profiles, available instruments and tools, component condition, role assignments, shared phrase familiarity, rhythmic anchor, current leader, handoff readiness, repair state, calibration state, and re-entry confidence.

Differences in skill should create coherent variation rather than random error.

## Universal instrument and tool dependency

All instrument classes and performance tools use:

```text
docs/STEGMUSIC_INSTRUMENT_COMPONENT_STANDARD.md
data/stegmusic/instrument-component-standard.v1.json
assets/stegmusic-instrument-physics.js
```

Strings remain a specialized canonical family through:

```text
data/stegmusic/string-component-standard.v1.json
assets/stegmusic-string-physics.js
```

The shared model covers tensioned strings, horns and air columns, reeds, lip-reed interfaces, membranes, bars, plates, bells, cymbals, resonators, electroacoustic components, bows, picks, hammers, mallets, beaters, brushes, pedals, mutes, repair tools, and test fixtures.

```text
shared component state
+ class-specific excitation adapter
+ resonator and coupling model
+ performer or tool interaction
= instrument-specific behavior
```

The standard does not make components acoustically identical. It standardizes physical state, wear, damage, excitation, environment, failure, repair, recalibration, and re-entry across classes.

## Failure and continuity

Examples include string rupture, reed split, pad leak, valve sticking, slide misalignment, loss of lip oscillation, membrane tear, lug shift, cymbal crack growth, mallet-head separation, bow-hair loss, electrical intermittence, clipping, and thermal protection.

The failure sequence is:

```text
component failure mid-gesture
-> intended sound fractures, changes, or disappears
-> performer adapts or drops out
-> nearby roles widen
-> rhythm and tune identity continue
-> another performer absorbs part of the missing function
-> repair, substitution, or recalibration occurs
-> affected instrument or tool re-enters imperfectly
```

The tune proves itself by continuing through disruption.

```text
continuity is demonstrated by successful role recovery,
not by pretending disruption never occurred
```

## Composition engine requirements

The engine requires an ensemble role graph, performer-role assignments, standardized component state, class-specific excitation adapters, resonator and coupling state, handoff rules, dropout recovery, phrase memory, rhythmic anchor, variation inheritance, repair, recalibration, re-entry, and room/proximity modeling.

A phrase must be represented as something several performers partially know and can preserve, not as a permanent clip owned by one track.

## Cultural lineage model

Subcultures are linked nodes rather than flat tags. Nodes may represent regional traditions, instruments, tools, techniques, rhythmic patterns, cadences, production methods, historical influences, and community functions.

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

Each domain must produce instrument, tool, technique, rhythm, cadence, form, production, lineage, uncertainty, and permitted-synthesis records.

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

Qualified musicians evaluate instrument realism, ensemble interaction, role circulation, handoff credibility, historical plausibility, timing variation, failure and recovery behavior, room interaction, cultural authenticity, emotional credibility, and mechanical-generation artifacts.

A successful result approaches chance-level origin classification while maintaining high cultural-authenticity ratings.

> I would not have believed it if I had not heard it for myself.

## Governed event model

Candidate event types include cultural_profile_selected, ensemble_circle_created, performer_role_assigned, instrument_handoff_started, instrument_handoff_completed, role_substitution_started, instrument_component_state_changed, instrument_condition_changed, component_failure_occurred, string_failure_occurred, ensemble_recovery_started, repair_started, repair_completed, recalibration_started, recalibration_completed, instrument_reentry_started, instrument_reentry_completed, cultural_fidelity_evaluated, blind_origin_classification_recorded, and provenance_disclosed.

Each event preserves observations, derived interpretation, confidence, uncertainty, profile scope, evidence references, and authority=`none` for Site fixtures.

## Authority boundaries

```text
cultural profile != cultural ownership
instrument sample != authentic performance
component realism != cultural authenticity
historical influence != unrestricted reproduction right
blind sensory test != permission to misrepresent provenance after disclosure
perceptual indistinguishability != factual identity
simulated failure != historical event evidence
Site fixture != production activation
```

## Internal testing gate

The slice is not internally complete until testers can select a cultural profile; inspect performers, roles, instruments, tools, adapters, and component condition; hear role circulation; observe stochastic failure; hear ensemble compensation; observe repair, recalibration, and imperfect re-entry; compare human and StegDJ examples blindly; inspect provenance after classification; and verify profile and rights boundaries.

## Destination

Primary destination: `StegVerse-Labs/Site` for public mirror, browser fixture, validation, and evidence presentation.

Later production destinations include the StegDJ composition engine, rights-resolution service, Master Records custody, blind-test evaluation service, and internal patent packet.
