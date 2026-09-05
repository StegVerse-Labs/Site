# Current News Releases Mirror Handoff

## Source of truth

This is the bounded continuation record for StegVerse-Labs/Site issue #967 and subsequent admitted publication extensions. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.

## Goal

Maintain a first-class **Current News Releases** surface on StegVerse.org and a coherent Papers publication surface, with deterministic newest-first ordering, stable canonical URLs, and no inference of runtime or governance authority from public display.

## Current implementation

Public routes include:

- `index.html` — homepage discovery for Current News Releases
- `news-releases.html` — Current News Releases index
- `papers/coherent-life-and-admissible-existence/index.html` — conjoined public projection of **Coherent Life and Admissible Existence** plus its first bounded empirical application
- `papers/coherent-life-and-admissible-existence/empirical-addendum-i.html` — retained legacy deep-link projection for **Empirical Addendum I: Unknown-Class Transformation at the Quantum-Gravitational Boundary**; not a separate Current News Releases entry
- `papers/stegverse-entity-economy-volume-ii/index.html` — Entity Economy Volume II
- `papers/stegverse-entity-economy/index.html` — Entity Economy Volume I
- `papers/stegverse-entity-economy/stegverse-entity-economy.pdf` — canonical nine-page Volume I PDF
- `news-releases/ai-is-becoming-infrastructure-sovereignty-must-go-further.html` — StegVerse LLC South Korea comparative statement
- `Papers.html` — public Papers index

## Coherent Life conjoined-publication extension — 2026-09-04

The canonical research work **Coherent Life and Admissible Existence: A Coupled Theory of Boundaries, Recoverability, Authority, Purpose, and Continued Coherence** is owned by `Admissible-Existence/AE`.

The Current News Releases surface now represents the formal paper and its first bounded empirical application as **one conjoined publication entry**. The former two-entry Current News Releases model is superseded.

Canonical Site entry:

```text
papers/coherent-life-and-admissible-existence/index.html
```

The conjoined page contains both:

1. the formal Coherent Life / Admissible Existence public projection; and
2. **Unknown-Class Transformation at the Quantum-Gravitational Boundary** as an integrated empirical application section.

The retained historical deep link:

```text
papers/coherent-life-and-admissible-existence/empirical-addendum-i.html
```

remains available for stable-link compatibility, but Current News Releases must not present it as an independent release.

The empirical application preserves the boundary:

```text
observation != interpretation != established knowledge
```

and does not claim that the experiment validates Admissible Existence, proves quantum gravity, or unifies general relativity with quantum mechanics.

Implementation commits for this conjoined projection:

- Current News Releases one-entry replacement: `054b807f0cf3e19e9e7a1133076ca50dba228844`
- conjoined Coherent Life public page: `ef02231b8c1b46658269c06bea4d2c3d1b5058e8`
- conjoined Current News Releases validator: `062984b52d5b02dbfa1dfbf87efdf085f129ff7a`

Prior installation commits retained as history:

- parent paper public landing page: `d47a6e996cf8f863f80083c5ede953042a2ba722`
- empirical addendum public page: `7df1c9a946a2bacacd4e55f7cb679a888e13d629`
- former two-entry ordering update: `18360f9ae229064e1a873056c780a1fa39337c70`
- Papers index feature update: `bdef246211191811f3cf20f8c07ed6d812c73cbd`
- publication-extension handoff state: `81212a6f096bd872d407d681bb6d7f053137a130`
- prior Current News Releases validator reconciliation: `2a5b806f5f99c3c38b742bdbaf5fd814dd79be06`

## Ordering contract

`news-releases.html` is deterministic by machine-readable publication date and explicit sequence. Newer dates sort first; same-day releases use sequence ordering. Existing canonical release URLs remain stable.

Current required Current News Releases ordering:

1. Coherent Life and Admissible Existence — conjoined formal paper + empirical application — 2026-09-04 sequence 5
2. The StegVerse Entity Economy — Volume II — 2026-09-03 sequence 3
3. The StegVerse Entity Economy — Volume I — 2026-09-03 sequence 2
4. AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model. — 2026-09-03 sequence 1

The separate Empirical Addendum I entry is prohibited on Current News Releases. Stable legacy access to its old route remains allowed.

## Prior Entity Economy evidence

The Entity Economy publication lane remains installed and unchanged in authority posture. Existing evidence includes the canonical Volume I PDF, landing page, Current News Releases ordering, and Papers projection. Economic entitlement does not create governance authority.

## Validation posture

`scripts/check_current_news_releases.py` now validates the conjoined model explicitly:

- one Current News Releases entry for Coherent Life;
- no standalone Empirical Addendum I Current News Releases route or title;
- conjoined-page classification marker;
- integrated empirical section title;
- primary DOI `10.1126/sciadv.aec8045`;
- `Observation → Constraint → Unknown transformation → Admissible interpretation` relation;
- canonical ownership and non-validation boundaries;
- deterministic conjoined Coherent Life → Entity Economy → South Korea ordering.

The legacy addendum file remains required only as a stable deep-link compatibility surface. `Papers.html` remains unchanged by this bounded Current News Releases correction and may continue to expose the addendum separately until that surface is intentionally consolidated.

No public availability claim is inferred solely from successful source installation or deployment machinery.

## Public observation state

Fresh independent public observation is required for:

- `news-releases.html` showing one conjoined Coherent Life entry and no standalone Empirical Addendum I release;
- `papers/coherent-life-and-admissible-existence/` rendering the integrated empirical application section;
- deterministic ordering of the remaining Current News Releases entries.

Current state for the conjoined correction:

`SOURCE_INSTALLED_PUBLIC_REOBSERVATION_PENDING`

## Classification boundary

Current News Releases and Papers are public communication/publication surfaces. They do not establish execution, activation, custody, certification, admissibility, credential authority, transition authority, empirical validation, or release authority.

## Remaining work

1. Obtain fresh independent public observation for the conjoined Current News Releases index and conjoined paper route.
2. Preserve the single-entry Coherent Life Current News Releases model; do not restore a separate addendum release card.
3. Keep the legacy addendum route stable for existing deep links unless a later governed migration intentionally redirects it.
4. Decide separately whether `Papers.html` should also collapse its parent/addendum discovery into one conjoined entry; this bounded change does not infer that decision.
5. Keep unrelated Site validation failures in their existing owning lanes; do not recast them as publication failures.
6. If canonical public PDF artifacts are later released by `Admissible-Existence/AE`, bind the Site projection to those exact artifacts rather than creating competing canonical research artifacts.
7. At actual release/tag readiness, verify any pertinent publication propagation to `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki`.

## Release posture

No repository tag or product release is created by this static Site integration. Source installation or successful deployment does not imply fresh public observation, empirical validation, or research-release authority.

## Archive readiness

The conjoined Current News Releases source change, validator contract, stable-link policy, and continuation requirements are repository-resident. No conversation-only information is required to continue public observation or a later intentional Papers-surface consolidation.
