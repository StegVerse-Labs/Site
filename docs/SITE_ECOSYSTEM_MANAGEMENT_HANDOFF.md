# Site Ecosystem Management Handoff

## Purpose

This handoff defines how future build sessions should continue Site work without manual chat recovery, prior-thread dependency, or silent guesses about the next action.

The goal is ecosystem-managed continuation: the repository should state its current boundary, identify the next safe build candidate, and distinguish pending evidence from completed readiness.

## Current Goal

```text
Goal: Continue building without manual actions needed through completion OR until task handoff and task completion is capable of being handled by the ecosystem's own management.
Repository: StegVerse-Labs/Site
Primary handoff: docs/SITE_MIRROR_HANDOFF.md
Companion handoff: docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md
Source repositories: GCAT-BCAT-Engine/Publisher, Admissible-Existence/TT, StegVerse-Labs/governance-observatory
Source paths: papers, TT propagation artifacts, Governance Observatory source-intake status
Target paths: papers, docs, public HTML surfaces
Activation state: pending_external_evidence
Management state: ecosystem-managed continuation ready after this packet and checker pass
```

## Done Definition

The Site repository can be treated as ecosystem-managed for this goal when:

```text
1. docs/SITE_MIRROR_HANDOFF.md remains the mirror activation source of truth.
2. docs/SITE_ECOSYSTEM_MANAGEMENT_HANDOFF.md records the continuation goal and next-action rules.
3. docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md records the autonomous continuation handoff.
4. scripts/check_site_ecosystem_management_handoff.py verifies this packet, the mirror handoff, and the computed status artifacts.
5. docs/SITE_EXTERNAL_EVIDENCE_STATE.json remains pending until computed evidence exists.
6. docs/SITE_FINAL_GOAL_STATUS.json remains pending until TT bundle-fed status is PASS and Governance Observatory status is valid.
7. The next build candidate can be selected from repository evidence without prior chat context.
8. Archive-readiness text states that the prior chat thread is no longer required for forward progress.
```

## Source Documents

```text
docs/SITE_MIRROR_HANDOFF.md
docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md
docs/SITE_EXTERNAL_EVIDENCE_STATE.json
docs/SITE_FINAL_GOAL_STATUS.json
docs/SITE_FINAL_ACTIVATION_PENDING.md
docs/SITE_SELF_MANAGED_COMPLETION.md
docs/SITE_TT_CODE_REPRESENTATION_STATUS.json
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.json
```

## Required Checks

```text
python scripts/check_site_mirror_handoff.py
python scripts/check_site_self_managed_completion.py
python scripts/check_site_ecosystem_management_handoff.py
python scripts/check_site_final_goal_status.py
python scripts/check_site_final_activation_pending.py
python scripts/check_site_governance_observatory_status.py
```

## Next-Action Selection Rules

Future sessions should choose the next action in this order:

```text
1. If docs/SITE_FINAL_GOAL_STATUS.json reports ready, verify the source-boundary non-claims before accepting it.
2. If TT bundle-fed status is not PASS, let site-autonomous-continuation or sync-tt-code-representation compute it.
3. If Governance Observatory status is not valid, repair only the failing Site status/checker path.
4. If external evidence state remains pending, do not claim readiness.
5. If all computed gates pass, update the handoff and choose the next integration target from the target handoff.
6. If gates do not pass, keep building repository-local management, validation, and handoff surfaces only.
```

## Current Next Build Candidate

```text
Candidate: wait for autonomous continuation to compute TT bundle-fed status, external evidence state, and final goal status
Reason: local continuation and validation paths are installed; remaining state is computed evidence
Boundary: Site display pages alone cannot move final goal status to ready
Activation impact: no readiness claim until computed gates pass
```

Note: `github/workflows/site-autonomous-continuation.yml` is displayed without the leading dot. The actual repository path is `.github/workflows/site-autonomous-continuation.yml`.

## Pending Evidence Gates

Readiness remains blocked until these computed gates are true:

```text
tt_bundle_fed_status_ready
governance_observatory_status_ready
external evidence state computed from checked-in artifacts
final goal status reports ready
```

## Non-Readiness Rule

Site-local display pages alone do not make the final goal ready. The final goal status must be computed from checked-in artifacts and validated by automation.

## Completion Boundary

This packet does not complete final goal readiness. It completes the repository-local management handoff layer for continuing the build without prior chat context.

## Archive Readiness

This file, together with docs/SITE_MIRROR_HANDOFF.md, docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md, and scripts/check_site_ecosystem_management_handoff.py, is sufficient for a future build session to determine the current goal, verify the pending evidence boundary, select the next safe build candidate, and continue without requiring the prior chat thread.
