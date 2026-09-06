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
  includes complete 36-page artifact discovery

papers/coherent-life-and-admissible-existence/artifact/index.html
  fail-closed browser reconstruction surface for the complete 36-page artifact

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
- companion and standalone Addendum I routes remain separately addressable but are not promoted as peer publication identities;
- the parent links the complete 36-page artifact reconstruction surface;
- the artifact surface references all nine repository-resident transport parts;
- the artifact loader fails closed unless it observes a PDF header, PDF EOF marker, and `/Count 36` catalog marker;
- the artifact loader computes SHA-256 over the reconstructed bytes before exposing open/download controls.

## Artifact posture

A corrected 14-page exact-source companion PDF was assembled from the three supplied PDFs in this order:

```text
1. ae-notation-and-witnesses
2. admissible_existence_empirical_addendum_quantum_equivalence
3. admissible_existence_empirical_addendum_ii_quantum_thermodynamics
```

This is a byte-preserving page concatenation of the three source PDFs, not a rewrite of the parent paper. It is an attached companion artifact candidate, not a replacement primary paper.

The earlier 15-page integrated-full-paper artifact is not canonical because it incorrectly absorbed the parent working paper into the companion synthesis.

### Complete Coherent Life 36-page artifact binding — 2026-09-05

The approved complete publication artifact consists of the original 22-page working paper followed by the 14 pages of attached companion materials, for 36 pages total.

Approved local source observation:

```text
filename: coherent-life-and-admissible-existence-with-attached-companion-materials.pdf
page_count: 36
byte_size: 413092
sha256: 6afed983e236b260718df548f40cac2e1a8c12cd9c8f82a28c7a5f757eefe918
parent_pages: 22
attached_companion_pages: 14
```

Existing repository-resident base64 transport parts were discovered under:

```text
papers/coherent-life-and-admissible-existence/artifact/coherent-life-36-page.part00.b64
...
papers/coherent-life-and-admissible-existence/artifact/coherent-life-36-page.part08.b64
```

These parts originated in earlier staging commits `caba7f1835cb1d4457007beda9d824761ded9a89` and `18e04d3a8d2780c6981adb5a17dc5c7feec33374`, whose commit messages identify them as the exact 36-page artifact carrier. They are reused rather than duplicated.

The connected GitHub contents writer exposes UTF-8 text writes but not a local binary-file parameter. The public artifact surface therefore reconstructs the repository-resident base64 parts in-browser and fails closed before exposing the PDF unless the reconstructed data has a PDF header, PDF EOF marker, and the expected 36-page catalog marker. It also computes SHA-256 over the reconstructed bytes and displays the observed digest.

Current source bindings:

```text
482418af176672857d13be18a60cebc90d4476d7  machine preflight + README completeness determination
2c8572df3d519092213e1acfd4c5cd64c0649d39  extend existing publication claim; no duplicate claim/task
a398bbddb8d4f20c4bb1a0bb8ce1a9d8ab2c6982  publish fail-closed 36-page artifact reconstruction surface
1bf07fe96efb414750118a534aed50983695491a  bind parent page to complete 36-page artifact
095aa108f344c9884cd38a34e8eb3636e8e33851  validate artifact route/parts/fail-closed checks
69db197a535deb0cd622514916d7ee2dec8fe579  reconcile task state to source-bound/public-reobservation-pending
```

Important evidence boundary: the repository transport parts have not yet been independently proven byte-identical to the 413092-byte local approved source in this continuation. The public loader's computed digest is therefore an observation to compare during fresh public verification; no exact-byte equivalence is inferred from the staging commit messages alone.

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

During the 36-page binding continuation, a fresh crawl of `https://stegverse.org/Papers.html` continued to show exactly one Coherent Life publication identity with attached companion materials described beneath it. The newly committed parent/artifact route could not yet be independently fetched by the public crawler, so fresh deployment of the 36-page artifact surface remains unproven.

Still required:

- `news-releases.html` rendering the new edition selector and default latest-edition feed;
- historical edition switching on `news-releases.html`;
- All releases aggregate mode on `news-releases.html`;
- `news-releases.html` pointing to the Coherent Life parent and describing attached extensions;
- `papers/coherent-life-and-admissible-existence/` showing the complete 36-page artifact link after deployment;
- `papers/coherent-life-and-admissible-existence/artifact/` reconstructing the 36-page PDF and reporting its observed SHA-256;
- `papers/coherent-life-companion/` remaining reachable as subordinate material;
- Volume I landing/PDF fresh public observation;
- Volume II landing/PDF fresh public observation after the canonical binary is installed.

Current state:

`COHERENT_LIFE_36_PAGE_SOURCE_BOUND_PUBLIC_REOBSERVATION_PENDING_AND_VOLUME_II_BINARY_PENDING`

## Classification boundary

Current News Releases and Papers are public communication/publication surfaces. They do not establish execution, activation, custody, certification, admissibility, credential authority, transition authority, empirical validation, or research-release authority.

## Remaining work

1. Complete current-main validation for the Coherent Life 36-page source binding and record the exact result.
2. Obtain fresh independent public observation of the Coherent Life parent and artifact loader, including the loader-reported reconstructed SHA-256; compare it with the approved local source digest without inferring equality if it differs.
3. Install the already-supplied canonical Entity Economy Volume II PDF at `papers/stegverse-entity-economy-volume-ii/stegverse-entity-economy-volume-ii.pdf` using an artifact-capable GitHub write path; verify the installed binary against SHA-256 `129accea04dcef0c5b063ae5799d9952e97462859fb36842c93a3ca7776fe95f`.
4. Obtain the remaining fresh independent public observations listed above; the Papers two-volume series presentation is already freshly observed.
5. Preserve deterministic date/sequence ordering as new releases are prepended.
6. Keep historical editions reconstructable instead of silently rewriting prior public states.
7. Preserve the parent working-paper identity and attached-companion relationship.
8. Keep the companion source set exactly notation/theorem witnesses + Addendum I + Addendum II unless the canonical AE owner intentionally revises it.
9. Keep the legacy Addendum I route stable for existing deep links unless a later governed migration intentionally redirects it.
10. At actual publication tag/release readiness, verify pertinent propagation to `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki`.

## README completeness determination — 2026-09-05 execution preflight

No README update is required for this publication-artifact binding. The repository README already states the applicable public-mirror/non-authority boundary and identifies `Papers.html` as the Papers/research surface. The change completes an already-declared static paper artifact and does not materially change repository behavior, runtime semantics, governance/authority boundaries, prerequisites, dependencies, failure authority, or capability meaning. The exact evidence and invalidation condition are recorded in `docs/COHERENT_LIFE_36_PAGE_ARTIFACT_PREFLIGHT.md`.

## Volume II binary-install machine preflight — 2026-09-05T20:44-05:00

```text
candidate_work: install already-supplied canonical Volume II PDF at the already-claimed repository path
canonical_task: SITE-CURRENT-NEWS-RELEASES-967
claim: SITE-CURRENT-NEWS-RELEASES-967-20260903 / CLAIMED_FOR_INTEGRATION
claim_contains_target_path: true
HIL_upload_task: COMPLETED by repository controller
exclusive_HIL_live_task: BLOCKED on sovereign carrier + custody/reconstruction predicates
open_PR_collision_on_target_pdf_path: none observed
open_PR_collision_on_news-releases.html: PR #989 exists; this step MUST NOT modify news-releases.html
master_records_role: observed reality/custody/reconstruction only; no task-admission authority inferred
canonical_task_registry_role: work intent/coordination only; no execution authority inferred
artifact_source: supplied Volume II PDF already resolved and hash-bound
expected_sha256: 129accea04dcef0c5b063ae5799d9952e97462859fb36842c93a3ca7776fe95f
functional_scope: binary artifact installation only
```

### README completeness predicate

**NO README CHANGE REQUIRED for the binary installation itself.** Installing the exact already-declared canonical paper artifact at its already-declared public-paper path does not change repository behavior, runtime semantics, interfaces, governance/authority boundaries, evidence semantics, prerequisites, dependencies, failure behavior, or capability meaning. It completes an existing publication artifact whose surface and non-authority semantics are already documented by the README and this handoff. If the installation step changes any public interface or authority semantics beyond making the declared PDF artifact present, this determination is invalid and README must be updated in that same change set.

Preflight result: `PASS_FOR_CLAIMED_BINARY_ARTIFACT_INSTALL_ONLY`.

## Release posture

No repository tag or product/research release is created by this static Site correction. Source installation or deployment does not imply fresh public observation, empirical validation, or research-release authority.

## Archive readiness

The editioned-feed contract, corrected parent-with-attached-companion hierarchy, 36-page artifact source binding, fail-closed artifact loader, validator contract, source-set boundary, Site routes, exclusions, supplied Volume II artifact identity/digest, README completeness determinations, collision state, and remaining public-observation/binary-install tasks are repository-resident. No conversation-only information is required to continue this Site lane.
