# StegMusic Browser Automation Handoff

## Goal

Provide repeatable browser-execution evidence for the Site-hosted StegMusic / StegDJ prototype without converting headless runtime behavior into a human audibility claim.

## Installed construction

```text
tests/test_stegmusic_browser.py
.github/workflows/stegmusic-browser-execution.yml
scripts/check_stegmusic_browser_automation_contract.py
```

The Playwright test serves the actual Site locally, loads `ecosystem-music.html` in Chromium, and exercises:

```text
Play
AudioContext running marker
composition progress advance
playback_started governed event
Adaptive next
adaptive_selection_decision governed event
Pause
playback_paused governed event
```

It writes:

```text
reports/stegmusic-browser-execution.json
```

## Claim boundary

```text
headless AudioContext execution != human-confirmed audible output
browser test PASS != iPhone Safari PASS
browser test receipt != custody
browser test receipt != activation authority
browser test receipt != catalog license
browser test receipt != royalty settlement
```

The receipt therefore retains:

```text
audible_output_confirmed=false
catalog_license_verified=false
custody_verified_by_this_check=false
activation_authority_granted=false
```

## Remaining obligation

```text
1. Observe the pull-request Playwright run and retain its artifact.
2. Repair any actual browser-runtime failure.
3. Merge only after Site validation and browser execution both pass.
4. Observe the main-branch execution receipt.
5. Separately retain iPhone Safari self-test and human audibility evidence.
```

## Session status

```text
DO NOT ARCHIVE
```
