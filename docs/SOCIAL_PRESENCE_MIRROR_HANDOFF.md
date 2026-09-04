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
- `scripts/check_social_presence.py` — fail-closed static validator
- scoped pre-work claim in `data/session-work-claims.d/site-social-presence-975-r2-20260904.json`

Successor branch: `feat/social-presence-975-r2`.

The first branch/PR #979 became stale as main advanced. R2 was recreated from current main rather than forcing or treating a diverged branch as current.

## External page state

No verified public LinkedIn Company Page URL or Facebook Page URL has been observed and no connector available to this session can create those external pages.

Accordingly, `data/social-presence.json` keeps both external destinations fail-closed with `canonical_url: null` until the platform pages actually exist and their canonical public URLs are verified.

Do not invent an account URL or treat a personal profile, search result, screenshot, or proposed handle as an official StegVerse page.

## Social provenance boundary

The Site may reference official account URLs, network page identifiers, creation/verification timestamps, publication cross-post URLs, discussion URLs, and bounded normalized metadata permitted by the source network.

External social posts and discussions do not become canonical StegVerse publication records. They remain provenance-linked distribution/discussion events associated with the relevant `publication_id`, version, and content hash.

## Remaining work

Destination `StegVerse-Labs/Site`:

- Add Social navigation from `index.html`, `Papers.html`, and `news-releases.html` on the R2 branch.
- Bind `scripts/check_social_presence.py` into the canonical validation path without creating a separate scheduler/runtime authority surface.
- Open the R2 PR from fresh current main and observe exact-head claim/orchestration validation.
- Close/supersede stale PR #979 after R2 is established.
- Merge only after required validation is green and branch freshness is preserved.
- Replace pending external destinations with verified URLs only after the external pages exist.
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

This Site slice is complete when the public social hub and per-network pages are merged, navigation resolves from Home, Papers, and News Releases, the manifest validates in canonical validation, and official external URLs are present only for actually created and verified pages.

External platform page creation is a separate completion predicate and must not be inferred from Site code.
