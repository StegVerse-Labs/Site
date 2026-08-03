# StegMusic / StegDJ Mirror Handoff

## Source of truth

This file is the current implementation handoff for the Site-hosted StegMusic / StegDJ service prototype.

## Current goal

```text
Goal: playable governed music service inside the Ecosystem Node that supports immediate listening, visible rights posture, preference refinement, synchronized governed projections, persistent session records, contribution-value inspection, adaptive StegDJ selection, transition-outcome learning, user-owned local playback, isolated invited-tester profiles, explicit machine-readable style profiles, and later licensed catalog/provider integration.
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

## Style-profile continuation transferred from PR #78

PR #78 contains a stale, non-mergeable implementation of a governed style-characteristic registry and a profile-driven EDM renderer. Its unique requirements are preserved here and in `data/tasks/SITE-STEGMUSIC-STYLE-PROFILES.json`; the old branch is not the canonical implementation lane.

Required capability:

```text
natural-language preferences resolve into explicit, inspectable style characteristics
genre labels remain descriptive references rather than render authority
EDM with bass drops and high energy resolves into tempo, energy, bass weight, drop prominence, danceability, percussion density, brightness, tension/release, and arrangement requirements
active style profile governs composition structure, not only UI sliders
EDM profile renders at least 32 bars with at least two materially distinct drops
pre-drop sections withhold or reduce bass and kick energy
release sections introduce sub-bass, impact transients, increased rhythmic density, and sustained post-drop energy
second release is structurally larger than the first
render receipt records profile ID, characteristic contract, required events, total bars, drop count, compression, normalization, no-upload status, and human-audibility boundary
```

Canonical owner and claim:

```text
task: data/tasks/SITE-STEGMUSIC-STYLE-PROFILES.json
owner: repository-native implementation and validation lane
claim state: CLAIMED_FOR_IMPLEMENTATION
collision boundary: do not revive or extend PR #78 directly; port requirements onto current main in a fresh implementation branch
release condition: current-main PR passes static, browser, hosted, and live-route validation and is merged
```

## Security floor

Applicable United States federal cybersecurity requirements are a minimum floor, not a completion target. StegMusic and adjacent StegVerse services must exceed the applicable baseline through measurable controls and retained evidence.

Required security characteristics include:

```text
defense in depth and least privilege
explicit separation of user intent, render authority, publication authority, and execution authority
cryptographic provenance for build, validation, deployment, and retained receipts
tamper-evident event and evidence chains
fail-closed behavior when rights, identity, entitlement, custody, or validation evidence is unavailable
secure software supply-chain controls and dependency review
reproducible or independently verifiable build outputs where practical
no upload or retention of user-owned source audio unless separately authorized
profile isolation and prevention of cross-profile raw-history disclosure
bounded retention, revocation, supersession, and deletion semantics
continuous validation and machine-observable release conditions
```

A statement that the system exceeds a federal baseline is prohibited until the applicable control mapping, implementation evidence, validation results, and independent assessment are retained.

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
ST-018 governed validation-evidence workflow: IMPLEMENTED AND MACHINE-OWNED
style-characteristic registry on current main: NOT IMPLEMENTED
profile-driven EDM two-drop renderer on current main: NOT IMPLEMENTED
browser audio execution: REPOSITORY EVIDENCE EXISTS; HUMAN AUDIBILITY REMAINS SEPARATE
iPhone/Safari audible output: NOT YET OBSERVED
same-device tester isolation: IMPLEMENTED BUT NOT YET BROWSER-OBSERVED
authenticated multi-user isolation: NOT IMPLEMENTED
verified public-domain source: NOT IMPLEMENTED
connected licensed provider: NOT IMPLEMENTED
```

## Next executable steps

Destination `StegVerse-Labs/Site`:

```text
execute data/tasks/SITE-STEGMUSIC-STYLE-PROFILES.json on a fresh branch from current main
port only the governed characteristic registry, resolver, current-runtime integration, and tests required by the task
preserve existing ST-018 validation-evidence ownership and avoid modifying its canonical files unless the task requires a validator binding
run static and browser interaction validation
merge only after hosted workflows pass and artifacts are inspected
observe deployed music route after merge
confirm generated audio and local-file playback on iPhone/Safari
confirm isolated profile switching and no cross-profile history display
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
style-profile resolution != aesthetic quality proof
federal-baseline mapping != proof the system exceeds the baseline
```

## Session consolidation

```text
MERGED INTO: StegVerse-Labs/Site/docs/STEGMUSIC_MIRROR_HANDOFF.md and data/tasks/SITE-STEGMUSIC-STYLE-PROFILES.json
Transferred: explicit EDM style characteristics, two-drop structure, profile-governed rendering, render receipts, no-upload and audibility boundaries, and federal-security-floor requirement.
Superseded lane: PR #78 and branch agent/stegmusic-style-runtime-v3.
Canonical continuation owner: repository-native task SITE-STEGMUSIC-STYLE-PROFILES.
Unique chat dependency remaining after merge of this handoff PR: false.
```

## Archive readiness

This handoff, Site issue #39, the ST-018 evidence task, the style-profile task, the music surface, music runtimes, validators, and repository history preserve the current continuation state. The implementation and target-device obligations remain repository-owned and do not require this originating chat after this handoff change is merged.
