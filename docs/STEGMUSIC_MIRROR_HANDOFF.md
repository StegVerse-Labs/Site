# StegMusic / StegDJ Mirror Handoff

## Source of truth

This file is the current implementation handoff for the Site-hosted StegMusic / StegDJ service prototype.

## Current goal

```text
Goal: playable governed music service inside the Ecosystem Node that supports immediate listening, visible rights posture, preference refinement, synchronized governed projections, persistent session records, contribution-value inspection, adaptive StegDJ selection, and later lawful catalog/provider integration.
Primary surface: ecosystem-music.html
Runtime: assets/ecosystem-music.js + assets/ecosystem-music-adaptive.js
Issue: StegVerse-Labs/Site#39
Authority: construction and fixture testing only
```

## Implemented playable slice

```text
partial Ecosystem Chat-style music window
direct launcher from ecosystem-chat.html
local catalog search
three locally generated StegDJ tracks
normal play/pause/stop/previous/next, adaptive-next, and volume controls
visible browser-audio startup, running, pause, and refusal status
session progress display
four-phase INTRO / BUILD / LIFT / RESOLVE generated composition form
session-intent selection
energy, brightness, bass-texture, and exploration controls
fine-grained feedback controls and free-text refinement
persistent browser-local trait model
intent-aware deterministic candidate scoring
adaptive next-track recommendation and selection
visible ranked candidate and learned-target inspection
adaptive-model reset control
always-visible playback, audio, composition, preference, projection, and royalty indicators
Conversation / Governed music play / Split / Raw JSONL tabs
stable event selection and cross-pane correlation highlighting
visible rights and source posture
local persistence of governed session events and prototype contribution estimate
expandable contribution-value panel
captured-versus-derived event inspection
bounded downstream projection inspection
downstream projection permission toggles
future-reuse revocation control
browser-local reset control
persistent named listening profile
JSON session export including profile and permission state
explicit fixture, authority, rights, privacy, and financial boundaries
```

## Adaptive model boundary

The adaptive model is stored under `stegmusic.trait-model.v1` in browser-local storage. It updates from explicit controls, session intent, and listener refinements. It ranks only the local StegDJ fixture catalog using energy, brightness, bass texture, and exploration distance.

```text
browser-local learned target != aggregate ecosystem rule
ranked candidate != autonomous authority
adaptive selection != proof of preference correctness
local model != cross-user training dataset
model reset != deletion of historical governed events
```

Aggregate reuse remains disabled unless separately authorized through the existing projection controls.

## Rights/source classes

```text
stegdj_generated_local_prototype: implemented and playable
public_domain_verified: planned
user_owned_or_purchased: planned
connected_licensed_provider: planned
bundled_catalog_entitlement: planned
authorized_per_track_source: planned
```

No commercial catalog license, streaming entitlement, royalty payment, or composition right is asserted by the prototype.

## Governed projections

Every search, selection, playback start, playback refusal, pause, stop, preference refinement, profile save, permission change, and revocation emits a local canonical-style event. Adaptive selection currently produces the ordinary music-selection event through the main runtime and preserves its separate local scoring model for inspection.

## Verification status

```text
static playable-slice verifier: IMPLEMENTED
adaptive-model verifier: IMPLEMENTED
canonical Site application validation binding: IMPLEMENTED FOR BOTH MUSIC CHECKS
Ecosystem Chat service launcher: IMPLEMENTED
browser audio failure visibility: IMPLEMENTED
structured composition phases: IMPLEMENTED
session intent and volume controls: IMPLEMENTED
persistent trait model: IMPLEMENTED
adaptive next-track scoring: IMPLEMENTED
browser audio execution: NOT YET OBSERVED IN DEPLOYED PREVIEW
iPhone/Safari audio execution: NOT YET OBSERVED
browser interaction tests: NOT YET IMPLEMENTED
accessibility tests: NOT YET IMPLEMENTED
invited tester isolation: NOT YET VERIFIED
```

## Next executable steps

Destination `StegVerse-Labs/Site`:

```text
observe canonical application validation in CI
add browser interaction tests for adaptive selection, playback success and refusal, tabs, correlation, inspection, permissions, profile save, reset, revocation, and export
add accessibility tests
add invited-tester profile-isolation tests
add a deployed preview link and confirm iPhone/Safari audio behavior
remove any duplicate or ambiguous control identifiers found by browser tests
```

Destination lawful source integration:

```text
add one verified public-domain audio source with durable license evidence
add user-owned/purchased local-file playback without uploading the source file
add one connected licensed provider path
resolve exact recording, territory, entitlement, quality, and user cost before playback
retain source and rights receipts without claiming ownership of source audio
```

Destination `StegDJ`:

```text
move adaptive selection into the canonical governed event runtime
add transition scoring between current and candidate tracks
make session intent alter composition structure as well as selection target
separate user-private learning from aggregate reusable rules
add rights-aware composition inputs and output licensing classes
expand generated compositions beyond one 64-step form
```

Adjacent destinations remain the financial contract, ecosystem invariants, Master Records/orchestration, Publisher, admissibility wiki, Guardian wiki, and internal patent packet.

## Internal-test viability

The prototype is internally usable when deployed through the Site branch preview and browser audio is permitted. Invited testing additionally requires profile isolation, clear fixture labeling, export and reset/revocation controls, no cross-user raw-history exposure, visible failures, rights evidence for every non-generated source, and confidentiality/contribution terms for patent-sensitive testing.

## Authority boundary

```text
browser-generated audio != commercial catalog
prototype rights label != license grant
local session persistence != Master Records custody
candidate contribution != realized value
prototype estimate != payable balance
fixture event != activation evidence
StegDJ generation != unrestricted composition right
permission toggle != universal consent
revocation record != deletion of historical occurrence
structured browser composition != production music generator
adaptive ranking != autonomous execution authority
```

## Archive readiness

This handoff, Site issue #39, `ecosystem-music.html`, both music runtime files, both music validation scripts, the canonical Site application validator, and repository history preserve the current music-service continuation state without requiring the originating conversation.