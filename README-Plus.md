# T13 Receipt-Bound Transition v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this implements

- Adds `T13` experiment: `receipt_bound_sweep_v1`.
- Adds fallback experiment registration for `T13`.
- Adds receipt-bound transition receipts with:
  - pre_state
  - action
  - post_state
  - pre_state_hash
  - action_hash
  - post_state_hash
  - receipt_payload_hash
  - receipt_bound
- Adds `receipt_binding_required` as a rule released by `T13` once tested.
- Adds `receipt_evidence_deterministic` sandbox class for T13–T14.
- Updates transition pages to display `Receipt bound`.

## Expected next workflow run

After upload, run:

```text
Actions → Transition Experimental Engine → Run workflow
```

Expected result:

```text
T13 advances from 2/5 Derived to 4/5 Tested.
T13 emits receipt_binding_fragment.
T13 receipts show receipt_bound=true and hashes for pre-state, action, and post-state.
```
