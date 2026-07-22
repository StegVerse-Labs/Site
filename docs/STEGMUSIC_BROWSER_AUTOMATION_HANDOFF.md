# StegMusic Browser Automation Handoff

## Goal

Provide repeatable browser-execution evidence for the current Site-hosted StegMusic / StegDJ implementation without converting headless runtime behavior into a human audibility claim.

## Installed construction

```text
tests/test_stegmusic_browser.py
.github/workflows/stegmusic-browser-execution.yml
scripts/check_stegmusic_browser_automation_contract.py
assets/ecosystem-music-profile-scope.js
scripts/check_stegmusic_adaptive_model.py
scripts/check_ecosystem_chat_application.py
```

The Playwright test serves the actual Site locally, loads `ecosystem-music.html` in Chromium, and exercises Play, generated composition progress, Adaptive next, governed decision emission, and Pause. It parses complete JSONL events and retains stage excerpts, console output, and page errors.

It writes:

```text
reports/stegmusic-browser-execution.json
```

## Defects closed during construction

```text
opaque browser wait failures replaced with staged evidence
Python syntax failures compile-gated
missing/null adaptive model storage fail-safe initialized per isolated profile
left-truncated event excerpts no longer used for event-type assertions
stale PR rebuilt on current main without discarding newer transition-learning work
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

The receipt retains `audible_output_confirmed=false`, `catalog_license_verified=false`, `custody_verified_by_this_check=false`, and `activation_authority_granted=false`.

## Remaining obligation

```text
1. Obtain successful Site and browser workflow receipts on the current-main branch.
2. Merge only after both pass.
3. Observe the main-branch browser execution receipt.
4. Separately retain iPhone Safari self-test and human audibility evidence.
```

## Session status

```text
DO NOT ARCHIVE
```
