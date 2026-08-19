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
scripts/check_semantic_shorthand_commands.py
```

The shared router currently defines `/help`, `/disability`, `/evidence`, `/timeline`, `/compare`, `/explain`, and `/visualize`.

VACC intercepts slash commands locally before its coordinated-provider runtime gate. Therefore `/disability` remains useful when Goal 2 is blocked and does not activate provider execution, document upload, retrieval, representation, rating prediction, or filing.

The VACC `/disability` neighborhood includes disability compensation, service connection, secondary conditions, TDIU, P&T, combined ratings, effective dates, claims/appeals, C&P exams, evidence/records, dependents, SMC, common forms, common regulations/references, and an explicit `I do not know which topic applies` escape route.

## Current scope state

```text
canonical issue: StegVerse-Labs/Site#396
branch: feat/vacc-semantic-shorthand-396
shared semantic router: IMPLEMENTED
VACC runtime integration: IMPLEMENTED
static deterministic validator: IMPLEMENTED
Ecosystem Chat runtime integration: NOT YET WIRED
hosted validation: NOT YET OBSERVED
merge/release: NOT YET COMPLETE
public deployment observation: NOT YET COMPLETE
```

The shared module contains an `ECOSYSTEM_CHAT` context, but that context is not considered activated until `ecosystem-chat.html` / `assets/ecosystem-chat.js` actually consumes it and hosted validation proves the behavior.

## Credential and authority boundaries

```text
credential authority: TV/TVC_ONLY
NON-TV/TVC secret/token introduced: false
network call from semantic router: none
storage mutation from semantic router: none
repo mutation from browser command: none
private document activation: false
filing activation: false
VA adjudication/rating authority: none
```

## Required next work

1. Wire the same router into Ecosystem Chat before generic route classification.
2. Add UI-level regression fixtures for recognized, unknown, and argument-bearing slash commands.
3. Run `python scripts/check_semantic_shorthand_commands.py` and existing VACC/Ecosystem Chat validators through hosted validation.
4. Merge only after collision/pre-work validation and existing Site gates pass.
5. Observe public deployment of `/disability` in VACC and the shared command behavior in Ecosystem Chat.
6. Propagate the semantic interaction contract to applicable downstream documentation only after merged/deployed evidence exists.

## Archive posture

NOT ARCHIVE COMPLETE. Source implementation exists on the feature branch, but Ecosystem Chat wiring, hosted validation, merge, deployment observation, and downstream evidence remain unfinished.
