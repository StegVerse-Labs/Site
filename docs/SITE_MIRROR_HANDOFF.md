# Site Mirror Handoff

## Purpose

This handoff lets the next build session continue Site mirror activation without needing prior chat context.

## Current Goal

```text
Goal: Continue building without manual actions needed through completion, or until task handoff and task completion are capable of being handled by the ecosystem's own management.
Repository: StegVerse-Labs/Site
Source repository: GCAT-BCAT-Engine/Publisher
Source path: papers
Target path: papers
Activation state: pending_publisher_closure_evidence
Self-management state: repository_managed_continuation_ready
```

## Built Files

```text
github/workflows/mirror-papers.yml
github/workflows/site-mirror-closure-guard.yml
github/workflows/site-self-managed-completion.yml
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
scripts/write_site_mirror_evidence.py
scripts/check_transition_table_public_copy.py
scripts/check_site_public_ingestion_contract.py
papers/papers_manifest.json
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
docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md
docs/SITE_TRAFFIC_AND_INGESTION_SIGNAL.md
docs/SITE_PUBLIC_PATHS.md
docs/SITE_INGESTION_SURFACES.md
docs/SITE_PUBLIC_PATH_AND_INGESTION_SURFACE_HARDENING.md
docs/SITE_MIRROR_HANDOFF.md
```

Note: `github/workflows/...` paths are displayed without the leading dot. The actual repository paths include the leading dot.

## Site Mirror Contract

The Site mirror must not become a separate editorial source of truth. Publisher remains authoritative.

The generated manifest must preserve:

```text
source_repository
source_ref
source_path
source_of_truth
target_repository
target_path
display_policy
mirror_protocol
workflow
generated_utc
count
aliases
entries
```

The checked-in `papers/papers_manifest.json` includes the required source-preserving metadata fields. Live activation still requires real Publisher and Site workflow evidence, but Site workflow-local evidence is generated automatically by `scripts/write_site_mirror_evidence.py`.

## Automated Site Evidence Path

The Site mirror workflow performs the Site-side evidence path automatically:

```text
1. Resolve Publisher source repository/ref/path.
2. Check Site paper display policy.
3. Check transition-table public copy.
4. Check public ingestion contract.
5. Validate pending evidence packet and live evidence state before mirror.
6. Validate that this handoff's Built Files list matches the repository structure.
7. Check out Publisher papers source.
8. Verify source papers path.
9. Mirror papers and generate public indexes.
10. Validate mirrored manifest metadata.
11. Validate paper aliases.
12. Run scripts/write_site_mirror_evidence.py.
13. Validate docs/SITE_MIRROR_EVIDENCE_PACKET.md after evidence writing.
14. Validate docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json after evidence writing.
15. Upload site-mirror-evidence-<run>-<attempt> artifact.
16. Nudge GCAT-BCAT-Engine/Publisher close-site-mirror-activation.yml when cross-repo credentials are available.
17. Commit mirrored papers and evidence updates when changed.
```

If cross-repo credentials are unavailable, the Site workflow exits that nudge step successfully and the scheduled Publisher closure workflow remains the fallback.

## Closure Guard Workflow

The no-secret closure guard workflow verifies closure-boundary documentation and checkers independently of the mirror workflow:

```text
github/workflows/site-mirror-closure-guard.yml
python scripts/check_site_mirror_handoff.py
python scripts/check_site_mirror_closure_next_build.py
python scripts/check_site_mirror_closure_guard.py
python scripts/check_site_mirror_activation_ledger.py
python scripts/check_site_mirror_activation_status.py
python scripts/check_site_mirror_evidence_requirements.py
```

This workflow does not dispatch Publisher, does not consume cross-repo credentials, and does not claim activation. It only confirms that Site closure-readiness documentation continues to preserve the Publisher activation boundary.

Note: `scripts/check_site_mirror_evidence_transition_rules.py` and `scripts/check_site_self_managed_completion.py` are enforced by repository-local validators and should be added to the closure guard workflow when workflow replacement is accepted by the connector.

## Validators

The manifest checker is:

```text
python scripts/check_papers_manifest_metadata.py
```

The alias checker is:

```text
python scripts/check_paper_aliases.py
```

The policy/config checker is:

```text
python scripts/check_paper_display_policy.py
```

The policy/config checker requires the automated evidence writer, evidence artifact upload path, and Publisher closure nudge/fallback path.

The evidence packet checker is:

```text
python scripts/check_site_mirror_evidence_packet.py
```

The live evidence state checker is:

```text
python scripts/check_site_mirror_live_evidence_state.py
```

The live evidence state checker verifies that non-pending values in `docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json` match the companion Markdown evidence fields in `docs/SITE_MIRROR_EVIDENCE_PACKET.md`.

The handoff checker is:

```text
python scripts/check_site_mirror_handoff.py
```

The handoff checker verifies that `docs/SITE_MIRROR_HANDOFF.md` keeps its Built Files list aligned with repository structure, retains required current-goal fields, records required validator commands, preserves required evidence terms, keeps closure terms present, records activation-ledger terms, records activation-status terms, records evidence-requirements terms, records evidence-transition terms, records self-managed completion terms, and keeps the pending activation boundary explicit.

The closure next-build checker is:

```text
python scripts/check_site_mirror_closure_next_build.py
```

The closure next-build checker verifies that `docs/SITE_MIRROR_CLOSURE_NEXT_BUILD.md` preserves the Publisher closure boundary and does not mark activation complete from Site-side evidence alone.

The closure guard checker is:

```text
python scripts/check_site_mirror_closure_guard.py
```

The closure guard checker verifies that `docs/SITE_MIRROR_CLOSURE_GUARD.md`, `github/workflows/site-mirror-closure-guard.yml`, and this handoff preserve the no-secret closure guard boundary.

The activation ledger checker is:

```text
python scripts/check_site_mirror_activation_ledger.py
```

The activation ledger checker verifies that `docs/SITE_MIRROR_ACTIVATION_LEDGER.json`, `docs/SITE_MIRROR_ACTIVATION_LEDGER.md`, and this handoff preserve a pending Site-side activation state until Publisher closure evidence exists.

The activation status checker is:

```text
python scripts/check_site_mirror_activation_status.py
```

The activation status checker verifies that `docs/SITE_MIRROR_ACTIVATION_STATUS.md` remains aligned with the activation ledger and does not advance beyond pending while required Publisher closure evidence remains pending.

The evidence requirements checker is:

```text
python scripts/check_site_mirror_evidence_requirements.py
```

The evidence requirements checker verifies that `docs/SITE_MIRROR_EVIDENCE_REQUIREMENTS.md`, `docs/SITE_MIRROR_ACTIVATION_LEDGER.json`, and this handoff preserve the exact evidence keys required before activation may advance.

The evidence transition rules checker is:

```text
python scripts/check_site_mirror_evidence_transition_rules.py
```

The evidence transition rules checker verifies that `docs/SITE_MIRROR_EVIDENCE_TRANSITION_RULES.md`, `docs/SITE_MIRROR_ACTIVATION_LEDGER.json`, and this handoff preserve the rule that evidence values may advance from pending only through governed Publisher/Site closure evidence.

The self-managed completion checker is:

```text
python scripts/check_site_self_managed_completion.py
```

The self-managed completion checker verifies that `docs/SITE_SELF_MANAGED_COMPLETION.md`, this handoff, the activation ledger, and activation status preserve repository-managed continuation readiness without claiming activation.

## Public Path and Ingestion Surface Contract

The Site repository is also documented as a public artifact endpoint and ingestion-facing repository.

```text
docs/SITE_PUBLIC_PATHS.md
docs/SITE_INGESTION_SURFACES.md
docs/SITE_PUBLIC_PATH_AND_INGESTION_SURFACE_HARDENING.md
python scripts/check_site_public_ingestion_contract.py
```

These documents do not activate the mirror. They prevent overclaiming by separating:

```text
ingestion from authority
upload from validation
display from source of truth
workflow visibility from activation evidence
traffic from adoption
```

## Evidence To Capture Automatically Or By Governed Follow-Up

```text
Publisher workflow run URL
Publisher verification receipt artifact
Publisher live dispatch workflow URL
Site mirror workflow URL
Site mirror commit SHA generated by workflow
papers/papers_manifest.json source_repository
papers/papers_manifest.json source_ref
papers/papers_manifest.json source_of_truth
public alias verification results
Site evidence artifact
Publisher closure nudge result
Site evidence packet completion commit
Site live evidence state completion commit
Publisher verification tracker activation commit
Publisher activation-status update commit
Publisher closure receipt
```

## Live Verification Packet

```text
docs/SITE_MIRROR_LIVE_VERIFICATION.md
docs/SITE_MIRROR_EVIDENCE_PACKET.md
docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json
```

## Closure Next-Build Packet

```text
docs/SITE_MIRROR_CLOSURE_NEXT_BUILD.md
python scripts/check_site_mirror_closure_next_build.py
```

This packet makes the next build boundary explicit: Site may prepare and validate closure-readiness evidence, but Publisher closure remains required before activation can be claimed.

## Closure Guard Packet

```text
docs/SITE_MIRROR_CLOSURE_GUARD.md
python scripts/check_site_mirror_closure_guard.py
```

This packet makes the closure guard workflow independently auditable as a read-only Site-local boundary check.

## Activation Ledger Packet

```text
docs/SITE_MIRROR_ACTIVATION_LEDGER.md
docs/SITE_MIRROR_ACTIVATION_LEDGER.json
python scripts/check_site_mirror_activation_ledger.py
```

This packet makes Site mirror activation state machine-verifiable while preserving the rule that Site-side evidence alone does not activate the mirror.

## Activation Status Packet

```text
docs/SITE_MIRROR_ACTIVATION_STATUS.md
python scripts/check_site_mirror_activation_status.py
```

This packet keeps human-readable activation status aligned with the activation ledger and prevents the older status file from drifting beyond pending before Publisher closure evidence exists.

## Evidence Requirements Packet

```text
docs/SITE_MIRROR_EVIDENCE_REQUIREMENTS.md
python scripts/check_site_mirror_evidence_requirements.py
```

This packet keeps the exact evidence keys required before activation may advance aligned with the activation ledger, status, and handoff.

## Evidence Transition Rules Packet

```text
docs/SITE_MIRROR_EVIDENCE_TRANSITION_RULES.md
python scripts/check_site_mirror_evidence_transition_rules.py
```

This packet defines how evidence values may advance from pending without allowing Site-local evidence alone to claim activation.

## Self-Managed Completion Packet

```text
docs/SITE_SELF_MANAGED_COMPLETION.md
python scripts/check_site_self_managed_completion.py
github/workflows/site-self-managed-completion.yml
```

This packet defines the new assessment goal: continue building without manual actions needed through completion, or until task handoff and task completion are capable of being handled by ecosystem management. It marks repository-managed continuation ready while keeping activation pending until governed Publisher closure evidence exists.

The self-managed completion workflow runs the primary handoff checker and self-managed completion checker whenever the handoff, assessment, activation ledger, activation status, or their checkers change.

## Traffic And Ingestion Signal Packet

```text
docs/SITE_TRAFFIC_AND_INGESTION_SIGNAL.md
docs/SITE_PUBLIC_PATHS.md
docs/SITE_INGESTION_SURFACES.md
docs/SITE_PUBLIC_PATH_AND_INGESTION_SURFACE_HARDENING.md
```

The traffic packet records the current GitHub traffic snapshot and prevents overclaiming. It treats clone/view activity as repository-behavior evidence only, not adoption, activation, endorsement, or live mirror proof.

The public path and ingestion-surface documents make observed high-interest routes legible without granting authority to uploaded, candidate, mirrored, generated, or workflow-visible artifacts by placement alone.

## Companion Publisher Handoff

```text
GCAT-BCAT-Engine/Publisher/docs/PUBLISHER_MIRROR_HANDOFF.md
```

Use the Publisher handoff for Publisher-side automated dispatch, Publisher receipt artifacts, closure workflow, and verification-tracker continuation.

## Cross-Repo Activation Boundary

The mirror may only be marked activated after:

```text
1. Publisher automated dispatch workflow produces a verification receipt artifact.
2. Publisher workflow dispatches Site mirror workflow successfully.
3. Site mirror workflow completes.
4. Site mirror workflow writes and uploads Site evidence artifact.
5. Site manifest metadata is verified.
6. Site paper aliases are verified.
7. Publisher closure workflow consumes Publisher and Site evidence artifacts.
8. Publisher closure workflow writes docs/mirror-activation-closures/<closure>.json.
9. Publisher verification tracker is updated to activated.
10. Publisher activation status is updated to activated.
```

## Current Delta

```text
Resolved: checked-in papers/papers_manifest.json includes required source metadata.
Resolved: Publisher has a companion mirror handoff for non-Site sessions.
Resolved: Site mirror workflow runs scripts/check_paper_aliases.py after manifest metadata verification.
Resolved: Site evidence packet checker requires the alias verification command and expected alias success output.
Resolved: Site evidence packet and checker require Publisher dry-run receipt and activation-status update evidence fields.
Resolved: Site has docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json as the machine-readable live activation state companion.
Resolved: Site has scripts/check_site_mirror_live_evidence_state.py to prevent activation claims while required evidence remains pending.
Resolved: Site live evidence state checker prevents drift between non-pending JSON evidence values and Markdown packet evidence values.
Resolved: Site public path and ingestion-surface documentation is enforced by scripts/check_site_public_ingestion_contract.py.
Resolved: Site mirror workflow writes Site evidence automatically using scripts/write_site_mirror_evidence.py.
Resolved: Site mirror workflow uploads site-mirror-evidence-<run>-<attempt> artifacts.
Resolved: Site mirror workflow nudges Publisher close-site-mirror-activation.yml when cross-repo credentials are available.
Resolved: Site paper display policy checker requires the automated evidence writer, artifact upload path, and Publisher closure nudge/fallback path.
Resolved: Site has scripts/check_site_mirror_handoff.py to verify handoff-to-repository structure alignment before mirror execution proceeds.
Resolved: Site mirror workflow runs the handoff verifier and records it in the workflow summary.
Resolved: Site has docs/SITE_MIRROR_CLOSURE_NEXT_BUILD.md to define the closure-readiness build boundary.
Resolved: Site has scripts/check_site_mirror_closure_next_build.py to prevent closure-readiness work from overclaiming activation.
Resolved: Site has github/workflows/site-mirror-closure-guard.yml to enforce closure-readiness docs and checkers without cross-repo credentials.
Resolved: Site has docs/SITE_MIRROR_CLOSURE_GUARD.md to make the closure guard workflow independently auditable.
Resolved: Site has scripts/check_site_mirror_closure_guard.py to verify the closure guard packet, workflow, and handoff alignment.
Resolved: Site has docs/SITE_MIRROR_ACTIVATION_LEDGER.json as the machine-readable pending activation ledger.
Resolved: Site has docs/SITE_MIRROR_ACTIVATION_LEDGER.md to document the activation ledger contract.
Resolved: Site has scripts/check_site_mirror_activation_ledger.py to verify the activation ledger remains pending until Publisher closure evidence exists.
Resolved: Site closure guard workflow runs scripts/check_site_mirror_activation_ledger.py.
Resolved: Site has docs/SITE_MIRROR_ACTIVATION_STATUS.md aligned to the activation ledger pending state.
Resolved: Site has scripts/check_site_mirror_activation_status.py to verify activation status remains aligned with the activation ledger.
Resolved: Site closure guard workflow runs scripts/check_site_mirror_activation_status.py.
Resolved: Site has docs/SITE_MIRROR_EVIDENCE_REQUIREMENTS.md to enumerate exact activation-blocking evidence keys.
Resolved: Site has scripts/check_site_mirror_evidence_requirements.py to verify the evidence requirements remain aligned with the ledger and handoff.
Resolved: Site closure guard workflow runs scripts/check_site_mirror_evidence_requirements.py.
Resolved: Site has docs/SITE_MIRROR_EVIDENCE_TRANSITION_RULES.md to define governed evidence transitions.
Resolved: Site has scripts/check_site_mirror_evidence_transition_rules.py to verify evidence transition rules remain aligned with the ledger and handoff.
Resolved: Site has docs/SITE_SELF_MANAGED_COMPLETION.md to define repository-managed continuation readiness under the new goal.
Resolved: Site has scripts/check_site_self_managed_completion.py to verify the self-managed completion assessment while preserving pending activation.
Resolved: Site has github/workflows/site-self-managed-completion.yml to run self-managed completion and handoff checks automatically on relevant changes.
Resolved: Site built-files ledger now records docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md as part of the repo-resident management handoff surface.
Pending: actual Publisher receipt artifact, actual Site evidence artifact, Publisher closure receipt, Publisher verification tracker activation, and Publisher activation-status update.
```

## Archive Readiness

This handoff contains the repo state, automated Site evidence path, Publisher closure nudge, validators, evidence requirements, evidence transition rules, self-managed completion assessment, self-managed completion workflow, Site mirror ecosystem management handoff, traffic-signal documentation, public path semantics, ingestion-surface semantics, enforced public ingestion contract, handoff-to-repository structure verification, closure next-build guard, no-secret closure guard workflow, independently auditable closure guard packet, machine-verifiable activation ledger, activation-status reconciliation, evidence-requirements reconciliation, and combined hardening packet needed to continue. The prior chat thread is no longer required for forward progress once this file is present in the repository.
