# Site Validator Compatibility Status

## State

Site validation now uses a manifest-driven compatibility contract instead of chasing stale validator failures one by one.

## Contract

Manifest:

```text
data/ai-entry-supported-validation-commands.json
```

Current schema:

```text
stegverse.ai_entry.supported_validation_commands.v0.2
```

Canonical workflow command:

```text
python scripts/check_ecosystem_chat_application.py
```

Legacy accepted commands:

```text
python scripts/check_ecosystem_chat_ai_entry.py
python scripts/check_ecosystem_chat_ai_entry_full.py
```

## Checker

```text
scripts/check_ai_entry_supported_validation_commands.py
```

The checker now accepts either the canonical consolidated command or legacy commands in workflow files, and verifies that the no-manual guard reads the registry instead of requiring every old command literal.

## Purpose

This prevents the failure pattern:

```text
fix validator A -> fail validator B -> fix validator B -> fail validator C
```

## Remaining verification

Green is not claimed until the following are visibly successful:

```text
Site Bootstrap Validate / bootstrap-validate
Site Task Runner / run-site-task
Pages deploy step inside Site Task Runner
```
