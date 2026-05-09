# T5 Observation-Lag + Receipt Normalizer v1

Upload-safe bundle. No leading-dot paths.

This bundle replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What it does

1. Normalizes old receipts and ledger display:
   - T2 simplex rows show `constraint=PASS` when the simplex delta is zero.
   - T3 bounded-action rows show bound status.
   - T4 capacity-margin rows show margin status.
2. Adds the first T5 experiment:
   - `observation_lag_sweep_v1`
3. Generates replayable receipts for both old and new ledger rows.
4. Keeps evidence at 4/5 Tested, not 5/5 Receipt-backed.

## Expected next workflow run

```text
Actions → Transition Experimental Engine → Run workflow
```

Expected selection:

```text
T5 — observation_lag_sweep_v1
```

Expected result:

```text
T5 advances from 1/5 Defined to 4/5 Tested
T5 emits lag_flip_fragment knowledge delta
T5 receipts include observed_state, lag_drift, commit_state, observed verdict, commit verdict, and lag_flip
```
