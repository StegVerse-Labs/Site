# T11 Conflict Transition v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this implements

- Adds `T11` experiment: `conflict_sweep_v1`.
- Adds fallback experiment registration for `T11`.
- Adds conflict receipts with:
  - shared_state
  - action_a
  - action_b
  - post_a
  - post_b
  - combined_action
  - combined_post_state
  - selected_action
  - rejected_action
  - resolved_post_state
  - verdict_a
  - verdict_b
  - combined_verdict
  - resolved_verdict
  - conflict_detected
  - conflict_flip
  - resolution_policy
- Adds `conflict_resolution_required` as a rule released by `T11` once tested.
- Updates transition pages to display `Conflict detected` and `Conflict flip`.

## Expected next workflow run

After upload, run:

```text
Actions → Transition Experimental Engine → Run workflow
```

Expected result:

```text
T11 advances from 1/5 Defined to 4/5 Tested.
T11 emits conflict_resolution_fragment.
T11 receipts show conflict detection and resolution policy.
```
