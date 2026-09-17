# Household Economic Conditions Site Mirror Handoff

## Canonical identity

- Goal Task ID: `ERL-HOUSEHOLD-ECONOMIC-CONDITIONS-SITE-001`
- central handoff: `StegVerse-Labs/.github/docs/ERL_HOUSEHOLD_ECONOMIC_CONDITIONS_SITE_MIRROR_HANDOFF.md`
- Site issue: `#1368`
- ERL issue: `StegVerse-Labs/Executive_Rhetoric_Ledger#163`
- coordination state: `ACTIVE`

## Site role

Site is presentation-only. It may display governed ERL household-state output but may not create a finding, bridge an evidence gap, splice incompatible historical definitions, or infer household welfare from headline macroeconomic data.

## Merged implementation evidence

Site PR `#1369` merged with expected-head protection at merge commit `33c83de3ebc0ab36f35f4563e6b01263a9f9d2ff` from exact head `c68e88665875b7d34ccce9fbcaf3a954b6e69fed`.

Every workflow returned for that exact head completed successfully, including:

- Site Bootstrap Validate - No Non-TV/TVC Credential Authority `35167451709`;
- Site Handoff Orchestrator `35167451717`;
- Ecosystem Heartbeat Orchestration `35167451682`;
- Node IndexedDB Schema Migration `35167451731`;
- Validate StegOS Persistent Card UX `35167451677`;
- No Required Third-Party Runtime `35167451705`;
- StegSocials Post Preparation `35167451703`;
- Ecosystem Visual Render Transport Validate `35167451737`;
- Verify NVIDIA Hugging Face publication `35167451723`;
- CFP Current-Season Ingestion `35167451722`;
- Validate ERL KV Provider Proof Projection `35167451714`.

The merged Site surfaces are:

- `Household-Economic-Conditions.html`;
- `data/household-economic-conditions.fixture.json`;
- `scripts/validate_household_economic_conditions_site.py`;
- `data/session-work-claims.d/site-household-economic-conditions-1368.json`;
- README household-economic-conditions documentation.

## Page behavior

The page provides:

- current-state cards for ten required household-state components;
- `1Y`, `5Y`, `10Y`, `2000→Now`, and `Max` history controls;
- normalized-index trajectory comparison;
- absolute-value mode that refuses mixed-unit overlays;
- visible Federal Reserve DSR, New York Fed CCP, and ACS methodology/coverage boundaries;
- explicit interpretation prohibitions;
- fail-closed fixture/public-activation state.

The fixture remains `evidence_state=FIXTURE_ONLY` and `public_activation_authorized=false`. It is not economic evidence.

## Upstream ERL state

ERL PR `#164` merged the household output schema, source inventory, fixture, deterministic contract validator, and README documentation. ERL PR `#165` subsequently merged exact official source identifiers plus fail-closed acquisition/normalization code for BLS, BEA, Board/FRED, New York Fed, and Census.

The Site page is not yet bound to those source candidates directly. Site must consume a governed ERL household-state output, not provider observations or source candidates independently.

## Fail-closed behavior

If a valid governed output is absent, stale, structurally invalid, or not explicitly authorized for public projection, Site must retain `UNKNOWN`/fail-closed presentation. Merge, branch-preview deployment, route reachability, or fixture loading is not public activation evidence.

## Longitudinal invariants

- 2000 is a requested horizon rather than a forced starting point.
- each series starts at its earliest defensible comparable observation;
- methodology and coverage breaks remain visible;
- incompatible definitions are never silently spliced;
- normalized mode compares trajectory only;
- absolute mode is permitted only for compatible units/definitions;
- missing values remain missing unless upstream ERL supplies an admissible reconstruction.

## Current state

- Site page shell: MERGED
- Site fixture: MERGED / FAIL-CLOSED
- deterministic Site contract validator: MERGED / PASS
- Site README reconciliation: MERGED
- exact active Site work claim: MERGED
- upstream ERL official identifiers/acquisition normalizers: MERGED
- governed ERL live household-state output: NOT IMPLEMENTED
- Site live-output endpoint binding: NOT IMPLEMENTED
- cohort selector/distribution views: PENDING
- current-iPhone Safari runtime validation: PENDING
- served-body/public activation verification: NOT OBSERVED
- public activation: NOT CLAIMED

## Next work

Wait for the first governed ERL household-state candidate that satisfies freshness, provenance, methodology-break, and household-state requirements. Then bind Site to that governed output with stale/invalid fail-closed behavior, validate the page against authentic data, and separately verify the served body before any public activation claim.
