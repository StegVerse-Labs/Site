# T10 Multi-Agent Transition v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What this implements

- Adds `T10` experiment: `multi_agent_sweep_v1`.
- Adds fallback experiment registration for `T10`.
- Adds multi-agent receipts with:
  - shared_state
  - agent_actions
  - individual_results
  - individual_verdicts
  - aggregate_action
  - aggregate_post_state
  - aggregate_verdict
  - composition_flip
  - all_individual_allow
- Adds `multi_agent_composition_required` as a rule released by `T10` once tested.
- Updates transition pages to display `Composition flip` and `All individual allow`.

## Expected next workflow run

Current engine status should be idle because no T10 experiment existed. After upload, run:

```text
Actions → Transition Experimental Engine → Run workflow
```

Expected result:

```text
T10 advances from 1/5 Defined to 4/5 Tested.
T10 emits multi_agent_fragment.
T10 receipts show individual verdicts vs aggregate verdict.
```
