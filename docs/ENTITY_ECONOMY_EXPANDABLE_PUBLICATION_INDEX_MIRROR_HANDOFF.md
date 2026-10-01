# Entity Economy Expandable Publication Index — Site Handoff

Updated: 2026-09-30

## Task
- Task ID: `SITE-ENTITY-ECONOMY-EXPANDABLE-INDEX-1477`
- Parent Goal: `ENTITY-ECONOMY-VOLUME-I-II-SUCCESSOR-PUBLICATION-001`
- Branch: `task/entity-economy-expandable-publication-index`
- PR: #1477
- Status: ACTIVE / SOURCE_VALIDATION_PENDING
- Authority effect: NONE

## Bounded workload
Update only the Entity Economy public series introduction/navigation so the top of the page presents a mobile-friendly expandable publication index. Numbered Volumes I–III remain distinct from non-numbered Companion Research. Each entry provides a concise description and direct existing publication link.

The five indexed works are Volume I, Volume II, Volume III, Convergence / Comparative Signal Treatment, and Entity Economy Empirical Research Proposal.

## Identity boundary
No paper artifact is mutated, merged, renumbered, replaced, or re-identified. Historical Volume I/II bytes and identities remain unchanged. Volume III remains the third numbered paper. The Treatment and Empirical Research Proposal remain companion research and are not Volume IV.

## Evidence boundary
Repository source validation, merge, Pages deployment, and credential-free served-body observation are separate predicates. No deployment or public readback is inferred from source or merge.

## Current state
The initial exact-head validation at `040067505bc4a04d6a46256659b74d5946b297e8` demonstrated one coordination failure only: the PR branch lacked an active pre-work claim mapped to an unfinished handoff workload. Page-content failures were not demonstrated. This focused handoff and its exact-branch claim repair that predicate without changing the selected page content.

## Completion predicates
- exact branch resolves to exactly one active pre-work claim
- exact-head Site validation succeeds
- PR merges with expected-head protection
- deployed custom-domain served body independently shows Numbered series and Companion research expandable groups
- all five direct publication links are present in the served body

## Manual work
None.
