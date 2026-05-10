# Autonomous Next-Step Selector Public Wiring Fix

This fixes the missing public wiring for the selector output.

## Replaces

```text
transition-release-index.html
data/transition-release-index-v1.json
data/page-contracts-v1.json
```

## Why

The selector output file existed, but the public release directory did not yet expose it as a first-class public JSON surface.

## Done

Page Contract Check should verify:

```text
data/next-transition-build-candidate-v1.json
Autonomous Next-Step Selector
Next Transition Build Candidate v1
```

## Run after upload

```text
1. Wait for Pages deployment.
2. Run Actions → Page Contract Check.
3. Run Actions → Select Next Transition Step.
```
