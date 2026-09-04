# StegVerse Social Presence Mirror Handoff

## Source of truth

This is the bounded continuation record for the StegVerse public social-presence surface in `StegVerse-Labs/Site` and issue #975.

Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`. Publication provenance work remains bounded by issue #975. This handoff grants no provider, credential, posting, publication, activation, custody, identity, or admissibility authority.

## Goal

Provide a stable Site-owned social-presence directory so visitors can discover official StegVerse social pages from StegVerse.org, while keeping external networks as distribution/discussion projections rather than sources of truth.

## Current implementation slice

Destination: `StegVerse-Labs/Site`

- `social.html` — public social hub
- `social/linkedin.html` — LinkedIn landing/verification page
- `social/facebook.html` — Facebook landing/verification page
- `data/social-presence.json` — canonical Site projection manifest for official network destinations
- `assets/social-presence.js` — renders account status and outbound links from the manifest
- `scripts/check_social_presence.py` — fail-closed static validator with exact-network hostname, platform-ID, authority, pending-state, and navigation checks
- `scripts/check_publication_manifest.py` — canonical application-validation binding for the social-presence validator
- Social navigation from `index.html`, `Papers.html`, and `news-releases.html`
- scoped pre-work claim in `data/session-work-claims.d/site-social-presence-975-r2-20260904.json`

Successor branch: `feat/social-presence-975-r2`.
Successor PR: #992.
Superseded PR: #979, closed without merge.

The first branch/PR #979 became stale as main advanced. R2 was recreated from current main rather than forcing or treating a diverged branch as current.

## Validation observations

The first exact-head PR #992 validation wave established that the scoped claim and workload mapping repair were accepted by the Site governance lane:

- Site Handoff Orchestrator: PASS observed on run 33919831145.
- Ecosystem Heartbeat Orchestration: PASS observed on run 33919831084.
- Site Homepage Chat: PASS observed.
- Site Node Continuity: PASS observed.

Subsequent source commits added the Papers navigation link, canonical publication-validation binding, and stronger social-destination checks. Fresh exact-head validation is required after those commits; earlier green results are not reused as proof for the new head.

## External page state

No verified public LinkedIn Company Page URL or Facebook Page URL has been observed and no connector available to this session can create those external pages.

Accordingly, `data/social-presence.json` keeps both external destinations fail-closed with `canonical_url: null` and `platform_id: null` until the platform pages actually exist and their canonical public URLs and platform identifiers are verified.

Do not invent an account URL or treat a personal profile, search result, screenshot, or proposed handle as an official StegVerse page.

## Social provenance boundary

The Site may reference official account URLs, network page identifiers, creation/verification timestamps, publication cross-post URLs, discussion URLs, and bounded normalized metadata permitted by the source network.

External social posts and discussions do not become canonical StegVerse publication records. They remain provenance-linked distribution/discussion events associated with the relevant `publication_id`, version, and content hash.

## Remaining work

Destination `StegVerse-Labs/Site`:

- Observe fresh exact-head Site Bootstrap, Site Handoff, heartbeat, and canonical application validation for the current R2 head.
- Reconcile branch freshness against current main before any merge.
- Merge only after required validation is green and branch freshness is preserved.
- Replace pending external destinations with verified URLs and platform IDs only after the external pages exist.
- Add the first social-post/discussion provenance records under issue #975.
- Extend publication pages with Social Activity / Discussion / Provenance sections using the canonical publication object model.

External platform work:

- Create the official StegVerse LinkedIn Company Page.
- Create the official StegVerse Facebook Page.
- Record their exact public URLs and platform identifiers.
- Verify organization identity, site URL, description, and branding against the Site projection.

Downstream after verified publication/social provenance integration:

- `GCAT-BCAT-Engine/Publisher`
- `StegVerse-Labs/admissibility-wiki`
- `StegVerse-002/stegguardian-wiki`

## Completion boundary

The repository-resident Site slice is source-complete when the public social hub and per-network pages are merged, navigation resolves from Home, Papers, and News Releases, and the fail-closed social manifest is covered by canonical validation.

The complete social-presence goal additionally requires actual verified LinkedIn and Facebook organization destinations. External platform page creation is a separate completion predicate and must not be inferred from Site code, CI, merge, or deployment.
