# Current News Releases Mirror Handoff

## Source of truth

This is the bounded continuation record for StegVerse-Labs/Site issue #967 and subsequent admitted publication extensions. Repository-wide authority remains `docs/SITE_MIRROR_HANDOFF.md`.

## Goal

Maintain a first-class **Current News Releases** surface on StegVerse.org and a coherent Papers publication surface, with deterministic newest-first ordering, stable canonical URLs, and no inference of runtime or governance authority from public display.

## Editioned feed UX — 2026-09-05

The Current News Releases landing page now uses an editioned mobile-first feed model inspired by the observed Edukors news surface while preserving StegVerse-specific provenance and publication boundaries.

Implemented source behavior:

```text
news-releases.html
  -> News feed container
  -> Edition selector
  -> latest edition selected by default
  -> historical date editions remain directly selectable
  -> All releases remains available as an explicit aggregate view
  -> filtering resolves from canonical data-published attributes
  -> deterministic data-published + data-sequence ordering remains preserved
  -> public authority-boundary language remains visible
```

Current edition options installed in source:

```text
2026-09-05
2026-09-04
2026-09-03
all
```

The edition selector is a discovery/reconstruction surface only. It does not rewrite historical records, create new publication identities, or grant execution, activation, custody, certification, admissibility, governance, or release authority.

Implementation commits:

```text
e50510064f49346dd69d5cca37e011de086c5e93  redesign Current News Releases as editioned mobile feed
509d57a310a93fb2efa345f85db4889ae0381f46  validate edition selector, historical editions, all-releases mode, and data-published filtering
```

Fresh public browser observation of the deployed edition selector and filtering behavior is still required before the redesign is called publicly verified.

## Corrected Coherent Life publication hierarchy — 2026-09-04

The prior over-integrated and later two-peer-publication projections are superseded.

There is one primary publication identity:

**Coherent Life and Admissible Existence: A Coupled Theory of Boundaries, Recoverability, Authority, Purpose, and Continued Coherence**.

The parent working paper remains unchanged in identity. Attached beneath it is one separately addressable companion bundle containing exactly:

```text
1. Supplement: Notation Table and Theorem Witnesses
2. Empirical Addendum I — Unknown-Class Transformation at the Quantum-Gravitational Boundary
3. Empirical/Theoretical Addendum II — Recoverable Capacity Across Representational Boundaries
```

The companion is subordinate to the parent publication. It is separately addressable for citation, reconstruction, and stable linking, but it is not a peer publication identity on Current News Releases or Papers.

The following adjacent papers remain excluded:

```text
Development Without Domination
Adversarial AI, Public Authority, and the Receipt Problem
```

## Public routes

```text
papers/coherent-life-and-admissible-existence/index.html
  primary Coherent Life working-paper public projection
  includes attached-companion discovery

papers/coherent-life-companion/index.html
  separately addressable attached companion bundle

papers/coherent-life-and-admissible-existence/empirical-addendum-i.html
  retained legacy deep-link compatibility surface only

news-releases.html
  publishes the Coherent Life parent as the release and states that companion extensions are attached

Papers.html
  exposes one Coherent Life publication identity; companion materials are described beneath the parent
```

Neither the companion route nor the legacy Addendum I route is an independent Current News Release or Papers publication card.

## Current News Releases ordering

Current required ordering:

1. Hugging Face, NVIDIA, and the Path From Capability to Consequence — 2026-09-05 sequence 6
2. Coherent Life and Admissible Existence — 2026-09-04 sequence 5
3. The StegVerse Entity Economy — Volume II — 2026-09-03 sequence 3
4. The StegVerse Entity Economy — Volume I — 2026-09-03 sequence 2
5. AI Is Becoming Infrastructure. Sovereignty Must Go Further Than the Model. — 2026-09-03 sequence 1

## Companion conceptual boundary

```text
notation / theorem witnesses
  -> preserve formal distinctions and prevent symbol drift

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

## Implemented hierarchy correction commits

```text
f4fa663dd833d628878f1cfc5498e462d1ca2532  attach companion discovery to parent
ec28bd9739301e3a57858a5ea6a4883bbaf8713a  Current News Releases points to parent with attached extensions
edeed58875694d6b751879c70e783fd48517760b  Papers exposes one parent identity with attached companion description
b313e974af01afa740934578457c38ba2345e45f  validate attached-companion hierarchy
```

Earlier commits that over-integrated the parent or promoted the companion as a peer publication remain historical evidence only and are not the current publication contract.

## Validation contract

`scripts/check_current_news_releases.py` requires:

- Current News Releases landing exists;
- machine-readable publication ordering is reverse chronological by date/sequence;
- edition selector exists and is accessibility-described;
- 2026-09-05 is the default current edition;
- 2026-09-04 and 2026-09-03 remain selectable historical editions;
- explicit All releases mode remains available;
- filtering resolves from each release's `data-published` value;
- parent working-paper route exists;
- attached companion route exists;
- parent does not embed either addendum into its body;
- parent exposes an **Attached companion materials** section linking the companion;
- companion contains notation/theorem witnesses + Addendum I + Addendum II;
- Current News Releases points to the parent, not the companion or standalone addendum;
- Papers exposes one Coherent Life publication card, with attached companion materials described beneath it;
- companion and standalone Addendum I routes remain separately addressable but are not promoted as peer publication identities.

## Artifact posture

A corrected 14-page exact-source companion PDF was assembled from the three supplied PDFs in this order:

```text
1. ae-notation-and-witnesses
2. admissible_existence_empirical_addendum_quantum_equivalence
3. admissible_existence_empirical_addendum_ii_quantum_thermodynamics
```

This is a byte-preserving page concatenation of the three source PDFs, not a rewrite of the parent paper. It is an attached companion artifact candidate, not a replacement primary paper.

The earlier 15-page integrated-full-paper artifact is not canonical because it incorrectly absorbed the parent working paper into the companion synthesis.

### Entity Economy Volume II supplied artifact — 2026-09-05

The canonical Volume II PDF has now been supplied to the execution session and inspected as a seven-page, openable, non-encrypted PDF.

```text
source filename: StegVerse_Entity_Economy_Volume_II(1).pdf
page count: 7
sha256: 129accea04dcef0c5b063ae5799d9952e97462859fb36842c93a3ca7776fe95f
intended repository path: papers/stegverse-entity-economy-volume-ii/stegverse-entity-economy-volume-ii.pdf
source artifact identity: The StegVerse Entity Economy — Volume II — Identity, Agency, Labor, Autonomy, and Legal Standing
artifact preflight: PASS / openable / not encrypted / not likely scanned
```

The supplied artifact resolves the prior missing-source blocker. Binary repository installation remains pending only because the currently connected GitHub write surface accepts UTF-8 text writes and Git object text/base64 payloads but exposes no direct local-file binary upload parameter. This transport limitation is not a request for the user to regenerate or resupply the PDF. The exact source bytes and digest above remain the installation target.

A fresh 2026-09-05 execution preflight rematerialized the supplied Volume II artifact and independently recomputed the same SHA-256 `129accea04dcef0c5b063ae5799d9952e97462859fb36842c93a3ca7776fe95f`; the target repository path remains absent on current `main`, so no duplicate binary installation is being inferred.

## Public observation state

Fresh independent public HTTP observation at `2026-09-05T19:31:00-05:00` confirmed `https://stegverse.org/Papers.html` publicly renders **The StegVerse Entity Economy — Volume II** immediately before **The StegVerse Entity Economy — Volume I**, while retaining the Site publication-boundary language. This satisfies the Papers two-volume series presentation observation only; it does not prove either paper route or either PDF artifact.

Still required:

- `news-releases.html` rendering the new edition selector and default latest-edition feed;
- historical edition switching on `news-releases.html`;
- All releases aggregate mode on `news-releases.html`;
- `news-releases.html` pointing to the Coherent Life parent and describing attached extensions;
- `papers/coherent-life-and-admissible-existence/` showing attached companion discovery;
- `papers/coherent-life-companion/` remaining reachable as subordinate material;
- Volume I landing/PDF fresh public observation;
- Volume II landing/PDF fresh public observation after the canonical binary is installed.

Current state:

`SOURCE_EDITION_FEED_AND_HIERARCHY_CORRECTED_PARTIAL_PUBLIC_REOBSERVATION_BINARY_INSTALL_PENDING`

## Classification boundary

Current News Releases and Papers are public communication/publication surfaces. They do not establish execution, activation, custody, certification, admissibility, credential authority, transition authority, empirical validation, or research-release authority.

## Remaining work

1. Install the already-supplied canonical Entity Economy Volume II PDF at `papers/stegverse-entity-economy-volume-ii/stegverse-entity-economy-volume-ii.pdf` using an artifact-capable GitHub write path; verify the installed binary against SHA-256 `129accea04dcef0c5b063ae5799d9952e97462859fb36842c93a3ca7776fe95f`.
2. Obtain the remaining fresh independent public observations listed above; the Papers two-volume series presentation is already freshly observed.
3. Preserve deterministic date/sequence ordering as new releases are prepended.
4. Keep historical editions reconstructable instead of silently rewriting prior public states.
5. Preserve the parent working-paper identity and attached-companion relationship.
6. Keep the companion source set exactly notation/theorem witnesses + Addendum I + Addendum II unless the canonical AE owner intentionally revises it.
7. Keep the legacy Addendum I route stable for existing deep links unless a later governed migration intentionally redirects it.
8. Install canonical AE source/artifact representations for the attached companion through an artifact-capable path.
9. At actual publication tag/release readiness, verify pertinent propagation to `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki`.

## README completeness determination — 2026-09-05 execution preflight

No README update is required for the evidence-only changes in this continuation step. The change records an independently observed public Papers projection and re-verifies the exact already-declared Volume II artifact digest; it does not change repository behavior, runtime semantics, interfaces, governance or authority boundaries, evidence semantics, prerequisites, dependencies, failure behavior, or capability meaning. The repository README already states the applicable public-mirror/non-authority boundary and identifies `Papers.html` as the Papers/research surface.

## Release posture

No repository tag or product/research release is created by this static Site correction. Source installation or deployment does not imply fresh public observation, empirical validation, or research-release authority.

## Archive readiness

The editioned-feed contract, publication hierarchy, source-set boundary, Site routes, validator behavior, exclusions, supplied Volume II artifact identity/digest, fresh Papers series observation, README completeness determination, and remaining artifact/public-observation tasks are repository-resident. No conversation-only information is required to continue this Site lane.
