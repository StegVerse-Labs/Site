# T9 Two-State Coupled Transition v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this implements

- Adds `T9` experiment: `two_state_coupling_sweep_v1`.
- Adds fallback experiment registration for `T9`.
- Adds coupled-state receipts with:
  - state_a
  - state_b
  - action_a
  - coupling_effect_on_b
  - post_state_a
  - post_state_b_without_coupling
  - post_state_b_with_coupling
  - a_verdict
  - b_verdict_without_coupling
  - b_verdict_with_coupling
  - coupling_flip
  - local_admissible_coupled_denied
- Adds `two_state_coupling_required` as a rule released by `T9` once tested.
- Adds `coupled_state_deterministic` sandbox class for T9–T12.

## Expected next workflow run

Current engine status should be idle because no T9 experiment existed. After upload, run:

```text
Actions → Transition Experimental Engine → Run workflow
```

Expected result:

```text
T9 advances from 1/5 Defined to 4/5 Tested.
T9 emits coupled_state_fragment.
T9 receipts show coupling_flip and local_admissible_coupled_denied.
```
