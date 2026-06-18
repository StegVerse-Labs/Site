# Site Ecosystem Management Handoff

## Purpose

This handoff defines how future build sessions should continue Site work without manual chat recovery, prior-thread dependency, or silent guesses about the next action.

The goal is ecosystem-managed continuation: the repository should be able to state its current boundary, identify the next safe build candidate, and distinguish pending evidence from completed activation.

## Current Goal

```text
Goal: Continue building without manual actions needed through completion OR until task handoff and task completion is capable of being handled by the ecosystem's own management.
Repository: StegVerse-Labs/Site
Primary handoff: docs/SITE_MIRROR_HANDOFF.md
Companion source handoff: GCAT-BCAT-Engine/Publisher/docs/PUBLISHER_MIRROR_HANDOFF.md
Source repository: GCAT-BCAT-Engine/Publisher
Source path: papers
Target path: papers
Activation state: pending Publisher/Site closure evidence
Management state: ecosystem-managed continuation ready after this packet and checker pass
```

## Done Definition

The Site repository can be treated as ecosystem-managed for this goal when:

```text
1. docs/SITE_MIRROR_HANDOFF.md remains the mirror activation source of truth.
2. docs/SITE_ECOSYSTEM_MANAGEMENT_HANDOFF.md records the continuation goal and next-action rules.
3. scripts/check_site_ecosystem_management_handoff.py verifies this packet, the mirror handoff, and the activation ledger.
4. The activation ledger remains pending until Publisher closure evidence exists.
5. The next build candidate can be selected from repository evidence without prior chat context.
6. The archive-readiness text states that the prior chat thread is no longer required for forward progress.
```

## Source Documents

```text
docs/SITE_MIRROR_HANDOFF.md
docs/SITE_MIRROR_CLOSURE_NEXT_BUILD.md
docs/SITE_MIRROR_CLOSURE_GUARD.md
docs/SITE_MIRROR_ACTIVATION_LEDGER.md
docs/SITE_MIRROR_ACTIVATION_LEDGER.json
docs/SITE_MIRROR_ACTIVATION_STATUS.md
docs/SITE_MIRROR_EVIDENCE_REQUIREMENTS.md
docs/SITE_MIRROR_EVIDENCE_TRANSITION_RULES.md
docs/SITE_PUBLIC_PATH_AND_INGESTION_SURFACE_HARDENING.md
```

## Required Checks

```text
python scripts/check_site_mirror_handoff.py
python scripts/check_site_mirror_closure_next_build.py
python scripts/check_site_mirror_closure_guard.py
python scripts/check_site_mirror_activation_ledger.py
python scripts/check_site_mirror_activation_status.py
python scripts/check_site_mirror_evidence_requirements.py
python scripts/check_site_mirror_evidence_transition_rules.py
python scripts/check_site_public_ingestion_contract.py
python scripts/check_site_ecosystem_management_handoff.py
```

## Next-Action Selection Rules

Future sessions should choose the next action in this order:

```text
1. If docs/SITE_MIRROR_ACTIVATION_LEDGER.json has activation_state other than pending, verify Publisher closure evidence before accepting it.
2. If any required evidence value is pending, do not claim activation.
3. If Site-local closure guard documentation or checkers are missing, build those before new public features.
4. If the no-secret closure guard workflow omits a required checker, add the checker to that workflow when workflow replacement is available.
5. If Publisher closure evidence exists, reconcile the ledger, evidence packet, live state, activation status, and handoff together.
6. If Publisher closure evidence does not exist, keep building repository-local management, verification, and handoff surfaces only.
```

## Current Next Build Candidate

```text
Candidate: promote scripts/check_site_mirror_evidence_transition_rules.py into github/workflows/site-mirror-closure-guard.yml
Reason: the handoff records the checker as enforced by the handoff verifier but not yet listed in the no-secret closure guard workflow.
Boundary: workflow replacement may be connector-blocked; if blocked, preserve the drop-in-ready workflow replacement and continue with repository-local handoff/checker hardening.
Activation impact: no activation claim
```

Note: `github/workflows/site-mirror-closure-guard.yml` is displayed without the leading dot. The actual repository path is `.github/workflows/site-mirror-closure-guard.yml`.

## Pending Activation Evidence

Activation remains blocked until these evidence values are real artifacts or commits, not placeholders:

```text
publisher_workflow_run_url
publisher_verification_receipt_artifact
publisher_live_dispatch_workflow_url
site_mirror_workflow_url
site_mirror_commit_sha
site_evidence_artifact
publisher_closure_nudge_result
publisher_closure_receipt
publisher_verification_tracker_activation_commit
publisher_activation_status_update_commit
```

## Non-Activation Rule

Site-side evidence alone does not activate the mirror. Publisher closure remains required before activation can be claimed.

## Completion Boundary

This packet does not complete live mirror activation. It completes the repository-local management handoff layer for continuing the build without prior chat context.

## Archive Readiness

This file, together with docs/SITE_MIRROR_HANDOFF.md and scripts/check_site_ecosystem_management_handoff.py, is sufficient for a future build session to determine the current goal, verify the pending activation boundary, select the next safe build candidate, and continue without requiring the prior chat thread.
