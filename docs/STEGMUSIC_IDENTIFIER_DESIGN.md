# StegMusic Governed Audio Identifier

## Purpose

Provide Shazam-like recognition inside StegMusic while keeping recognition, provenance, rights, and execution authority as separate determinations.

## User flow

```text
Tap Identify
→ choose microphone capture or local file
→ capture a short bounded sample
→ derive a local acoustic fingerprint
→ search permitted fingerprint indexes
→ return ranked candidates with confidence and timing offset
→ show source and rights posture separately
→ allow user actions only when separately authorized
```

## Identification pipeline

```text
Audio sample
→ mono normalization
→ windowed spectral analysis
→ local peak extraction
→ landmark pairs: frequency_a, frequency_b, delta_time
→ fingerprint hashes
→ candidate lookup
→ offset-consistency scoring
→ confidence classification
```

The raw microphone or file sample should not be retained by default. The normal record is the bounded fingerprint, sample duration, capture source, processing version, candidate references, confidence result, and user-approved retention posture.

## Result classes

```text
MATCH_CONFIRMED
MATCH_PROBABLE
MATCH_AMBIGUOUS
NO_MATCH
INSUFFICIENT_AUDIO
INDEX_UNAVAILABLE
CAPTURE_REFUSED
```

A recognition result is not a rights decision.

```text
identified=true != ownership_verified
identified=true != playback_license_granted
identified=true != training_permission
identified=true != royalty_entitlement
identified=true != publication_authority
```

## Candidate result

```json
{
  "candidate_id": "catalog-or-provider-reference",
  "title": "Candidate title",
  "artist": "Candidate artist",
  "confidence": 0.94,
  "matched_landmarks": 183,
  "offset_consistency": 0.91,
  "sample_offset_seconds": 42.3,
  "source_index": "provider-or-local-index",
  "rights_status": "unknown_or_separately_resolved"
}
```

## Governed events

```text
music_identification_requested
music_capture_started
music_capture_completed
music_fingerprint_derived
music_identification_candidate_found
music_identification_confirmed
music_identification_ambiguous
music_identification_no_match
music_identification_retention_changed
music_identification_reuse_revoked
```

## Capture boundaries

Microphone capture must be user initiated and visibly active. The UI must show capture duration, stop control, retention posture, and whether processing is local or provider-backed.

Default posture:

```text
raw_audio_retained=false
fingerprint_retained=false until user confirms
cross_service_reuse=false
external_training=false
publication_authority=false
royalty_state=not_realized
```

## Index architecture

StegMusic can support multiple indexes without collapsing them into one imposed catalog:

```text
1. StegDJ-generated artifact index
2. user-owned local library index
3. licensed provider fingerprint index
4. public-domain / openly licensed index
5. organization-governed private index
```

Each candidate must preserve its source index and evidence path. Conflicting matches remain visible rather than being silently collapsed.

## StegVerse-specific advantage

The identifier can recognize more than a commercial song. It can also identify:

```text
StegDJ-generated compositions
prior versions and derivations
licensed stems
user-contributed recordings
sound effects and environmental recordings
governed publication artifacts
```

That allows identification to feed continuity and attribution records while still refusing to infer ownership or payment rights from resemblance alone.

## Initial implementation stages

```text
Stage 1 — local file fingerprinting against StegDJ-generated tracks
Stage 2 — microphone capture and bounded local fingerprint derivation
Stage 3 — provider adapter contract for licensed external indexes
Stage 4 — multi-index candidate reconciliation
Stage 5 — continuity, attribution, and governed contribution linkage
```

## Authority boundary

The Site surface may demonstrate capture, fingerprint derivation, candidate ranking, and governed receipts. It must not claim external catalog coverage, ownership verification, licensing, custody, royalty settlement, or activation authority unless those are independently provided and evidenced.

## Status

```text
DESIGN_READY
IMPLEMENTATION_PENDING
DO NOT ARCHIVE
```
