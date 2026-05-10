# Autonomous Next-Step Selector Complete v1

Upload-safe complete replacement for the selector layer.

## Includes

```text
transition-release-index.html
data/transition-release-state-v1.json
data/transition-decision-rules-v1.json
data/next-transition-build-candidate-v1.json
data/transition-release-index-v1.json
data/page-contracts-v1.json
tools/transition_next_step_selector.py
.github/workflows/select-next-transition-step.yml
```

## Display note

If displayed without the leading dot, the workflow path is:

```text
github/workflows/select-next-transition-step.yml
```

In GitHub, the actual path must be:

```text
.github/workflows/select-next-transition-step.yml
```

## Done checks

```text
1. Wait for Pages deployment.
2. Run Actions → Page Contract Check.
3. Run Actions → Select Next Transition Step.
```

Expected selector result before reports are available in the workspace:

```text
next_system_action = run_required_checks
promotion_allowed = false
human_required = false
```
