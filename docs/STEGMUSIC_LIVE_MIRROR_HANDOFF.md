# StegMusic Live Mirror Handoff

## Source of truth

This file is the live-publication continuation record for the Site-hosted StegMusic / StegDJ surface.

## Current goal

```text
Goal: keep the playable StegDJ prototype published on the live Site, machine-verify every deployed music route and runtime, and separately retain browser/device audio evidence without converting publication into authority.
Primary page: ecosystem-music.html
Live base: https://stegverse-labs.github.io/Site
Implementation handoff: docs/STEGMUSIC_MIRROR_HANDOFF.md
Issue: StegVerse-Labs/Site#39
```

## Installed production gate

Merged commit:

```text
08faa2dd5fdfd6aaefb82715620dee644bdf5c6d
```

Installed files:

```text
.github/workflows/stegmusic-live-verification.yml
scripts/check_stegmusic_live_routes.py
scripts/check_stegmusic_live_verification_contract.py
scripts/check_ecosystem_chat_application.py
```

The post-deployment workflow runs after a successful `Site Task Runner` execution on `main`, retries through GitHub Pages propagation, and verifies:

```text
ecosystem-music.html
assets/ecosystem-music.js
assets/ecosystem-music-adaptive.js
assets/ecosystem-music-local-source.js
ecosystem-chat.html
```

It writes and uploads:

```text
reports/stegmusic-live-verification.json
```

## Verified construction evidence

```text
PR: StegVerse-Labs/Site#41
Site Bootstrap Validate run: 29890060625
Result: SUCCESS
ST-017 isolated validation: SUCCESS
Canonical application validation: SUCCESS
Merge: SUCCESS
```

## Browser self-test construction

Merged branch and PR:

```text
feature/stegmusic-browser-self-test
StegVerse-Labs/Site#42
```

Files:

```text
ecosystem-music.html
assets/ecosystem-music-diagnostics.js
scripts/check_stegmusic_browser_self_test.py
scripts/check_ecosystem_chat_application.py
docs/STEGMUSIC_LIVE_MIRROR_HANDOFF.md
```

The in-page `Run audio self-test` control performs one user-initiated generated-audio execution cycle and verifies that:

```text
browser audio transport reports active execution
composition progress advances
playback event appears in the canonical browser event stream
pause returns control to the user
pass/fail diagnostic event is retained in the governed stream
```

A passing self-test confirms browser runtime execution only. It deliberately records `audible_output_confirmed=false`; a human target-device observation is still required to establish that sound was actually heard.

## Automated browser execution

```text
PR: StegVerse-Labs/Site#49
Result: MERGED
```

The current-main browser execution workflow verifies Play, composition progress, Adaptive Next, governed decision emission, and Pause without claiming human audibility or iPhone compatibility.

## iPhone-safe generated media transport

Active branch and draft PR:

```text
branch: agent/stegmusic-iphone-media-transport
PR: StegVerse-Labs/Site#53
```

Files:

```text
assets/ecosystem-music-media-transport.js
assets/ecosystem-music-diagnostics.js
scripts/check_stegmusic_browser_self_test.py
docs/STEGMUSIC_LIVE_MIRROR_HANDOFF.md
```

The transport:

```text
renders each generated composition with OfflineAudioContext
encodes the result as a browser-local WAV Blob
plays the Blob through an HTML audio element
adds Media Session play, pause, stop, previous, and Adaptive Next controls
records visibilitychange, pagehide, pageshow, freeze, and resume events
adds direct human confirmation controls for audibility and screen-state continuity
never uploads rendered or user-owned source audio
```

Direct target-device confirmation controls:

```text
I hear audio
Adaptive Next worked
Continued while screen dimmed
Continued while screen locked
Resumed after returning
```

Only the human `I hear audio` action may create a record with `human_audibility_confirmed=true`. Automated tests and lifecycle observations retain that claim as false.

## Claim boundary

A passing live-route receipt establishes only that the public Site served the expected files and markers.

```text
public file presence != browser audio execution
HTTP 200 != audible output
script publication != AudioContext or HTML media playback
browser self-test PASS != audible output confirmed
headless media playback != iPhone Safari compatibility
lifecycle event != uninterrupted audible output
generated browser audio != commercial catalog
prototype rights label != license grant
live mirror receipt != custody
live mirror receipt != activation authority
live mirror receipt != royalty settlement
```

The receipt therefore keeps these claims false until their specific evidence exists:

```text
browser_audio_execution_verified=false until a runtime self-test event exists
human_audibility_verified=false until direct target-device confirmation
iphone_safari_compatibility_verified=false until target-device execution
screen_dim_continuity_verified=false until direct observation
screen_lock_continuity_verified=false until direct observation
catalog_license_verified=false
custody_verified_by_this_check=false
activation_authority_granted=false
```

## Remaining active obligation

```text
1. Complete repository and browser validation for PR #53.
2. Merge the generated media transport into main and observe the next Pages deployment.
3. Open the live page on iPhone Safari and tap Play once.
4. Confirm audible generated playback using the in-page I hear audio action.
5. Test Adaptive Next and record the direct confirmation.
6. Test local-file playback with a user-authorized device file.
7. Test dimmed-screen, locked-screen, and return-to-page continuity.
8. Retain the governed lifecycle and direct-observation events.
9. Fix any observed target-device failure without weakening user-gesture, rights, privacy, or authority boundaries.
```

## Session status

```text
DO NOT ARCHIVE
```

The durable media transport is under review, but live deployment and target-device audibility evidence remain open.
