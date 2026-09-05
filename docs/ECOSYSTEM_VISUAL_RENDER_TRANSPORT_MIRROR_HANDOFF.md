# Ecosystem Visual Render Transport Mirror Handoff

Repository: `StegVerse-Labs/Site`  
Issue: `#1015`  
Branch: `feat/ecosystem-visual-render-transport-1015`  
State: `SOURCE_IMPLEMENTATION_STARTED`  
Authority effect: `NONE_PROJECTION_TRANSPORT_ONLY`

## Source of truth

This is the focused continuation record for Site #1015. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`. The completed predecessor contract is `docs/ECOSYSTEM_VISUAL_PROJECTION_MIRROR_HANDOFF.md` / Site #1007 / merge `8112e3609cde4bdddbae010054f2bb0bff876f1e`.

## Goal

Define the provider-neutral request/receipt transport contract between a canonical `stegverse.ecosystem_visual_projection/v1` document and an optional renderer, including an AI SiteFlow-compatible Next.js/WebGL/realtime-3D renderer, without giving the renderer semantic, admission, transition, identity, credential, custody, publication, or execution authority.

## Planned source

```text
schemas/ecosystem-visual-render-request.schema.json
schemas/ecosystem-visual-render-receipt.schema.json
assets/ecosystem-visual-render-transport.js
tests/ecosystem-visual-render-transport.test.cjs
scripts/check_ecosystem_visual_render_transport.py
.github/workflows/ecosystem-visual-render-transport-validate.yml
data/session-work-claims.d/site-ecosystem-visual-render-transport-1015.json
docs/ECOSYSTEM_VISUAL_RENDER_TRANSPORT_MIRROR_HANDOFF.md
```

## Authority boundary

Renderer transport is projection-only. Endpoint/credential configuration is not canonical projection content and is not embedded in fixtures. A valid render request/receipt cannot mutate canonical events, grant admission, invent evidence, authorize provider credentials, or convert selection/refinement intents into state changes.

## Dependency boundary

Site #242 remains the authentic Ecosystem Chat runtime activation owner. This source transport contract may complete before #242, but a live external renderer handshake cannot be claimed until authentic canonical events and a real renderer transport are available.

## Current work

1. install request schema;
2. install receipt schema;
3. implement deterministic request hashing/binding and fail-closed receipt validation;
4. add positive/negative fixtures/tests;
5. add credential-free path-scoped validation;
6. merge/release only after Site claim/orchestration/heartbeat/application gates pass.

## Remaining destinations

- `StegVerse-Labs/Site`: source transport contract and later chat binding.
- `master-records/orchestration`: future retained render request/receipt reconstruction after real renderer execution.
- `StegVerse-org/LLM-adapter`: only if canonical event transport later requires an adapter seam.
- `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, `StegVerse-002/stegguardian-wiki`: only after a pertinent live renderer release/projection gate.

No external endpoint, token, or credential has been supplied or requested by this source task.
