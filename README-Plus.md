# Evidence-Gated Sequence + Rule Release + T6/T7 v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this implements

- Rule releases generated from tested transition elements.
- `data/transition-rule-releases.json`.
- Evidence-gated automation mode:
  - Before T5: `manual_single`
  - After T5: `sequence_lag_row`, max 2 steps
  - After T7: `bounded_batch`, max 3 steps
  - After T13/T14: `scheduled_ready`
- Proper lag-aware sandbox class after T5.
- T6 Decision-Lag experiment.
- T7 Actuation-Lag experiment.
- Applied rules recorded on each run manifest and receipt.
- Transition pages display released rules and applied rules.

## Expected next workflow run

Because T5 is already tested, the engine should enter:

```text
sequence_lag_row
```

Expected sequence:

```text
T6 decision_lag_sweep_v1
T7 actuation_lag_sweep_v1
```

The run stops after max 2 sequence steps.
