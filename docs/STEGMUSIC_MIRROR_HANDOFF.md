# StegMusic / StegDJ Mirror Handoff

## Source of truth

This file is the current implementation handoff for the Site-hosted StegMusic / StegDJ service prototype.

## Current goal

```text
Goal: playable governed music service inside the Ecosystem Node that supports immediate listening, visible rights posture, preference refinement, synchronized governed projections, persistent session records, contribution-value inspection, and later lawful catalog/provider integration.
Primary surface: ecosystem-music.html
Runtime: assets/ecosystem-music.js
Issue: StegVerse-Labs/Site#39
Authority: construction and fixture testing only
```

## Implemented playable slice

```text
partial Ecosystem Chat-style music window
local catalog search
three locally generated StegDJ tracks
normal play/pause/stop/previous/next controls
session progress display
energy, brightness, bass-texture, and exploration controls
fine-grained feedback controls and free-text refinement
always-visible playback, preference, projection, and royalty indicators
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

Every search, selection, playback, pause, stop, preference refinement, profile save, permission change, and revocation emits a local canonical-style event containing:

```text
event identity and parent relationship
service and medium
profile-bound actor projection
human projection
governed projection
rights/source status
captured records
derived records
permitted and prohibited reuse
downstream service projection
contribution eligibility
royalty state
reuse-revocation state
policy, artifact, and continuity references
preview-only hash and authority boundary
```

## Clarifications implemented

### Captured versus derived records

Captured records are direct observations such as the selected track, search query, playback action, position, explicit feedback, profile name, permission selection, and current trait controls.

Derived records are interpretations created from those observations, such as decreasing brightness, retaining bass texture, reducing transition distance, classifying an interaction as a candidate contribution, or recomputing a bounded projection scope.

The selected-event panel displays these records separately.

### Downstream projections

A downstream projection is a bounded record that another service may use without receiving the private raw listening history.

Current browser-local controls permit the listener to authorize or deny:

```text
selected preference refinements to StegDJ
aggregate reusable music rules
bounded alertness preference to a future Wellness service
```

Raw listening history is prohibited from cross-user reuse. Revocation disables future downstream projections but does not erase historical occurrence receipts already retained in the local session.

### Contribution and financial display

The expandable contribution-value panel shows candidate event count, a prototype estimate, realized royalty, payable status, and current listening profile. The prototype estimate is intentionally non-payable and cannot be represented as a balance, security, royalty statement, or entitlement.

## Verification status

```text
static playable-slice verifier: UPDATED FOR INSPECTION, PERMISSIONS, PROFILE, RESET, AND REVOCATION MARKERS
browser audio execution: NOT YET OBSERVED IN DEPLOYED PREVIEW
iPhone/Safari audio execution: NOT YET OBSERVED
browser interaction tests: NOT YET IMPLEMENTED
accessibility tests: NOT YET IMPLEMENTED
cross-pane correlation source implementation: IMPLEMENTED
captured-versus-derived inspection: IMPLEMENTED
downstream permission toggles: IMPLEMENTED
future reuse revocation: IMPLEMENTED
browser-local reset: IMPLEMENTED
named profile persistence: IMPLEMENTED
invited tester isolation: NOT YET VERIFIED
```

## Next executable steps

Destination `StegVerse-Labs/Site`:

```text
add a direct StegMusic service launcher inside ecosystem-chat.html
bind scripts/check_stegmusic_playable_slice.py into canonical application validation
observe the restored CI run
add browser interaction tests for playback, tabs, correlation, inspection, permissions, profile save, reset, revocation, and export
add accessibility tests
add invited-tester profile-isolation tests
add visible audio startup/failure status for iPhone autoplay and AudioContext restrictions
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
improve generated audio from fixed patterns to structured compositions
persist musical trait and sequence models
add transition scoring and next-track selection
add context-specific profiles and session intents
separate user-private learning from aggregate reusable rules
add rights-aware composition inputs and output licensing classes
```

Adjacent destinations:

```text
financial contract: contribution eligibility, direct/indirect derivation, pools, disputes, allocations
invariants: governed database participation and non-extractive reuse
master-records/orchestration: custody and reconstruction of interaction, derivation, reuse, and value lineage
GCAT-BCAT-Engine/Publisher: publication-safe service contracts and verified projections
StegVerse-Labs/admissibility-wiki: cross-service reuse admissibility
StegVerse-002/stegguardian-wiki: consent, revocation, protected identity, misuse escalation
patent packet: governed multimodal learning, rights-aware brokerage, adaptive sequencing, contribution-linked value, cross-service projections
```

## Internal-test viability

The prototype is internally usable when deployed through the Site branch preview and browser audio is permitted. Invited testing requires:

```text
profile isolation
clear fixture labeling
export and reset/revocation controls
no cross-user raw-history exposure
visible failures
rights evidence for every non-generated source
confidentiality and contribution terms for patent-sensitive testing
```

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
```

## Archive readiness

This handoff, Site issue #39, `ecosystem-music.html`, `assets/ecosystem-music.js`, `scripts/check_stegmusic_playable_slice.py`, and repository history preserve the current music-service continuation state without requiring the originating conversation.