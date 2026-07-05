# AI Entry Cross-Repo Status

## Current integration goal

StegVerse AI Entry is now split into three repo-local, self-verifying preview surfaces.

## Repos and responsibilities

```text
StegVerse-Labs/Site
  -> one-window AI Entry UI
  -> route manifest
  -> browser adapter
  -> adapter extension contract
  -> local API wrapper
  -> validate workflow and iOS mirror
  -> no-manual-task verifier

StegVerse-org/LLM-adapter
  -> provider comparison boundary
  -> interim backend response scaffold
  -> endpoint wrapper
  -> service wrapper
  -> validate workflow and iOS mirror
  -> no-manual-task verifier

StegVerse-org/StegVerse-SDK
  -> AI Entry receipt preview boundary
  -> SDK-side preview validation
  -> validate workflow and iOS mirror
  -> no-manual-task verifier
```

## Canonical validation commands

```bash
# Site
python scripts/check_ecosystem_chat_ai_entry.py

# LLM-adapter
python scripts/verify_goal4.py

# StegVerse-SDK
python scripts/verify_goal4.py
```

## Current invariant

```text
site_contract_sync_complete == true
adapter_preview_backend_complete == true
sdk_receipt_preview_complete == true
manual_verification_gap_converted_to_repo_local_checks == true
live_provider_calls_enabled == false
live_sdk_calls_enabled == false
execution_authority_issued == false
real_receipt_issued == false
workflow_count_exceeds_two == false
```

## Remaining work

```text
external workflow-run confirmation remains dependent on GitHub Actions status exposure
future governed-live activation remains separate from preview/local-ready work
```

## Next integration candidate

Create a shared integration verifier or release/readiness index that checks the three canonical commands from a coordinating repo or future backend service repo.

## Archive posture

This file captures the cross-repo AI Entry integration state so the current thread can be archived without needing additional context to continue.
