# VA Claims Chat Actions Fanout Mirror Handoff

Updated: 2026-08-22
Repository: `StegVerse-Labs/Site`
Issue: `#434`
Claim: `SITE-VA-CLAIMS-CHAT-CLOCK-RETIREMENT-434-20260822`
Branch: `claim/site-va-claims-chat-clock-retirement-434`
State: `VALIDATED_BLOCKED_ON_INDEPENDENT_BRIDGE_VALIDATOR_REPAIR`

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

`va-claims-chat.html` is a compatibility, deterministic-help, testing, and deep-work destination. This Actions task owns only its validation carrier plus one bounded public-UI validator-consistency correction. It cannot activate the coordinated runtime, private-document capability, filing, custody, provider execution, or a second primary chat stack.

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

## Public-UI validator drift discovered and corrected

The first PR #437 attempt launched direct carrier run `32608184362`, job `97116631518`. Credential refusal, anonymous exact-source acquisition, preinstalled Python, and receipt preservation passed, but the unchanged surface validator rejected current `va-claims-chat.html` because it contained the exact internal public-UI token:

```text
SOURCE-GROUNDED PROCEDURAL HELP
```

with:

```text
technical_or_internal_ui_token_present:SOURCE-GROUNDED PROCEDURAL HELP
```

The parent VA handoff already requires internal capability enums, runtime names, receipt mechanics, worker state, governance labels, and scaffolding status to remain hidden from veteran-facing UI. #434 therefore removed only that one technical-label paragraph. Navigation, guided flow, privacy boundary, 21-526EZ fallback, runtime bridge, claimant review/submission control, and all authority/activation state remain unchanged.

## Exact-head #434 validation evidence

PR #438 exact branch head:

```text
00d0a0e0e5f0f587834c6e9fe937366ed0390875
validated merge ref: a41bbf85d4f03a6ec3d6656c58c5eee3692c1d23
```

Task-owned and repository gates:

```text
VA Claims Chat Surface Validation: PASS
run: 32608567184
job: 97117620348

Site Bootstrap Validate: PASS
run: 32608567218
job: 97117620352

Ecosystem Heartbeat Orchestration: PASS
run: 32608567178
job: 97117620148

Site Handoff Orchestrator: PASS
run: 32608567223
job: 97117620276

Check StegFin Phone Projection: PASS
run: 32608567169
job: 97117620254
```

The direct carrier specifically proves credential refusal, exact anonymous source acquisition, unchanged surface validator PASS, tracked-receipt restoration, repository writeback `NONE`, artifact custody `NONE`, and validation-only containment.

## Independent stale bridge-validator blocker

The page change also triggered `.github/workflows/va-claims-chat-llm-bridge.yml`:

```text
run: 32608567211
job: 97117620315
result: FAIL
error: VA_CLAIMS_CHAT_LLM_BRIDGE_FAIL:chat_truthful_inactive_label
```

`validate_va_claims_chat_llm_bridge.py` still requires the exact string `SOURCE-GROUNDED PROCEDURAL HELP`, while `validate_va_claims_chat_surface.py` explicitly forbids that same string as internal/governance-heavy veteran-facing copy. These assertions are mutually contradictory.

The bridge task `data/tasks/SITE-VA-COORDINATED-LLM-BRIDGE-002.json` is already `COMPLETE` / `RELEASED_COMPLETE_PENDING_RUNTIME_ACTIVATION` and records a prior stale-validator repair for governance-heavy veteran-facing copy. #434 does not own that validator path and will not bypass registry ownership to change it.

Durable continuation is Site issue #439: `Reconcile contradictory VA Claims Chat bridge/surface validators`. #439 must admit its own bridge-validator claim, preserve all fail-closed runtime checks, replace only the stale internal-label assertion, and prove both validators PASS on one exact head.

## Required retained validation

- `workflow_dispatch` retained;
- `pull_request` validation present;
- bounded `main` push validation present;
- all direct surface-validator inputs trigger validation;
- exact PR merge ref or push SHA fetched anonymously;
- credential-bearing environments fail closed;
- preinstalled Python used;
- existing surface validator executes unchanged;
- derived receipt PASS;
- private document upload remains false;
- automated filing remains false;
- public upload remains false;
- veteran submission authority remains preserved;
- authority and activation effects remain false;
- tracked receipt restored before completion, including failed attempts;
- repository writeback absent;
- artifact custody absent;
- GitHub-token production/runtime authority absent;
- TV/TVC remains credential authority;
- no Render.

## Collision boundaries

- `va-claims-chat.html` change is limited to removal of the exact forbidden internal technical-label paragraph proven by run `32608184362`; no other page semantics are in #434 scope.
- Do not mutate `scripts/validate_va_claims_chat_llm_bridge.py` under #434; Site #439 owns admission of that newly separated repair.
- Do not modify VACC provider/runtime/public activation semantics owned by Site #113 / Site #239 / LLM-adapter.
- Do not modify Site #116 secure-document semantics.
- Do not modify `.github/workflows/validate.yml` while Site #388 claims it.
- Do not modify #413 or #420 carrier paths.
- Preserve concurrently admitted claims and state-projection work.
- Workflow success is validation evidence only.

## Completion gate

#434 is not releasable yet. Its own repaired carrier and all primary Site gates pass, but merge remains correctly blocked until #439 repairs the contradictory stale bridge assertion and the regenerated PR head proves both Claims Chat validators pass together. After that, rebase #434 onto exact current `main`, rerun all gates, merge, record release evidence in this handoff and `data/session-work-claims.json`, and close Site #434. Merge or workflow success alone is not product activation.
