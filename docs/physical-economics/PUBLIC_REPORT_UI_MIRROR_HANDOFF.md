# Physical Economics Public Report UI Mirror Handoff

## Authority
Bounded continuation record for the Site-side public UI integration of the ERL Physical Economics `GENERATE_REPORT` contract.

Parent repository authority: `SITE_MIRROR_HANDOFF.md`.
Upstream machine authority: `StegVerse-Labs/Executive_Rhetoric_Ledger/docs/physical-economics/reporting/PHYSICAL_ECONOMICS_REPORTING_MIRROR_HANDOFF.md`.
Canonical Site issue: `StegVerse-Labs/Site#496`.
Implementation branch: `feature/physical-economics-public-report-ui-496`.

## Goal
Expose a public, non-authorizing report request UI that can submit a bounded Physical Economics report request and render returned report/boundary/verification states without reimplementing ERL evidence, pertinence, boundary, uncertainty, conflict, or finding authority in Site.

## Collision boundary
This Site lane may own only newly created Physical Economics UI/client surfaces and its bounded validation/handoff surfaces. It must not modify active StegFin/VA claims, StegGate policy/runtime, Ecosystem Chat authority, wallet authority, or credential infrastructure.

## Authority boundary
Site is presentation/request transport only.

Site MUST NOT:
- decide report attribute pertinence;
- widen report historical or completeness boundaries;
- invent or promote findings;
- recompute ERL evidence authority;
- treat missing report backend availability as success;
- hold NON-TV/TVC credentials;
- use GitHub-token runtime authority;
- require Render.

## Active pre-work claim
`data/session-work-claims.json` now contains:
- claim id `SITE-PHYSICAL-ECONOMICS-PUBLIC-REPORT-UI-496-20260826`
- task id `SITE-PHYSICAL-ECONOMICS-PUBLIC-REPORT-UI-496`
- branch `feature/physical-economics-public-report-ui-496`
- state `CLAIMED_FOR_IMPLEMENTATION`
- dependency surface `site:physical-economics-public-report-ui`

Claimed implementation paths:
- `Physical-Economics.html`
- `js/physical-economics-report.js`
- `tests/physical-economics-report-ui.test.js`
- `docs/physical-economics/PUBLIC_REPORT_UI_MIRROR_HANDOFF.md`
- `data/session-work-claims.json`

The two earlier pre-claim placeholder markers have been removed on this branch and are not implementation progress.

## Required UI behavior
The Site surface must submit only a bounded report request, fail closed when the report backend is absent or invalid, render the upstream boundary/completeness statement before findings, preserve uncertainty and unresolved states, expose portable verification status, and never manufacture report findings.

## Release boundary
Issue #496 remains incomplete until claim/orchestration validation and deterministic UI tests pass, the integration merges, actual public publication is separately verified, and that publication evidence is propagated back to the ERL Physical Economics reporting handoff.

## Current state
- upstream ERL backend: implemented, not publicly activated;
- canonical Site issue: `#496` open;
- isolated Site branch: active;
- active Site pre-work claim: installed;
- placeholder cleanup: complete on branch;
- Site public UI/client code: authorized, not yet implemented;
- public activation: not authorized.

## Next executable transition
`CLAIMED_FOR_IMPLEMENTATION -> UI_CLIENT_IMPLEMENTED` after the claimed page, client, and deterministic test surfaces are created and validated.
