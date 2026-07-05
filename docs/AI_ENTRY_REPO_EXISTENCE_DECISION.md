# AI Entry Repo Existence Decision

## Question

Are all necessary repos in existence for the current StegVerse AI Entry build?

## Answer

Yes for the current preview/local-ready build.

## Required repos confirmed

```text
StegVerse-Labs/Site
  status: exists
  role: one-window AI Entry UI, route contract, browser adapter, Site validation

StegVerse-org/LLM-adapter
  status: exists
  role: provider comparison boundary, interim backend response scaffold, endpoint/service wrapper

StegVerse-org/StegVerse-SDK
  status: exists
  role: SDK receipt preview boundary and SDK-side validation
```

## Repo not required yet

A dedicated backend service repo is not required for the current preview/local-ready phase because `StegVerse-org/LLM-adapter` now contains the interim endpoint/service-wrapper boundary.

A future dedicated backend repo may still be created if governed-live activation requires a separate service boundary.

## Current decision

```text
new_repo_required_now == false
current_repo_set_sufficient_for_preview_build == true
future_backend_repo_candidate == optional
```

## Next build target

Install a shared integration verifier or release/readiness index that references the three canonical validation commands:

```bash
# Site
python scripts/check_ecosystem_chat_ai_entry.py

# LLM-adapter
python scripts/verify_goal4.py

# StegVerse-SDK
python scripts/verify_goal4.py
```
