# MS-012H Path Function Sentinel Sandbox Loop

This version formalizes the last stage:

```text
sentinel observes path deficiency
→ writes sandbox repair task
→ sandbox tests repair
→ repair bundle passes back through ingestion
→ sentinel returns to idle only after ingestion path compliance is restored
```

## Important

`triggered_loop/` is not a runaway automation mechanism. It is a bounded state marker showing that the path-function sentinel detected deficiencies and emitted a sandbox task.

## Verdicts

```text
IDLE_READY
SANDBOX_TASK_REQUIRED
FAIL_CLOSED
```

## Run

```text
python tools/path_function_sentinel_test.py \
  --policy data/path-tests/path-function-sentinel-policy-v2.json \
  --out-dir path_function_reports
```
