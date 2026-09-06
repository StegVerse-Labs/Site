# TGA Site Projection Mirror Handoff

Status: IMPLEMENTED_PENDING_VALIDATION
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

This goal is not owned by the initiating session. Its committed task object is `data/tasks/SITE-1028-TGA-PROJECTION.json`, with repository-native ownership and automatic discovery/admission through the existing Site task controller.

```text
external_session_ownership = false
repository_native_owner = scripts/admit_repository_tasks.py
completion_observer = scripts/observe_and_complete_repository_tasks.py
auto_admit = true
execution_class = PARALLEL_SAFE
```

## Implemented source slice

- `tga-reexamine.html` — governed Re-examine projection surface.
- `assets/tga-reexamine.js` — deterministic renderer, exact window controls, local-only video binding, JSON record loading.
- `data/tga/tga-site-sample.json` — explicitly synthetic counterfactual baseball fixture with unresolved evidence and no authority claim.
- `scripts/check_tga_site_projection.py` — fail-closed static contract validator.
- `.github/workflows/verify-tga-site-projection.yml` — dedicated pull-request/main validation workflow.

The renderer performs no external media acquisition. Local media uses browser `URL.createObjectURL`; source references and custody posture remain explicit and independent.

## Required projection semantics

The Site projection preserves the distinction between:

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

## Completion boundary

The goal is source-complete when the dedicated validator emits `TGA_SITE_PROJECTION=PASS`, the implementation PR merges, and the repository-native Site task controller observes the committed task as COMPLETE.

Public deployment/reachability is a separate evidence layer and must not be inferred from source merge.

## Downstream

After validated canonical Site evidence exists:

- reconcile `tga_site_projection_available` in StegIndex;
- release Publisher candidate `GCAT-BCAT-Engine/Publisher#54` for owner-side evaluation;
- keep wiki candidates blocked until Publisher produces validated evidence.

```yaml
source_state: IMPLEMENTED_ON_FEATURE_BRANCH
validation_state: PENDING
site_predicate_state: UNSATISFIED_PENDING_VALIDATION_AND_MERGE
user_action_required: false
authority_effect: NONE_PROJECTION_ONLY
thread_archive_ready: false
```
