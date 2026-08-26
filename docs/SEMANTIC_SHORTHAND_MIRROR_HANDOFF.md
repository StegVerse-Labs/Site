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
current PR: #500
superseded PR: #397 / feat/vacc-semantic-shorthand-396 / CLOSED_AS_SUPERSEDED
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
fresh R2 hosted validation: PASS
merge: MERGED at a3a2801da0c149e36cee2b0edb78f367b0c3ffa1
Pages deployment: OBSERVED SUCCESS for merge commit
deployed artifact content: VERIFIED
fresh public route network behavior: NOT YET OBSERVED
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

## R2 validation, merge, and deployment evidence

Exact PR head `455aea54a612f470f3e11e7affb06c7668427ed5`:

```text
Ecosystem Heartbeat Orchestration 33023216669: SUCCESS
Site Handoff Orchestrator 33023216659: SUCCESS
VA Claims Chat LLM Bridge 33023216651: SUCCESS
VA Claims Chat Surface Validation 33023216689: SUCCESS
Check StegFin Phone Projection 33023216646: SUCCESS
Site Bootstrap Validate 33023216696: SUCCESS
Canonical Site application: PASS
Semantic shorthand checker: PASS
```

PR #500 merged at `a3a2801da0c149e36cee2b0edb78f367b0c3ffa1`.

Post-merge main evidence:

```text
Ecosystem Heartbeat Orchestration 33023272270: SUCCESS
Site Handoff Orchestrator 33023272253: SUCCESS
VA Claims Chat LLM Bridge 33023272288: SUCCESS
VA Claims Chat Surface Validation 33023272267: SUCCESS
Check StegFin Phone Projection 33023272306: SUCCESS
Site Bootstrap Validate 33023272321: SUCCESS
Pages build/deployment 33023271659: SUCCESS
Pages artifact 9627374238
Pages artifact digest sha256:c6c0e525d7a6e60dac3a3523a406f5d678808e5225f07286388b37da53dd2032
```

The exact Pages artifact was inspected and contains `ecosystem-chat.html`, `va-claims-chat.html`, the shared semantic router, the Ecosystem Chat semantic bridge, and the VACC runtime. Script ordering and VACC semantic-interception markers are present. Durable evidence is stored in `receipts/semantic-shorthand-396-r2-deployment.json`.

Repository task observer run `33023272293` failed closed only because existing TIDC split tasks and the coherent-transition-threshold activation task remain blocked. It did not report a semantic-shorthand failure and does not roll back the validated merge/deployment evidence.

## Required next work

1. Obtain fresh public-route network observation of the deployed semantic assets and user-facing `/disability` behavior; Pages deployment success and artifact inspection are already durable but do not substitute for a fresh route fetch.
2. After fresh public behavior is observed, use the existing Publisher -> admissibility-wiki -> StegGuardian downstream contracts; do not create duplicate propagation lanes.
3. Record downstream verified ingestion/evidence.
4. Terminalize the task/claim only after the required downstream evidence exists.

## User action

None for current machine-executable source/CI work.

Future current-iPhone WebAuthn/PREPARE work belongs to Site#388/StegFin continuation and is not required to validate or merge this semantic-discovery layer.

## Archive posture

Conversation context is not canonical. Continue from this handoff, the task record, issue #396, the active R2 claim, current PR evidence, Site#388, and repository orchestration state.
