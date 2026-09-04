# Current News Releases Mirror Handoff

## Source of truth

This is the bounded continuation record for StegVerse-Labs/Site issue #967 and the Entity Economy extension performed under the same admitted publication claim. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.

## Goal

Maintain a first-class **Current News Releases** surface on StegVerse.org and a coherent Papers publication surface, with deterministic newest-first ordering, stable canonical URLs, and no inference of runtime or governance authority from public display.

## Current implementation

Public routes:

- `index.html` — homepage discovery for Current News Releases
- `news-releases.html` — Current News Releases index
- `news-releases/ai-is-becoming-infrastructure-sovereignty-must-go-further.html` — StegVerse LLC South Korea comparative statement
- `papers/stegverse-entity-economy/index.html` — Entity Economy paper landing page
- `papers/stegverse-entity-economy/stegverse-entity-economy.pdf` — canonical nine-page PDF
- `Papers.html` — public Papers index, with Entity Economy as the current featured publication

## South Korea statement

The StegVerse LLC statement **AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model.** uses South Korea's "AI for All" initiative as an external convergence indicator and distinguishes national/model sovereignty from StegVerse's entity-, credential-, data-, action-, transition-, evidence-, and economics-level architecture.

Primary source:
https://www.msit.go.kr/eng/bbs/view.do?bbsSeqNo=42&mId=4&mPid=2&nttSeqNo=1285&sCode=eng

Secondary source:
https://www.techspot.com/news/113664-south-korea-giving-entire-population-free-access-ai.html

## Entity Economy extension — 2026-09-04

The canonical working paper **The StegVerse Entity Economy: A Governed Economic Model for Human and AI Entities** is now installed as a bounded Site publication.

Implemented evidence:

- canonical PDF binary commit: `cac375315d91f4327c9e7c6f794a5fbf57f3dec0`
- PDF download enabled on landing page: `149408e53c36869016e8983385cc89e5efc7ea34`
- Entity Economy surfaced above the South Korea statement with explicit same-day sequence ordering
- Entity Economy surfaced as the current featured paper in `Papers.html`: `b4b9183d0df17b6ac08542d9b3bbbd2434326c45`
- validator extended through PDF and Papers-index assertions: `1d94eb6e2ad19c5401c3e7856ce6913b2e920958`
- publication task evidence/state recorded through `717b34985f7126d5a98ce9c355a0402bf3b69542`

The paper preserves the boundary that economic entitlement does not create governance authority. Compensation does not grant transition, credential, custody, or decision authority.

## Homepage claim correction

The Workspace interoperability claim had retained `index.html` after the Workspace homepage entry had already been integrated. That ownership was narrowed at commit `1d2ab3a0e87f6422bc4278611ace10e198f88418`; Workspace retains only its actual implementation/runtime paths.

The existing Current News Releases claim then acquired `index.html` for completion of its recorded follow-on work. Homepage discovery was committed at `36d7299b361b60a83c2c8da26d90162aeeef15da`.

The active HIL implementation paths remain untouched.

## Ordering contract

`news-releases.html` is deterministic by machine-readable publication date and explicit sequence. Newer dates sort first; same-day releases use sequence ordering. Existing canonical release URLs remain stable.

Current required ordering:

1. The StegVerse Entity Economy
2. AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model.

## Validation and deployment evidence

For repository state through commit `717b34985f7126d5a98ce9c355a0402bf3b69542`:

- Site Bootstrap Validate run `33912889822`: `SUCCESS`
- GitHub Pages build/deployment run `33912888808`: `SUCCESS`
- repository task observer failure is unrelated to this publication lane; it is the existing `SITE-0001-COHERENT-TRANSITION-THRESHOLD-ACTIVATION` blocker, currently missing `required_transitions_jointly_ready`, `continuation_conditions_preserved`, and `next_cycle_admissible`

No publication completion claim is inferred from the unrelated repository-wide transition blocker.

## Public observation state

Historical user observation already proves that `news-releases.html` and the South Korea statement rendered publicly on StegVerse.org before the Entity Economy extension.

Fresh machine crawler observation after the Entity Economy deployment still returns an older cached `Papers.html` snapshot showing five Site-native publications and the prior featured paper. Therefore the current Entity Economy ordering/Papers integration is:

`DEPLOYED_VALIDATED_AWAITING_FRESH_PUBLIC_REOBSERVATION`

A stale public crawler result is not treated as contradictory deployment evidence, but it is also not promoted to fresh public observation.

## Classification boundary

Current News Releases and Papers are public communication/publication surfaces. They do not establish execution, activation, custody, certification, admissibility, credential authority, transition authority, or release authority.

## Remaining work

1. Obtain one fresh independent public observation showing:
   - `news-releases.html` with Entity Economy above the South Korea statement;
   - `papers/stegverse-entity-economy/` rendering;
   - canonical PDF opening from that landing page; and
   - `Papers.html` showing Entity Economy as current featured publication.
2. Terminalize claim `SITE-CURRENT-NEWS-RELEASES-967-20260903` after that observation.
3. Use canonical StegVerse.org publication URLs for social posts.
4. For future publication-system propagation, evaluate GCAT-BCAT-Engine/Publisher, admissibility-wiki, and stegguardian-wiki without inferring authority merely from Site publication.

## Release posture

No repository tag or product release is required for this static publication integration. Source, PDF, validation, and Pages deployment are complete; only fresh independent public observation remains before claim release.

## Archive readiness

Repository state is self-contained. No conversation-only information is required to continue this publication lane.
