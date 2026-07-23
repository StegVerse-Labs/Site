# StegMusic Instrument and Tool Component Standard

## Purpose

StegDJ must use one shared physical-state vocabulary across all musical instrument and performance-tool classes. Strings, air columns, reeds, lips, membranes, bars, plates, shells, resonators, valves, keys, beaters, bows, mallets, pickups, microphones, mechanical drivers, repair fixtures, and test rigs are modeled as physical components with class-specific adapters.

```text
shared component state
+ excitation adapter
+ resonator and coupling model
+ performer or tool interaction
= class-specific sound and behavior
```

A class adapter may extend the common schema. It may not replace measurable component state with a genre label, fixed sample, or assumed cultural identity.

## Canonical component groups

Every component record uses the following groups wherever meaningful:

```text
identity
component_class
construction
geometry
material_state
mechanical_state
acoustic_state
attachment_and_coupling
environment
usage_and_excitation
condition_and_damage
control_surface_state
failure
repair
recalibration
re-entry
```

Fields that do not apply remain explicitly not-applicable rather than being silently omitted or redefined.

## Component classes

### Tensioned linear components

Strings, sympathetic strings, bow-hair bundles, wires, tension lines, and related test or repair components.

Primary state includes length, diameter, linear density, tension, breaking load, winding, coating, wear, fatigue, tuning drift, anchor state, and rupture behavior.

Canonical dependency: `data/stegmusic/string-component-standard.v1.json`.

### Aerophones and air-path components

Flutes, whistles, recorders, organ pipes, brass tubing, woodwind bores, ducts, bells, mouthpieces, leadpipes, tone holes, vents, slides, valves, pads, and wind-machine tools.

Primary state includes:

```text
air-column effective length
bore profile
cross-sectional area
openings and vent state
pressure and flow
jet or lip coupling
impedance
leakage
condensation
wall and edge condition
resonance modes
radiation geometry
```

### Reed components

Single reeds, double reeds, free reeds, cane, synthetic reeds, reed plates, tongues, ligatures, staples, and reed-adjustment tools.

Primary state includes stiffness, thickness profile, curvature, opening, moisture, fatigue, edge damage, clamping, response threshold, beating state, and instability.

### Lip-reed interfaces

Brass instruments and related mouthpiece systems use the player's lips as an active oscillator coupled to the mouthpiece, air column, valves or slide, and bell.

Primary state includes lip tension, aperture, contact, pressure, airflow, embouchure stability, mouthpiece geometry, valve or slide state, and acoustic loading.

### Membranophones

Drumheads, frame-drum skins, synthetic membranes, resonant heads, snares, tensioning systems, pedals, beaters, and membrane test fixtures.

Primary state includes membrane material, thickness, radius, tension map, anisotropy, humidity, temperature, edge seating, lug distribution, impact location, beater state, damping, fatigue, denting, tearing, and delamination.

### Idiophones

Bars, plates, bells, cymbals, gongs, triangles, claves, shakers, rattles, lamellae, tongues, and struck or shaken tools.

Primary state includes geometry, alloy or material, stiffness, mass distribution, suspension, strike point, striker hardness, residual stress, cracks, deformation, damping, and modal response.

### Chordophone assemblies

Stringed instruments are assemblies of canonical strings, bridges, nuts, frets, soundboards, bodies, resonant cavities, tailpieces, pickups, and controls. The assembly does not duplicate string state; it references shared string components.

### Electroacoustic and electronic components

Pickups, microphones, transducers, preamps, amplifiers, filters, oscillators, speakers, exciters, controllers, cables, pedals, and digital or analog synthesis tools.

Primary state includes transfer function, gain, noise, nonlinearity, clipping, latency, phase, bandwidth, impedance, control position, thermal state, drift, damage, and calibration.

### Excitation and maintenance tools

Bows, picks, fingers, hammers, mallets, beaters, brushes, sticks, pedals, breath controllers, mutes, slides, valve tools, tuning devices, repair jigs, gauges, and mechanical drivers.

Tools have their own condition and geometry. A worn pick, softened mallet, damaged pad tool, warped bow, or uneven drum key changes the interaction rather than merely selecting a sound preset.

## Shared interaction model

Every audible event must preserve:

```text
source component state
excitation source and gesture
contact or coupling conditions
resonator response
room or radiation path
resulting transient and sustained behavior
```

The same performer gesture applied to different component states must not produce an identical result.

## Failure and degradation

Failure is class-specific but governed by one pattern:

```text
baseline material and construction limits
+ accumulated use and fatigue
+ current excitation load
+ environment
+ existing defects
= bounded stochastic degradation or failure hazard
```

Examples include:

```text
string rupture
reed split or collapse
pad leak
valve sticking
slide friction or misalignment
lip oscillation loss
membrane tear
lug or hoop shift
cymbal crack growth
bar fracture
mallet-head separation
bow-hair loss
pickup or cable intermittence
amplifier clipping or thermal protection
```

The hazard can be increasingly predictable while exact occurrence remains uncertain. It must not be locked to a bar line, scripted dramatic point, or fixed sample trigger.

## Continuity after component change

A component event must propagate into the performance:

```text
component degrades or fails
-> intended sound changes or disappears
-> performer and ensemble detect or compensate
-> role, technique, pressure, fingering, voicing, or instrumentation changes
-> repair, replacement, recalibration, or substitution occurs
-> component re-enters with believable residual instability
```

Perfect reset is prohibited unless a governed replacement and calibration event supports it.

## Cultural boundary

Physical accuracy is necessary but not sufficient for cultural authenticity.

```text
component realism != performance tradition
instrument class != genre
historical construction != historical identity
adapter availability != lawful sample or model rights
Site fixture != production synthesis activation
```

The cultural-performance model determines how physical capabilities are used within a tradition. The component standard determines how instruments and tools physically behave.

## Canonical machine records

- `data/stegmusic/instrument-component-standard.v1.json`
- `data/stegmusic/string-component-standard.v1.json`

## Prototype runtime

- `assets/stegmusic-instrument-physics.js`
- `assets/stegmusic-string-physics.js`

## Validation

- `scripts/check_stegmusic_instrument_component_standard.py`
- `scripts/check_stegmusic_string_component_standard.py`
