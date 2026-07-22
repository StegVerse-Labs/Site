# StegMusic complexity, harmony, and loudness handoff

## Active objective

Increase perceived loudness on iPhone without clipping, and move generated compositions from a single melodic line into layered harmonic arrangements.

## Required implementation

- render through a dynamics compressor and output gain stage;
- normalize rendered PCM before WAV encoding;
- retain HTML audio output volume at unity while the player slider controls render loudness;
- add chord pads, harmonic bass motion, counter-melody, and complexity-sensitive percussion;
- retain browser-local rendering and all existing rights, audibility, and authority boundaries;
- emit governed render evidence describing normalization, compression, harmony, and complexity.

## User observation

The user directly reported that generated playback was audible but too quiet while both the iPhone hardware volume and the StegMusic player volume were at maximum.

## Completion condition

CI passes, the change is merged and deployed, and the user confirms improved loudness and richer harmonic complexity on iPhone.

## Session status

DO NOT ARCHIVE
