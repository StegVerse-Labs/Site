# Current News Releases Mirror Handoff

## Source of truth

This is the bounded continuation record for StegVerse-Labs/Site issue #967 and subsequent admitted publication extensions. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.

## Goal

Maintain a first-class **Current News Releases** surface on StegVerse.org and a coherent Papers publication surface, with deterministic newest-first ordering, stable canonical URLs, and no inference of runtime or governance authority from public display.

## Corrected Coherent Life publication contract — 2026-09-04

The prior over-integrated Site projection is superseded.

The publication family has two identities:

1. **Original parent working paper** — `Coherent Life and Admissible Existence: A Coupled Theory of Boundaries, Recoverability, Authority, Purpose, and Continued Coherence`.
2. **Separate companion publication** — notation/theorem witnesses + Empirical Addendum I + Empirical/Theoretical Addendum II.

The original working paper must remain independently discoverable and must not absorb either addendum into its body.

The companion source set is exactly:

```text
Supplement: Notation Table and Theorem Witnesses
Empirical Addendum I — Unknown-Class Transformation at the Quantum-Gravitational Boundary
Empirical/Theoretical Addendum II — Recoverable Capacity Across Representational Boundaries
```

The following adjacent papers are explicitly excluded from this companion publication:

```text
Development Without Domination
Adversarial AI, Public Authority, and the Receipt Problem
```

## Public routes

```text
papers/coherent-life-and-admissible-existence/index.html
  preserved parent-paper public projection

papers/coherent-life-companion/index.html
  new three-document companion projection

papers/coherent-life-and-admissible-existence/empirical-addendum-i.html
  retained legacy deep-link compatibility surface only

news-releases.html
  publishes the companion as the current Coherent Life news release

Papers.html
  exposes both the companion and preserved parent as two publication identities
```

The legacy Addendum I URL is not an independent Current News Release and is not a third Papers publication identity.

## Current News Releases ordering

`news-releases.html` is deterministic by machine-readable publication date and explicit sequence.

Current required ordering:

1. Coherent Life and Admissible Existence — Companion Extensions — 2026-09-04 sequence 5
2. The StegVerse Entity Economy — Volume II — 2026-09-03 sequence 3
3. The StegVerse Entity Economy — Volume I — 2026-09-03 sequence 2
4. AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model. — 2026-09-03 sequence 1

The original Coherent Life working paper and the standalone Addendum I legacy route are prohibited as separate Current News Releases entries for this correction.

## Companion conceptual boundary

The three source documents form one companion because they address a common representation-preservation problem from complementary directions:

```text
notation / theorem witnesses
  -> prevent symbol drift and preserve explicit formal distinctions

Addendum I
  -> avoid unsupported promotion of observation into certainty

Addendum II
  -> avoid destructive collapse of successor capacities under boundary crossing or abstraction
```

Joint preservation principle:

```text
Preserve every distinction required to reconstruct materially different claims or materially different future transitions.
```

Neither physics extension is treated as empirical validation of the complete Admissible Existence theory.

## Implemented correction commits

```text
2ce465ea5940c05141b8c8c6e8a2278a7413bad8  restore standalone parent projection
c72d6dea8be4bcde9da27089aecaf3d6abc9ac93  publish three-document companion projection
f8d7799b3cd249a966eaab80dc13a5baf0e6f9c3  point Current News Releases to companion
d9681542b37b560879a281e17c7d9a3ccb9c77d1  separate parent and companion in Papers
82771920a41fe7926a64fa4b6d13394583aabd31  validate corrected two-publication identity
```

The earlier commits that over-integrated the parent paper and Addendum I remain historical evidence only and are not the current publication contract.

## Validation contract

`scripts/check_current_news_releases.py` now requires:

- parent working-paper route exists;
- separate companion route exists;
- parent does not contain the former integrated empirical-application section;
- companion contains all three intended components;
- companion explicitly states that it does not replace or rewrite the parent;
- Current News Releases points only to the companion for this release;
- neither the parent route nor standalone Addendum I route appears as an additional news release;
- Papers lists companion and parent separately;
- Papers does not expose Addendum I as a third publication identity;
- legacy Addendum I deep link remains present for stable-link compatibility.

## Artifact posture

A corrected 14-page exact-source companion PDF was assembled from the three supplied PDFs in this order:

```text
1. ae-notation-and-witnesses
2. admissible_existence_empirical_addendum_quantum_equivalence
3. admissible_existence_empirical_addendum_ii_quantum_thermodynamics
```

This is a byte-preserving page concatenation of the three source PDFs, not a rewrite of the parent paper. It is not yet repository-resident through the current GitHub text-file write surface and therefore is not claimed as a canonical AE release artifact.

The earlier 15-page `integrated full-paper` artifact is not canonical because it incorrectly absorbed the original parent paper into the companion synthesis.

## Public observation state

Fresh independent public observation remains required for:

- `news-releases.html` showing the companion and not the parent/addendum as separate current releases;
- `papers/coherent-life-companion/` rendering;
- `papers/coherent-life-and-admissible-existence/` rendering as the standalone parent;
- `Papers.html` showing exactly two Coherent Life publication identities: companion + parent.

Current state:

`SOURCE_CORRECTED_PUBLIC_REOBSERVATION_PENDING`

## Classification boundary

Current News Releases and Papers are public communication/publication surfaces. They do not establish execution, activation, custody, certification, admissibility, credential authority, transition authority, empirical validation, or research-release authority.

## Remaining work

1. Obtain fresh independent public observation of the corrected routes.
2. Preserve the original parent-paper identity; do not fold either addendum into it again.
3. Preserve the companion as exactly notation/theorem witnesses + Addendum I + Addendum II unless the canonical AE owner intentionally revises that source set.
4. Keep the legacy Addendum I route stable for existing deep links unless a later governed migration intentionally redirects it.
5. Install the corrected companion source/artifact into `Admissible-Existence/AE` through an artifact-capable repository path before claiming a canonical AE PDF.
6. At actual publication tag/release readiness, verify pertinent propagation to `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki`.

## Release posture

No repository tag or product/research release is created by this static Site correction. Source installation or deployment does not imply fresh public observation, empirical validation, or research-release authority.

## Archive readiness

The corrected publication identity, source-set boundary, Site routes, validator behavior, excluded adjacent papers, and remaining artifact-installation/public-observation tasks are repository-resident. No conversation-only information is required to continue this Site lane.
