# Two Entry Points Mirror Handoff

## Source of truth

This file is the canonical continuation record for the two public entry points established by the originating session. Live repository state, issue state, workflow runs, receipts, deployments, and runtime observations override prior chat statements.

## Active goal and goal ID

```text
goal_id: TWO-ENTRY-POINTS-2026-08-02
active_goal: Complete and activate two continuously extensible but fully functional public entry points
entry_points:
  - Ecosystem Chat
  - VA Claim Assistant
repository: StegVerse-Labs/Site
branch: main
canonical_issue: StegVerse-Labs/Site#152
```

Originating session goal: neither surface may be represented as complete until its intended end-to-end path is installed, validated, integrated, activated, and durably owned.

## Canonical continuation locations

```text
Cross-entry coordination:
  StegVerse-Labs/Site#152
  docs/TWO_ENTRY_POINTS_MIRROR_HANDOFF.md
  data/two-entry-points-execution-state.json
  scripts/validate_two_entry_points_execution_state.py
  .github/workflows/two-entry-points-execution-state.yml

Ecosystem Chat runtime:
  StegVerse-org/LLM-adapter#18
  StegVerse-org/LLM-adapter/LLM_ADAPTER_MIRROR_HANDOFF.md

Ecosystem Chat Site activation:
  StegVerse-Labs/Site#24
  StegVerse-Labs/Site/docs/SITE_MIRROR_HANDOFF.md

VA Claim Assistant:
  StegVerse-Labs/Site#113
  docs/VA_CLAIM_ASSISTANT_GOVERNED_SESSION.md
  data/va-claim-assistant/source-registry.json
```

## Transfer rule

Work is transferred only when a named executor has accepted a bounded claim, has mutation authority, and produces inspectable commits, runs, logs, artifacts, deployments, or receipts. A handoff alone never proves transfer or execution.

## Claim policy

All active claims are bounded to 24 hours without new inspectable evidence. Renewal requires a new commit, workflow run, artifact, receipt, deployment observation, or issue-state change. A stale claim is invalid and must be blocked and released for reclaim rather than silently renewed.

The machine-readable source is `data/two-entry-points-execution-state.json`. The validator rejects:

- duplicate task IDs;
- missing owners, evidence, blockers, release conditions, or next actions;
- unbounded or expired active claims;
- duplicate collision-boundary ownership;
- unsupported completion;
- unsupported merge or archive state;
- authority escalation;
- treatment of a handoff as transfer evidence.

## Active claims

### ECP-001 — Ecosystem Chat runtime activation

```text
repository: StegVerse-org/LLM-adapter
branch: main
owner: issue #18 and repository-native activation workflows
role: implementation and validation
claim_state: MACHINE_OWNED
completion_state: BLOCKED
claim_expires_at: 2026-08-03T08:35:00Z
blocker: no verified authorized persistent runtime supplies provider and Master-Records configuration and exposes a healthy endpoint
machine release condition: receipts/ecosystem-chat-live-activation.verified.json has state VERIFIED and blockers []
next task: ECP-002 imports and validates the immutable adapter receipt
```

### ECP-002 — Ecosystem Chat Site activation and propagation

```text
repository: StegVerse-Labs/Site
branch: main
owner: issue #24
role: integration
claim_state: CLAIMED_FOR_INTEGRATION
completion_state: BLOCKED
claim_expires_at: 2026-08-03T08:35:00Z
blocker: adapter immutable verified receipt is absent
machine release condition: adapter immutable receipt exists and Site activation validator reports ACTIVATION_COMPLETE
next task: verify Publisher, admissibility-wiki, and stegguardian-wiki ingestion receipts
```

### VACP-001 — VA governed claim session

```text
repository: StegVerse-Labs/Site
branch: main
owner: issue #113
role: implementation
claim_state: CLAIMED_FOR_IMPLEMENTATION
completion_state: PARTIALLY_IMPLEMENTED
claim_expires_at: 2026-08-03T08:35:00Z
blocker: governed retrieval, document-aware session, TVC capability, custody, and reconstruction chain remain incomplete
machine release condition: VA activation receipt validates with all ten gates true and blockers []
next task: derive public capability status from the verified activation receipt
```

### CONS-001 — Cross-session consolidation

```text
repository: StegVerse-Labs/Site
branch: main
owner: issue #152
role: integration and validation
claim_state: CLAIMED_FOR_INTEGRATION
completion_state: IN_PROGRESS
claim_expires_at: 2026-08-03T08:35:00Z
blocker: hosted validator workflow run and retained receipt have not yet been observed
machine release condition: reports/two-entry-points-execution-state-validation.json reports PASS and hosted workflow evidence exists
next task: reclassify this session only after no unique execution responsibility remains
```

## Installed coordination controls

```text
commit 98f441b01caf9940f6a5230047b73886a0928a32
  created this canonical handoff

commit 59aa5c1d0e768aafdd25a9908c57d77c885f82e7
  created the machine-readable execution registry

commit 3dc00412492ee6fd9ca38a575746fb6e4801242a
  installed the fail-closed execution-state validator

commit fc208fb133359880a9aa8a51e8c4ce2859c68e27
  installed push, pull-request, scheduled, and manual validation workflow

commit 922041b37d76a11b78c3af6cf405c5e2c3118fd6
  added bounded claims, collision boundaries, expected evidence, and post-release routing

commit ada55f96fb525c0efcc98468ecf86a1816f311a0
  enforced claim expiration, stale-claim failure, false completion rejection, and archive gating
```

## Automation behavior

Workflow `.github/workflows/two-entry-points-execution-state.yml` runs on relevant pushes and pull requests, every six hours, and explicit dispatch. It:

1. validates the canonical registry;
2. produces `reports/two-entry-points-execution-state-validation.json`;
3. validates the receipt hash and authority boundary;
4. commits the receipt on `main` when changed;
5. uploads registry and receipt evidence;
6. publishes task and archive posture in the workflow summary.

The workflow has not yet been proven successful by an inspected hosted run. File installation is not workflow success.

## Required Ecosystem Chat capability

- governed request and real provider response;
- durable provider-usage persistence;
- authenticated provider-usage custody;
- transition custody;
- reconstruction PASS for both chains;
- immutable zero-blocker activation receipt;
- Site activation;
- verified Publisher, admissibility-wiki, and stegguardian-wiki propagation.

## Required VA Claim Assistant capability

- bounded procedural guide retained;
- source-authority registry and freshness/supersession checks;
- claim-route classification;
- proposition-level provenance and citations;
- source fact, user-record fact, inference, contradiction, and uncertainty separation;
- document identity, page anchors, hashes, privacy classes, and contradiction extraction;
- TVC-scoped provider/source execution;
- Master-Records custody and reconstruction;
- deployed end-to-end governed claim session;
- exact public capability status derived from verified evidence.

## Validation commands

```bash
python scripts/validate_two_entry_points_execution_state.py
python -m json.tool data/two-entry-points-execution-state.json >/dev/null
python -m json.tool reports/two-entry-points-execution-state-validation.json >/dev/null
```

## Cross-repository dependencies and propagation

```text
StegVerse-org/LLM-adapter
  produces immutable Ecosystem Chat activation receipt

StegVerse-Labs/TVC and TV
  provide scoped VA provider/source execution and capability admission

master-records/orchestration
  provides provider-usage, transition, document, and session custody/reconstruction

StegVerse-Labs/Site
  imports verified receipts and exposes exact public capability status

GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
  receive verified downstream projections only after Site activation
```

No propagation is claimed merely because destinations are named.

## Duplicate and supersession record

- Site issue `#153` was closed as duplicate of canonical issue `#152`.
- Site issues `#154` and `#155` were accidental empty issues, closed as not planned, and own no work.
- Existing issues `LLM-adapter#18`, `Site#24`, and `Site#113` remain canonical implementation lanes and are not replaced by issue `#152`.

## Authority boundary

No handoff, task claim, workflow, monitor, provider output, receipt, custody event, reconstruction result, or public display independently grants deployment, adjudication, medical, representation, publication, release, or execution authority.

## Completion percentages

Denominators cover nine shared coordination and activation-control deliverables, eight validation classes, seven integrations, and four originating session goals.

```text
developed files: 7/9
validation: 3/8 installed or statically inspectable; hosted execution unobserved
integration: 2/7
session consolidation: 4/4 requirements durably represented
goal activation: Ecosystem Chat pending; VA Claim Assistant building
```

## Incomplete work

```text
StegVerse-Labs/Site
  reports/two-entry-points-execution-state-validation.json — not yet observed from hosted workflow
  hosted workflow run, jobs, logs, and artifact — not yet inspected
  Ecosystem Chat Site ACTIVATION_COMPLETE — not observed
  Publisher/wiki ingestion receipts — not observed
  VA source-grounded and document-aware session — incomplete

StegVerse-org/LLM-adapter
  authorized persistent endpoint — not verified
  real provider-use receipt — not verified
  provider-usage custody and reconstruction — not verified
  transition custody and reconstruction — not verified
  immutable zero-blocker activation receipt — not observed

StegVerse-Labs/TVC / TV
  VA scoped source/provider capability receipt — not observed

master-records/orchestration
  VA document/session custody and reconstruction receipts — not observed
```

## Session consolidation state

All unique requirements introduced in the originating session are now represented in issue `#152`, this handoff, and the machine registry. That preservation does not complete or transfer unfinished implementation. This session still owns the distinct validation and consolidation role until the hosted registry workflow is observed and its claim is either completed or actually transferred.

## Archive conditions

This workstream is not complete until both entry points are activated or every incomplete item is actually transferred to separately verified active executors. Documentation without active execution is insufficient. No archive state may be asserted while any archival-dependent task remains nonterminal or any active claim is stale, unvalidated, or unsupported by evidence.
