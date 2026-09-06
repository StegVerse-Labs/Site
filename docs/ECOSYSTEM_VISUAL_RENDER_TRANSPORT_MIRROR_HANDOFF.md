# Ecosystem Visual Render Transport Mirror Handoff

Repository: `StegVerse-Labs/Site`  
Issue: `#1015`  
Pull request: `#1053`  
Branch: `feat/ecosystem-visual-render-transport-1015-r2`  
State: `SOURCE_IMPLEMENTED_VALIDATED / READY_TO_MERGE / LIVE_RENDERER_NOT_INTEGRATED`  
Authority effect: `NONE_PROJECTION_TRANSPORT_ONLY`

## Source of truth

This is the focused continuation record for Site #1015. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`. The completed predecessor contract is `docs/ECOSYSTEM_VISUAL_PROJECTION_MIRROR_HANDOFF.md` / Site #1007 / merge `8112e3609cde4bdddbae010054f2bb0bff876f1e`.

The original branch `feat/ecosystem-visual-render-transport-1015` became stale relative to current main and is superseded by this current-main successor branch for the same task/claim identity.

## Goal

Define the provider-neutral request/receipt transport contract between a canonical `stegverse.ecosystem_visual_projection/v1` document and an optional renderer, including an AI SiteFlow-compatible Next.js/WebGL/realtime-3D renderer, without giving the renderer semantic, admission, transition, identity, credential, custody, publication, or execution authority.

## Machine preflight

`docs/ECOSYSTEM_VISUAL_RENDER_TRANSPORT_PREFLIGHT.md` records `PASS / ADMIT_ON_CURRENT_MAIN_SUCCESSOR_BRANCH`.

README impact is `README_UPDATE_REQUIRED` because this task adds a repository-level interface and failure/authority semantics. `README.md` is included in the claim and updated in PR #1053.

## Implemented source

```text
schemas/ecosystem-visual-render-request.schema.json
schemas/ecosystem-visual-render-receipt.schema.json
assets/ecosystem-visual-render-transport.js
tests/ecosystem-visual-render-transport.test.cjs
scripts/check_ecosystem_visual_render_transport.py
.github/workflows/ecosystem-visual-render-transport-validate.yml
data/session-work-claims.d/site-ecosystem-visual-render-transport-1015.json
docs/ECOSYSTEM_VISUAL_RENDER_TRANSPORT_MIRROR_HANDOFF.md
docs/ECOSYSTEM_VISUAL_RENDER_TRANSPORT_PREFLIGHT.md
README.md
```

Implemented behavior:

- canonical SHA-256 binding of the exact projection document;
- deterministic render-request construction and request hashing;
- exact ordered source-event binding;
- requested capabilities constrained to projection-supported capabilities;
- selection/refinement policy is intent-only and cannot authorize state mutation;
- canonical request source refuses embedded endpoint/credential/token fields;
- receipts bind request hash, projection hash, exact source events, provider identity, capabilities actually used, status, artifact identity, provenance, and intents;
- `RENDERED` fails closed without artifact identity plus hash or bounded locator;
- capability escalation, request/projection mismatch, source-event mismatch, unsupported intents, and any authority escalation fail closed;
- renderer authority remains `PROJECTION_ONLY` with admission, mutation, evidence invention, credential, publication, custody, and execution authority all false.

## Validation evidence

Exact PR #1053 head before this handoff reconciliation: `1a0cabcf39943cca663fb0937341f1dda1fce55d`.

Observed successful gates on that head:

```text
Ecosystem Visual Render Transport Validate run 34002803437: SUCCESS
Site Handoff Orchestrator run 34002803404: SUCCESS
Ecosystem Heartbeat Orchestration run 34002803391: SUCCESS
Site Bootstrap Validate run 34002803428: SUCCESS
Validate StegOS Persistent Card UX run 34002803441: SUCCESS
```

The dedicated verifier also checks README completeness and invokes the deterministic Node positive/negative contract suite. Hosted validation has no renderer, provider, credential, custody, publication, or activation authority.

This handoff update advances the PR head, so exact-head gates must pass again before merge.

## Authority boundary

Renderer transport is projection-only. Endpoint/credential configuration is not canonical projection content and is not embedded in fixtures. A valid render request/receipt cannot mutate canonical events, grant admission, invent evidence, authorize provider credentials, or convert selection/refinement intents into state changes.

## Dependency boundary

Site #242 remains the authentic Ecosystem Chat runtime activation owner. This source transport contract may complete before #242, but a live external renderer handshake cannot be claimed until authentic canonical events and a real renderer transport are available.

`master-records/orchestration` remains the custody/reconstruction authority. This Site task defines receipt content and validation only; it does not create a second custody executor. The existing Master Records Ecosystem Chat custody lane is already source/hosted validated and waits on authentic upstream evidence rather than a second implementation.

## Remaining work and destinations

Destination `StegVerse-Labs/Site`:
- complete exact-head revalidation after this handoff update;
- merge PR #1053 only after all required gates pass;
- release the #1015 claim after merge;
- later bind one authentic Site#242 canonical projection to a real renderer transport.

Destination `master-records/orchestration` after real renderer execution:
- retain the exact render request/receipt, hashes, artifact identity, and reconstruction linkage through the existing custody/reconstruction authority; do not create a second custody executor.

Destination `StegVerse-org/LLM-adapter` only if later canonical event transport requires an adapter seam.

Downstream only after a pertinent live renderer release/projection gate:
- `StegVerse-Labs/Sit`
- `GCAT-BCAT-Engine/Publisher`
- `StegVerse-Labs/admissibility-wiki`
- `StegVerse-002/stegguardian-wiki`

No external endpoint, token, or credential has been supplied or requested by this source task.

## Completion accounting

Bounded source/claim/preflight/README files: 10/10 implemented.  
Scaffolding/stubs among bounded files: 0.  
Dedicated transport validation: PASS on prior exact head.  
Repository claim/orchestration/heartbeat/application gates: PASS on prior exact head.  
README completeness: PASS.  
Live external renderer handshake: NOT IMPLEMENTED / NOT PROVEN.  
Master Records render-receipt custody: NOT YET APPLICABLE WITHOUT REAL RENDER RECEIPT.  
Site#242 canonical runtime dependency: OPEN.
