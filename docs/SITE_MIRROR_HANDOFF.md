# Site Mirror Handoff

## Purpose

This handoff lets the next build session continue Site mirror activation without needing prior chat context.

## Current Goal

```text
Goal: Continue building without manual actions needed through completion, or until task handoff and task completion are capable of being handled by the ecosystem's own management.
Repository: StegVerse-Labs/Site
Source repository: GCAT-BCAT-Engine/Publisher, Admissible-Existence/TT, StegVerse-Labs/governance-observatory, and StegVerse-Labs/repo-standards
Source path: papers, TT propagation artifacts, Governance Observatory source-intake status, and repository standards release-candidate surface
Target path: papers, docs, and public HTML surfaces
Activation state: pending_external_evidence
Self-management state: repository_managed_continuation_ready
Repo standards mirror state: installed_display_only
```

## Built Files

```text
github/workflows/mirror-papers.yml
github/workflows/site-autonomous-continuation.yml
github/workflows/site-external-evidence-state.yml
github/workflows/site-local-completion-receipt.yml
github/workflows/site-mirror-closure-guard.yml
github/workflows/site-final-goal-status.yml
github/workflows/site-public-mirror-status-guard.yml
github/workflows/site-self-managed-completion.yml
github/workflows/site-task-elimination-guard.yml
github/workflows/sync-tt-code-representation.yml
github/workflows/validate-governance-observatory-status.yml
scripts/mirror_papers.py
scripts/check_paper_display_policy.py
scripts/check_papers_manifest_metadata.py
scripts/check_paper_aliases.py
scripts/check_site_mirror_evidence_packet.py
scripts/check_site_mirror_live_evidence_state.py
scripts/check_site_mirror_handoff.py
scripts/check_site_mirror_closure_next_build.py
scripts/check_site_mirror_closure_guard.py
scripts/check_site_mirror_activation_ledger.py
scripts/check_site_mirror_activation_status.py
scripts/check_site_mirror_evidence_requirements.py
scripts/check_site_mirror_evidence_transition_rules.py
scripts/check_site_self_managed_completion.py
scripts/check_site_ecosystem_management_handoff.py
scripts/check_site_tt_code_representation_mirror.py
scripts/check_site_tt_public_page.py
scripts/check_site_non_activation_mirror_status.py
scripts/check_site_final_activation_pending.py
scripts/check_site_final_goal_status.py
scripts/check_site_manual_task_elimination.py
scripts/write_site_local_completion_receipt.py
scripts/check_site_local_completion_receipt.py
scripts/update_site_final_goal_status.py
scripts/write_site_external_evidence_state.py
scripts/render_tt_code_representation_status.py
scripts/write_site_mirror_evidence.py
scripts/check_transition_table_public_copy.py
scripts/check_site_public_ingestion_contract.py
scripts/check_site_governance_observatory_status.py
scripts/check_site_repo_standards_mirror.py
papers/papers_manifest.json
tt-code-representation.html
governance-observatory.html
repo-standards.html
docs/SITE_PAPER_DISPLAY_POLICY.md
docs/README_SITE_PAPERS_MIRROR.md
docs/SITE_MIRROR_ACTIVATION_STATUS.md
docs/SITE_MIRROR_LIVE_VERIFICATION.md
docs/SITE_MIRROR_ALIAS_VERIFICATION.md
docs/SITE_MIRROR_EVIDENCE_PACKET.md
docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json
docs/SITE_MIRROR_CLOSURE_NEXT_BUILD.md
docs/SITE_MIRROR_CLOSURE_GUARD.md
docs/SITE_MIRROR_ACTIVATION_LEDGER.md
docs/SITE_MIRROR_ACTIVATION_LEDGER.json
docs/SITE_MIRROR_EVIDENCE_REQUIREMENTS.md
docs/SITE_MIRROR_EVIDENCE_TRANSITION_RULES.md
docs/SITE_SELF_MANAGED_COMPLETION.md
docs/SITE_ECOSYSTEM_MANAGEMENT_HANDOFF.md
docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md
docs/SITE_TRAFFIC_AND_INGESTION_SIGNAL.md
docs/SITE_PUBLIC_PATHS.md
docs/SITE_INGESTION_SURFACES.md
docs/SITE_PUBLIC_PATH_AND_INGESTION_SURFACE_HARDENING.md
docs/SITE_TT_CODE_REPRESENTATION_MIRROR.md
docs/SITE_TT_CODE_REPRESENTATION_STATUS.md
docs/SITE_TT_CODE_REPRESENTATION_STATUS.json
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.md
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.json
docs/SITE_EXTERNAL_EVIDENCE_STATE.md
docs/SITE_EXTERNAL_EVIDENCE_STATE.json
docs/SITE_EXTERNAL_EVIDENCE_REQUIREMENTS.md
docs/SITE_FINAL_ACTIVATION_PENDING.md
docs/SITE_FINAL_GOAL_STATUS.md
docs/SITE_FINAL_GOAL_STATUS.json
docs/SITE_LOCAL_COMPLETION_RECEIPT.md
docs/SITE_LOCAL_COMPLETION_RECEIPT.json
docs/SITE_MANUAL_TASK_ELIMINATION.md
docs/SITE_TASK_ELIMINATION_GUARD.md
docs/SITE_REPO_STANDARDS_MIRROR.md
docs/SITE_REPO_STANDARDS_STATUS.md
docs/SITE_MIRROR_HANDOFF.md
```

Note: `github/workflows/...` paths are displayed without the leading dot. The actual repository paths include the leading dot.

## Site Mirror Contract

The Site mirror must not become a separate editorial source of truth. Publisher remains authoritative for papers. `Admissible-Existence/TT` remains authoritative for Transition Table code-representation semantics. `StegVerse-Labs/governance-observatory` remains authoritative for Governance Observatory source-intake records. `StegVerse-Labs/repo-standards` remains authoritative for repository standards, schemas, templates, validators, correction tooling, and release readiness.

## Public TT Code Representation Page

Site exposes a public HTML mirror surface:

```text
tt-code-representation.html
```

This page explains TT code representation, links to Site-rendered status artifacts, and preserves the boundary that rendered Site pages are display only.

The public page checker is:

```text
python scripts/check_site_tt_public_page.py
```

## Governance Observatory Status Page

Site exposes a public HTML status surface:

```text
governance-observatory.html
```

This page displays Governance Observatory source-intake status, links to Site status artifacts, and preserves the boundary that Site display does not certify external sources, prove SDK compatibility, or issue commit-time permission.

Validation path shown without leading period for iOS compatibility:

```text
github/workflows/validate-governance-observatory-status.yml
```

Canonical repository path begins with a leading period.

## Repo Standards Mirror Page

Site exposes a public HTML mirror surface:

```text
repo-standards.html
```

This page displays the `StegVerse-Labs/repo-standards` release-candidate surface and adoption path. It preserves the boundary that Site display does not certify release validation, grant correction authority, or replace source repository evidence.

The checker is:

```text
python scripts/check_site_repo_standards_mirror.py
```

The status document is:

```text
docs/SITE_REPO_STANDARDS_STATUS.md
```

## Autonomous Continuation

Site has one scheduled continuation workflow that performs the local continuation sequence without manual coordination:

```text
github/workflows/site-autonomous-continuation.yml
```

It runs on schedule, manual dispatch, relevant pushes, and completed upstream workflow runs from:

```text
Sync TT Code Representation
Validate Governance Observatory Status
```

It performs:

```text
checkout Site
checkout Admissible-Existence/TT
build TT propagation bundle
copy TT bundle into Site
render TT status
check Governance Observatory status
write external evidence state
update final goal status
validate final goal status
validate final activation boundary
commit computed state changes
```

This removes manual coordination between the TT sync workflow, external evidence state writer, and final goal status updater. The workflow writes `pending_external_evidence` until the required evidence is present and only lets the final goal status become `ready` when computed gates pass.

## Local Completion Receipt

Site has a repository-managed local completion receipt workflow:

```text
github/workflows/site-local-completion-receipt.yml
```

It runs:

```text
python scripts/write_site_local_completion_receipt.py
python scripts/check_site_local_completion_receipt.py
```

The workflow writes and validates:

```text
docs/SITE_LOCAL_COMPLETION_RECEIPT.md
docs/SITE_LOCAL_COMPLETION_RECEIPT.json
```

This receipt confirms repository-managed continuation surfaces exist. It does not activate the Site mirror, grant commit-time permission, or move source authority into Site.

## Manual Task Elimination

Site has a task-elimination guard workflow:

```text
github/workflows/site-task-elimination-guard.yml
```

It runs:

```text
python scripts/check_site_manual_task_elimination.py
```

The guard verifies local continuation work is workflow-managed and no local manual inspection is required to determine the state of TT status, Governance Observatory status, repo standards status, external evidence state, or final goal status.

## Ecosystem Management Handoffs

Site has ecosystem management handoffs:

```text
docs/SITE_ECOSYSTEM_MANAGEMENT_HANDOFF.md
docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md
```

They are checked by:

```text
python scripts/check_site_ecosystem_management_handoff.py
```

The checker verifies that future sessions can determine the current goal, pending evidence boundary, autonomous continuation path, and archive-readiness state from repository files rather than prior chat context.

## Automated External Evidence State

Site has a workflow-managed external evidence state:

```text
github/workflows/site-external-evidence-state.yml
```

It runs on schedule, manual dispatch, relevant pushes, and completed upstream workflow runs from:

```text
Sync TT Code Representation
Validate Governance Observatory Status
```

It runs:

```text
python scripts/write_site_external_evidence_state.py
```

The writer produces:

```text
docs/SITE_EXTERNAL_EVIDENCE_STATE.md
docs/SITE_EXTERNAL_EVIDENCE_STATE.json
```

## Current Repo Standards Mirror Completion

```text
Site repo-standards mirror: installed
Public page: installed
Checker: installed
Status artifact: installed
Source validation evidence: pending in source repo
Publisher mirror: pending
admissibility-wiki mirror: pending
stegguardian-wiki mirror: pending
```

## Next Integration Goal Candidate

Continue with `GCAT-BCAT-Engine/Publisher` standards-publication task after source validation evidence is available or after a governed decision accepts release-candidate display-only propagation.
