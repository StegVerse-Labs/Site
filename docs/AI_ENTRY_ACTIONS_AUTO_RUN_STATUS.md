# AI Entry Actions Auto-Run Status

## Current finding

The validate workflows are configured to run automatically on edits/fixes pushed to the repo.

## Workflow triggers

Each current validate workflow uses:

```yaml
on:
  push:
  pull_request:
  workflow_dispatch:
```

## Repos

```text
StegVerse-Labs/Site
  workflow: .github/workflows/validate.yml
  command: python scripts/check_ecosystem_chat_ai_entry.py
  observed: push-triggered run occurred and failed before repair

StegVerse-org/LLM-adapter
  workflow: .github/workflows/validate.yml
  command: python scripts/verify_goal4.py
  observed: push-triggered run occurred and failed before repair

StegVerse-org/StegVerse-SDK
  workflow: .github/workflows/validate.yml
  command: python scripts/verify_goal4.py
  observed: push-triggered run occurred and failed before repair
```

## Correction to previous status language

Earlier status files recorded that workflow runs were not exposed by the available commit-run status tool. That was incomplete because the available commit-run tool only exposed pull-request filtered runs in this context. The user-provided GitHub Actions screenshots confirm push-triggered validate workflows are running.

## Current repair state

```text
Site route-priority bug patched
StegVerse-SDK pytest raises dependency patched
LLM-adapter aggregate validation narrowed to AI Entry validation set
```

## Remaining confirmation

Wait for the next automatic push-triggered validate runs or inspect the GitHub Actions UI for the repaired commits.
