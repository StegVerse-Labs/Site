# VA Claims Chat Actions Fanout Mirror Handoff

Updated: 2026-08-22
Repository: `StegVerse-Labs/Site`
Issue: `#434`
Claim: `SITE-VA-CLAIMS-CHAT-CLOCK-RETIREMENT-434-20260822`
Branch: `claim/site-va-claims-chat-clock-retirement-434`
State: `IMPLEMENTATION_IN_PROGRESS`

## Goal

Retire the VA Claims Chat compatibility/deep-work surface's redundant six-hour GitHub-hosted validation clock, repository writeback, credential persistence, and 30-day artifact custody while preserving complete deterministic validation of every source the validator consumes.

## Canonical product boundary

Parent source of truth: `docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`.

VACC product/runtime ownership remains separate:

```text
Site#113: VACC public activation
Site#239: unified conversational capability
StegVerse-org/LLM-adapter#90: provider/runtime execution
Site#116: secure documents
master-records/orchestration#15: custody/reconstruction
```

`va-claims-chat.html` is a compatibility, deterministic-help, testing, and deep-work destination. This Actions task owns only its validation carrier plus one bounded validator-consistency correction. It cannot activate the coordinated runtime, private-document capability, filing, custody, provider execution, or a second primary chat stack.

## Pre-repair carrier

```text
workflow: .github/workflows/va-claims-chat-surface.yml
schedule: 41 */6 * * *
minimum scheduled starts: 4/day
permissions: contents: write
checkout persist-credentials: true
repository writeback: data/va-claim-assistant/chat-surface-validation.json
artifact custody: 30 days
pull_request trigger: absent
validator inputs omitted from trigger paths:
  - api/va-claim-assistant/runtime-projection.json
  - assets/va-claims-chat-runtime.js
```

The validator is deterministic and derives one receipt from repository state. The six-hour clock does not execute or observe the resident VACC runtime.

## Exact-head validator drift discovered during repair

PR #437 head `07faa11d7476fc377d1ab04c6a4fbdb3219dd230` launched direct carrier run `32608184362`, job `97116631518`.

Credential refusal, anonymous exact-source acquisition, preinstalled Python, and receipt preservation all passed. The unchanged validator then failed because current `va-claims-chat.html` contains the exact forbidden public-UI token:

```text
SOURCE-GROUNDED PROCEDURAL HELP
```

The validator reported:

```text
technical_or_internal_ui_token_present:SOURCE-GROUNDED PROCEDURAL HELP
```

This is consistent with the parent VA handoff, which requires internal capability enums, runtime names, receipt mechanics, worker state, governance labels, and scaffolding status to remain hidden from the public UI. The label was introduced by the now-released #404/R3 repair chain; neither prior owner remains active and no current registry claim owns `va-claims-chat.html`.

Therefore #434 may remove only that one technical-label paragraph as a bounded incidental validator-consistency dependency. That correction does not change VACC provider/runtime capability, upload/filing authority, claimant authority, page navigation, deterministic guide flow, or activation state. The validator itself must remain unchanged.

## Required retained validation

- `workflow_dispatch` retained;
- `pull_request` validation present;
- bounded `main` push validation present;
- all validator inputs trigger validation:
  - `data/va-claim-assistant/chat-capability-state.json`;
  - `api/va-claim-assistant/runtime-projection.json`;
  - `va-claims-chat.html`;
  - `assets/va-claims-chat-runtime.js`;
  - `scripts/validate_va_claims_chat_surface.py`;
  - `.github/workflows/va-claims-chat-surface.yml`;
- exact PR merge ref or push SHA fetched anonymously;
- credential-bearing environments fail closed;
- preinstalled Python used;
- existing validator executes unchanged;
- derived receipt must PASS;
- private document upload remains false;
- automated filing remains false;
- public upload remains false;
- veteran submission authority remains preserved;
- authority and activation effects remain false;
- tracked receipt is restored before completion, including failed validation attempts;
- repository writeback is absent;
- artifact custody is absent;
- GitHub-token production/runtime authority is absent;
- TV/TVC remains credential authority;
- no Render.

## Collision boundaries

- `va-claims-chat.html` change is limited to removal of the exact forbidden internal technical-label paragraph proven by run `32608184362`; no other page semantics are in #434 scope.
- Do not modify VACC provider/runtime/public activation semantics owned by Site #113 / Site #239 / LLM-adapter.
- Do not modify Site #116 secure-document semantics.
- Do not modify `.github/workflows/validate.yml` while Site #388 claims it.
- Do not modify #413 or #420 carrier paths.
- Preserve the concurrently admitted Thought Experiments #433 claim and all other live claim-registry state.
- Workflow success is validation evidence only.

## Completion gate

Release requires the unchanged Claims Chat validator and repaired workflow to pass exact-head PR validation, Site claim/orchestration gates and full Bootstrap to pass (or any unrelated failure to be independently proven), integration to merge, durable release evidence to be recorded here and in `data/session-work-claims.json`, and Site #434 to close. Merge or workflow success alone is not product activation.
