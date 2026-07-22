# StegMusic / StegDJ Mirror Handoff

## Source of truth

This file is the current implementation handoff for the Site-hosted StegMusic / StegDJ service prototype.

## Current goal

```text
Goal: playable governed music service inside the Ecosystem Node supporting immediate listening, visible rights posture, preference refinement, synchronized governed projections, contribution-value inspection, adaptive selection, transition-outcome learning, intent-shaped composition, user-owned local playback, isolated invited-tester profiles, and later licensed catalog/provider integration.
Primary surface: ecosystem-music.html
Runtime: assets/ecosystem-music-profile-scope.js + assets/ecosystem-music.js + assets/ecosystem-music-adaptive.js + assets/ecosystem-music-local-source.js + assets/ecosystem-music-diagnostics.js + assets/ecosystem-music-intent-composition.js
Issue: StegVerse-Labs/Site#39
Authority: construction and fixture testing only
```

## Implemented playable slice

```text
partial Ecosystem Chat-style music window and direct launcher
three locally generated StegDJ tracks
normal playback, adaptive-next, volume, progress, and local-file controls
INTRO / BUILD / LIFT / RESOLVE generated form
session-intent controls that now alter selection targets and phase-specific composition structure
energy, brightness, bass-texture, and exploration controls
quick and free-text preference refinement
browser-local trait model and deterministic ranking
preference fit, transition fit, repeat penalty, and learned outcome adjustment
canonical adaptive_selection_decision event
profile-scoped accepted / skipped / replayed / completed transition outcomes
canonical transition_outcome_recorded event
user-owned or purchased local audio without upload
rights assertion, refusal, object-URL creation, and revocation
Conversation / Governed music play / Split / Raw JSONL projections
stable event correlation and captured-versus-derived inspection
projection permissions, future-reuse revocation, reset, and JSON export
prototype contribution-value inspection with non-payable boundary
browser-local isolated profile namespaces
browser audio self-test with explicit non-audibility claim
accessibility labels, landmarks, live regions, tab roles, and keyboard-focusable records
```

## Profile isolation boundary

All StegMusic storage keys are namespaced under the active browser-local profile:

```text
stegmusic.profile.<profile_id>.<original_stegmusic_key>
```

This separates each tester's events, permissions, prototype value, display profile, adaptive model, and transition model.

```text
browser-local namespace isolation != authenticated account isolation
profile ID != verified identity
cross-profile read is disabled through the profile-scope runtime
```

## Adaptive, transition, and intent-composition boundary

Adaptive ranking combines preference distance, transition distance, repeat penalty, and bounded prior-outcome adjustment. Transition outcomes are explicit listener evidence and not verified preference truth.

`assets/ecosystem-music-intent-composition.js` adds phase-specific structural profiles:

```text
fine_tune -> BALANCED LAB
stay_alert -> ALERTNESS ARC
focus -> FOCUS PLATEAU
settle -> DESCENDING SETTLE
explore -> BOUNDARY EXPLORATION
```

Each profile changes energy, brightness, bass texture, and exploration differently during INTRO, BUILD, LIFT, and RESOLVE. The underlying generated-audio runtime reads those live controls, so session intent now changes the produced phase structure rather than only the recommendation target.

Each newly applied phase profile emits `composition_intent_profile_applied` with the session intent, composition phase, base controls, applied controls, profile label, active profile scope, and authority=`none`.

```text
intent-shaped structure != proof of therapeutic effect
phase modulation != production composition engine
profile-local learning != aggregate ecosystem rule
adaptive ranking != autonomous execution authority
transition outcome != verified listener truth
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

Local source bytes are not uploaded, entered into Master Records, or retained by the Site. User authorization is a governed assertion, not independent proof of ownership.

No commercial catalog license, streaming entitlement, royalty payment, public-distribution right, or unrestricted composition right is asserted.

## Governed event coverage

```text
music_selection
playback_started / playback_paused / playback_stopped / playback_refused
preference_refinement
adaptive_selection_decision / adaptive_model_reset
transition_outcome_recorded
composition_intent_profile_applied
local_source_loaded / local_source_refused / local_source_cleared
local_playback_started / local_playback_paused / local_playback_completed / local_playback_refused
profile_saved
projection_permissions_changed
future_reuse_revoked
audio_self_test_passed / audio_self_test_failed
```

## Verification status

```text
Site Bootstrap Validate for transition-learning PR #47: PASS
transition-learning PR #47: MERGED
static playable-slice verifier: IMPLEMENTED
adaptive-model verifier: IMPLEMENTED
intent-composition verifier: IMPLEMENTED
browser self-test contract: IMPLEMENTED
live verification contract: IMPLEMENTED
profile-isolation and accessibility verifier: IMPLEMENTED
canonical Site application validation binding: IMPLEMENTED
browser audio execution in deployed preview: NOT YET OBSERVED
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
validate intent-composition branch in CI
merge after green validation
observe deployed music route and browser self-test
confirm generated audio and local-file playback on iPhone/Safari
confirm isolated profile switching and no cross-profile history display
confirm intent forms audibly differ across session intents
confirm transition outcomes affect only the active profile
add automated browser interaction coverage
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
learn from automatic playback completion and explicit skip timing
separate user-private learning from aggregate reusable rules
add rights-aware composition inputs and output licensing classes
expand generated compositions beyond one 64-step form
sequence generated and lawfully sourced tracks without treating protected audio as training ownership
```

Adjacent destinations remain the ecosystem session contract, financial contract, invariants, Master Records/orchestration, Publisher, admissibility wiki, Guardian wiki, and internal patent packet.

## Internal-test viability

After deployment and target-browser confirmation, the prototype supports controlled testing of generated music, adaptive selection, transition learning, intent-shaped phase structure, governed records, contribution-candidate display, local authorized audio, and separate same-device tester profiles.

Invited testing additionally requires clear fixture and rights labeling, one isolated profile ID per tester, no cross-profile raw-history exposure, visible failures, target-device evidence, and confidentiality/contribution terms for patent-sensitive testing.

Production viability still requires authenticated identity, server-side tenant isolation, durable custody, lawful catalog access, provider entitlement resolution, and non-prototype financial accounting.

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
intent-shaped composition != medical or therapeutic claim
browser self-test != audible-output confirmation
```

## Archive readiness

This handoff, Site issue #39, the music surface, music runtimes, validators, and repository history preserve the current continuation state. Deployment and target-device observations remain unresolved obligations.
