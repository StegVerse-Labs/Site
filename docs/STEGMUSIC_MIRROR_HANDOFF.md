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

## Implemented first slice

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
visible rights and source posture
local persistence of governed session events and prototype contribution estimate
expandable contribution-value panel
JSON session export
explicit fixture, authority, rights, and financial boundaries
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

Every search, selection, playback, pause, stop, and preference refinement emits a local canonical-style event containing:

```text
event identity and parent relationship
service and medium
human projection
governed projection
rights/source status
captured records
derived records
permitted and prohibited reuse
downstream service projection
contribution eligibility
royalty state
policy, artifact, and continuity references
preview-only hash and authority boundary
```

## Clarifications resolved from the design session

### Captured versus derived records

Captured records are direct observations such as the selected track, search query, playback action, position, and explicit feedback.

Derived records are interpretations created from those observations, such as decreasing brightness, retaining bass texture, reducing transition distance, or classifying an interaction as a candidate contribution.

### Downstream projections

A downstream projection is a bounded record that another service may use without receiving the private raw listening history. The current prototype permits selected refinement events to project only to StegDJ and identifies broader aggregate reuse as requiring separate authorization.

### Contribution and financial display

The expandable contribution-value panel shows candidate event count, a prototype estimate, realized royalty, and payable status. The prototype estimate is intentionally non-payable and cannot be represented as a balance, security, royalty statement, or entitlement.

## Next executable steps

Destination `StegVerse-Labs/Site`:

```text
add a direct StegMusic service launcher inside ecosystem-chat.html
add static application validation for required StegMusic markers
add browser interaction and accessibility tests
add correlation highlighting across Conversation, Governed, and Split panes
add user-controlled clear/revoke/reset actions
add explicit captured-versus-derived inspection panel
add downstream projection permission toggles
add persistent named listening profiles
add invited-tester isolation tests
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
```

## Archive readiness

This handoff, Site issue #39, `ecosystem-music.html`, `assets/ecosystem-music.js`, and repository history preserve the current music-service continuation state without requiring the originating conversation.
