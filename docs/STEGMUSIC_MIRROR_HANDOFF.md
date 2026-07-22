# StegMusic / StegDJ Mirror Handoff

## Source of truth

This file is the current implementation handoff for the Site-hosted StegMusic / StegDJ service prototype.

## Current goal

```text
Goal: playable governed music service inside the Ecosystem Node that supports immediate listening, visible rights posture, preference refinement, synchronized governed projections, persistent session records, contribution-value inspection, adaptive StegDJ selection, user-owned local playback, and later licensed catalog/provider integration.
Primary surface: ecosystem-music.html
Runtime: assets/ecosystem-music.js + assets/ecosystem-music-adaptive.js + assets/ecosystem-music-local-source.js
Issue: StegVerse-Labs/Site#39
Authority: construction and fixture testing only
```

## Implemented playable slice

```text
partial Ecosystem Chat-style music window
direct launcher from ecosystem-chat.html
local generated catalog search
three locally generated StegDJ tracks
normal play/pause/stop/previous/next, adaptive-next, volume, and native local-file controls
visible browser-audio startup, running, pause, refusal, decode-failure, and local-source status
session progress display
four-phase INTRO / BUILD / LIFT / RESOLVE generated composition form
session-intent selection
energy, brightness, bass-texture, and exploration controls
fine-grained feedback controls and free-text refinement
persistent browser-local trait model
intent-aware deterministic candidate scoring
transition-aware adaptive next-track scoring
canonical adaptive-selection decision event
visible ranked candidate, preference fit, transition fit, and learned-target inspection
adaptive-model reset control
user-owned or purchased local audio selection without upload
required user playback-authorization affirmation
local object-URL creation and revocation
local load, play, pause, completion, refusal, and clear governed events
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
explicit fixture, authority, rights, privacy, source-retention, and financial boundaries
unique DOM identifiers enforced by static validation
```

## Adaptive model boundary

The adaptive model is stored under `stegmusic.trait-model.v1` in browser-local storage. It updates from explicit controls, session intent, and listener refinements. It ranks only the local StegDJ generated catalog using preference distance, transition distance, and a repeat penalty.

```text
browser-local learned target != aggregate ecosystem rule
ranked candidate != autonomous authority
adaptive selection != proof of preference correctness
local model != cross-user training dataset
model reset != deletion of historical governed events
transition score != guaranteed transition quality
```

Every adaptive-next request now emits `adaptive_selection_decision` before selection. The record includes current controls, intent, prior track, selected candidate, rejected candidate scores, preference fit, transition fit, repeat penalty, model version, and authority=`none`.

## Rights/source classes

```text
stegdj_generated_local_prototype: implemented and playable
user_owned_or_purchased_local: implemented and playable in browser session
public_domain_verified: planned
connected_licensed_provider: planned
bundled_catalog_entitlement: planned
authorized_per_track_source: planned
```

The local-source path uses `URL.createObjectURL`; source bytes are not uploaded, copied into repository storage, entered into Master Records, or persisted by the Site. Clearing the source or leaving the page revokes the object URL. The user authorization checkbox is a governed assertion and is not independent evidence of ownership.

No commercial catalog license, streaming entitlement, royalty payment, public-distribution right, or composition right is asserted by the prototype.

## Governed projections

Generated and local-source events enter the same browser-local canonical projection runtime. Event types now include:

```text
music_selection
playback_started / playback_paused / playback_stopped / playback_refused
preference_refinement
adaptive_selection_decision / adaptive_model_reset
local_source_loaded / local_source_refused / local_source_cleared
local_playback_started / local_playback_paused / local_playback_completed / local_playback_refused
profile_saved
projection_permissions_changed
future_reuse_revoked
```

Local-source records retain metadata and rights assertions but explicitly prohibit source-audio upload, retention, external training, and public distribution.

## Verification status

```text
static playable-slice verifier: IMPLEMENTED AND ENFORCES UNIQUE DOM IDS
adaptive-model verifier: IMPLEMENTED FOR GOVERNED DECISION AND TRANSITION SCORING
canonical Site application validation binding: IMPLEMENTED
Ecosystem Chat service launcher: IMPLEMENTED
browser audio failure visibility: IMPLEMENTED
structured composition phases: IMPLEMENTED
session intent and volume controls: IMPLEMENTED
persistent trait model: IMPLEMENTED
adaptive next-track scoring: IMPLEMENTED
transition scoring: IMPLEMENTED
canonical adaptive decision event: IMPLEMENTED
user-owned local-file path without upload: IMPLEMENTED
source object-URL revocation: IMPLEMENTED
browser audio execution: NOT YET OBSERVED IN DEPLOYED PREVIEW
iPhone/Safari audio execution: NOT YET OBSERVED
browser interaction tests: NOT YET IMPLEMENTED
accessibility tests: NOT YET IMPLEMENTED
invited tester isolation: NOT YET VERIFIED
verified public-domain source: NOT YET IMPLEMENTED
connected licensed provider: NOT YET IMPLEMENTED
```

## Next executable steps

Destination `StegVerse-Labs/Site`:

```text
observe canonical application validation in CI
add browser interaction tests for generated and local playback, adaptive decision, refusal, tabs, correlation, inspection, permissions, profile save, reset, revocation, and export
add accessibility tests
add invited-tester profile-isolation tests
add a deployed preview link and confirm iPhone/Safari AudioContext and local-file behavior
record browser evidence without converting fixture or local assertions into authority
```

Destination lawful source integration:

```text
add one verified public-domain audio source with durable license evidence
add one connected licensed provider path
resolve exact recording, territory, entitlement, quality, and user cost before playback
retain source and rights receipts without claiming ownership of source audio
keep ordinary playback cost comparable to the sourced service
```

Destination `StegDJ`:

```text
make session intent alter composition structure as well as selection target
learn from transition acceptance, skips, replays, and completion
separate user-private learning from aggregate reusable rules
add rights-aware composition inputs and output licensing classes
expand generated compositions beyond one 64-step form
add adaptive sequencing across generated and lawfully sourced tracks without treating protected source audio as training ownership
```

Adjacent destinations remain the financial contract, ecosystem invariants, Master Records/orchestration, Publisher, admissibility wiki, Guardian wiki, and internal patent packet.

## Internal-test viability

The prototype is internally usable when deployed through the Site branch preview and browser audio is permitted. The user can already test generated composition, adaptive selection, trait refinement, governed records, financial-candidate display, and locally owned audio without uploading it.

Invited testing additionally requires:

```text
profile isolation
clear fixture and user-assertion labeling
export and reset/revocation controls
no cross-user raw-history exposure
visible failures
rights evidence for every non-generated shared source
confidentiality and contribution terms for patent-sensitive testing
browser evidence on the target devices
```

## Authority boundary

```text
browser-generated audio != commercial catalog
user authorization assertion != independent proof of ownership
local object URL != uploaded or retained source artifact
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
transition score != verified listener satisfaction
```

## Archive readiness

This handoff, Site issue #39, `ecosystem-music.html`, all three music runtime files, both music validation scripts, the canonical Site application validator, and repository history preserve the current music-service continuation state without requiring the originating conversation.