# SDK Public Developer Wiki Site Projection Mirror Handoff

Updated: 2026-09-21
Goal Task ID: `SDK-PUBLIC-DEVELOPER-WIKI-001`
Canonical coordination handoff: `StegVerse-Labs/.github:docs/SDK_PUBLIC_DEVELOPER_WIKI_MIRROR_HANDOFF.md`
Canonical SDK source: `StegVerse-org/StegVerse-SDK`
Public origin: `https://sdk.stegverse.org/`
Status: `ACTIVE / PRE-WORK CLAIMED / SITE PROJECTION IMPLEMENTED / VALIDATION PENDING`

## Scope

Site adds only public discovery/navigation for the SDK developer wiki. SDK content, schemas, examples, receipts, replay/reconstruction semantics, implementation status, and authority boundaries remain owned by `StegVerse-org/StegVerse-SDK`.

Site does not duplicate the SDK wiki and does not gain governance, execution, transition, credential, custody, evidence, processor-selection, or publication authority.

## Evidence basis

The SDK public wiki source and Pages workflow were merged under SDK PR #300. The DNS target was corrected to `stegverse-org.github.io`. User-supplied GitHub Pages evidence on 2026-09-21 shows:

- `https://sdk.stegverse.org/` live;
- DNS check successful;
- Enforce HTTPS enabled.

This Site projection consumes only that branded public URL.

## COSV

COSV projection: `20010000100000` (`CLAIMED_IMPLEMENTATION`) derived from the active Site claim. This projection is non-authorizing and does not replace the canonical Goal Task identity.

## Pre-work ownership

Active claim: `SITE-SDK-PUBLIC-DEVELOPER-WIKI-1446-20260921` on branch `sdk-public-developer-wiki-001`. The claim owns only the bounded Site discovery files listed in its claim fragment and grants no runtime or publication authority.

## Site changes

- `data/wiki-public-links.json` gains the SDK developer wiki entry;
- `wikis.html` gains a developer-facing SDK card and link;
- README records the projection boundary.

## Completion gates

1. exact-head Site validation passes;
2. Site PR merges;
3. public Site wiki directory visibly links to `https://sdk.stegverse.org/`;
4. central handoff is reconciled after propagation evidence.

## Next executable step

Validate this branch at exact head, repair only deterministic Site projection failures, merge when clean, then observe the deployed Site directory and reconcile the canonical task state.
