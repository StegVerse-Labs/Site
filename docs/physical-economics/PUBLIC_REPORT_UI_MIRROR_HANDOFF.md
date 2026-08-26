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

Independent local execution of the exact checked-in Node suite produced all six expected PASS markers:

```text
PHYSICAL_ECONOMICS_REPORT_UI_REQUEST_CONTRACT=PASS
PHYSICAL_ECONOMICS_REPORT_UI_FAIL_CLOSED_BACKEND=PASS
PHYSICAL_ECONOMICS_REPORT_UI_BOUNDARY_BEFORE_FINDINGS=PASS
PHYSICAL_ECONOMICS_REPORT_UI_PORTABLE_VERIFICATION=PASS
PHYSICAL_ECONOMICS_REPORT_UI_NO_INVENTED_FINDINGS=PASS
PHYSICAL_ECONOMICS_REPORT_UI_HTML_ESCAPING=PASS
```

This is local deterministic validation only. It does not substitute for repository-hosted validation, merge proof, publication proof, or live backend execution.

### `.github/workflows/validate-physical-economics-report-ui.yml`
A dedicated credential-free validation workflow is installed and machine-claim owned. It anonymously fetches the exact PR merge ref, refuses credential-bearing environment variables, runs Site session-claim and handoff-orchestration validators, runs the Node UI contract suite, and asserts the published endpoint remains unconfigured/fail-closed pending a real backend.

## PR state
Fresh live query on 2026-08-26 after all implementation commits:

```text
PR: #499
state: open
is_draft: true
merged: false
head: c09fae59eb1304909520de0e3adb6497bd35a2a4
base: 380ac32127e052893c08e44eb699772109ba1665
mergeable: false
```

This supersedes the earlier intermediate `mergeable: true` observation. Mergeability is live state and must be queried again before any future merge action.

## Validation state
Hosted validation is **attempted but not passed** on exact head `c09fae59eb1304909520de0e3adb6497bd35a2a4`.

Fresh GitHub evidence on 2026-08-26:

```text
Validate Physical Economics Report UI
run_id: 32985301150
run_number: 2
event: pull_request
status: completed
conclusion: startup_failure
job_id: 98230430068
job_name: validate
job_conclusion: cancelled
runner_id: 0
steps_executed: 0
job_log: unavailable / GitHub BlobNotFound
```

The run reached GitHub but no runner was assigned and no validation step executed. Therefore this is not a test failure and not a PASS; it is a provider/runtime startup gate failure whose root cause is not established by available logs.

Two other exact-head workflow observations preserve the broader Site runtime posture:
- `Check StegFin Phone Projection - Validation Only / No GitHub Token Authority`, run `32985311227`: `startup_failure`;
- `Ecosystem Heartbeat Orchestration`, run `32985300393`: still `queued` at last observation.

Do not rewrite these as Physical Economics code failures. Do not rewrite queue/startup state as hosted success.

## Release boundary
Issue #496 remains incomplete until:
1. session-work claim validation passes;
2. Site handoff/orchestration validation passes;
3. deterministic UI/client tests pass;
4. PR #499 becomes merge-admissible and merges;
5. actual public publication is independently verified;
6. verified publication is propagated to the ERL Physical Economics reporting handoff.

Even after those Site gates, a blank backend endpoint means the report button remains intentionally fail-closed. A real validated HTTP adapter around the ERL report transaction is the next cross-repository integration goal required for functional report generation.

## External / user-action boundary
No credential or iPhone-only user action is currently proven necessary for Issue #496 itself. The exact-head hosted startup failure has no retrievable step log and no runner assignment, so its cause must be diagnosed before assigning a manual GitHub billing/settings/provider action to the user.

If later public HTTP deployment requires provider credentials, those credentials remain TV/TVC-only. Do not place provider secrets in Site, GitHub-token runtime authority, or conversation state. Render is not an authorized dependency.

## Current state
- upstream ERL report backend transaction: implemented, not publicly activated;
- Site issue #496: open;
- Site PR #499: open draft, unmerged, currently non-mergeable;
- active Site machine claim: installed;
- Site page/client/tests: implemented;
- deterministic Node suite: locally PASS;
- dedicated validation workflow: implemented;
- hosted Physical Economics validation: exact-head run observed, `startup_failure`, zero steps executed;
- ecosystem heartbeat on exact head: queued at last observation;
- public page publication: not verified;
- report HTTP endpoint: not configured;
- public report activation/release: not authorized.

## Next executable transition
`UI_CLIENT_IMPLEMENTED_HOSTED_STARTUP_BLOCKED -> UI_CLIENT_VALIDATED` only after the hosted runner/startup condition is resolved and the exact PR head/merge ref executes the required validation steps successfully.

Then:

```text
hosted validation PASS
-> resolve current PR mergeability/review gates
-> merge PR #499
-> independently verify actual public publication
-> record publication receipt/evidence here and upstream
-> build/validate governed HTTP adapter around ERL report transaction
-> only after adapter/runtime proof populate the Site endpoint
-> execute and independently verify a real end-to-end VERIFIABLE report
```

Do not treat static publication as functional report activation, and do not treat an implemented HTTP adapter as deployed or released without live proof.

## Archive posture
All Issue #496 session-specific implementation facts, corrected hosted-runtime evidence, local deterministic PASS evidence, merge/publication boundaries, credential boundaries, and cross-repository continuation requirements are durably captured here. Continued work does not require rereading the originating conversation for this Site lane.