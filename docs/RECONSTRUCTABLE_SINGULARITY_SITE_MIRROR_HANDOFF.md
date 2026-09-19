# Reconstructable Singularity Site Mirror Handoff

## Canonical identity

- Goal Task ID: `ADMISSIBILITY-RECONSTRUCTABLE-SINGULARITY-001`
- source handoff: `StegVerse-Labs/admissibility-wiki/docs/formalisms/RECONSTRUCTABLE_SINGULARITY_MIRROR_HANDOFF.md`
- Site parent authority: `docs/SITE_MIRROR_HANDOFF.md`
- current public route: `papers/reconstructable-singularity.html`
- legacy compatibility route: `reconstructive-singularity.html`
- index: `Papers.html`
- posture: `RESEARCH_NOTE / SOURCE_MIRROR`
- supersedes: former standalone Site paper `The Reconstructive Singularity`

## Scope

Site publishes one current integrated paper: **Reconstructable Singularity**. It incorporates the useful reconstruction/reachability material from the former Reconstructive Singularity Site paper and adds the newer minimum continuity-resolving perspective formalism from Admissibility Wiki.

The former paper is not retained as a separate current publication. Its old URL remains only as a compatibility redirect.

## New formalism incorporated

The current paper includes:

- realized-state continuity with one cost-bearing transition between adjacent realized states;
- candidate histories `Γ` and admissibility-consistent histories `Γ_A`;
- affirmative and exclusionary observer evidence;
- singleton reconstruction `|C_A(I)| = 1`;
- minimum continuity-resolving perspective threshold `k_A*`;
- injective combined observer maps `G_I`;
- pairwise distinguishing sets and equivalent minimum hitting-set formulation;
- observer disagreement classes;
- explicit ontic-realization versus epistemic-uncertainty separation.

## Earlier useful scope retained

The integrated paper also retains bounded treatment of:

- reachability versus achievability/admissibility/authority/execution;
- temporal reconstruction without physical reinstatement;
- cross-domain coordinate transformation;
- identity continuity;
- drift and common-cause controls;
- unknowns, information loss, residuals, underdetermination, and falsification.

Historical deterministic simulation or procedural-validation statements attached to the older paper are not treated as validation of the newly added formalism unless the current canonical source validation independently establishes them.

## Non-claims

Site publication does not establish empirical proof, universal reconstruction completeness, physical collapse or access to histories, runtime execution, custody, admissibility, certification, release, legal, or clinical authority.

## Validation

```text
python3 scripts/check_reconstructable_singularity_publication.py
```

The checker must require:

1. exactly one current Papers index entry for Reconstructable Singularity;
2. no current Papers index entry for Reconstructive Singularity;
3. the old route to be a compatibility redirect only;
4. the current page to contain the newer singleton/minimum-perspective/injectivity formalism;
5. the public registry to identify the new paper as current and the old title as superseded provenance;
6. authority and empirical non-claims.

## README impact

`NO_README_CHANGE_REQUIRED`.

The repository README already identifies `Papers.html` as the papers/research aggregation surface and documents the public-mirror boundary. This is a publication supersession inside that existing mechanism, not a new Site runtime capability.

## Completion gates

1. Admissibility Wiki canonical formalism validation passes on the current source PR.
2. Site exact-head validation passes.
3. Site PR merges to `main`.
4. The current public route is directly observed with the expected title/formalism markers.
5. The legacy URL is directly observed redirecting to the current paper.
6. Source handoff is reconciled with the final Site propagation evidence.

Until those gates pass, source/CI state must not be described as deployed public verification.
