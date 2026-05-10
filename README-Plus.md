# T8 Trust-Drift Experiment v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this implements

- Adds `T8` experiment: `trust_drift_sweep_v1`.
- Adds fallback experiment registration for `T8`.
- Adds trust-drift receipts with:
  - initial trust
  - decayed trust
  - lambda
  - tau
  - pre-decay capacity
  - post-decay capacity
  - pre-decay verdict
  - trust-decay verdict
  - trust_flip
- Adds `trust_drift_required` as a rule released by `T8` once tested.
- Updates transition pages to display `Trust flip` in receipt cards.

## Expected next workflow run

Because T7 is already tested, the engine should be in bounded-batch mode. The next eligible runnable element should be:

```text
T8 — trust_drift_sweep_v1
```

Expected result:

```text
T8 advances from 2/5 Derived to 4/5 Tested.
T8 emits a trust_drift_fragment knowledge delta.
T8 receipts show trust decay and trust_flip values.
```
