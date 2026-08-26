# iPhone Heartbeat Transition Projection Mirror Handoff

Updated: `2026-08-26T14:53:00-05:00`

## Current classification

```text
goal_id: SITE-IPHONE-HB30-TRANSITION-PROJECTION-001
repository: StegVerse-Labs/Site
historical_goal_state: COMPLETE_RELEASED
current_protocol_role: HISTORICAL_PRE_HB32_TRANSITION_EVIDENCE_ONLY
current_heartbeat_activation_role: NONE
credential_authority: TV/TVC
github_token_runtime_authority: NONE
authority_effect: NONE
```

The HB29→HB30 iPhone capsule was a valid historical portability/materialization surface for the pre-HB32 transition lineage. It is **not** a current heartbeat activation requirement and must not be used to imply that protocol progression depends on iPhone execution, WorkerCoordinator observation, repository mutation, or receipt materialization.

## Canonical current heartbeat

Current heartbeat semantics are owned by `StegVerse-Labs/.github/docs/HEARTBEAT_CARRIER_SIGNAL_MIRROR_HANDOFF.md` and the HB32 protocol anchor.

```text
anchor_epoch: HB32
anchor_time_utc: 2026-08-23T19:00:00.000Z
period_ms: 10
reference_rate_hz: 100
progression_dependency: OSCILLATOR_ONLY
continuous_reference_stream: true
new_reference_every_10ms: true
continuous_process_required: false
resident_sampler_required_for_progression: false
observation_is_causal: false
LIVE-009: COMPLETED / INDEPENDENT_HEARTBEAT_LIVE_PROOF_VERIFIED
```

Every 10 ms of elapsed oscillator phase corresponds to a new canonical heartbeat reference whether or not an iPhone, worker, workflow, or sampler observes it.

## Historical released Site surfaces

```text
heartbeat-transition/index.html
heartbeat-transition/heartbeat-transition.js
scripts/check_iphone_heartbeat_transition_projection.py
Site PR #368
merge: 37c8ac81b8b00e22310b8f03687f4b9f42581d31
```

These surfaces remain preserved as historical evidence and compatibility tooling. Historical HB29/HB30 artifacts must not be rewritten merely because current protocol authority moved to HB32.

## Historical validation evidence

```text
Site Bootstrap Validate: 32054685239 SUCCESS
IPHONE_HB30_PROJECTION_PASS
SESSION_WORK_CLAIMS_PASS
SITE_HANDOFF_ORCHESTRATION_PASS
ECOSYSTEM_HEARTBEAT_ORCHESTRATION_PASS
ECOSYSTEM_CHAT_APPLICATION_PASS
ST-017 sandbox PASS
Site Handoff Orchestrator: 32054685374 SUCCESS
Ecosystem Heartbeat Orchestration: 32054685170 SUCCESS
```

This evidence validates the historical source projection only. It is not current HB32 runtime/protocol activation proof.

## Current public-surface requirement

`heartbeat-transition/index.html` must identify itself as a historical HB29→HB30 capsule and direct readers to the current HB32 continuous-carrier semantics. Generating the historical portable receipt must never be described as the next required step for current heartbeat continuity.

## Authority and collision boundary

```text
iPhone historical receipt != protocol heartbeat progression
iPhone execution != heartbeat activation
WorkerCoordinator observation != heartbeat progression
HB29/HB30 historical materialization != current HB32 authority
protocol heartbeat reference != execution authority
```

No manual iPhone action is required for current heartbeat continuity. Any separate iPhone/StegOS/StegFin workflow remains governed by its own canonical handoff.

## Archive posture

The original HB29→HB30 projection goal is complete and historical. This handoff remains only to prevent stale pre-HB32 instructions from being interpreted as current activation requirements.
