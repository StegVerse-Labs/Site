# Two Entry Points Mirror Handoff

## Source of truth

This is the canonical Site continuation record for the originating two-entry-point session. Live repository state, current owner handoffs, claim registries, workflow runs/jobs/logs, receipts, deployments, and runtime observations override older claim timestamps and prior chat statements.

## Goal

```text
goal_id: TWO-ENTRY-POINTS-2026-08-02
originating_goal: Complete and activate two continuously extensible but fully functional public entry points
entry_points: Ecosystem Chat; VA Claim Assistant
repository: StegVerse-Labs/Site
canonical_branch: main
canonical_issue: Site#152
stale_claim_reconciliation: MERGED_INTO_CANONICAL_WORKSTREAM
reconciliation_pr: #373
reconciliation_merge: 792eff2396758761f94c2c062c5662f6e5132e4b
reconciliation_head: ef8275ae9d21a86ca0e6b175c097abc2eb49b43e
active_chat_support_claim: NONE
product_authority_effect: NONE
```

## Canonical current owners

### Ecosystem Chat

```text
runtime/provider transport: StegVerse-org/LLM-adapter#18
runtime handoff: StegVerse-org/LLM-adapter/LLM_ADAPTER_MIRROR_HANDOFF.md
canonical local model/runtime: StegVerse-002/micro-node-runtime#16/#22
sovereign carrier lifecycle: StegVerse-Labs/.github#60 / SHWP-ECOSYSTEM-CHAT-INFERENCE-001
route authority: StegVerse-Labs/TVC
custody/reconstruction: master-records/orchestration
Site activation/projection: StegVerse-Labs/Site#24/#239/#242 + docs/SITE_MIRROR_HANDOFF.md
downstream after verified activation: Publisher + admissibility-wiki + stegguardian-wiki
```

Repository-local adapter implementation, formal local-model/runtime implementation, persistent local endpoint proof, and same-carrier executor implementation are complete/released. The remaining gap is direct machine-owned same-carrier runtime observation, provider-usage custody/reconstruction, same-execution transition reconstruction, immutable zero-blocker activation receipt, Site activation, and downstream ingestion. No chat or Site validation claim may substitute for those observations.

### VA Claim Assistant

```text
Guide / public Site coordination: Site#113
secure-document lifecycle: Site#116 + #178-#184
claimant/submission binding: Site#180
provider runtime: StegVerse-org/LLM-adapter#90
custody/reconstruction: master-records/orchestration#15
canonical Site handoff: docs/VA_CLAIM_ASSISTANT_MIRROR_HANDOFF.md
```

Current VA posture remains fail-closed: deterministic Guide complete; coordinated LLM path blocked at authorized real-provider execution; secure-document contracts/privacy preprocessing partially complete with public private-document activation disabled; official VA.gov submission fallback complete. The veteran remains claimant/fact confirmer/certifier/submission authority unless an independently authorized representative acts within scope.

## Reconciliation evidence — COMPLETE / RELEASED

The earlier handoff said the hosted two-entry validation workflow had not been observed. Live history proved 64 hosted runs. The latest pre-repair scheduled run was directly inspected:

```text
run: 32032867908
job: 95396593477
conclusion: FAILURE
stale_claims: ECP-001, ECP-002, VACP-001, CONS-001
failure_reason: all four legacy active claims expired on 2026-08-03
```

The failure was correct fail-closed behavior. PR #373 then reconciled current ownership without renewing any expired product claim.

Exact final-head validation after preserving all required StegFin release anchors:

```text
Two Entry Points Execution State: 32057353466 SUCCESS
receipt result: PASS
stale_claims: none
errors: none
receipt_sha256: 16449c36a21ba316a2ed705b40dbb788d183eb6ad8bb198d5eb4f5d65f2f4959
authority_granted: false
release_authorized: false
Site Handoff Orchestrator: 32057353527 SUCCESS
Ecosystem Heartbeat Orchestration: 32057353465 SUCCESS
Site Bootstrap Validate: 32057353481 SUCCESS
Check StegFin Phone Projection: 32057353472 SUCCESS
branch divergence immediately before merge: 4 ahead / 0 behind
merge: 792eff2396758761f94c2c062c5662f6e5132e4b
support claim release: 7a34f676bb7e6034059adaf74294c005f7fe05c0
execution-state release: aafa592c46ed6bedf1684566294ceecbc04f4f4a
```

A first PR-head validation also proved the registry repair itself but exposed missing compacted StegFin history anchors. StegFin correctly failed; those immutable release anchors were restored rather than weakening the StegFin validator. The corrected exact head then passed all five required groups.

## Current execution registry

Canonical machine state: `data/two-entry-points-execution-state.json`.

```text
ECP-001: BLOCKED
  canonical continuation: LLM-adapter#18 + sovereign carrier + TVC + Master Records
  blocker: real same-carrier provider execution and custody/reconstruction not observed

ECP-002: BLOCKED
  canonical continuation: Site activation integration
  blocker: immutable zero-blocker upstream VERIFIED receipt absent

VACP-001: BLOCKED
  canonical continuation: Site#113/#116 + LLM-adapter#90 + master-records#15
  blocker: authorized real-provider execution and required custody/runtime evidence incomplete

CONS-001: MERGED_INTO_CANONICAL_WORKSTREAM
  completion: MERGED
  hosted validation: PASS
  active chat claimant: NONE
```

The three expired product claims were not renewed. Their blockers, machine-observable release conditions, and current owners are explicit. The reconciliation support role is released and may not become a standing product owner.

## Validation and automation

```text
validator: scripts/validate_two_entry_points_execution_state.py
observer: .github/workflows/two-entry-points-execution-state.yml
```

The validator continues to reject duplicate IDs, stale active claims, collisions, unsupported completion, false archival, authority escalation, incomplete fields, and handoff-only transfer claims.

The observer currently uses GitHub `contents: write`, persisted checkout credentials, setup-python, repository writeback, and artifact transport. Those mechanics are **not product authority**, but they remain a separate Site #268 cost-containment candidate now that stale ownership is repaired. Any cleanup must preserve deterministic validation/receipt integrity and may not alter ECP/VACP product ownership.

## Collision and authority boundaries

- Do not implement, launch, or activate Ecosystem Chat runtime from this coordination record.
- Do not duplicate local-model/runtime, sovereign carrier, TVC route, or Master Records work.
- Do not implement or activate VACC provider/private-document runtime here.
- Do not touch active StegOS/HIL/wallet authority surfaces.
- No NON-TV/TVC secret/token.
- No Render production path.
- Validation or receipt success grants no deployment, execution, publication, adjudication, filing, custody, medical, representation, wallet, or release authority.

## Session consolidation

The stale-claim reconciliation contains no remaining unique chat-owned implementation, validation, integration, propagation, or observation responsibility. Product continuation is fully transferred to the canonical owners above.

```text
reconciliation_session: MERGED_INTO_CANONICAL_WORKSTREAM
chat_only_reconciliation_requirements_remaining: 0
Ecosystem Chat product activation: BLOCKED / MACHINE_OWNED RUNTIME OBSERVATION
VA Claim Assistant product activation: PARTIAL / BLOCKED AT GOVERNED PROVIDER + DOCUMENT GATES
project_archive_state: ACTIVE_DISTINCT_SUPPORT_WORK_REMAINS because product work remains with canonical owners
```

MERGED INTO: `StegVerse-Labs/Site/docs/TWO_ENTRY_POINTS_MIRROR_HANDOFF.md` + `data/two-entry-points-execution-state.json` + current product-owner handoffs named above.
