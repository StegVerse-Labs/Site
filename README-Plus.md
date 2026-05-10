# Autonomous Next-Step Selector Complete v1 — Dotless Workflow Bundle

This bundle intentionally contains **no leading-dot paths**.

## Includes

```text
transition-release-index.html
data/transition-release-state-v1.json
data/transition-decision-rules-v1.json
data/next-transition-build-candidate-v1.json
data/transition-release-index-v1.json
data/page-contracts-v1.json
tools/transition_next_step_selector.py
github/workflows/select-next-transition-step.yml
```

## Important workflow note

The workflow file is intentionally placed here without the leading dot:

```text
github/workflows/select-next-transition-step.yml
```

If GitHub needs to recognize it as an Actions workflow, the file must ultimately live at:

```text
.github/workflows/select-next-transition-step.yml
```

This bundle follows the dotless-path upload/display rule.

## Done checks

```text
1. Upload files.
2. Ensure the workflow file is placed in GitHub at .github/workflows/select-next-transition-step.yml.
3. Wait for Pages deployment.
4. Run Actions → Page Contract Check.
5. Run Actions → Select Next Transition Step.
```

Expected selector result before workflow reports are readable inside the workspace:

```text
next_system_action = run_required_checks
promotion_allowed = false
human_required = false
```
