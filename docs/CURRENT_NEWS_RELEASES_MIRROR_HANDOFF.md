# Current News Releases Mirror Handoff

## Source of truth

This is the bounded continuation record for StegVerse-Labs/Site issue #967 and subsequent admitted publication extensions. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.

## Goal

Maintain a first-class **Current News Releases** surface on StegVerse.org and a coherent Papers publication surface, with deterministic newest-first ordering, stable canonical URLs, and no inference of runtime or governance authority from public display.

## Current implementation

Public routes now include:

- `index.html` — homepage discovery for Current News Releases
- `news-releases.html` — Current News Releases index
- `papers/coherent-life-and-admissible-existence/index.html` — public projection of **Coherent Life and Admissible Existence**
- `papers/coherent-life-and-admissible-existence/empirical-addendum-i.html` — **Empirical Addendum I: Unknown-Class Transformation at the Quantum-Gravitational Boundary**
- `papers/stegverse-entity-economy-volume-ii/index.html` — Entity Economy Volume II
- `papers/stegverse-entity-economy/index.html` — Entity Economy Volume I
- `papers/stegverse-entity-economy/stegverse-entity-economy.pdf` — canonical nine-page Volume I PDF
- `news-releases/ai-is-becoming-infrastructure-sovereignty-must-go-further.html` — StegVerse LLC South Korea comparative statement
- `Papers.html` — public Papers index

## Admissible Existence extension — 2026-09-04

The canonical research work **Coherent Life and Admissible Existence: A Coupled Theory of Boundaries, Recoverability, Authority, Purpose, and Continued Coherence** is owned by `Admissible-Existence/AE`. It was not present as a public Site paper before this extension; the only matching prior Site references were internal coordination/ownership references rather than a public paper route.

Installed Site projection:

```text
papers/coherent-life-and-admissible-existence/index.html
```

The public projection preserves the canonical paper's bounded thesis and non-claims while leaving canonical research ownership, validation, release authority, and source mathematics in `Admissible-Existence/AE`.

The first empirical addendum is installed immediately after the parent paper in Current News Releases and Papers:

```text
papers/coherent-life-and-admissible-existence/empirical-addendum-i.html
```

Title:

**Empirical Addendum I — Unknown-Class Transformation at the Quantum-Gravitational Boundary**

The addendum applies the AE state/uncertainty distinction to the 2026 quantum equivalence-principle experiment. It explicitly preserves the boundary:

```text
observation != interpretation != established knowledge
```

and does not claim that the experiment validates Admissible Existence, proves quantum gravity, or unifies general relativity with quantum mechanics.

Implementation commits:

- parent paper public landing page: `d47a6e996cf8f863f80083c5ede953042a2ba722`
- empirical addendum public page: `7df1c9a946a2bacacd4e55f7cb679a888e13d629`
- Current News Releases ordering update: `18360f9ae229064e1a873056c780a1fa39337c70`
- Papers index feature update: `bdef246211191811f3cf20f8c07ed6d812c73cbd`
- publication-extension handoff state: `81212a6f096bd872d407d681bb6d7f053137a130`
- Current News Releases validator reconciliation: `2a5b806f5f99c3c38b742bdbaf5fd814dd79be06`

## Ordering contract

`news-releases.html` is deterministic by machine-readable publication date and explicit sequence. Newer dates sort first; same-day releases use sequence ordering. Existing canonical release URLs remain stable.

Current required ordering:

1. Coherent Life and Admissible Existence — 2026-09-04 sequence 5
2. Empirical Addendum I — Unknown-Class Transformation at the Quantum-Gravitational Boundary — 2026-09-04 sequence 4
3. The StegVerse Entity Economy — Volume II — 2026-09-03 sequence 3
4. The StegVerse Entity Economy — Volume I — 2026-09-03 sequence 2
5. AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model. — 2026-09-03 sequence 1

## Prior Entity Economy evidence

The Entity Economy publication lane remains installed and unchanged in authority posture. Existing evidence includes the canonical Volume I PDF, landing page, Current News Releases ordering, and Papers projection. Economic entitlement does not create governance authority.

## Validation and deployment evidence

Exact publication-extension head `81212a6f096bd872d407d681bb6d7f053137a130` received successful GitHub Pages build/deployment evidence:

```text
workflow: pages build and deployment
run: 33936094235
result: SUCCESS
completed: 2026-09-05T01:29:44Z
```

The same exact head received a failure in the repository-wide `Site Bootstrap Validate - No Non-TV/TVC Credential Authority` workflow run `33936094630`. Inspection of the failed job shows the publication/orchestration preconditions passed, including session-work claims, Site handoff orchestration, and ecosystem heartbeat orchestration. The failure occurred later in the canonical Site application check because `scripts/check_stegos_ipod_bootstrap_projection.py` rejected a changed `stegos-bootstrap/index.html` blob that was not present in its allowed blob set. That is an adjacent StegOS projection-drift failure and is not evidence that this publication extension failed.

A publication-lane validation defect was also discovered and repaired: `scripts/check_current_news_releases.py` still asserted the former Papers-page literal `Site-native bounded publications: 6` and did not validate the new Admissible Existence parent/addendum routes. Commit `2a5b806f5f99c3c38b742bdbaf5fd814dd79be06` replaces that stale count coupling with explicit validation of:

- parent paper and addendum file presence;
- deterministic parent → addendum → existing-release ordering;
- canonical Site routes;
- parent/addendum authority and empirical-validation boundaries;
- addendum DOI and transition relation;
- Papers discovery and parent-before-addendum ordering.

No public availability claim is inferred solely from successful deployment machinery.

## Public observation state

Previously observed public Site surfaces remain historical evidence for their exact deployed bytes.

Fresh independent public observation remains required for:

- `news-releases.html` showing the Admissible Existence parent paper first and the addendum immediately second;
- `papers/coherent-life-and-admissible-existence/` rendering;
- `papers/coherent-life-and-admissible-existence/empirical-addendum-i.html` rendering;
- `Papers.html` showing the parent paper as current featured publication and the addendum immediately adjacent.

Current state for the new extension:

`DEPLOYMENT_SUCCESS_PUBLIC_REOBSERVATION_PENDING`

## Classification boundary

Current News Releases and Papers are public communication/publication surfaces. They do not establish execution, activation, custody, certification, admissibility, credential authority, transition authority, empirical validation, or release authority.

## Remaining work

1. Obtain fresh independent public observation for the four routes listed above.
2. Preserve the parent-paper → empirical-addendum ordering in Current News Releases and Papers.
3. Keep the unrelated StegOS bootstrap-projection blob drift in its existing owning lane; do not recast it as a publication failure.
4. If a canonical public PDF of the parent paper is later released by `Admissible-Existence/AE`, bind the Site landing page to that exact artifact rather than creating an independent competing canonical PDF.
5. If the empirical addendum PDF is admitted into canonical AE publication, bind the Site addendum page to that exact canonical artifact rather than treating the current Site HTML projection as canonical research source.
6. At actual release/tag readiness, verify any pertinent publication propagation to `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki`.

## Release posture

No repository tag or product release is created by this static Site integration. Source installation plus successful Pages deployment does not imply fresh public observation, empirical validation, or research-release authority.

## Archive readiness

Repository state contains the full continuation record for this publication extension, including deployment evidence, the unrelated repository-wide validation failure classification, and the reconciled publication validator. No conversation-only information is required to continue public observation or later canonical-artifact binding.
