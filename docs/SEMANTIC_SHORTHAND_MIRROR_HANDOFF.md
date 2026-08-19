# Semantic Shorthand Mirror Handoff

## Source of truth

This file is the bounded continuation record for `StegVerse-Labs/Site#396`.
Repository-wide authority remains `SITE_MIRROR_HANDOFF.md`; VA Claims Chat authority remains `docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`.

## Goal

Install a shared low-language-bandwidth semantic command grammar for Ecosystem Chat and VACC so a user can name a recognizable concept without having to construct an expert prompt. Commands expose an intent/topic neighborhood before any materially ambiguous intent is committed.

## Governing interaction invariant

```text
shorthand -> semantic neighborhood -> recognizable choices -> narrower user intent -> governed action path
```

A command is not an execution primitive. Command recognition alone has:

```text
commit_intent=false
authority_effect=false
activation_effect=false
```

When multiple materially different interpretations remain admissible, the command layer exposes choices instead of silently choosing one.

## Installed implementation

```text
assets/semantic-command-router.js
assets/va-claims-chat-runtime.js
assets/ecosystem-chat-semantic-commands.js
ecosystem-chat.html
scripts/check_semantic_shorthand_commands.py
```

The shared router currently defines `/help`, `/disability`, `/evidence`, `/timeline`, `/compare`, `/explain`, and `/visualize`.

VACC intercepts slash commands locally before its coordinated-provider runtime gate. Therefore `/disability` remains useful when Goal 2 is blocked and does not activate provider execution, document upload, retrieval, representation, rating prediction, or filing.

The VACC `/disability` neighborhood includes disability compensation, service connection, secondary conditions, TDIU, P&T, combined ratings, effective dates, claims/appeals, C&P exams, evidence/records, dependents, SMC, common forms, common regulations/references, and an explicit `I do not know which topic applies` escape route.

Ecosystem Chat now loads the shared router and a capture-phase semantic discovery bridge before generic chat classification. Slash commands therefore render a local semantic neighborhood without provider calls or generic route/intent commitment. The bridge writes ordinary `.chat-message` and `.receipt-block` DOM records so the existing canonical event-stream observer ingests the interaction instead of creating an untracked side channel.

## Current scope state

```text
canonical issue: StegVerse-Labs/Site#396
pull request: StegVerse-Labs/Site#397
branch: feat/vacc-semantic-shorthand-396
shared semantic router: IMPLEMENTED
VACC runtime integration: IMPLEMENTED
Ecosystem Chat runtime integration: IMPLEMENTED
static deterministic validator: IMPLEMENTED
hosted validation: EXECUTING / CLAIM-METADATA FAILURE OBSERVED
merge/release: NOT YET COMPLETE
public deployment observation: NOT YET COMPLETE
```

Observed hosted evidence on candidate head `536dbee437d121c8c88a1dd8dfd642c594740f56`:

- `VA Claims Chat LLM Bridge` run `32200602644`: SUCCESS.
- `Observe and Complete Canonical Gateway Tasks` run `32200602616`: SUCCESS.
- `Ecosystem Heartbeat Orchestration` run `32200602614`: FAILED at `Validate exclusive pre-work claims` because this new claim was missing required `handoff_revision` and `next_task_after_release` fields.
- That failure is claim metadata, not semantic-command behavioral validation. It must be corrected and fresh exact-head validation re-observed before merge.

## Credential and authority boundaries

```text
credential authority: TV/TVC_ONLY
NON-TV/TVC secret/token introduced: false
network call from semantic router: none
network call from Ecosystem semantic bridge: none
storage mutation from semantic router/bridge: none
repo mutation from browser command: none
provider call from semantic discovery: false
private document activation: false
filing activation: false
VA adjudication/rating authority: none
```

## Required next work

1. Correct the branch claim with required handoff revision and downstream task fields and add the newly claimed Ecosystem Chat files.
2. Add deterministic recognized/unknown/argument-bearing command fixtures or equivalent browser-level regression coverage.
3. Re-observe exact-head `python scripts/check_semantic_shorthand_commands.py` plus Site/VACC/Ecosystem Chat hosted validation after the claim correction.
4. Merge only after collision/pre-work validation and all required Site gates pass on the exact candidate.
5. Observe public deployment of `/disability` in VACC and the shared command behavior in Ecosystem Chat.
6. Propagate the semantic interaction contract to `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki` only after merged/deployed evidence exists and applicable target handoffs are read.

## Archive posture

NOT ARCHIVE COMPLETE. Source implementation now covers both VACC and Ecosystem Chat, but claim correction, regression coverage, fresh validation, merge/release, deployment observation, and downstream propagation remain unfinished.
