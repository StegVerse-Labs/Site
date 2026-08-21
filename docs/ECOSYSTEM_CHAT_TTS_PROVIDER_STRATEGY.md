# Ecosystem Chat TTS Provider Strategy

## Status

```text
decision: ADOPT_PROVIDER_ABSTRACTION_FOR_TTS
initial_external_candidate: ElevenLabs
hard_dependency: false
production_authority: none
governance_authority: StegVerse
review_state: retained_for_future_scaling_review
```

## Decision

ElevenLabs TTS is worth integrating into StegVerse/Ecosystem Chat as a near-term voice-rendering provider and scaling benchmark, but it must not become production authority or a hard architectural dependency.

The purpose of the integration is to shorten the path from text Ecosystem Chat to a genuinely conversational interface while preserving StegVerse control over governance, admissibility, continuity, execution, and evidence.

## Authority boundary

The voice provider sits after StegVerse has already determined what response is admissible:

```text
user speech
-> speech-to-text
-> governed conversational state
-> reasoning/model
-> admissibility decision
-> approved response text
-> TTS provider
-> audio stream
```

The TTS provider may render admitted text into audio. It does not determine:

- whether a response is admissible;
- whether an action may execute;
- conversational continuity;
- policy standing;
- governance state;
- custody or reconstruction state;
- publication, release, or activation authority.

Provider output is rendering, not authority.

## Provider-neutral interface

Implement TTS behind a StegVerse-owned provider abstraction rather than binding Ecosystem Chat directly to ElevenLabs.

Conceptual shape:

```text
StegVoiceProvider
|- ElevenLabsAdapter
|- LocalTTSAdapter
`- additional provider adapters when justified
```

Conceptual contract:

```text
render(text, voice_profile, locale, session_receipt) -> audio_stream
```

The actual implementation may refine this contract, but provider substitution must not change governance semantics or authority boundaries.

## Scaling strategy

1. Integrate a mature external TTS provider rather than delaying conversational UX while recreating commodity voice infrastructure.
2. Capture measured latency, speech quality, cost, privacy posture, reliability, concurrency behavior, and failure behavior.
3. Treat those measurements as benchmark targets for sovereign/local TTS development.
4. Develop and validate local voice capability against the observed benchmark.
5. Shift traffic toward local/sovereign voice when economics, privacy, reliability, availability, or governance justify the transition.
6. Retain external providers only as replaceable adapters or bounded fallback paths where useful.

## Scaling review triggers

Reevaluate provider allocation when any of the following becomes material:

- TTS expenditure;
- concurrency limits;
- provider latency;
- provider outages or dependency risk;
- retention/privacy requirements;
- sovereign/local TTS quality parity;
- sovereign/local TTS cost advantage;
- jurisdictional or contractual constraints.

## Evidence to retain

A production-quality evaluation should retain enough provider-neutral evidence to compare implementations over time:

```text
provider_id
provider_model_or_engine
request_id / transition_id
input_character_or_token_count
output_audio_duration
first_audio_latency_ms
total_generation_latency_ms
success_or_failure
fallback_used
measured_usage
measured_cost_or_cost_basis
privacy_or_retention_profile_ref
quality_test_profile_ref
```

No field in this telemetry grants execution or governance authority.

## Local-sovereign convergence goal

ElevenLabs should function as an accelerator and reference implementation, not the destination architecture.

The long-term goal is a provider-neutral voice layer in which StegVerse can choose among external and sovereign/local renderers using measured capability and cost while keeping the governed conversational state and all authority inside StegVerse.

## Core principle

> Exploit mature third-party voice capability where it reduces implementation burden, while keeping governance, continuity, admissibility, execution, and authority entirely within StegVerse.

## Future review

This document intentionally records the architectural decision before implementation so future work can distinguish:

```text
decision documented != adapter implemented
adapter implemented != live provider validated
live provider validated != sovereign replacement complete
provider availability != authority
```

Before implementation or expansion, read the current `docs/SITE_MIRROR_HANDOFF.md`, Ecosystem Chat handoffs, orchestration state, and heartbeat state to avoid conflicting with active work ownership.
