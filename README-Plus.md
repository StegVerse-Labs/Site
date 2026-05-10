# Ledger Display + Automation Release Verifier v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this combines

This bundle includes both:

1. The experimental ledger display fix.
2. The next automation test: `automation_release_verifier_v1`.

## Generated files

```text
data/experimental-ledger-summary.json
data/automation-release-verifier.json
```

## What the verifier checks

The verifier checks that each automation release mode is backed by the required evidence level:

```text
manual_single: T1–T4 >= 4
sequence_mode: T5 >= 4
bounded_batch: T7 >= 4
coupled_batch: T9–T12 >= 4
receipt_governed: T13–T14 >= 5
irreversibility_guarded: T15 >= 4
self_modification_guarded: T16 >= 4
```

## Expected next workflow run

After upload, run:

```text
Actions → Transition Experimental Engine → Run workflow
```

Expected result:

```text
No new transition experiment runs.
T13 and T14 remain 5/5 Receipt-backed.
Experimental ledger summary updates newest-first.
Automation-release verifier writes ALLOW if all modes satisfy their release evidence gates.
```
