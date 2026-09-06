# Containment / Transition Governance Research Lane Mirror Handoff

## Canonical task

- Site issue: #1045
- Branch: `research/containment-transition-governance`
- Goal: produce one incident-driven bounded Site-native research paper explaining why containment is not sufficient governance and connect it to existing StegVerse transition-governance publications.

## Canonical state resolved before functional mutation

Resolved sources of truth:

- `SITE_MIRROR_HANDOFF.md` — repository-wide Site continuation authority.
- `docs/SESSION_PREWORK_CLAIMS_MIRROR_HANDOFF.md` — mutable Site work must carry exactly one active machine-readable pre-work claim and must fail closed on collision.
- `data/session-work-claims.json` + `scripts/check_session_work_claims.py` — local claim registry and validator.
- `StegVerse-Labs/.github/docs/CROSS_REPO_DEPENDENCY_CLAIMS_MIRROR_HANDOFF.md` + `control/claims-active.json` — stronger cross-repository dependency-surface coordination authority.
- `master-records/orchestration/MASTER_RECORDS_ORCHESTRATION_MIRROR_HANDOFF.md` — Master Records remains custody/reconstruction only and does not grant publication, runtime, release, or admissibility authority.
- `GCAT-BCAT-Engine/Publisher/PUBLISHER_MIRROR_HANDOFF.md` — Publisher machine-owned propagation lanes remain separate and must not be entered by this Site research task.
- `PUBLICATION_PROCESS.md` — Site is a public mirror, not proof authority; this lane uses `RESEARCH_NOTE` posture.
- `Papers.html` and `public-registry.json` — current public research index and publication posture registry.

## Reused existing theory and publications

This lane MUST link and extend, not duplicate or supersede:

- `docs/public-positioning/ai-safety-to-transition-admissibility.md`
- `papers/authority-at-the-commit-boundary.html`
- `minimum-pre-self-management-governance.html`
- `reconstructive-singularity.html`
- the existing GCAT/BCAT paper lineage exposed by `Papers.html`, including adversarial robustness, boundary coherence, consequence horizon, and admissible existence.

The existing draft `From AI Safety to Transition Admissibility` already states that evaluation, execution, reconstructability, and commit-time admissibility are distinct. The new paper therefore narrows the research contribution to the systemic-failure argument: containment is retrospective, discovery is not authority, and novel reachable paths must remain non-executable until governed as admissible transitions.

## Pre-work claim

```text
claim_id: SITE-CONTAINMENT-TRANSITION-GOVERNANCE-1045-20260905
fragment: data/session-work-claims.d/site-containment-transition-governance-1045-20260905.json
state: CLAIMED_FOR_IMPLEMENTATION
dependency_surfaces:
  - site:papers-publication
  - site:public-research-positioning
authority_effect: false
activation_effect: false
```

The organization-level `control/claims-active.json` currently contains no active global claims, and the current default-branch Site corpus contains no existing claim using either dependency surface above. No competing machine-owned Publisher, Master Records, runtime, heartbeat, custody, or wiki execution scope is entered.

## README impact completeness predicate

**Determination: no README change is required for this change set.**

Evidence-supported rationale:

1. `README.md` already exposes `Papers.html` as the Site papers/research route.
2. This task does not change repository behavior, runtime semantics, interfaces, governance or authority boundaries, prerequisites, dependencies, failure behavior, or capability meaning.
3. It adds one bounded `RESEARCH_NOTE` inside the already documented Papers/publication mechanism and records the posture in `public-registry.json`.
4. The paper explicitly preserves the existing Site boundary: publication is not proof, authority, execution, custody, activation, or admissibility.

A future change that alters any of those semantics must update `README.md` in the same change set or carry a new evidence-supported no-change determination.

## Machine preflight result

```text
canonical_handoff_resolved: PASS
local_task_registry_resolved: PASS
master_records_boundary_resolved: PASS
cross_repo_coordination_resolved: PASS
existing_predicates_and_papers_reused: PASS
local_claim_acquired: PASS
cross_repo_dependency_collision_observed: NONE
readme_impact_predicate: PASS_NO_CHANGE_REQUIRED
functional_mutation_admissible: YES
```

Hosted/branch validation remains required before merge; source/preflight completion does not establish merge, publication, release, deployment, or runtime evidence.

## Evidence boundary

Publication, source presence, merge, CI, release, deployment, observation, and runtime evidence are distinct. This research lane must not infer execution authority, runtime activation, or admissibility from publication.

## Remaining implementation

1. Add `papers/containment-is-not-governance.html` as a bounded research note.
2. Link the paper from `Papers.html`.
3. Add a `RESEARCH_NOTE` posture entry to `public-registry.json`.
4. Validate the Site claim/handoff/publication gates.
5. After merge/validation, assess whether bounded awareness should be propagated to `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/admissibility-wiki`, and `StegVerse-002/stegguardian-wiki`; do not claim propagation until each target accepts it.

## Current state

`PREFLIGHT_PASSED_IMPLEMENTATION_ADMISSIBLE`
