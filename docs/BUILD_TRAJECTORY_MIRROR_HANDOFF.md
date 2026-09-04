# Build Trajectory Mirror Handoff

## Source of truth

This is the bounded continuation record for the public StegVerse Build Trajectory and weekly accomplishment log in `StegVerse-Labs/Site`. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.

## Goal

Publish a durable public page that explains why the log exists and prepends concise weekly reports. The page must demonstrate actual progress while preserving the distinction among:

1. implementation;
2. validation;
3. release or deployment;
4. runtime proof; and
5. governed activation.

A plan, assignment, issue, source merge, CI success, deployment, runtime event, or activation must never be presented as another stage.

## Intended public routes

- `build-trajectory.html` — public explanation and newest-first weekly log.
- `news-releases.html` — a stable discovery link under Current News Releases.

## Canonical truth and projection contract

`data/build-trajectory.json` is the only semantic source of truth for this surface.

`scripts/render_build_trajectory.py` deterministically projects that record into `build-trajectory.html`. The HTML is a generated artifact and must never be interpreted or edited as an independent report source.

`scripts/check_build_trajectory.py` requires exact-byte reconstruction from the canonical record. Any independently edited or stale projection fails closed.

The canonical record also owns:

- evidence-stage definitions;
- newest-first ordering;
- safe evidence references;
- incomplete and unproven-claim classifications;
- append-only dated corrections;
- destination-specific remaining work;
- public/private evidence boundaries; and
- PR-only weekly publication policy.

Broad percentage-complete claims are excluded from the public record unless a stable public denominator and calculation method are added to the canonical schema.

## Weekly report contract

Every entry must:

- use an explicit reporting period;
- appear before older entries;
- identify evidence for every completed outcome;
- place assigned, queued, documented, scaffolded, blocked, or awaiting-evidence work under **Not completed**;
- place unsupported completion language under **Unproven completion claims** and name the missing proof;
- name remaining installation or integration destinations when known;
- state explicitly when no qualifying completed outcome exists;
- preserve exact repository and artifact names;
- avoid duplicate accomplishments.

## Implemented on successor branch

- public page: `build-trajectory.html`
- sole canonical report record: `data/build-trajectory.json`
- deterministic renderer: `scripts/render_build_trajectory.py`
- exact-projection validator: `scripts/check_build_trajectory.py`
- successor task record: `data/tasks/SITE-BUILD-TRAJECTORY-001.json`
- Current News Releases discovery link: `news-releases.html`
- local bounded validation: `PASS`

Canonical-projection implementation head: `06b24a6e310748e54466966c2c0c48c6bc2b54c1`

This proves implementation and local validation on the branch. It does not prove merge, deployment, public observation, runtime execution, or activation.

## Current state

`IMPLEMENTED_AND_VALIDATED_AWAITING_EXISTING_NEWS_RELEASES_CLAIM_RELEASE`

The new route, source data, and validator may be developed on an isolated successor branch. The branch must not merge while `news-releases.html` remains owned by claim `SITE-CURRENT-NEWS-RELEASES-967-20260903`.

That older claim is awaiting fresh public observation of:

- `papers/stegverse-entity-economy/`;
- the canonical Entity Economy PDF; and
- `Papers.html` featuring Entity Economy.

## Validation plan

The bounded validator must establish:

- the discovery link exists;
- the public page explains its purpose;
- weekly entries are reverse chronological;
- the five evidence stages are named;
- completed outcomes include direct evidence links;
- Not completed and Unproven completion claims remain distinct;
- the page disclaims activation inference from publication;
- the committed HTML exactly reconstructs from the canonical JSON;
- manual projection edits are prohibited;
- correction records are append-only and dated;
- evidence URLs use approved HTTPS canonical-file paths without duplication;
- completion counts reconcile to canonical outcomes; and
- PR-only publication and sensitive-evidence policy remain fail-closed.

Validation does not establish deployment, public observation, runtime proof, or governed activation.

## Publication boundary

Repository implementation and validation are not public deployment. A successful Pages workflow is deployment evidence, not independent public observation. Site display grants no execution, custody, certification, admissibility, release, or activation authority.

## Remaining work

1. Release or supersede claim `SITE-CURRENT-NEWS-RELEASES-967-20260903`.
2. Admit the successor publication task through Site orchestration.
3. Merge the implementation after validation.
4. Observe `https://stegverse.org/build-trajectory.html` and its Current News Releases link independently after deployment.
5. On future Fridays, update only `data/build-trajectory.json`, run the deterministic renderer and validator, and open a PR.
6. Independently verify that cited evidence still exists before merging each weekly report; structural link validation does not prove remote availability.
7. Consider quarterly trajectory summaries only as projections from the same canonical record—never as separately authored truth.

## Downstream installation posture

No downstream propagation is required for this Site-only public reporting surface. Evaluate `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki` only if they later need explicit awareness of the public log.

## Archive readiness

This handoff is self-contained. No conversation-only information is required to continue the build-trajectory publication lane.
