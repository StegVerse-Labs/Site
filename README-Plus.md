# T15 Irreversible Transition v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this implements

- Adds `T15` experiment: `irreversibility_sweep_v1`.
- Adds fallback experiment registration for `T15`.
- Adds irreversible transition receipts with:
  - pre_state
  - action
  - committed_state
  - reversal_budget
  - attempted_reversal_state
  - residual_delta
  - residual_norm
  - irreversible
  - point_of_no_return
  - pre_verdict
  - committed_verdict
  - attempted_reversal_verdict
- Adds `irreversibility_detection_required` as a rule released by `T15` once tested.
- Adds `open_boundary_deterministic` sandbox class for T15–T16.
- Updates transition pages to display:
  - Irreversible
  - Point of no return

## Expected next workflow run

After upload, run:

```text
Actions → Transition Experimental Engine → Run workflow
```

Expected result:

```text
T15 advances from 1/5 Defined to 4/5 Tested.
T15 emits irreversibility_fragment.
T15 receipts show irreversible and point_of_no_return fields.
```
