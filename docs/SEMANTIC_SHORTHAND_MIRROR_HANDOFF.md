# Semantic Shorthand Mirror Handoff

## Source of truth

This file is the bounded continuation record for `StegVerse-Labs/Site#396`.
Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`; VA Claims Chat authority remains `docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md`.

## Goal

Install a shared low-language-bandwidth semantic command grammar for Ecosystem Chat and VACC so a user can name a recognizable concept without having to construct an expert prompt. Commands expose an intent/topic neighborhood before materially ambiguous intent is committed.

## Governing interaction invariant

```text
shorthand -> semantic neighborhood -> recognizable choices -> narrower user intent -> governed action path
```

Command recognition alone has:

```text
commit_intent=false
authority_effect=false
activation_effect=false
```

## Canonical execution lane

```text
canonical issue: StegVerse-Labs/Site#396
current branch: feat/semantic-shorthand-396-r2
current PR: PENDING_CREATION
superseded PR: #397 / feat/vacc-semantic-shorthand-396
supersession reason: old branch diverged 1454 commits behind current main and is no longer a safe merge candidate
shared Site gate owner: StegVerse-Labs/Site#388
shared Site gate repair: a3569c07aee530e4d0d55743e639127db21d5f57
credential authority: TV/TVC_ONLY
NON-TV/TVC secret/token: prohibited
```

PR #397 remains historical evidence for the first semantic implementation and hosted validation. It must not be merged after this successor lane is admitted. This R2 branch ports only the semantic feature onto current `main` and preserves unrelated current Site state.

## Installed implementation

```text
assets/semantic-command-router.js
assets/ecosystem-chat-semantic-commands.js
assets/va-claims-chat-runtime.js
ecosystem-chat.html
scripts/check_semantic_shorthand_commands.py
tests/semantic-command-router.test.cjs
scripts/check_ecosystem_chat_application.py
```

The shared router defines `/help`, `/disability`, `/evidence`, `/timeline`, `/compare`, `/explain`, and `/visualize`.

VACC intercepts slash commands before coordinated-provider runtime gating. Ecosystem Chat loads semantic routing before the current simple chat runtime. The command layer performs no provider call, storage mutation, repository mutation, filing, rating, adjudication, or credential operation.

The VACC `/disability` neighborhood includes disability compensation, service connection, secondary conditions, TDIU, P&T, combined ratings, effective dates, claims/appeals, C&P exams, evidence/records, dependents, SMC, common forms, common regulations/references, and an explicit ambiguity escape route.

## Shared Site gate repair

The earlier R1 candidate was semantically green but aggregate Site validation failed because `scripts/check_stegfin_phone_projection.py` required historical strings no longer present in the current canonical `docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md`.

Existing Site#388 ownership was preserved. The validator itself was repaired on current main at:

```text
a3569c07aee530e4d0d55743e639127db21d5f57
```

The repair validates the current handoff authority/activation contract while exact source/blob provenance remains checked separately. This is implementation of the shared-gate repair, not proof of a fresh passing candidate.

## Current state

```text
shared semantic router: IMPLEMENTED_ON_R2
VACC integration: IMPLEMENTED_ON_R2
Ecosystem Chat integration: IMPLEMENTED_ON_R2
recognized/unknown/argument regression: IMPLEMENTED_ON_R2
canonical Site application binding: IMPLEMENTED_ON_R2
shared StegFin validator repair: IMPLEMENTED_ON_MAIN
fresh R2 hosted validation: PENDING
merge: NOT_MERGED
deployment observation: NOT_OBSERVED
downstream propagation: NOT_STARTED
activation effect: NONE
```

## Historical validation retained from superseded R1

On R1 candidate `4a47f7e73a1f6c6bb71b6d7847a85d5d9ee24bb9`:

```text
Ecosystem Heartbeat Orchestration 32201188056: SUCCESS
Site Handoff Orchestrator 32201188038: SUCCESS
VA Claims Chat LLM Bridge 32201188049: SUCCESS
Observe and Complete Canonical Gateway Tasks 32201188069: SUCCESS
Site Bootstrap 32201188127: semantic/current-work steps PASS, then unrelated StegFin projection failure
Check StegFin Phone Projection 32201188150: FAIL_CURRENT_HANDOFF_LEGACY_INVARIANT_MISMATCH
```

These runs prove the R1 semantic implementation behavior only. They do not validate R2.

## Required next work

1. Add the R2 claim to the current Site claim registry and mark R1 as superseded.
2. Create the R2 integration PR from current main and close/supersede PR #397.
3. Observe exact-head R2 claim/orchestration, semantic, Site Bootstrap, StegFin projection, and VACC bridge validation.
4. Repair only R2-specific failures; do not reopen unrelated current Site work.
5. Merge only after required exact-head gates pass.
6. Observe deployed/public `/disability` behavior in VACC and shared command behavior in Ecosystem Chat.
7. After merge/deployment evidence, use existing Publisher -> admissibility-wiki -> StegGuardian downstream contracts; do not create duplicate propagation lanes.
8. Terminalize task/claim only after required downstream evidence exists.

## User action

None for current machine-executable source/CI work.

Future current-iPhone WebAuthn/PREPARE work belongs to Site#388/StegFin continuation and is not required to validate or merge this semantic-discovery layer.

## Archive posture

Conversation context is not canonical. Continue from this handoff, the task record, issue #396, the active R2 claim, current PR evidence, Site#388, and repository orchestration state.
