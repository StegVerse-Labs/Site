# Physical Economics Public Report UI Mirror Handoff

## Authority
Bounded continuation record for the Site-side public UI integration of the ERL Physical Economics `GENERATE_REPORT` contract.

Parent repository authority: `SITE_MIRROR_HANDOFF.md`.
Upstream machine authority: `StegVerse-Labs/Executive_Rhetoric_Ledger/docs/physical-economics/reporting/PHYSICAL_ECONOMICS_REPORTING_MIRROR_HANDOFF.md`.

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

## Pre-work claim requirement
No implementation mutation beyond creating this bounded handoff is authorized until a canonical Site issue and active `data/session-work-claims.json` claim own the exact new UI/client paths.

## Planned new-only paths
- `Physical-Economics.html`
- `js/physical-economics-report.js`
- `tests/physical-economics-report-ui.test.js` or repository-native equivalent
- `docs/physical-economics/PUBLIC_REPORT_UI_MIRROR_HANDOFF.md`
- bounded claim entry in `data/session-work-claims.json`

## Current state
- upstream ERL backend: implemented, not publicly activated;
- Site public UI: not implemented;
- canonical Site issue: pending;
- active Site pre-work claim: pending;
- public activation: not authorized.
