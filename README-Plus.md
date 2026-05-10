# Autonomous Next-Step Selector v1

This bundle adds the first self-validating transition selection layer.

## Adds

```text
data/transition-release-state-v1.json
data/transition-decision-rules-v1.json
tools/transition_next_step_selector.py
.github/workflows/select-next-transition-step.yml
```

## Display note

The workflow path may be displayed as:

```text
github/workflows/select-next-transition-step.yml
```

In the repository, it must include the leading dot:

```text
.github/workflows/select-next-transition-step.yml
```

## What done means

The repo can answer:

```text
Given the current transition release state, what should happen next, and why?
```

The selector does not promote from chat messages, screenshots, or implied status. Missing evidence defaults to no promotion.

## Current expected output

Until readable workflow reports exist inside the workspace, the selector should produce:

```text
next_system_action = run_required_checks
promotion_allowed = false
human_required = false
```

After both required reports are available and passing, it should produce:

```text
next_system_action = promote_candidate_milestone
promotion_allowed = true
human_required = false
```

## Run

```text
Actions → Select Next Transition Step → Run workflow
```

Download the artifact:

```text
next-transition-step-report
```
