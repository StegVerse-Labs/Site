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

## Pre-work claim requirement
No UI/client implementation mutation is authorized until an active `data/session-work-claims.json` entry owns the exact new UI/client paths for Issue #496.

The current connector can read the large claim registry but only exposes whole-file replacement for mutation. Because a safe complete registry reconstruction is not available through the current tool surface, the claim has **not** been fabricated or bypassed. Implementation remains fail-closed at the claim gate.

## Planned new-only claim surface
- `Physical-Economics.html`
- `js/physical-economics-report.js`
- `tests/physical-economics-report-ui.test.js` or repository-native equivalent
- `docs/physical-economics/PUBLIC_REPORT_UI_MIRROR_HANDOFF.md`
- bounded claim entry in `data/session-work-claims.json`

Suggested claim identity once registry mutation is safely available:
- claim id: `SITE-PHYSICAL-ECONOMICS-PUBLIC-REPORT-UI-496-20260826`
- task id: `SITE-PHYSICAL-ECONOMICS-PUBLIC-REPORT-UI-496`
- normalized work key: `site-physical-economics-public-report-ui-496`
- dependency surface: `site:physical-economics-public-report-ui`
- role: `IMPLEMENTATION`
- state: `CLAIMED_FOR_IMPLEMENTATION`
- credential authority: `TV/TVC`
- credential requirement: `NONE`
- GitHub-token runtime authority: `NONE`
- Render required: `false`
- authority effect: `false`
- activation effect: `false`

## Governance cleanup note
Two repository markers were created before the claim gate was fully enforced:
- `docs/physical-economics/.keep`
- `docs/physical-economics/CLAIM_GATE_PENDING.md`

They contain no UI implementation or runtime authority. They should be removed on the governed Issue #496 branch after the active claim is installed. They must not be counted as implementation progress.

## Current state
- upstream ERL backend: implemented, not publicly activated;
- canonical Site issue: `#496` open;
- isolated Site branch: created;
- active Site pre-work claim: pending / fail-closed blocker;
- Site public UI/client code: not implemented;
- public activation: not authorized.

## Next executable transition
`CLAIM_PENDING -> CLAIMED_FOR_IMPLEMENTATION` only after the complete claim registry can be safely updated and repository claim/orchestration validation can consume the new entry.

Only then may the branch add the new Physical Economics page/client/test surfaces.
