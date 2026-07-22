# StegMusic Live Trigger Handoff

## Goal

Ensure every StegMusic change merged to `main` automatically produces a post-deployment public-route receipt that includes the iPhone-safe generated media transport.

## Branch

```text
agent/stegmusic-live-trigger
```

## Changes

```text
.github/workflows/stegmusic-live-verification.yml
scripts/check_stegmusic_live_routes.py
docs/STEGMUSIC_LIVE_TRIGGER_HANDOFF.md
```

The workflow now runs on relevant pushes to `main`, remains manually dispatchable, and still follows successful `Site Task Runner` executions.

The live verifier now requires publication of:

```text
assets/ecosystem-music-diagnostics.js
assets/ecosystem-music-media-transport.js
```

It verifies publication markers for offline rendering, WAV encoding, HTML media playback events, Media Session handling, explicit human audibility confirmation, and screen-lock continuity confirmation.

## Claim boundary

A passing live receipt confirms publication only. It does not establish audible output, iPhone Safari compatibility, screen-lock continuity, catalog licensing, custody, activation authority, or royalty settlement.

## Remaining obligation

```text
1. Validate and merge this trigger repair.
2. Observe the push-to-main live verification run.
3. Retain the live publication receipt.
4. Perform direct iPhone Safari playback and continuity confirmation.
```

## Session status

```text
DO NOT ARCHIVE
```
