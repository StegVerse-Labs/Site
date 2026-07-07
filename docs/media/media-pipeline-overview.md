# Media Pipeline Overview

status: publishable-draft
manual_actions_required: false
source_repo: StegVerse-Labs/collective-environment-engine
site_repo: StegVerse-Labs/Site
current_goal: Site-publication-mirror

## Purpose

The media pipeline converts a user-selected mood channel into governed media planning receipts. At this stage, it proves deterministic planning and replay across connector-visible media repositories. It does not activate cameras, microphones, external platforms, or live broadcast transport.

## Connector-Visible Pipeline

1. `mood-channel-selector` receives the channel intent.
2. `media-governance` decides whether the request is admissible.
3. `media-runtime` records device-facing readiness metadata without raw media transfer.
4. `music-engine` emits a composition plan.
5. `video-engine` emits a visual plan.

`broadcast-engine` is the pending downstream stage and remains inactive until connector visibility exists.

## Canonical Request

The canonical request fixture remains in the source repository:

- `examples/media-pipeline-integration/media_request.example.json`

It includes request identity, manual action boundary, source repository, channel mood, style, intensity, visibility, consent flags, and requested output flags.

## Stage Map

The deterministic stage map remains in the source repository:

- `examples/media-pipeline-integration/stage_map.json`

It defines execution order and identifies the pending broadcast stage.

## Receipt Bundle

The source integration runner emits:

- `artifacts/media-pipeline-integration/receipt_bundle.json`

The bundle includes request hash, stage-map hash, ordered stage receipts, chained receipt hashes, final hash, pending stages, and pipeline state.

## Replay Verification

Replay is verified in the source repository by:

- `tools/check_media_pipeline_replay.py`

The replay checker recomputes request hash, stage-map hash, each receipt hash, and final hash. Any mismatch fails validation.

## Current Boundary

This Site page is a mirror of the governed planning and replay surface. It is not a live media platform. It does not claim live camera use, live microphone use, external platform streaming, public broadcast, live provider execution, or platform connector capability.

## Next Integration Candidate

The next integration candidate is Site validation wiring for this mirrored page, followed by downstream summaries to Publisher, admissibility-wiki, and stegguardian-wiki after Site validation passes.
