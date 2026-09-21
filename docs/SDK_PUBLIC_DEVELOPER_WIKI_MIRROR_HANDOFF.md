# SDK Public Developer Wiki Site Projection Mirror Handoff

Updated: 2026-09-21
Goal Task ID: `SDK-PUBLIC-DEVELOPER-WIKI-001`
Canonical coordination handoff: `StegVerse-Labs/.github:docs/SDK_PUBLIC_DEVELOPER_WIKI_MIRROR_HANDOFF.md`
Canonical SDK source: `StegVerse-org/StegVerse-SDK`
Public origin: `https://sdk.stegverse.org/`
Status: `ACTIVE / SITE PROJECTION MERGED + PUBLICLY OBSERVED / CLAIM TERMINALIZATION PENDING`

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

## Completion evidence

1. Site PR #1446 merged as `110de303b9f88922c926c4a75dbabcc86630d42e`.
2. Exact-head Site validation passed before merge.
3. Post-merge Site Pages deployment run `35637977873` completed successfully.
4. Independent SDK public-observation workflow run `35649334318` fetched `https://stegverse.org/wikis.html` over HTTPS with HTTP 200 and observed both `StegVerse SDK Developer Wiki` and `https://sdk.stegverse.org/` in the served body.
5. The same observation run fetched the deployed SDK ingress schema, external-framework example, and receipt-navigation resource over HTTPS with HTTP 200 and required served-body markers; all four predicates passed.

The active pre-work claim intentionally remains active for this closure update. After this handoff/README closure merges, release it through the repository's atomic claim/COSV terminalization-only path.

## Next executable step

Validate and merge this closure-only handoff/README update on the existing claimed branch. Then perform a separate claim-registry-only atomic terminalization that releases `SITE-SDK-PUBLIC-DEVELOPER-WIKI-1446-20260921` and removes its active COSV projection without changing authority or activation semantics.
