# Site Mirror Handoff

## Purpose

This file is the current source of truth for continuing `StegVerse-Labs/Site` without prior chat context.

## Current goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat
Phase: governed-transition-observatory-installed
Primary surface: ecosystem-chat.html
New operational projection: governed-transitions.html
Site remains preview-only
Live backend: not installed
Site local mode: true
Live provider invocation: false
Live solver execution: false
Live signatures: false
Verified receipt issuer: false
Workflow standard: exactly two active workflows
```

## Governed transition observatory

Installed:

```text
governed-transitions.html
assets/governed-transitions.js
data/governed-transition-index.json
scripts/check_governed_transition_observatory.py
scripts/run_site_task.py
```

The page consumes the canonical projection shape derived from:

```text
master-records/orchestration/schemas/governed.transition.relationship.schema.json
master-records/orchestration/schemas/governed.transition.index.schema.json
```

Current displayed relationship classes include:

```text
transition_id and run_id
origin event and manifest
repository, actor, task, and handoff
parent transition and previous receipt
admissibility and commit-time validity
verification and final receipt
Master-Records custody status
reconstruction status
next task
visibility and redaction class
```

The checked-in data is a projection fixture. It is not a live Master-Records feed and does not prove custody or reconstruction.

## Current cross-repository path

```text
StegVerse-SDK / LLM-adapter
  -> emit DECLARED canonical candidates

hybrid-collab-bridge
  -> preserve identity and attach bridge evidence

Ecosystem-Delegation
  -> preserve identity and attach delegation references

master-records/orchestration
  -> verify bounded intake
  -> govern lifecycle, final receipt, custody, reconstruction
  -> generate Site projection

StegVerse-Labs/Site
  -> render the bounded projection only
```

## Installed Ecosystem Chat capabilities

```text
single governed chat entry
local route and transition-intent classification
INTRA / INTER / RESEARCH / PROVIDER / SOLVER / RECEIPT bands
fixture-bound HPS visualization
bounded request-to-receipt traversal preview
provider, quota, usage, cost, latency, and fallback previews
governed solver fixture
negative and positive authority handshake previews
execution dry-run preview
backend-shaped authority and execution receipt envelopes
local SDK manifest and receipt-window previews
restricted-admin fail-closed routing
```

## Documentation mesh

```text
Endpoint registry: data/ecosystem-documentation-endpoints.json
Cross-wiki health: data/cross-wiki-health-status.json
Validator: scripts/check_documentation_mesh_status.py
State: pending_live_peer_checks
```

## Non-negotiable public boundary

```text
Site may draft, classify, visualize, and offer governed transition destinations.
Site must not execute shell commands, access credentials, mutate repositories, grant admissibility, sign receipts, verify receipt issuers, issue governing receipts, or claim Master-Records custody.
A projection is not the source of truth.
Authority ALLOW remains distinct from execution.
Commit-time validity remains distinct from state change.
Receipt structure remains distinct from cryptographic proof.
Site remains preview-only until a governed backend independently validates transitions and issues verified receipts.
```

## Validation surface

```text
python scripts/check_governed_transition_observatory.py
python scripts/run_site_task.py validate
python scripts/run_site_task.py public-guard
python scripts/run_site_task.py all-local
```

The observatory validator is registered in both `validate` and `public-guard` through the existing task runner.

## Workflow standard

```text
Active workflow 1: .github/workflows/validate.yml
Active workflow 2: .github/workflows/site-task-runner.yml
```

No additional workflow may be created for the transition observatory. Validators and tasks remain behind these two stable workflows.

## Next task

```text
1. Verify Site validate and public-guard with the observatory installed.
2. Add a generated-data handoff from master-records/orchestration without making Site the source of truth.
3. Add live URL verification for governed-transitions.html after deployment.
4. Replace projection fixtures with receipted generated artifacts when orchestration output is available.
5. Add Master-Records custody and reconstruction references only when independently recorded.
6. Continue Phase 12 canonical receipt payload and signature-verification preview contracts without enabling Site signing.
```

## Downstream publication targets after Site validation

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
StegVerse-Labs/Sit
```

## Handoff instruction

Continue from this file before relying on prior chat context. The complete thread is ready for archiving; no additional part of the thread is required.
