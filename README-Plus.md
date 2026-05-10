# Receipt-Backed Automation v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this implements

- Adds `receipt_backing_verifier_v1`.
- Promotes only:
  - T13 from 4/5 Tested to 5/5 Receipt-backed when receipt binding verifies.
  - T14 from 4/5 Tested to 5/5 Receipt-backed when reconstruction verifies.
- Adds generated files:
  - data/receipt-backing-verifier.json
  - data/automation-release-state.json
- Adds page sections:
  - Automation Release State
  - Receipt-Backed Verification
- Does not promote T1–T12, T15, or T16 to 5/5.

## Expected next workflow run

After upload, run:

```text
Actions → Transition Experimental Engine → Run workflow
```

Expected result:

```text
No new transition experiment runs.
T13 advances to 5/5 Receipt-backed.
T14 advances to 5/5 Receipt-backed.
Automation release state becomes receipt_backed_automation_ready if all release gates are satisfied.
```
