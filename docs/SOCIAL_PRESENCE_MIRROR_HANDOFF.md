# StegVerse Social Presence Mirror Handoff

## Source of truth

This is the bounded continuation record for the StegVerse public social-presence surface in `StegVerse-Labs/Site` and issue #975.

Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`. Publication provenance work remains bounded by issue #975. This handoff grants no provider, credential, posting, publication, activation, custody, identity, or admissibility authority.

## Goal

Provide a stable Site-owned social-presence directory so visitors can discover official StegVerse social pages from StegVerse.org, while keeping external networks as distribution/discussion projections rather than sources of truth.

The first target networks are:

- LinkedIn
- Facebook

Additional networks may be added only when an official StegVerse destination is created and recorded in the manifest.

## Current implementation slice

Destination: `StegVerse-Labs/Site`

- `social.html` — public social hub
- `social/linkedin.html` — LinkedIn landing/verification page
- `social/facebook.html` — Facebook landing/verification page
- `data/social-presence.json` — canonical Site projection manifest for official network destinations
- `assets/social-presence.js` — renders account status and outbound links from the manifest
- `scripts/check_social_presence.py` — fail-closed static validator
- navigation links from `index.html`, `Papers.html`, and `news-releases.html`

## External page state

At creation of this handoff, no verified public LinkedIn Company Page URL or Facebook Page URL has been observed and no connector available to this session can create those external pages.

Accordingly, `data/social-presence.json` must keep each external destination fail-closed until the platform page actually exists and its canonical public URL has been verified.

Do not invent an account URL or treat a personal profile, search result, screenshot, or proposed handle as an official StegVerse page.

## Social provenance boundary

The Site may reference or project:

- official account URL
- network account/page identifier when returned by the platform
- creation/verification timestamp
- publication cross-post URL
- discussion URL
- bounded normalized metadata permitted by the source network

External social posts and discussions do not become canonical StegVerse publication records. They remain provenance-linked distribution/discussion events associated with the relevant `publication_id`, version, and content hash.

## Remaining work

Destination `StegVerse-Labs/Site`:

- Merge the Site social hub and per-network landing pages after validation.
- Replace `PENDING_EXTERNAL_PAGE_CREATION` with verified LinkedIn and Facebook page URLs only after the external pages exist.
- Add the first social-post/discussion provenance records under issue #975.
- Extend publication pages with Social Activity / Discussion / Provenance sections using the canonical publication object model.

External platform work:

- Create the official StegVerse LinkedIn Company Page.
- Create the official StegVerse Facebook Page.
- Record their exact public URLs and platform identifiers.
- Verify that the organization identity, site URL, description, and branding match the Site projection.

Downstream after verified publication/social provenance integration:

- `GCAT-BCAT-Engine/Publisher`
- `StegVerse-Labs/admissibility-wiki`
- `StegVerse-002/stegguardian-wiki`

## Completion boundary

This Site slice is complete when the public social hub and per-network pages are merged, navigation resolves, the manifest validates, and official external URLs are present only for actually created and verified pages.

External platform page creation is a separate completion predicate and must not be inferred from Site code.
