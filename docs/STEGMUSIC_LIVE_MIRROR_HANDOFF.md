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

Active branch:

```text
feature/stegmusic-browser-self-test
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
AudioContext reports active browser execution
composition progress advances
playback_started appears in the canonical browser event stream
pause returns control to the user
pass/fail diagnostic event is retained in the governed stream
```

A passing self-test confirms browser runtime execution only. It deliberately records `audible_output_confirmed=false`; a human target-device observation is still required to establish that sound was actually heard.

## Claim boundary

A passing live-route receipt establishes only that the public Site served the expected files and markers.

```text
public file presence != browser audio execution
HTTP 200 != audible output
script publication != AudioContext running
browser self-test PASS != audible output confirmed
browser-generated audio != commercial catalog
prototype rights label != license grant
live mirror receipt != custody
live mirror receipt != activation authority
live mirror receipt != royalty settlement
```

The receipt therefore keeps these claims false:

```text
browser_audio_execution_verified=false until a runtime self-test event exists
human_audibility_verified=false
catalog_license_verified=false
custody_verified_by_this_check=false
activation_authority_granted=false
```

## Remaining active obligation

```text
1. Complete repository validation for the browser-self-test branch.
2. Merge the self-test into main and observe the next Pages deployment.
3. Run the self-test on iPhone Safari and retain its governed diagnostic event.
4. Test audible Play, Adaptive next, generated composition, and local-file playback on iPhone Safari.
5. Record whether AudioContext starts, remains running, pauses, resumes, and survives screen-state changes.
6. Fix any target-device failure without weakening user-gesture, rights, privacy, or authority boundaries.
7. Add automated browser execution where Web Audio behavior can be meaningfully observed without claiming human audibility.
```

## Session status

```text
DO NOT ARCHIVE
```

The live route gate is installed, but browser runtime and target-device audibility obligations remain open.
