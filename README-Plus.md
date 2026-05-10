# T14 Reconstruction Transition v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this implements

- Adds `T14` experiment: `reconstruction_sweep_v1`.
- Adds fallback experiment registration for `T14`.
- Adds reconstruction receipts with:
  - pre_state
  - action
  - observed_post_state
  - reconstructed_post_state
  - receipt_packet
  - observed_post_state_hash
  - reconstructed_post_state_hash
  - reconstruction_delta
  - reconstruction_exact
  - observed_verdict
  - reconstructed_verdict
  - reconstruction_verdict_match
  - reconstruction_confidence
- Adds `receipt_reconstruction_required` as a rule released by `T14` once tested.
- Updates transition pages to display:
  - Reconstruction exact
  - Reconstruction verdict match

## Expected next workflow run

After upload, run:

```text
Actions → Transition Experimental Engine → Run workflow
```

Expected result:

```text
T14 advances from 2/5 Derived to 4/5 Tested.
T14 emits reconstruction_fragment.
T14 receipts show exact reconstruction and verdict matching.
```
