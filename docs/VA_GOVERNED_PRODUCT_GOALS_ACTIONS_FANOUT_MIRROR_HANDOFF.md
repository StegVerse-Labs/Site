# VA Governed Product Goals Actions Fanout Mirror Handoff

Updated: 2026-08-22
Repository: `StegVerse-Labs/Site`
Issue: `#427`
Claim: `SITE-VA-GOVERNED-PRODUCT-GOALS-CLOCK-RETIREMENT-427-20260822`
Branch: `claim/site-va-governed-product-goals-clock-retirement-427`
State: `IMPLEMENTATION_IN_PROGRESS`

## Goal

Remove the redundant six-hour GitHub-hosted validation clock, repository writeback, credential persistence, and 90-day artifact custody from `.github/workflows/va-governed-product-goals.yml` while preserving deterministic validation of the canonical governed VA product-goal contract.

## Canonical product boundary

Parent source of truth: `docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`.

`data/va-claim-assistant/governed-product-goals.json` remains product state owned by Site #113, Site #116, StegVerse-org/LLM-adapter, TVC, and Master Records. VA-GOAL-01/02/03 remain active implementation goals and VA-GOAL-04 remains a future governed filing target. This Actions repair owns none of those implementations and cannot activate them.

## Pre-repair carrier

`.github/workflows/va-governed-product-goals.yml` currently has:

```text
schedule: 29 */6 * * *
minimum scheduled starts: 4/day
permissions: contents: write
credential-persisting checkout: yes
repository writeback: data/va-claim-assistant/governed-product-goals-validation.json
artifact custody: 90 days
cancel-in-progress: false
```

The validator is deterministic and writes one derived receipt. The recurring clock does not execute VA product goals or prove runtime activation.

## Required retained validation

- `workflow_dispatch` retained;
- existing `pull_request` validation retained;
- bounded main-push validation retained for the goal contract, validator, relevant canonical handoffs/public guide, and workflow source;
- exact PR merge-ref or push SHA acquired anonymously;
- credential-bearing environments fail closed;
- preinstalled Python is used;
- deterministic validator executes;
- derived goal-validation receipt must PASS;
- `required_goals_present=true`;
- `veteran_submission_authority_preserved=true`;
- `automated_filing_active=false`;
- `authority_effect=false`;
- `activation_effect=false`;
- `blockers=[]`;
- active/future goal states remain unchanged;
- locally derived receipt is restored before completion;
- repository writeback is absent;
- artifact custody is absent;
- GitHub-token runtime/production authority is absent;
- TV/TVC remains credential authority;
- no Render.

## Collision boundaries

- Do not modify VA-GOAL-01/02/03/04 product semantics or owners.
- Do not claim Site #113/#116, LLM-adapter, TVC, or Master Records work complete.
- Do not modify `.github/workflows/validate.yml` while Site #388 claims it.
- Do not modify the shared Actions handoff while Site #404 claims it.
- Workflow success is validation evidence only.

## Completion gate

Release requires the repaired workflow itself to pass exact-head PR validation, Site claim/orchestration gates to pass except for independently proven pre-existing failures, integration to merge, durable release evidence to be recorded here and in `data/session-work-claims.json`, and Site #427 to close. Merge or workflow success alone is not product activation.