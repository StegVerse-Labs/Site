# T16 Self-Modifying Transition v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this implements

- Adds `T16` experiment: `self_modifying_rule_sweep_v1`.
- Adds fallback experiment registration for `T16`.
- Adds self-modifying rule receipts with:
  - pre_rule_state
  - rule_patch
  - rule_delta_hash
  - safety_constraints
  - post_rule_state
  - constraints_pass
  - self_modification_safe
  - rule_patch_verdict
- Adds `self_modification_required` as a rule released by `T16` once tested.
- Updates transition pages to display:
  - Self-modification safe

## Expected next workflow run

After upload, run:

```text
Actions → Transition Experimental Engine → Run workflow
```

Expected result:

```text
T16 advances from 0/5 Proposed to 4/5 Tested.
T16 emits self_modification_fragment.
T16 receipts show allowed guarded rule patches and blocked unsafe rule patches.
```
