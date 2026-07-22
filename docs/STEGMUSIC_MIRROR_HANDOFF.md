# StegMusic / StegDJ Mirror Handoff

## Source of truth

This file is the current implementation handoff for the Site-hosted StegMusic / StegDJ service prototype.

## Current goal

```text
Goal: playable governed music service inside the Ecosystem Node that supports immediate listening, visible rights posture, preference refinement, synchronized governed projections, persistent session records, contribution-value inspection, adaptive StegDJ selection, transition-outcome learning, user-owned local playback, isolated invited-tester profiles, and later licensed catalog/provider integration.
Primary surface: ecosystem-music.html
Runtime: assets/ecosystem-music-profile-scope.js + assets/ecosystem-music.js + assets/ecosystem-music-adaptive.js + assets/ecosystem-music-local-source.js + assets/ecosystem-music-diagnostics.js
Issue: StegVerse-Labs/Site#39
Authority: construction and fixture testing only
```

## Implemented playable slice

```text
partial Ecosystem Chat-style music window and direct service launcher
three locally generated StegDJ tracks with INTRO / BUILD / LIFT / RESOLVE form
normal playback, adaptive-next, volume, progress, and local-file controls
session intent plus energy, brightness, bass-texture, and exploration controls
quick and free-text preference refinement
browser-local trait model and deterministic candidate scoring
preference fit, transition fit, repeat penalty, and learned outcome adjustment
canonical adaptive_selection_decision event
profile-scoped transition outcomes: accepted, skipped, replayed, completed
canonical transition_outcome_recorded event
user-owned or purchased local audio without upload
rights assertion, refusal, object-URL creation, and object-URL revocation
Conversation / Governed music play / Split / Raw JSONL projections
stable event correlation and captured-versus-derived inspection
projection permissions, future-reuse revocation, reset, and JSON export
prototype contribution-value inspection with non-payable boundary
browser-local isolated profile namespaces for separate testers
browser audio self-test and explicit non-audibility claim
accessibility labels, landmarks, live regions, tab roles, and keyboard-focusable records
```

## Profile isolation boundary

`assets/ecosystem-music-profile-scope.js` loads before every music runtime and namespaces StegMusic browser storage under the active profile ID.

```text
active profile pointer: stegmusic.active-profile.v1
profile registry: stegmusic.profile-registry.v1
scoped runtime key: stegmusic.profile.<profile_id>.<original_stegmusic_key>
```

This separates each tester's local events, prototype value, permissions, display profile, adaptive model, and transition model in the same browser.

```text
browser-local namespace isolation != authenticated account isolation
separate local profile != server-side tenant boundary
profile ID != verified identity
cross-profile read is disabled through the profile-scope runtime
```

## Adaptive and transition-learning boundary

The adaptive trait model is stored under `stegmusic.trait-model.v1`. Transition outcomes are stored under `stegmusic.transition-model.v1`. Both keys are automatically scoped to the active isolated profile.

The ranking combines:

```text
preference distance
transition distance
repeat penalty
bounded prior-outcome adjustment
```

The listener may rate the most recent Adaptive next transition as:

```text
accepted
skipped
replayed
completed
```

Each rating emits `transition_outcome_recorded` before the persistent pair statistics alter later ranking. A skip records the poor fit before requesting another adaptive candidate. Replay records the outcome before replaying the selected generated track.

```text
explicit transition outcome != verified preference truth
learned pair adjustment != autonomous execution authority
profile-local model != aggregate ecosystem rule
transition score != guaranteed transition quality
model reset != deletion of historical governed events
```

## Rights/source classes

```text
stegdj_generated_local_prototype: implemented and playable
user_owned_or_purchased_local: implemented and playable in browser session
public_domain_verified: planned
connected_licensed_provider: planned
bundled_catalog_entitlement: planned
authorized_per_track_source: planned
```

The local-source path uses `URL.createObjectURL`; source bytes are not uploaded, copied into repository storage, entered into Master Records, or persisted by the Site. The authorization checkbox is a governed assertion and is not independent evidence of ownership.

No commercial catalog license, streaming entitlement, royalty payment, public-distribution right, or unrestricted composition right is asserted.

## Governed event coverage

```text
music_selection
playback_started / playback_paused / playback_stopped / playback_refused
preference_refinement
adaptive_selection_decision / adaptive_model_reset
transition_outcome_recorded
local_source_loaded / local_source_refused / local_source_cleared
local_playback_started / local_playback_paused / local_playback_completed / local_playback_refused
profile_saved
projection_permissions_changed
future_reuse_revoked
audio_self_test_passed / audio_self_test_failed
```

Local-source records retain metadata and rights assertions but prohibit source-audio upload, retention, external training, and public distribution.

## Verification status

```text
Site Bootstrap Validate for profile isolation PR #46: PASS
static playable-slice verifier: IMPLEMENTED AND ENFORCES UNIQUE DOM IDS
adaptive-model verifier: IMPLEMENTED FOR DECISIONS, TRANSITION SCORING, AND OUTCOME LEARNING
browser self-test contract: IMPLEMENTED
live verification contract: IMPLEMENTED
profile-isolation and accessibility verifier: IMPLEMENTED
canonical Site application validation binding: IMPLEMENTED
Ecosystem Chat service launcher: IMPLEMENTED
browser-local profile namespaces: IMPLEMENTED
profile-scoped transition learning: IMPLEMENTED
browser audio execution: NOT YET OBSERVED IN DEPLOYED PREVIEW
iPhone/Safari audible output: NOT YET OBSERVED
full browser interaction automation: NOT YET IMPLEMENTED
same-device tester isolation: IMPLEMENTED BUT NOT YET BROWSER-OBSERVED
authenticated multi-user isolation: NOT IMPLEMENTED
verified public-domain source: NOT IMPLEMENTED
connected licensed provider: NOT IMPLEMENTED
```

## Next executable steps

Destination `StegVerse-Labs/Site`:

```text
validate transition-learning branch in CI
merge after green validation
observe deployed music route and browser self-test
confirm generated audio and local-file playback on iPhone/Safari
confirm isolated profile switching and no cross-profile history display
confirm transition acceptance, skip, replay, and completion affect only the active profile
add automated browser interaction coverage
record target-device evidence without converting browser observations into authority
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
learn from automatic playback completion and explicit skip timing
separate user-private learning from aggregate reusable rules
add rights-aware composition inputs and output licensing classes
expand generated compositions beyond one 64-step form
sequence generated and lawfully sourced tracks without treating protected audio as training ownership
```

Adjacent destinations remain the ecosystem session contract, financial contract, invariants, Master Records/orchestration, Publisher, admissibility wiki, Guardian wiki, and internal patent packet.

## Internal-test viability

After deployment and target-browser confirmation, the prototype supports controlled testing of generated music, adaptive selection, explicit transition learning, trait refinement, governed records, contribution-candidate display, local authorized audio, and separate same-device tester profiles.

Invited testing additionally requires:

```text
clear fixture and rights-assertion labeling
one distinct isolated profile ID per tester
export and reset/revocation controls
no cross-profile raw-history exposure
visible failures
rights evidence for every non-generated shared source
confidentiality and contribution terms for patent-sensitive testing
target-device browser evidence
```

Production viability still requires authenticated identity, server-side tenant isolation, durable custody boundaries, lawful catalog access, provider entitlement resolution, and non-prototype financial accounting.

## Authority boundary

```text
browser-generated audio != commercial catalog
user authorization assertion != independent proof of ownership
local object URL != uploaded or retained source artifact
browser-local profile namespace != authenticated tenant isolation
candidate contribution != realized value
prototype estimate != payable balance
fixture event != activation evidence
StegDJ generation != unrestricted composition right
adaptive ranking != autonomous execution authority
transition outcome != verified listener truth
browser self-test != audible-output confirmation
```

## Archive readiness

This handoff, Site issue #39, the music surface, music runtimes, validators, and repository history preserve the current continuation state. Deployment and target-device observations remain unresolved obligations.
