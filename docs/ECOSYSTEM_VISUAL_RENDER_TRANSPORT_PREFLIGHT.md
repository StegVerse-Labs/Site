# Ecosystem Visual Render Transport Machine Preflight

Repository: `StegVerse-Labs/Site`
Task: `SITE-ECOSYSTEM-VISUAL-RENDER-TRANSPORT-1015`
Issue: `#1015`
Evaluated: 2026-09-05
Decision: `ADMIT_ON_CURRENT_MAIN_SUCCESSOR_BRANCH_ONLY`

## Canonical inputs resolved

- repository handoff: `docs/SITE_MIRROR_HANDOFF.md`
- focused handoff: `docs/ECOSYSTEM_VISUAL_RENDER_TRANSPORT_MIRROR_HANDOFF.md`
- task/claim: `data/session-work-claims.d/site-ecosystem-visual-render-transport-1015.json`
- repository orchestration state: `data/site-orchestration-state.json`
- repository heartbeat/work-health state: `data/ecosystem-heartbeat-state.json`
- predecessor implementation: `docs/ECOSYSTEM_VISUAL_PROJECTION_MIRROR_HANDOFF.md` / Site #1007
- Master Records authority: `master-records/orchestration/docs/ECOSYSTEM_CHAT_CUSTODY_MIRROR_HANDOFF.md`

## Ownership / collision result

The #1015 dependency surface is `site:ecosystem-visual-render-transport`. No current-main claim was found owning that surface. The active HIL upload task owns `humans-as-interoperability-layer.html`, `assets/hil-*`, and `scripts/check_hil_*upload*`; those paths do not overlap #1015. Master Records owns custody/reconstruction only and must not be duplicated by this Site transport source task.

## Stale branch result

The original `feat/ecosystem-visual-render-transport-1015` branch is 167 commits behind current `main` and has two task-only commits. Functional implementation MUST NOT continue on that stale base. Existing handoff/claim content must be carried forward to one current-main successor branch for the same task; this is continuation, not a second workload.

## README completeness predicate

Decision: `README_UPDATE_REQUIRED`.

Reason: #1015 introduces a new repository-level provider-neutral visual render request/receipt interface and defines failure/authority semantics for renderer transport. That materially changes documented interfaces and capability meaning even though it grants no new authority. Therefore `README.md` must be updated in the same change set. The active claim must include `README.md` in `claimed_paths` before functional source files are installed.

## Authority / dependency result

- renderer role remains `PROJECTION_ONLY`;
- no provider endpoint or credential is embedded in canonical fixtures;
- Site#242 remains authentic Ecosystem Chat runtime activation owner;
- `master-records/orchestration` remains custody/reconstruction owner;
- no live renderer handshake, runtime execution, custody, publication, or activation may be inferred from source/CI.

## Machine admission

`PASS`, conditional on continuation from current `main`, preservation of the existing #1015 claim identity, inclusion of `README.md` in the same bounded change set, and repository orchestration/claim/heartbeat/application validation before merge.
