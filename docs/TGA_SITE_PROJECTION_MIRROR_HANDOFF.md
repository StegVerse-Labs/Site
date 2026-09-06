# TGA Site Projection Mirror Handoff

Status: CANDIDATE_REGISTERED_FOR_REPOSITORY_ADMISSION
Updated: 2026-09-05
Repository: StegVerse-Labs/Site
Goal ID: SITE-1028-TGA-PROJECTION
Issue: #1028
Parent capability: `stegverse:capability:temporal-governed-analysis:v1`

## Mission

Provide the first governed Site projection for Temporal Governed Analysis (TGA): a browser surface that can project canonical TGA records, preserve exact source/time/rule-context/provenance/variance semantics, and optionally bind a user-local video file for bounded temporal playback without acquiring, redistributing, or asserting custody of media.

## Canonical upstream evidence

- `StegVerse-Labs/StegCore#184` — TGA core, merged/validated.
- `StegVerse-Labs/StegCore#186` — temporal media/event ingestion, merged/validated.
- `StegVerse-Labs/StegIndex#29` — core capability registration, merged/validated.
- `StegVerse-Labs/StegIndex#30` — media-ingestion predicate reconciliation, merged/validated.
- StegIndex first remaining predicate: `tga_site_projection_available`.

## Repository admission boundary

This goal is not owned by the initiating session. It is a repository-local candidate task and may be admitted only by `scripts/admit_repository_tasks.py` under the existing Site task-controller workflow.

```text
external_session_ownership = false
repository_native_owner = scripts/admit_repository_tasks.py
completion_observer = scripts/observe_and_complete_repository_tasks.py
auto_admit = true
execution_class = PARALLEL_SAFE
```

## Required projection semantics

The Site projection must preserve the distinction between:

1. source/media reference and custody posture;
2. exact temporal window;
3. observations / encoded representation;
4. governing rule/law/context version;
5. contemporaneous versus counterfactual applicability;
6. evaluation result;
7. uncertainty / unresolved / contradictory states;
8. provenance and reconstruction references.

Hard invariants:

- canonical representation != canonical reality;
- encoding precision does not imply correctness;
- media availability does not imply custody;
- counterfactual projection does not rewrite historical applicability;
- unresolved evidence stays unresolved;
- Site projection grants no legal, officiating, enforcement, publication, custody, or adjudicative authority;
- narration/presentation is projection only, never canonical evidence.

## Planned implementation locations

- `tga-reexamine.html`
- `assets/tga-reexamine.js`
- `data/tga/tga-site-sample.json`

## Planned verification locations

- `scripts/check_tga_site_projection.py`
- `.github/workflows/verify-tga-site-projection.yml`
- this handoff

## Completion boundary

The goal is source-complete when the repository-local task is admitted, all implementation and verification locations exist, the dedicated validator emits `TGA_SITE_PROJECTION=PASS`, the relevant PR merges, and the Site task controller observes the committed task as COMPLETE.

Public deployment/reachability is a separate evidence layer and must not be inferred from source merge.

## Downstream

After validated canonical Site evidence exists:

- reconcile `tga_site_projection_available` in StegIndex;
- release Publisher candidate `GCAT-BCAT-Engine/Publisher#54` for owner-side evaluation;
- keep wiki candidates blocked until Publisher produces validated evidence.

```yaml
source_state: NOT_YET_IMPLEMENTED
admission_state: CANDIDATE_PENDING_REPOSITORY_CONTROLLER
site_predicate_state: UNSATISFIED
user_action_required: false
authority_effect: NONE_PROJECTION_ONLY
thread_archive_ready: false
```
