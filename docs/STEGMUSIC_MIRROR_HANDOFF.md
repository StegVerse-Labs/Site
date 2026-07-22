# StegMusic / StegDJ Mirror Handoff

## Source of truth

This file is the current implementation handoff for the Site-hosted StegMusic / StegDJ service prototype.

## Current goal

```text
Goal: playable governed music service inside the Ecosystem Node that supports immediate listening, visible rights posture, preference refinement, synchronized governed projections, persistent session records, contribution-value inspection, adaptive StegDJ selection, user-owned local playback, isolated invited-tester profiles, and later licensed catalog/provider integration.
Primary surface: ecosystem-music.html
Runtime: assets/ecosystem-music-profile-scope.js + assets/ecosystem-music.js + assets/ecosystem-music-adaptive.js + assets/ecosystem-music-local-source.js + assets/ecosystem-music-diagnostics.js
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
browser-local isolated profile namespaces for separate testers
JSON session export including profile and permission state
explicit fixture, authority, rights, privacy, source-retention, financial, and profile-isolation boundaries
unique DOM identifiers enforced by static validation
accessibility labels, landmarks, live regions, tab roles, and keyboard-focusable record panels
```

## Profile isolation boundary

`assets/ecosystem-music-profile-scope.js` loads before every music runtime and namespaces StegMusic browser storage under the active profile ID.

```text
active profile pointer: stegmusic.active-profile.v1
profile registry: stegmusic.profile-registry.v1
scoped runtime key: stegmusic.profile.<profile_id>.<original_stegmusic_key>
```

This separates each tester's local events, prototype value, permissions, display profile, and adaptive model in the same browser. Switching profile IDs reloads the page into the selected namespace.

```text
browser-local namespace isolation != authenticated account isolation
separate local profile != server-side tenant boundary
profile ID != verified identity
cross-profile read is disabled through the profile-scope runtime
profile registry metadata != listening-history disclosure
```

The isolation is sufficient for controlled same-device prototype testing when testers use distinct profile IDs. It is not sufficient for production multi-user service, shared-device adversarial isolation, or authenticated custody.

## Adaptive model boundary

The adaptive model updates from explicit controls, session intent, and listener refinements. It ranks only the local StegDJ generated catalog using preference distance, transition distance, and a repeat penalty.

```text
browser-local learned target != aggregate ecosystem rule
ranked candidate != autonomous authority
adaptive selection != proof of preference correctness
local model != cross-user training dataset
model reset != deletion of historical governed events
transition score != guaranteed transition quality
```

Every adaptive-next request emits `adaptive_selection_decision` before selection. The record includes current controls, intent, prior track, selected candidate, rejected candidate scores, preference fit, transition fit, repeat penalty, model version, and authority=`none`.

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

Generated and local-source events enter the same browser-local canonical projection runtime. Event types include:

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
audio_self_test_passed / audio_self_test_failed
```

Local-source records retain metadata and rights assertions but explicitly prohibit source-audio upload, retention, external training, and public distribution.

## Verification status

```text
static playable-slice verifier: IMPLEMENTED AND ENFORCES UNIQUE DOM IDS
adaptive-model verifier: IMPLEMENTED FOR GOVERNED DECISION AND TRANSITION SCORING
browser self-test contract: IMPLEMENTED
live verification contract: IMPLEMENTED
profile-isolation and accessibility verifier: IMPLEMENTED
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
browser-local profile namespaces: IMPLEMENTED
accessibility semantics contract: IMPLEMENTED
browser audio execution: NOT YET OBSERVED IN DEPLOYED PREVIEW
iPhone/Safari audio execution: NOT YET OBSERVED
full browser interaction automation: NOT YET IMPLEMENTED
invited tester same-device namespace isolation: IMPLEMENTED BUT NOT YET BROWSER-OBSERVED
authenticated multi-user isolation: NOT IMPLEMENTED
verified public-domain source: NOT YET IMPLEMENTED
connected licensed provider: NOT YET IMPLEMENTED
```

## Next executable steps

Destination `StegVerse-Labs/Site`:

```text
merge the green Site validation-phase repair
validate this profile-isolation branch in CI
add deployed browser interaction evidence for generated playback, local playback, adaptive decision, profile switching, tabs, correlation, inspection, permissions, reset, revocation, and export
confirm iPhone/Safari AudioContext and local-file behavior
verify VoiceOver labels and tab navigation on iPhone
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

The prototype is internally usable when deployed through the Site branch preview and browser audio is permitted. The user can test generated composition, adaptive selection, trait refinement, governed records, financial-candidate display, locally owned audio without uploading it, and separate browser-local tester profiles.

Invited testing additionally requires:

```text
clear fixture and user-assertion labeling
one distinct isolated profile ID per tester
export and reset/revocation controls
no cross-profile raw-history exposure
visible failures
rights evidence for every non-generated shared source
confidentiality and contribution terms for patent-sensitive testing
browser evidence on the target devices
```

Production viability still requires authenticated identity, server-side tenant isolation, durable custody boundaries, lawful sourced catalog access, provider entitlement resolution, and non-prototype financial accounting.

## Authority boundary

```text
browser-generated audio != commercial catalog
user authorization assertion != independent proof of ownership
local object URL != uploaded or retained source artifact
prototype rights label != license grant
local session persistence != Master Records custody
browser-local profile namespace != authenticated tenant isolation
candidate contribution != realized value
prototype estimate != payable balance
fixture event != activation evidence
StegDJ generation != unrestricted composition right
permission toggle != universal consent
revocation record != deletion of historical occurrence
structured browser composition != production music generator
adaptive ranking != autonomous execution authority
transition score != verified listener satisfaction
browser self-test != audible-output confirmation
```

## Archive readiness

This handoff, Site issue #39, `ecosystem-music.html`, all music runtime files, music validation scripts, the canonical Site application validator, and repository history preserve the current music-service continuation state without requiring the originating conversation. Deployment and target-device observations remain external obligations.
