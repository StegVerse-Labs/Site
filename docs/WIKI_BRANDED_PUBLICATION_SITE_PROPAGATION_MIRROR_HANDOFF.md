# Wiki Branded Publication and Site Propagation Mirror Handoff

Status: ACTIVE_VALIDATION_PENDING  
Task ID: `WIKI-BRANDED-PUBLICATION-SITE-PROPAGATION-001`  
Parent task: `ADMISSIBILITY-WIKI-PUBLIC-DOMAIN-001`

## Goal

Use the existing branded wiki hostnames as the preferred public origins while preserving each existing wiki repository and GitHub Actions Pages deployment as the canonical publication source.

Public origins:

- `https://admissibility.stegverse.org/`
- `https://stegguardian.stegverse.org/`
- `https://stegtalk.stegverse.org/`

Site remains a lightweight public directory and bridge. It does not copy or re-own wiki content.

## Repository lanes

### Admissibility Wiki

Canonical source: `StegVerse-Labs/admissibility-wiki`  
Public hostname: `admissibility.stegverse.org`  
Domain task: `ADMISSIBILITY-WIKI-PUBLIC-DOMAIN-001`

### StegGuardian Wiki

Canonical source: `StegVerse-002/stegguardian-wiki`  
Public hostname: `stegguardian.stegverse.org`  
GitHub Pages custom-domain evidence: user-supplied screenshot with DNS check successful.  
Source branch/PR for this task: `branded-public-domain` / PR #44.

### StegTalk Wiki

Canonical source: `StegVerse-Labs/stegtalk-wiki`  
Public hostname: `stegtalk.stegverse.org`  
GitHub Pages custom-domain evidence: user-supplied screenshot with DNS check successful and Enforce HTTPS enabled.  
Source branch/PR for this task: `branded-public-domain` / PR #3.

## Site projection

Site source: `StegVerse-Labs/Site`

The Site projection includes:

- `wikis.html` public directory with all three branded wiki entry points;
- homepage link to the Wikis directory;
- `data/wiki-public-links.json` branded canonical public URLs;
- Ecosystem Chat StegTalk wiki navigation updated to the branded URL;
- documentation-mesh records updated to the branded wiki origins;
- `Papers.html` formalism links updated to `admissibility.stegverse.org`;
- existing Site public pages that link into Admissibility Wiki updated to the branded origin;
- no wiki content duplicated onto Site.

## Validation gates

1. Central task registration merged.
2. StegGuardian exact-head PR validation passes.
3. StegGuardian merge succeeds and branded root/public records are observed.
4. StegTalk exact-head PR validation passes.
5. StegTalk merge succeeds and branded root is observed over HTTPS.
6. Admissibility branded-host task reaches its valid merge/public-route boundary.
7. Site exact-head validation passes with branded wiki registry/navigation.
8. Site PR merges.
9. Public Site `/wikis.html` exposes all three branded wiki entry points.
10. Site `/Papers.html` formalism links use `admissibility.stegverse.org`.

## Authority boundary

Branded-domain publication and Site navigation do not grant execution, custody, admissibility, certification, release, Guardian, messaging, or governance authority. Each wiki repository remains the source owner of its own content and validation posture.
