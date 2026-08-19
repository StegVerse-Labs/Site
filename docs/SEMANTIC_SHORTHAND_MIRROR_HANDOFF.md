# Semantic Shorthand Mirror Handoff

## Source of truth

This file is the bounded continuation record for `StegVerse-Labs/Site#396`.
Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`; VA Claims Chat authority remains `docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`.

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
tests/semantic-command-router.test.cjs
scripts/check_ecosystem_chat_application.py
```

The shared router defines `/help`, `/disability`, `/evidence`, `/timeline`, `/compare`, `/explain`, and `/visualize`.

VACC intercepts slash commands locally before its coordinated-provider runtime gate. Therefore `/disability` remains useful while coordinated-provider execution is unavailable and does not activate provider execution, document upload, retrieval, representation, rating prediction, or filing.

The VACC `/disability` neighborhood includes disability compensation, service connection, secondary conditions, TDIU, P&T, combined ratings, effective dates, claims/appeals, C&P exams, evidence/records, dependents, SMC, common forms, common regulations/references, and an explicit `I do not know which topic applies` escape route.

Ecosystem Chat loads the shared router and capture-phase semantic discovery bridge before generic chat classification. Slash commands therefore render a local semantic neighborhood without provider calls or generic route/intent commitment. The bridge writes ordinary `.chat-message` and `.receipt-block` DOM records so the existing canonical event-stream observer ingests the interaction instead of creating an untracked side channel.

## Current scope state

```text
canonical issue: StegVerse-Labs/Site#396
pull request: StegVerse-Labs/Site#397
branch: feat/vacc-semantic-shorthand-396
validated candidate head: f01b41964e5033e5de91b3fee96bf690c7d39444
shared semantic router: IMPLEMENTED
VACC runtime integration: IMPLEMENTED
Ecosystem Chat runtime integration: IMPLEMENTED
recognized/unknown/argument regression: IMPLEMENTED
canonical Site application binding: IMPLEMENTED
semantic-specific hosted validation: PASS
pre-work claim validation: PASS
Site handoff orchestration: PASS
aggregate Site Bootstrap: BLOCKED BY PRE-EXISTING STEGFIN VALIDATOR/HANDOFF MISMATCH
merge/release: NOT YET COMPLETE
public deployment observation: NOT YET COMPLETE
```

## Hosted evidence on candidate `f01b41964e5033e5de91b3fee96bf690c7d39444`

```text
Ecosystem Heartbeat Orchestration run 32200999432: SUCCESS
Site Handoff Orchestrator run 32200999446: SUCCESS
VA Claims Chat LLM Bridge run 32200999416: SUCCESS
Observe and Complete Canonical Gateway Tasks run 32200999418: SUCCESS
Site Bootstrap Validate run 32200999428: FAILURE AT UNRELATED STEGFIN PHONE PROJECTION STEP
Check StegFin Phone Projection run 32200999434: FAILURE
```

Inside Site Bootstrap run `32200999428`, the following exact semantic/current-work gates passed before the unrelated StegFin step failed:

```text
SESSION_WORK_CLAIMS_PASS
SITE_HANDOFF_ORCHESTRATION_PASS
ECOSYSTEM_HEARTBEAT_ORCHESTRATION_PASS
SITE_APPLICATION_CHECK_PASS: scripts/check_semantic_shorthand_commands.py
ECOSYSTEM_CHAT_APPLICATION_PASS
ST-017 sandbox validate-application: PASS
```

The aggregate failure is not a semantic-command failure. `scripts/check_stegfin_phone_projection.py` rejects the current canonical `docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md` because it expects legacy invariant strings that the current handoff no longer contains. That surface is actively claimed by the existing Site#388 validation workstream and is outside Site#396 ownership. Site#396 has not mutated that handoff or validator. Blocker evidence was posted to Site#388 as comment `5335944525` so its current owner can reconcile the existing gate without duplicate execution.

Because the semantic handoff requires all required Site gates to pass before merge, this PR remains unmerged despite its semantic-specific validation being green.

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

1. Consume the existing Site#388 owner result when the StegFin handoff/validator mismatch is repaired; do not duplicate that work from Site#396.
2. Re-run/re-observe the exact final candidate Site Bootstrap and StegFin projection gates after the external blocker is repaired.
3. Merge PR #397 only after the required exact-candidate gate set is green.
4. Observe public deployment of `/disability` in VACC and the shared command behavior in Ecosystem Chat; deployment alone is not activation proof.
5. Read applicable target mirror handoffs and detect claims before propagating the released interaction contract to `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki`.
6. Record downstream verified ingestion/evidence and terminalize the task/claim only when those required surfaces are actually complete.

## Archive posture

NOT ARCHIVE COMPLETE. Source implementation and semantic-specific hosted validation are complete, but an existing cross-workstream Site gate remains failed; merge, public deployment observation, downstream propagation, and terminal evidence remain unfinished.
