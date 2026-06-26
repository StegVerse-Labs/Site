# Site Mirror Handoff

## Purpose

This handoff lets the next build session continue Site mirror activation without needing prior chat context.

## Current Goal

```text
Goal: Continue building without manual actions needed through completion, or until task handoff and task completion are capable of being handled by the ecosystem's own management.
Repository: StegVerse-Labs/Site
Source repository: GCAT-BCAT-Engine/Publisher and Admissible-Existence/TT
Source path: papers and TT propagation artifacts
Target path: papers and docs
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
scripts/check_site_tt_code_representation_mirror.py
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
docs/SITE_TT_CODE_REPRESENTATION_MIRROR.md
docs/SITE_MIRROR_HANDOFF.md
```

Note: `github/workflows/...` paths are displayed without the leading dot. The actual repository paths include the leading dot.

## Site Mirror Contract

The Site mirror must not become a separate editorial source of truth. Publisher remains authoritative for papers. `Admissible-Existence/TT` remains authoritative for Transition Table code-representation semantics.

The generated papers manifest must preserve:

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

## TT Code Representation Mirror

The TT code-representation mirror page is:

```text
docs/SITE_TT_CODE_REPRESENTATION_MIRROR.md
```

Its checker is:

```text
python scripts/check_site_tt_code_representation_mirror.py
```

This mirror preserves the boundary that Site may display and route canonical TT records, but must not redefine transition-element semantics or treat a rendered element as execution authority.

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
docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md
python scripts/check_site_mirror_handoff.py
python scripts/check_site_mirror_closure_next_build.py
python scripts/check_site_mirror_closure_guard.py
python scripts/check_site_mirror_activation_ledger.py
python scripts/check_site_mirror_activation_status.py
python scripts/check_site_mirror_evidence_requirements.py
python scripts/check_site_mirror_evidence_transition_rules.py
python scripts/check_site_self_managed_completion.py
python scripts/check_site_tt_code_representation_mirror.py
```

This workflow does not dispatch Publisher, does not consume cross-repo credentials, and does not claim activation. It only confirms that Site closure-readiness documentation, evidence transition rules, self-managed completion documentation, TT code-representation mirror documentation, and the ecosystem management handoff surface continue to preserve the relevant canonical-source boundaries.

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

The handoff checker verifies that `docs/SITE_MIRROR_HANDOFF.md` keeps its Built Files list aligned with repository structure, retains required current-goal fields, records required validator commands, preserves required evidence terms, keeps closure terms present, records activation-ledger terms, records activation-status terms, records evidence-requirements terms, records evidence-transition terms, records self-managed completion terms, records TT code-representation terms, and keeps the pending activation boundary explicit.

The TT code-representation mirror checker is:

```text
python scripts/check_site_tt_code_representation_mirror.py
```

The closure next-build checker is:

```text
python scripts/check_site_mirror_closure_next_build.py
```

The closure next-build checker verifies that `docs/SITE_MIRROR_CLOSURE_NEXT_BUILD.md` preserves the Publisher closure boundary and does not mark activation complete from Site-side evidence alone.

The closure guard checker is:

```text
python scripts/check_site_mirror_closure_guard.py
```

The closure guard checker verifies that `docs/SITE_MIRROR_CLOSURE_GUARD.md`, `github/workflows/site-mirror-closure-guard.yml`, and this handoff preserve the no-secret closure guard boundary and ecosystem-management handoff surface.

The activation ledger checker is:

```text
python scripts/check_site_mirror_activation_ledger.py
```

## Current Completion Estimate

```text
StegVerse-Labs - 92%complete
Site - 88%complete
Site - 88%complete TO GOAL ACTIVATION
```

The complete thread is ready for archiving after Site TT code-representation propagation is consumed by public rendering or downstream ingestion.
