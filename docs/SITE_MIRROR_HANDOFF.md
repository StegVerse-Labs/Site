# Site Mirror Handoff

## Purpose

This file is the current source of truth for continuing the StegVerse-Labs/Site build without prior chat context.

## Current Goal

```text
Goal: unified governed Site experience centered on Ecosystem Chat as the primary operating surface
Repository: StegVerse-Labs/Site
Primary surface: ecosystem-chat.html
Activation state: phase_11_backend_receipt_envelope_previews_installed
Live backend state: not installed
Site local mode: preserved true
Live provider invocation: false
Live solver execution: false
Authority preview states: DENY and ALLOW fixtures installed
Execution preview state: DRY_RUN_ONLY
State change: false
Receipt envelope state: backend-shaped previews installed
Live signatures: false
Verified receipt issuer: false
Workflow standard: exactly two active workflows
Documentation mesh state: shared endpoint registry and Site cross-wiki health record installed
Site remains preview-only
```

## Installed Ecosystem Chat capabilities

```text
- single primary governed chat entry
- local route and transition-intent classification
- contextual continuation panel
- INTRA / INTER / RESEARCH / PROVIDER / SOLVER / RECEIPT interaction bands
- fixture-bound HPS heartbeat and standing visualization
- bounded request-to-receipt traversal preview
- fixture-bound provider routing, fallback, quota, usage, cost, and latency visualization
- governed solver fixture with proof steps, units, verification, and resource limits
- negative authority handshake: DENY + NOT_ATTEMPTED
- positive authority evaluation: ALLOW + NOT_ATTEMPTED
- execution-transition dry run consuming ALLOW authority input
- commit-time revalidation of identity, delegation, policy, evidence freshness, operation allowlist, and resource limits
- authority input explicitly insufficient for execution by itself
- execution state explicitly DRY_RUN_ONLY with no state change
- backend-shaped authority receipt envelope preview
- backend-shaped execution receipt envelope preview
- authority and execution receipt artifacts remain distinct
- preview-shaped SHA-256 digests with null signatures, null key IDs, and unverified issuers
- receipt bindings include policy, evidence, validity, replay, reconstruction, resource use, state change, and supersession posture
- Site receipt issuance remains false
- local mode preserved through all previews
- local SDK manifest and receipt-window previews
- restricted-admin fail-closed routing
```

## Documentation Mesh

```text
Endpoint registry: data/ecosystem-documentation-endpoints.json
Cross-wiki health: data/cross-wiki-health-status.json
Validator: scripts/check_documentation_mesh_status.py
Validation surfaces: scripts/run_site_task.py validate and public-guard
Current health state: pending_live_peer_checks
```

Canonical endpoints:

```text
https://stegverse-labs.github.io/Site/
https://stegverse-labs.github.io/admissibility-wiki/
https://stegverse-002.github.io/stegguardian-wiki/
https://stegverse-labs.github.io/stegtalk-wiki/
```

Documentation discovery and health records do not grant authority, execution standing, admissibility, receipt standing, or cross-repo control.

## Built files central to the current phase

```text
ecosystem-chat.html
assets/ecosystem-chat.js
assets/ecosystem-chat-hps.js
assets/ecosystem-chat-traversal.js
assets/ecosystem-chat-provider.js
assets/ecosystem-chat-solver.js
fixtures/ecosystem-chat/hps-visualization-status.example.json
fixtures/ecosystem-chat/provider-status.example.json
fixtures/ecosystem-chat/solver-response.example.json
fixtures/ecosystem-chat/authority-handshake-request.example.json
fixtures/ecosystem-chat/authority-handshake-response.example.json
fixtures/ecosystem-chat/authority-handshake-positive-request.example.json
fixtures/ecosystem-chat/authority-handshake-positive-response.example.json
fixtures/ecosystem-chat/execution-transition-request.example.json
fixtures/ecosystem-chat/execution-transition-response.example.json
fixtures/ecosystem-chat/authority-receipt-envelope.example.json
fixtures/ecosystem-chat/execution-receipt-envelope.example.json
data/ecosystem-documentation-endpoints.json
data/cross-wiki-health-status.json
scripts/check_ecosystem_chat_boundary.py
scripts/check_ecosystem_chat_traversal.py
scripts/check_ecosystem_chat_provider_status.py
scripts/check_ecosystem_chat_solver_response.py
scripts/check_ecosystem_chat_authority_handshake.py
scripts/check_ecosystem_chat_positive_authority.py
scripts/check_ecosystem_chat_execution_transition.py
scripts/check_ecosystem_chat_receipt_envelopes.py
scripts/check_site_hps_visualization.py
scripts/check_site_unified_governed_experience.py
scripts/check_documentation_mesh_status.py
scripts/run_site_task.py
docs/hps/ecosystem-chat-visualization.md
docs/ECOSYSTEM_CHAT_PROVIDER_STATUS.md
docs/ECOSYSTEM_CHAT_SOLVER_STATUS.md
docs/ECOSYSTEM_CHAT_AUTHORITY_HANDSHAKE.md
docs/ECOSYSTEM_CHAT_EXECUTION_TRANSITION.md
docs/ECOSYSTEM_CHAT_RECEIPT_ENVELOPES.md
docs/SITE_MIRROR_HANDOFF.md
.github/workflows/validate.yml
.github/workflows/site-task-runner.yml
```

## Non-negotiable public boundary

```text
Site may draft, classify, visualize, and offer governed transition destinations.
Site must not execute shell commands, access credentials, mutate repositories, grant admissibility, sign receipts, verify receipt issuers, or issue governing receipts.
A local hash or preview digest must not be described as an authority-issued receipt or live signature.
HPS, traversal, provider, solver, authority-handshake, execution-transition, and receipt-envelope inputs must fail closed when preview contracts are not satisfied.
Provider fixture values must not be described as live provider state, current pricing, actual billing, account quota, or model availability.
Solver fixture values must not be described as live execution or independent verification.
Handshake, execution, or receipt schema existence must not be treated as backend activation.
Authority ALLOW must remain distinct from execution.
Commit-time revalidation PASS must remain distinct from state change.
Receipt structure must remain distinct from cryptographic proof.
Payment, quota, provider availability, solver correctness, endpoint registration, or documentation health must never be treated as execution standing.
```

## Validation surface

```text
python scripts/run_site_task.py validate
python scripts/check_ecosystem_chat_application.py
python scripts/check_ecosystem_chat_boundary.py
python scripts/check_ecosystem_chat_traversal.py
python scripts/check_ecosystem_chat_provider_status.py
python scripts/check_ecosystem_chat_solver_response.py
python scripts/check_ecosystem_chat_authority_handshake.py
python scripts/check_ecosystem_chat_positive_authority.py
python scripts/check_ecosystem_chat_execution_transition.py
python scripts/check_ecosystem_chat_receipt_envelopes.py
python scripts/check_site_hps_visualization.py
python scripts/check_site_unified_governed_experience.py
python scripts/check_documentation_mesh_status.py
python scripts/run_site_task.py public-guard
python scripts/run_site_task.py all-local
```

The consolidated task runner includes receipt-envelope validation in both `validate` and `public-guard`.

## Workflow standard

```text
Active workflow 1: .github/workflows/validate.yml
Active workflow 2: .github/workflows/site-task-runner.yml

Do not create additional workflows for HPS, traversal, provider, solver, authority, execution, receipt, or documentation-mesh work. Add validators and declared tasks behind the two stable workflows.
```

## Latest CI handling

```text
Event: Site Bootstrap Validate failure
Run: 29140167458
Commit: 5cbd5475907cb6bce6fe8ea33135f119c5651ccb
Job: bootstrap-validate
Failure class: exact public-boundary declaration mismatch
Observed failures:
- docs/media/media-pipeline-overview.md missing "does not claim live microphone use"
- docs/SITE_MIRROR_HANDOFF.md missing "Site remains preview-only"
Repair commit 1: 24d2e3f9b5d73fa957db70547008acb4dd14a24e
Repair posture: bounded documentation-only clarification; no activation, deployment, signing, release, or authority change
Verification: pending canonical workflow run on current main
Next task after green verification: continue Phase 12 canonical receipt payload and signature-verification preview contracts
```

## Remaining targets

### StegVerse-Labs/Site

```text
1. Verify validate and all-local on the current main branch.
2. Confirm GitHub Pages publishes HPS, traversal, provider, solver, endpoint-registry, and cross-wiki health surfaces.
3. Define actual receipt canonicalization and signature-verification contracts without enabling Site signing.
4. Define live provider response provenance and pricing-source requirements.
5. Define live solver operation allowlist, independent verification posture, and receipt path.
6. Do not change STEGVERSE_LOCAL_MODE until a governed backend independently validates authority and execution at commit time and issues verified receipts.
7. Do not update public verification JSON until the live URL checker confirms deployed state.
```

### StegVerse-org/StegVerse-SDK

```text
- ingest interaction profile and bands
- ingest HPS, provider, solver, authority, execution, and receipt posture
- independently reconstruct identity, delegation, policy, evidence freshness, operation allowlisting, resource limits, recoverability, and actual resource use
- canonicalize and verify receipt envelopes using governed backend keys
- keep authority and execution receipts separate
- return explicit authority, execution, provider, solver, pricing, state-change, rollback, signature, issuer, and supersession results
```

### StegVerse-org/LLM-adapter

```text
- implement bounded provider-routing contract
- provide quota and free-tier counters with provenance
- provide cost and latency accounting schema
- provide fallback posture
- preserve no-capability-by-payment governance rule
```

### Documentation mesh destinations

```text
Installed:
- StegVerse-Labs/Site
- StegVerse-Labs/admissibility-wiki
- StegVerse-002/stegguardian-wiki
- StegVerse-Labs/stegtalk-wiki

Next:
- verify all four public registry and health-record URLs
- compare record schemas and report drift
- promote reusable documentation-mesh standard to StegVerse-Labs/repo-standards
```

### Downstream publication targets

```text
GCAT-BCAT-Engine/Publisher: publication/import awareness after Site validation
StegVerse-Labs/admissibility-wiki: downstream implementation summary after Site validation
stegguardian-wiki: boundary and authority summary after Site validation
StegVerse-Labs/Sit: integration status after Site validation
```

## Next integration goal

```text
Phase 12: canonical receipt payload and signature-verification preview contracts.

Add canonical payload fixtures, digest recomputation checks, governed key metadata, signature-verification result posture, expiry/revocation fields, and fail-closed handling. Do not include or claim a live private key or valid production signature.
```

## Handoff instruction

Continue from this file before relying on prior conversation context. The complete thread is ready for archiving; no additional part of the thread is needed to move forward.
