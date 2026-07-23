# StegMusic String Component Standard

## Purpose

Every tensioned musical string or string-like linear performance element uses one canonical attribute model. Instrument-specific adapters may add technique and construction detail, but they may not rename or redefine the shared physical fields.

```text
one string standard
+ instrument adapter
+ performer/tool interaction
= instrument-specific behavior
```

## Canonical scope

The standard applies across plucked, bowed, struck, resonant, sympathetic, experimental, and repair/test contexts, including guitar, banjo, mandolin, fiddle, violin, cello, bass, harp, piano, hammered dulcimer, sitar, zither, bow-hair bundles, mechanical string drivers, test-rig strings, and repair-jig tension lines.

A bow-hair bundle or tool-mounted tension line is not asserted to be acoustically identical to an instrument string. It uses the same physical vocabulary where the attributes are meaningful.

## Shared attribute groups

```text
identity
construction
geometry
mechanical state
tuning state
attachment
environment
usage and excitation
condition and damage
acoustics
failure
repair and re-entry
```

Required examples include material, core, winding, coating, speaking length, diameter, linear density, current and breaking tension, tuning drift, anchor types, temperature, humidity, age, cycles, attack rate, excitation force, bow pressure, wear, fatigue, notch severity, fray, damping, inharmonicity, failure hazard, break transient, repair method, retension, and re-entry stability.

## Instrument adapters

Instrument adapters define how a performer or tool excites the shared component.

```text
plucked adapter: pick/finger position, release angle, displacement
bowed adapter: bow pressure, speed, contact point, rosin/friction state
struck adapter: hammer mass, velocity, hardness, strike point
sympathetic adapter: coupling path and excitation transfer
repair adapter: tension release, splice/replacement, retension sequence
```

Adapters may extend the model. They cannot substitute a genre label for physical state or assign fixed failure sounds independent of the component state.

## Failure model

Failure probability is derived from the common state:

```text
tension-to-breaking-load ratio
+ excitation intensity and rate
+ wear, fatigue, notch, fray, flattening
+ environment and corrosion
= bounded stochastic failure hazard
```

The hazard may become predictable while the exact occurrence remains uncertain. Failure is not locked to a bar, measure, beat, or dramatic phrase point.

The break transient may contain pitch instability, rupture impulse, loose-segment motion, instrument-body contact, missing subsequent attack, and sympathetic response. The instrument adapter determines how those shared components are rendered for the specific instrument.

## Repair continuity

Repair is part of the same component state. A replacement or temporary repair must change later tuning stability, tension, timbre, and re-entry confidence rather than restoring a perfect pre-failure state instantly.

## Boundaries

```text
shared schema != identical sound
instrument adapter != cultural authenticity
failure simulation != historical occurrence evidence
standardized attributes != certified engineering measurements
Site runtime != production synthesis activation
```

Primary machine-readable record: `data/stegmusic/string-component-standard.v1.json`

Prototype runtime: `assets/stegmusic-string-physics.js`
