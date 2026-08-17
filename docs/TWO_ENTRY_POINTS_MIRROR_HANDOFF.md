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
current_support_claim: SITE-TWO-ENTRY-POINTS-STALE-CLAIM-RECONCILIATION-20260817
support_branch: claim/site-two-entry-stale-claim-reconciliation-20260817
support_role: VALIDATION_RECONCILIATION
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

## Hosted execution evidence and stale-claim finding

The earlier handoff incorrectly stated that the hosted two-entry validation workflow had not been observed. Live workflow history now proves 64 hosted runs.

Latest inspected run:

```text
workflow: Two Entry Points Execution State
run: 32032867908
job: 95396593477
head: e53fe54d617bc4ae6a314ad73e602940e0bf213c
event: schedule
conclusion: FAILURE
validator_result: FAIL
stale_claims: ECP-001, ECP-002, VACP-001, CONS-001
failure_reason: active_claim_stale for all four 2026-08-02 claims
```

The failure is a correct fail-closed result. The prior active claims expired on 2026-08-03 and were never validly renewed by new evidence. The workflow also currently uses `contents: write`, persisted checkout credentials, setup-python, writeback, and artifact transport; those mechanics are a separate cost-containment concern and are not changed by this reconciliation.

## Reconciled execution registry

Canonical machine state: `data/two-entry-points-execution-state.json`.

```text
ECP-001: BLOCKED
  successor owner: LLM-adapter#18 + sovereign carrier/TVC/Master Records chain
  blocker: real same-carrier provider execution and custody/reconstruction not observed

ECP-002: BLOCKED
  successor owner: Site activation integration
  blocker: immutable zero-blocker upstream VERIFIED receipt absent

VACP-001: BLOCKED
  successor owners: Site#113/#116 + LLM-adapter#90 + master-records#15
  blocker: authorized real-provider execution and required custody/runtime evidence incomplete

CONS-001: CLAIMED_FOR_VALIDATION
  claimant: SITE-TWO-ENTRY-POINTS-STALE-CLAIM-RECONCILIATION-20260817
  expires: 2026-08-18T13:50:00-05:00
  scope: stale-claim reconciliation and hosted validator proof only
```

The three expired product claims were **not renewed**. `BLOCKED` preserves their exact owner, blocker, release condition, and next action without pretending this session owns implementation. Only the distinct reconciliation role receives a fresh bounded claim.

## Validation contract

```text
python scripts/validate_two_entry_points_execution_state.py
```

The validator must continue to reject duplicate IDs, unsupported completion, stale active claims, claim collisions, false archival, authority escalation, incomplete required fields, and handoff-only transfer claims. Required task IDs remain `ECP-001`, `ECP-002`, `VACP-001`, and `CONS-001`.

Required release evidence for the current support claim:

1. `data/two-entry-points-execution-state.json` validates PASS with `stale_claims: []`.
2. Pull-request hosted workflow succeeds and receipt hash/authority checks pass.
3. Site pre-work claim validation, Site Handoff Orchestrator, Ecosystem Heartbeat, Site Bootstrap, and StegFin projection remain PASS where triggered.
4. Branch is current with `main` immediately before merge.
5. Claim is released after merge and this handoff records final evidence.

## Collision boundaries

- Do not implement, launch, or activate Ecosystem Chat runtime from this support lane.
- Do not duplicate formal local-model/runtime, sovereign carrier, TVC route, or Master Records work.
- Do not implement or activate VACC provider/private-document runtime from this support lane.
- Do not touch active StegOS/HIL/wallet authority surfaces.
- No NON-TV/TVC secret/token may be introduced or exposed.
- No Render production path.
- Validation/receipt success grants no deployment, execution, publication, adjudication, filing, custody, medical, representation, or release authority.

## Automation and continuation

`.github/workflows/two-entry-points-execution-state.yml` remains the repository-native observer for this coordination registry during reconciliation. Its product-independent CI/token/writeback cleanup is not part of the present claim and must be handled only through a separate collision-free Site #268 remediation after this owner state is stable.

Product continuation remains entirely with the canonical owners above. Once `CONS-001` reconciliation is validated and integrated, this support claim must release; it must not become a standing product owner.

## Completion / archival posture

The originating session requirements are durably represented, but the two products are not both activated. Therefore product goal completion and archive readiness must not be inferred from this reconciliation.

```text
Ecosystem Chat activation: BLOCKED / MACHINE_OWNED RUNTIME OBSERVATION
VA Claim Assistant activation: PARTIAL / BLOCKED AT GOVERNED PROVIDER + DOCUMENT GATES
cross-entry stale-claim reconciliation: ACTIVE DISTINCT SUPPORT ROLE
archive_state: ACTIVE_DISTINCT_SUPPORT_WORK_REMAINS
```

MERGED INTO canonical continuation after reconciliation: `StegVerse-Labs/Site/docs/TWO_ENTRY_POINTS_MIRROR_HANDOFF.md` + `data/two-entry-points-execution-state.json` + current product-owner handoffs named above.
