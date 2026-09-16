# Household Economic Conditions Site Mirror Handoff

## Canonical identity

- Goal Task ID: `ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001`
- central handoff: `StegVerse-Labs/.github/docs/ERL_HOUSEHOLD_ECONOMIC_CONDITIONS_SITE_MIRROR_HANDOFF.md`
- Site issue: `#1368`
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

## Fail-closed behavior

The page refuses to claim live conditions from the fixture. If the contract cannot be loaded or the fixture boundary is wrong, the page renders an unknown/fail-closed state. A future live binding must require governed ERL output, freshness validation, source vintage, methodology-break metadata, and explicit public activation authorization.

## Longitudinal behavior

The page treats 2000 as a requested horizon rather than a forced start date. Each governed series must carry its own earliest comparable date. Normalized mode compares trajectory only. Absolute mode is allowed only when selected series share compatible units and definitions; otherwise the graph refuses the overlay instead of using a misleading dual axis.

## Not yet complete

- exact ERL live endpoint/output binding;
- deterministic contract validation in Site CI;
- real official observations;
- cohort selector and distribution views;
- served-body/public activation verification;
- current-iPhone Safari runtime validation;
- navigation integration from the public index after activation criteria are satisfied.

## Next work

Bind Site validation to the ERL output schema/fixture contract, validate the branch, reconcile README/navigation documentation, then connect a governed ERL output only after the source lane produces current authentic data.
