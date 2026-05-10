# T12 Consensus Transition v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this implements

- Adds `T12` experiment: `consensus_sweep_v1`.
- Adds fallback experiment registration for `T12`.
- Adds consensus receipts with:
  - canonical_state
  - proposal_action
  - canonical_post_state
  - validator_results
  - validator_verdicts
  - allow_votes
  - deny_votes
  - quorum_threshold
  - quorum_result
  - canonical_verdict
  - consensus_flip
- Adds `validator_consensus_required` as a rule released by `T12` once tested.
- Updates transition pages to display `Consensus flip`.

## Expected next workflow run

After upload, run:

```text
Actions → Transition Experimental Engine → Run workflow
```

Expected result:

```text
T12 advances from 1/5 Defined to 4/5 Tested.
T12 emits consensus_fragment.
T12 receipts compare validator quorum against canonical admissibility.
```
