# StegLearn Site Mirror Handoff

## Scope

Repository: `StegVerse-Labs/Site`

Public route source: `steglearn/index.html`

Intended public URL: `https://stegverse.org/steglearn`

Canonical learning-source repository: `StegVerse-Labs/StegLearn`

## Goal

Publish a clear public orientation surface for StegLearn containing:

- Vision;
- Purpose;
- operating guidelines;
- product roadmap;
- StegVerse Foundations curriculum with short module descriptions;
- explicit current-vs-roadmap state;
- source links for technical inspection.

The page is intended to be shareable before a deeper external-learning integration exists. It explains StegLearn first and leaves any external relationship as a later, reciprocal, explicitly bounded capability rather than presenting an external site as an object of unilateral integration.

## Canonical sources resolved before mutation

The following state was resolved before the landing-page source was created:

- `StegVerse-Labs/Site/docs/SITE_MIRROR_HANDOFF.md` — repository source of truth;
- `StegVerse-Labs/Site/data/site-orchestration-state.json` — repository orchestration state `ACTIVE`, no admitted external task and no active parallel-safe task;
- `StegVerse-Labs/Site/data/ecosystem-heartbeat-state.json` — `HEALTHY_BLOCKED`, active tasks empty, exclusive HIL runtime work blocked on external authentic evidence;
- `StegVerse-Labs/.github/data/canonical-task-registry.json` — generation 15 as resolved in the current StegLearn/coordination work;
- `StegVerse-Labs/.github/docs/CANONICAL_WORK_COORDINATION_SYSTEM_MIRROR_HANDOFF.md` — Task Registry / WorkerCoordinator / Master Records / Interlock-InTr authority separation;
- `StegVerse-Labs/StegLearn/STEGLEARN_MIRROR_HANDOFF.md` — canonical StegLearn repository continuation;
- `StegVerse-Labs/StegLearn/docs/STEGVERSE_FOUNDATIONS_MIRROR_HANDOFF.md` — canonical Foundations curriculum lane;
- `StegVerse-Labs/StegLearn/lessons/stegverse-foundations/path.json` — twelve-module curriculum roadmap;
- `StegVerse-Labs/.github/docs/ECOSYSTEM_PURPOSE_INVARIANT.md` — canonical organization-level purpose and authority distinctions used by Foundations lesson 01.

Cross-task search found no existing `steglearn/` public Site route. Open StegLearn PR #3 contains adjacent product-model/public-landing work, but it remains an unmerged branch and is not treated as current canonical Site publication authority. The Site page therefore uses current merged StegLearn/Foundations semantics and avoids claiming PR #3 behavior as already active.

## Machine preflight result

`PASS_FOR_STATIC_PUBLIC_STEGLEARN_ORIENTATION_SURFACE`

Reason:

- no competing StegLearn landing route existed in Site;
- the Site heartbeat shows no active parallel-safe task collision;
- the page creates no runtime, scheduler, WorkerCoordinator, Interlock/InTr implementation, credential path, custody path, or execution authority;
- the page is a static public mirror of already-declared StegLearn purpose and curriculum state;
- roadmap items are explicitly separated from materialized content.

## README completeness predicate

`NO_ROOT_README_CHANGE_REQUIRED`

Evidence-supported reason: `Site/README.md` already defines Site as a public mirror that renders product information from canonical source data. This change adds a static informational route under that existing product-information role. It does **not** change Site runtime behavior, API/interface contracts, governance or authority boundaries, evidence semantics, prerequisites, dependencies, failure behavior, activation semantics, credential requirements, or capability meaning. The route introduces no new executable capability. Therefore the root README does not require a semantic update for completeness.

If the Site public-page index is later treated as an exhaustive navigation inventory rather than descriptive documentation, adding `steglearn/` to that table is a documentation follow-up, not a prerequisite for this static route's authority or correctness.

## Public content contract

The landing page contains these first-order sections:

1. Vision — learning that increases capability without capturing identity or authority.
2. Purpose — turn curiosity into governed growth.
3. Guidelines — non-capture, evidence/revision preservation, review, capability/authority separation, source-bound teaching, bounded external learning.
4. Roadmap — Foundations, multi-format rendering, interactive checkpoints/receipts, goal→curriculum→review→teaching, adaptive/longitudinal learning, external learning ecosystem.
5. StegVerse Foundations — all twelve canonical module titles with short descriptions and explicit `MATERIALIZED`/`ROADMAP` posture.
6. Development posture — StegLearn owns knowledge representation; renderers remain downstream.

## Authority and evidence boundaries

The landing page must not imply:

- accreditation or credentialing authority;
- autonomous educational authority;
- production classroom deployment;
- completed AI SiteFlow integration;
- public runtime activation;
- completion of roadmap modules 02–12;
- Edukors partnership or production interoperability;
- learner understanding merely because static content exists or is viewed.

Site remains a public mirror. StegLearn remains the canonical learning-source repository. Generated media remains downstream and non-authoritative unless a later governed publication contract states otherwise.

## Validation

Static validator target: `scripts/check_steglearn_landing.py`.

Required checks:

- route source exists;
- canonical URL is `https://stegverse.org/steglearn`;
- Vision, Purpose, Guidelines, Roadmap, and StegVerse curriculum sections exist;
- exactly twelve numbered curriculum modules are represented;
- module 01 is marked `MATERIALIZED`;
- modules 02–12 remain `ROADMAP`;
- current boundary text rejects accreditation, completed SiteFlow integration, and roadmap-completion inference;
- source link points to `StegVerse-Labs/StegLearn`;
- external-learning roadmap uses reciprocal/bounded language rather than claiming a unilateral live integration.

## Current state

`SOURCE_LANDING_PAGE_IMPLEMENTED_VALIDATION_PENDING`

Source commit creating the public route:

`e900e899526efff79e102feb04965cdc8fcdcb0c`

No public deployment/reachability observation is claimed from source commit alone.

## Remaining work

1. install and run the static landing-page validator;
2. bind that validator into an appropriate existing Site validation surface when doing so does not collide with unrelated active workflow work;
3. observe deployed reachability at `https://stegverse.org/steglearn` after the Site deployment path carries the source;
4. keep page curriculum descriptions synchronized to canonical StegLearn lesson state;
5. when StegLearn PR #3 or its successor is merged, reconcile the public page with the generalized goal/curriculum/review/teaching model rather than duplicating it;
6. do not name an external educational organization as integrated until a reciprocal relationship is actually defined and admitted.

## Human action

None required for the static source page. Sharing should wait for deployed public reachability if the intent is to send a working `stegverse.org/steglearn` URL rather than a repository preview.
