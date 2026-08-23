# VA Claims Chat Actions Fanout Mirror Handoff

Updated: 2026-08-23
Repository: `StegVerse-Labs/Site`
Issue: `#434`
Claim: `SITE-VA-CLAIMS-CHAT-CLOCK-RETIREMENT-434-R2-20260823`
Branch: `claim/site-va-claims-chat-clock-retirement-434-r2`
State: `VALIDATED_READY_FOR_INTEGRATION_NOT_RELEASED`

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

This Actions task changes validation transport only plus the one veteran-facing internal-label correction already required by the parent handoff. It grants no runtime, provider, custody, upload, filing, claimant, publication, or activation authority.

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

## Implemented repair

The reconstructed current-main branch now:

- removes the six-hour schedule;
- retains `workflow_dispatch`;
- adds pull-request validation;
- retains bounded `main` push validation;
- covers every direct surface-validator input, including runtime projection and runtime bridge;
- uses `permissions: {}`;
- refuses credential-bearing environments;
- fetches the exact PR merge ref or push SHA anonymously;
- uses preinstalled Python;
- runs the existing surface validator unchanged;
- validates the derived receipt ephemerally;
- restores the tracked receipt and proves no worktree persistence;
- removes repository commit/push writeback;
- removes GitHub artifact custody;
- removes the veteran-facing `SOURCE-GROUNDED PROCEDURAL HELP` internal capability label required to be hidden by the parent handoff.

## Consumed dependency output

Site #439 / PR #440 merged the independently owned bridge-validator consistency repair before this reconstruction. The bridge validator no longer requires the internal label that the surface validator forbids. No #439-owned runtime or product behavior is incorporated into this Actions task.

## Exact-head validation evidence

Reconstructed head before this handoff-only evidence commit:

```text
head: 9bdf7904f77d0295e71897ea939ff98e0954aec9
VA Claims Chat Surface Validation: 32611772672 SUCCESS
  job: 97125877853
VA Claims Chat LLM Bridge: 32611772675 SUCCESS
  job: 97125877896
Site Bootstrap Validate: 32611772671 SUCCESS
Ecosystem Heartbeat Orchestration: 32611772610 SUCCESS
Site Handoff Orchestrator: 32611772681 SUCCESS
```

The direct surface job proves credential refusal, anonymous exact-source acquisition, preinstalled Python, unchanged validator PASS, tracked-receipt restoration, repository writeback `NONE`, artifact custody `NONE`, and validation-only containment.

Because this handoff commit changes a trigger-covered evidence file, the resulting exact PR head must pass the same applicable gates before integration. Passing validation is not release; merge and terminal evidence remain required.

## Required retained validation

- `workflow_dispatch` retained;
- pull-request validation retained;
- bounded `main` push validation retained;
- all direct surface-validator inputs trigger validation;
- exact PR merge ref or push SHA fetched anonymously;
- credential-bearing environments fail closed;
- existing surface validator executes unchanged;
- bridge validator remains independently repaired and must pass on the same head;
- private document upload remains false;
- automated filing remains false;
- public upload remains false;
- veteran submission authority remains preserved;
- authority and activation effects remain false;
- repository writeback absent;
- artifact custody absent;
- GitHub-token production/runtime authority absent;
- TV/TVC remains credential authority;
- no Render.

## Collision boundaries

- Do not modify `scripts/validate_va_claims_chat_llm_bridge.py`; Site #439 owns that released repair.
- Do not modify VACC provider/runtime/public activation semantics owned by Site #113 / Site #239 / LLM-adapter.
- Do not modify Site #116 secure-document semantics.
- Do not modify `.github/workflows/validate.yml` while Site #388 claims it.
- Do not modify #413 or #420 carrier paths.
- Preserve concurrently admitted claims and state-projection work.
- Workflow success is validation evidence only.

## Completion gate

This repair is implemented and validated but is **not released** until the reconstructed PR head passes the post-handoff exact-head gates, integrates into `main`, the claim fragment is terminalized with exact merge evidence, the parent Actions cost-containment handoff advances its released accounting, and Site #434 closes completed. None of those states imply VACC product/runtime activation.
