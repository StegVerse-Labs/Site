# Household Economic Conditions Site Mirror Handoff

## Canonical identity

- Goal Task ID: `ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001`
- central handoff: `StegVerse-Labs/.github/docs/ERL_HOUSEHOLD_ECONOMIC_CONDITIONS_SITE_MIRROR_HANDOFF.md`
- Site issue: `#1368`
- Site PR: `#1369`
- ERL issue: `StegVerse-Labs/Executive_Rhetoric_Ledger#163`
- branch: `feat/household-economic-conditions-site-1368`
- coordination state: `ACTIVE`

## Site role

Site is presentation-only. It may display governed ERL household-state output but may not create a finding, bridge an evidence gap, splice incompatible historical definitions, or infer household welfare from headline macroeconomic data.

## Implemented in this branch

- `Household-Economic-Conditions.html`
  - persistent household-state page shell;
  - current-state cards for the ten required household components;
  - history controls for `1Y`, `5Y`, `10Y`, `2000→Now`, and `Max`;
  - normalized-index comparison mode;
  - absolute mode that refuses mixed-unit overlays;
  - visible Federal Reserve DSR, New York Fed CCP, and ACS methodology/coverage boundaries;
  - interpretation prohibitions consistent with ERL semantics;
  - fail-closed public activation banner.
- `data/household-economic-conditions.fixture.json`
  - fixture-only contract used to exercise the graph and state-card UI;
  - `evidence_state=FIXTURE_ONLY`;
  - `public_activation_authorized=false`;
  - values are illustrative UI fixtures and are explicitly not economic evidence.
- `data/session-work-claims.d/site-household-economic-conditions-1368.json`
  - exact active pre-work claim for this branch/task;
  - no authority or activation effect.

## Validation and repair evidence

Initial PR validation failed at the Site orchestration gate because the branch did not yet resolve to an exact active pre-work claim. That was a coordination defect, not a page/runtime failure. It was repaired by adding the bounded claim fragment above.

Current exact head after repair: `fe9df5aabd715c0957e34db5d37665a1e7f1e417`.

Exact-head validations:

- Site Handoff Orchestrator `35162631957`: `SUCCESS`;
- Ecosystem Heartbeat Orchestration `35162632000`: `SUCCESS`;
- Node IndexedDB Schema Migration `35162631871`: `SUCCESS`;
- Site Bootstrap Validate - No Non-TV/TVC Credential Authority `35162631877`: `SUCCESS`.

These validations establish source/coordination consistency only. They do not prove deployment, live economic data, governed ERL runtime output, or public activation.

## Fail-closed behavior

The page refuses to claim live conditions from the fixture. If the contract cannot be loaded or the fixture boundary is wrong, the page renders an unknown/fail-closed state. A future live binding must require governed ERL output, freshness validation, source vintage, methodology-break metadata, and explicit public activation authorization.

## Longitudinal behavior

The page treats 2000 as a requested horizon rather than a forced start date. Each governed series must carry its own earliest comparable date. Normalized mode compares trajectory only. Absolute mode is allowed only when selected series share compatible units and definitions; otherwise the graph refuses the overlay instead of using a misleading dual axis.

## Current state

- page shell: IMPLEMENTED ON PR #1369
- fixture contract: IMPLEMENTED / FAIL-CLOSED
- exact active Site work claim: IMPLEMENTED
- exact-head orchestration/bootstrap validation: PASS
- README.md reconciliation: PENDING
- exact ERL live endpoint/output binding: NOT IMPLEMENTED
- deterministic Site contract validator: PENDING
- real official observations: NOT BOUND
- cohort selector and distribution views: PENDING
- current-iPhone Safari runtime validation: PENDING
- served-body/public activation verification: NOT OBSERVED
- public activation: NOT CLAIMED

## Next work

Reconcile `README.md` for this material new public surface, add deterministic Site contract validation, re-run exact-head gates, and only then merge with expected-head protection. After source merge, bind authentic governed ERL output and separately verify served public content before any activation claim.
