# StegVerse Multi-Entity Domain / Origin Architecture Mirror Handoff

Status: ACTIVE / DESIGNING_FOR_ENTITY_SEPARATION_NOW
Repository: StegVerse-Labs/Site
Created: 2026-08-28
Goal ID: SITE-MULTI-ENTITY-DOMAIN-ORIGIN-ARCH

## Purpose

Design the StegVerse public-domain and publication topology now so later legal/entity formation does not require a disruptive migration of websites, public routes, authority boundaries, or canonical public-interest surfaces.

The planned entity topology is:

- StegVerse AI LLC
- StegVerse Governance LLC
- StegVerse Infra LLC
- future StegVerse RaS nonprofit (Research and Services)

The domain/origin architecture should anticipate those boundaries before all entities are formally activated.

## Canonical domain roles

```text
stegverse.com
  StegVerse commercial/product/ecosystem front door
  umbrella navigation and product discovery
  not a runtime/control-plane authority

stegverse.ai
  StegVerse AI LLC public/product origin
  governed AI, agents, model interaction, AI services, inference/evidence surfaces
  current redirect to stegverse.org is transitional only

stegverse.me
  individual user operating surface
  My KV, device Node, Services, receipts, personal StegOS projection
  not itself a corporate entity boundary

stegverse.org
  preserve as the future natural StegVerse RaS nonprofit/public-interest origin
  research, standards, public evidence, publications, governance/public-service resources
  current general-site use is transitional and must not create migration lock-in

governance.stegverse.com
  initial public origin candidate for StegVerse Governance LLC
  may later move to a dedicated registered domain without changing internal authority semantics

infra.stegverse.com
  initial public origin candidate for StegVerse Infra LLC
  may later move to a dedicated registered domain without changing internal authority semantics
```

## Design principle

```text
one semantic / organizational boundary
  -> one independently deployable origin
  -> zero authority transfer to the web origin
```

Each origin should be independently:

- buildable;
- deployable;
- observable;
- recoverable;
- replaceable;
- migratable to a different carrier/provider;
- capable of retaining stable public routes without changing the underlying StegVerse authority model.

## Authority invariants

No domain or web host becomes:

- TV/TVC credential authority;
- KnowledgeVault custody authority;
- identity authority;
- Interlock/InTr authority;
- service activation authority;
- receipt authority;
- HeartBeat authority;
- infrastructure control-plane authority merely by serving a page;
- AI decision authority merely by serving the AI-facing page.

Entity identity/branding and operational authority remain separate concepts.

## Shared primitives vs separate origins

Separate origins do NOT imply duplicated systems.

The following should remain reusable/shared where appropriate:

- design system and static assets;
- KV schemas and semantics;
- node continuity / Receipt #1 logic;
- Interlock/InTr contracts;
- TV/TVC credential boundaries;
- service governance vocabularies;
- evidence/receipt formats;
- deployment tooling;
- validation tooling.

Each entity origin may consume those shared primitives while exposing only the routes and actions appropriate to its legal/product boundary.

## Migration-safe route policy

Current public routes on `stegverse.org` should be treated as transitional when their long-term semantic owner is another future origin.

When a route is later moved:

1. preserve a durable redirect/compatibility path;
2. preserve route meaning;
3. preserve receipt/evidence references where applicable;
4. avoid changing authority merely because the hostname changes;
5. publish a migration observation receipt;
6. keep the prior origin usable as a non-authoritative redirect for an appropriate transition period.

## Current transition state

```text
stegverse.org
  live canonical Site origin today
  future RaS/public-interest destination role reserved

stegverse.ai
  currently forwards to stegverse.org
  dedicated AI origin: NOT YET ESTABLISHED

stegverse.me
  dedicated-origin implementation lane active under Site #581

stegverse.com
  dedicated commercial/front-door role: DESIGN DEFINED / ORIGIN NOT YET ESTABLISHED

governance.stegverse.com
  role reserved / origin not yet established

infra.stegverse.com
  role reserved / origin not yet established
```

## Near-term implementation order

1. complete `stegverse.me` dedicated-origin package and cutover pattern;
2. generalize the origin package/deployment/observation tooling so it is reusable;
3. establish `stegverse.com` as commercial/product front door without taking over RaS/public-interest semantics;
4. establish dedicated `stegverse.ai` origin and retire the temporary redirect only after direct observation;
5. establish Governance and Infra origins;
6. when StegVerse RaS is formed, transition `stegverse.org` to its durable nonprofit/public-interest role using pre-planned compatibility redirects rather than a structural rebuild.

## Non-claim

This document records architectural intent and migration constraints. It does not claim:

- formation of any LLC or nonprofit;
- legal ownership by any future entity;
- deployment of any future origin;
- DNS activation;
- TLS activation;
- provider migration;
- operational authority.

## Completion target

This architecture is considered implemented when every semantic/entity boundary above has:

- an independently deployable origin;
- explicit route ownership;
- documented authority boundary;
- portable publication bundle;
- DNS/TLS recovery path;
- direct observation receipt;
- migration/redirect compatibility test;
- no hidden dependency on another entity's public origin for canonical operation.
