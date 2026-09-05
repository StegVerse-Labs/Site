# Ecosystem Chat Visual Projection Mirror Handoff

Repository: `StegVerse-Labs/Site`  
Issue: `#1007`  
Prework claim: `#1008`  
Branch: `feat/ecosystem-visual-projection-1007`  
State: `SOURCE_IMPLEMENTED_ON_BRANCH / LIVE_RENDERER_NOT_INTEGRATED`  
Authority effect: `NONE_PROJECTION_ONLY`

## Purpose

Provide a provider-neutral projection contract between the canonical Ecosystem Chat governed event stream and optional visual renderers such as interactive diagrams, topology viewers, animations, or real-time 3D runtimes.

This contract exists so a renderer can make governed system state visible without becoming semantic authority, admission authority, execution authority, custody authority, identity authority, or source of truth.

## Canonical topology

```text
canonical governed event stream
-> deterministic visual projection builder
-> provider-neutral projection document
-> optional renderer adapter
-> visual / interactive / 3D projection
```

The canonical event stream remains the source of truth. A renderer is a projection consumer only.

## Implemented source

```text
schemas/ecosystem-visual-projection.schema.json
assets/ecosystem-visual-projection.js
tests/ecosystem-visual-projection.test.cjs
tests/fixtures/ecosystem-visual-projection/canonical-events.json
scripts/check_ecosystem_visual_projection.py
docs/ECOSYSTEM_VISUAL_PROJECTION_MIRROR_HANDOFF.md
```

The builder deterministically converts canonical event IDs, parent relationships, governed dispositions, evidence refs, policy refs, artifact refs, and continuity refs into a visual topology document.

## Authority boundary

Every valid projection requires:

```text
renderer_role = PROJECTION_ONLY
renderer_may_mutate_canonical_events = false
renderer_may_grant_admission = false
renderer_may_invent_evidence = false
```

Any attempted authority escalation fails closed.

A renderer may:
- render 2D/2.5D/3D topology;
- animate transitions;
- expose bounded selection/focus interactions;
- request a bounded visual refinement;
- present provenance and evidence relationships.

A renderer may not:
- modify canonical events;
- convert DENY/DEFER into ALLOW;
- fabricate evidence or policy refs;
- silently rewrite provenance;
- grant execution, identity, publication, custody, or admission authority.

## AI SiteFlow compatibility target

The source includes a capability descriptor for a candidate AI SiteFlow-style renderer:

```text
provider_id: ai-siteflow-compatible
runtime_hints: nextjs, webgl, realtime-3d
capabilities: 2d, 3d, interactive-selection, bounded-refinement, animation, topology
integration_state: CAPABILITY_DESCRIPTOR_ONLY
endpoint: null
credential_ref: null
```

This is not an endpoint integration, commercial commitment, external dependency, or runtime proof. It is a provider-neutral compatibility target based on the currently discussed Next.js / real-time 3D collaboration possibility.

## Deterministic validation

`tests/ecosystem-visual-projection.test.cjs` proves:

1. identical canonical events produce byte-equivalent JS objects;
2. stable event-derived nodes and parent edges are preserved;
3. ALLOW/PASS/ADMITTED dispositions normalize only to visual state `ADMITTED`;
4. provenance refs remain attached;
5. unresolved parent references fail closed;
6. renderer admission-authority escalation fails closed;
7. missing provenance fails closed;
8. the SiteFlow-compatible capability descriptor contains no endpoint or credential.

`scripts/check_ecosystem_visual_projection.py` is the dependency-light repository verifier and invokes the Node contract test.

## Collision boundary

This lane does **not** modify or claim:

```text
ecosystem-chat.html
assets/ecosystem-chat.js
semantic shorthand / Site#396
HIL upload paths
StegVerse-org/LLM-adapter
TVC route/runtime
Master Records custody/reconstruction
HB / oscillator / WorkerCoordinator
Site#242 live Ecosystem Chat activation
```

The contract is additive and can be source-complete without reopening those owners.

## Next integration sequence

After source validation/merge:

```text
Site#242 authentic Ecosystem Chat cycle
-> canonical gateway-origin governed event stream available
-> feed exact canonical events to buildProjection(...)
-> expose projection document through a bounded visual projection endpoint or browser adapter
-> negotiate renderer capabilities
-> first AI SiteFlow-compatible prototype renders exact projection
-> renderer interaction returns selection/refinement intent only
-> Ecosystem Chat decides any semantic/state change through the canonical governed path
-> preserve projection/provider/render receipt refs for reconstruction
```

## Remaining work and destinations

Destination `StegVerse-Labs/Site`:
- bind `scripts/check_ecosystem_visual_projection.py` into canonical Site validation after branch admission;
- merge this source after required repository gates pass;
- after Site#242 runtime activation, bind gateway-origin canonical events into the builder;
- add user-facing visual projection switch/launch control without creating a second chat UI.

Destination `StegVerse-org/LLM-adapter` only if runtime transport requires it:
- expose canonical event/projection transport fields without granting renderer authority.

Destination `master-records/orchestration` after real renderer execution:
- retain projection request/hash, renderer capability selection, returned render identity/hash, refinement intents, and reconstruction linkage.

Potential external collaborator:
- AI SiteFlow: candidate first implementation of the provider-neutral visual renderer interface.

## Completion accounting

Source contract files planned in #1007: 6  
Source contract files implemented on branch: 6/6  
Scaffolding/stubs among these files: 0  
Live external renderer integration: NOT IMPLEMENTED  
Public Ecosystem Chat visual projection activation: NOT PROVEN  
Site#242 dependency: OPEN

Source completion must not be reported as external integration or public activation.
