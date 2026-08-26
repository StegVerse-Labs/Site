# Physical Economics Public Report UI Mirror Handoff

## Authority
Bounded continuation record for the Site-side public UI integration of the ERL Physical Economics `GENERATE_REPORT` contract.

Parent repository authority: `SITE_MIRROR_HANDOFF.md`.
Upstream machine authority: `StegVerse-Labs/Executive_Rhetoric_Ledger/docs/physical-economics/reporting/PHYSICAL_ECONOMICS_REPORTING_MIRROR_HANDOFF.md`.
Canonical Site issue: `StegVerse-Labs/Site#496`.
Implementation branch: `feature/physical-economics-public-report-ui-496`.
Integration PR: `StegVerse-Labs/Site#499`.

## Goal
Expose a public, non-authorizing report request UI that submits a bounded Physical Economics report request and renders returned report/boundary/verification states without reimplementing ERL evidence, pertinence, boundary, uncertainty, conflict, or finding authority in Site.

## Collision and authority boundary
This lane owns only its machine-claimed Physical Economics page/client/test/handoff/validation surfaces. It does not own active StegFin/VA surfaces, StegGate policy/runtime, Ecosystem Chat authority, wallet authority, or credential infrastructure.

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
Claim id: `SITE-PHYSICAL-ECONOMICS-PUBLIC-REPORT-UI-496-20260826`.
State: `CLAIMED_FOR_IMPLEMENTATION`.
Dependency surface: `site:physical-economics-public-report-ui`.

Claimed paths now include:
- `Physical-Economics.html`
- `js/physical-economics-report.js`
- `tests/physical-economics-report-ui.test.js`
- `.github/workflows/validate-physical-economics-report-ui.yml`
- `docs/physical-economics/PUBLIC_REPORT_UI_MIRROR_HANDOFF.md`
- `data/session-work-claims.json`

The unrelated historical `SITE-TWO-ENTRY-VALIDATION-CLOCK-RETIREMENT-409-20260822` task identity was checked after claim expansion and restored exactly after one reconstruction typo; Issue #496 leaves that lane unchanged.

## Implemented Site surfaces
### `Physical-Economics.html`
A complete static public report-request page now exists. It exposes question/scope, all 16 upstream claim classes, vintage policy, optional date bounds, output-surface controls, request JSON inspection, report-result rendering, and explicit non-authorizing/fail-closed language.

The endpoint meta value remains intentionally blank. Page publication alone therefore cannot cause report generation or imply backend activation.

### `js/physical-economics-report.js`
The client is a browser/CommonJS module. It:
- builds the upstream request shape;
- binds `required_attribute_sets_version` to upstream pertinence matrix version `0.1`;
- never exposes required-attribute exclusion (`excluded_attributes` is always empty);
- requires backend state `GENERATED_NOT_PUBLICLY_ACTIVATED`;
- requires portable verification state `VERIFIABLE`;
- rejects report/receipt identity or renderer-version mismatches;
- restricts finding postures to governed classes;
- renders boundary before findings;
- renders no findings when none are supplied;
- escapes rendered strings;
- uses credential-omitting/no-store/error-on-redirect fetch semantics;
- fails closed when endpoint/network/HTTP/JSON/report/verification state is invalid.

A live upstream contract inspection caught and corrected an initial client version-string mismatch before validation: the canonical pertinence matrix version is exactly `0.1`.

### `tests/physical-economics-report-ui.test.js`
Deterministic Node tests cover request/version binding, claim/date rejection, verification-state enforcement, backend-state enforcement, unconfigured-backend failure, boundary-before-findings ordering, no invented findings, transport options, and HTML escaping.

### `.github/workflows/validate-physical-economics-report-ui.yml`
A dedicated credential-free validation workflow is installed and machine-claim owned. It anonymously fetches the exact PR merge ref, refuses credential-bearing environment variables, runs Site session-claim and handoff-orchestration validators, runs the Node UI contract suite, and asserts the published endpoint remains unconfigured/fail-closed pending a real backend.

## PR state
Draft PR `#499` is open. A fresh query before the latest handoff commit reported `mergeable: true`; mergeability must be queried again after later head movement before any merge action.

## Validation state
Hosted validation is **not yet established**. Exact-head queries through commit `422d188957677221de9987965076659f97880694` returned no pull-request workflow runs. Workflow presence is not treated as PASS.

The dedicated workflow was added so a subsequent PR-head event can prove the exact merge ref. Until a run is observed and consumed, validation remains pending.

## Release boundary
Issue #496 remains incomplete until:
1. session-work claim validation passes;
2. Site handoff/orchestration validation passes;
3. deterministic UI/client tests pass;
4. PR #499 merges;
5. actual public publication is independently verified;
6. verified publication is propagated to the ERL Physical Economics reporting handoff.

Even after those Site gates, a blank backend endpoint means the report button remains intentionally fail-closed. A real validated HTTP adapter around the ERL report transaction is the next cross-repository integration goal required for functional report generation.

## Current state
- upstream ERL report backend transaction: implemented, not publicly activated;
- Site issue #496: open;
- Site PR #499: open draft;
- active Site machine claim: installed;
- Site page/client/tests: implemented;
- dedicated validation workflow: implemented;
- hosted validation: pending/no exact-head run observed yet;
- public page publication: not verified;
- report HTTP endpoint: not configured;
- public report activation/release: not authorized.

## Next executable transition
`UI_CLIENT_IMPLEMENTED_VALIDATION_PENDING -> UI_CLIENT_VALIDATED` only after exact-head hosted validation is observed and consumed. After merge/publication verification, continue to the governed HTTP-adapter integration rather than treating the static page as a functional report service.
