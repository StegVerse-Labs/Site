# StegVerse-Labs / Site

Public mirror for the StegVerse ecosystem. Renders proof surfaces, transition status,
governance documentation, and product information from canonical source data.

**Live site:** https://stegverse-labs.github.io/Site/

---

## Boundary

```
formalism-tests    =  proof/test authority
StegVerse-002      =  governed deployment authority
Site               =  public mirror only

Site publishes receipts. Site does not generate them.
Site must never become the authority for receipts, transitions, or accreditation.
```

---

## Site structure

### Public pages

| Page | Purpose |
|------|---------|
| [`index.html`](index.html) | Home — proof status, product overview, live evidence |
| [`demo.html`](demo.html) | Execution demo — commit-boundary decision with receipt hash |
| [`stegverse-002.html`](stegverse-002.html) | StegVerse-002 / core-lite mirror — gate map, live evidence |
| [`formalism-tests-stage-1-to-31.html`](formalism-tests-stage-1-to-31.html) | Stage 1–31 proof mirror — Beta_Orionis / StegVerse-001 |
| [`stegfinco.html`](stegfinco.html) | StegFinCo — governed financial execution layer |
| [`product.html`](product.html) | Trust & Risk Systems Audit — product details |
| [`pricing.html`](pricing.html) | Pricing — rendered from canonical manifest |
| [`methodology.html`](methodology.html) | Methodology — evidence over self-attestation |
| [`about.html`](about.html) | About StegVerse |
| [`support.html`](support.html) | Support StegVerse Research |
| [`Papers.html`](Papers.html) | Papers and research |

### Public positioning

| Document | Purpose |
|----------|---------|
| [`docs/public-positioning/ai-safety-to-transition-admissibility.md`](docs/public-positioning/ai-safety-to-transition-admissibility.md) | External bridge from AI safety framing to StegVerse transition admissibility, GLM, EVIDE, and runtime governance |

### Transition pages

| Page | Purpose |
|------|---------|
| [`transition-proof-surface.html`](transition-proof-surface.html) | Proof progression, verified task chain, source artifacts |
| [`transition-release-index.html`](transition-release-index.html) | Release index — all 31 stages, current release state |
| [`transition-development-status.html`](transition-development-status.html) | Current gate, next integration target, SV002 status |
| [`transition-verification-guide.html`](transition-verification-guide.html) | How to verify receipts, task chains, proof artifacts |
| [`transition-table-visual.html`](transition-table-visual.html) | Visual periodic-table-style element map — block structure |
| [`transition-table.html`](transition-table.html) | Transition table class browser |
| [`transition-table-classes.html`](transition-table-classes.html) | Detailed transition class browser |
| [`transition-replay-packet.html`](transition-replay-packet.html) | Replay packet |
| [`stage10-canonical-release.html`](stage10-canonical-release.html) | Stage 10 — Canonical Transition Table Release |

### Design system

| File | Purpose |
|------|---------|
| [`sv-shared.css`](sv-shared.css) | Shared design system — all pages link to this |
| [`assets/transition-site-status.js`](assets/transition-site-status.js) | Shared client-side renderer for transition status pages |

### Data

| File | Purpose |
|------|---------|
| [`data/formalism-tests/transition-proof-surface.json`](data/formalism-tests/transition-proof-surface.json) | **Single source of truth** for all transition status pages |

---

## Updating status

To update the public transition status across all transition pages, edit only:

```
data/formalism-tests/transition-proof-surface.json
```

Fields that propagate to all transition pages:

```
current_stage
status
stages[*].status
stage6_result
verified_tasks
source_artifacts
next_integration_target
authority_boundary
```

No workflow files need to change for a status update.

---

## Current proof state

### StegVerse-001 / Beta_Orionis
- Stages 1–31 complete
- Stage 31 — Production Accreditation and Revocation Boundary — PASSED
- 26 cases · 66 assertions · 26 receipts

### StegVerse-002 / core-lite
- Version: `v1.0.0-sv002-m10`
- Gates M0–M10 complete
- Intake proven live — `status: success` · `stop_condition_met: true`
- CGE decision: `ALLOW` · `sha256:33aa60e7...`
- Receipt chain: `sha256:a151deed...` · live
- Repo: https://github.com/StegVerse-002/core-lite

---

## Transition Table — Visual Element Map

[`transition-table-visual.html`](transition-table-visual.html) organizes transition elements
using the same structural logic as the periodic table of elements.

**Two independent axes:**
- Rows — consequence tier (T0 identity → T12 quorum)
- Columns — decision class (ALLOW → FAIL-CLOSED)

**Block structure — the organizing dimension beneath both axes:**

The 9 canonical coupling classes (from Stage 10: `coupling_class_count: 9`) create
block regions where elements share the same relationship to prior state.

| Block | Name | Tiers | Core rule |
|-------|------|-------|-----------|
| B1 | Identity | T0 | No prior state required |
| B2 | Data | T1–T2 | Same data ≠ same continuation admissibility |
| B3 | Composite | T3–T4 | Local allow + local allow ≠ composite allow |
| B4 | Commit-Time | T5–T6 | Admissibility at the binding moment only |
| B5 | Discovery | T7–T8 | Observes, proposes — does not install |
| B6 | Packet | T8–T9 | Portable evidence — not authority |
| B7 | Install-Plan | T9–T10 | Candidate transition — not authority |
| B8 | Production | T11–T12 | Accredited participation — not sovereign authority |
| B9 | Replay | T3, T11 | Reconstructs — cannot reverse (displaced, f-block equivalent) |

**Predicted cells** — empty cells are not blank. The formalism constrains which
combinations are possible, mandatory, derivable, or structurally excluded.
Click any non-populated cell to see which rule applies.

---

## Node and FinCo boundary

Core installation does not imply node participation.
Node participation does not imply FinCo eligibility.

```json
{
  "core_unit_installed": true,
  "node_participation_opt_in": false,
  "node_status": "NOT_A_NODE",
  "finco_participation_requested": false,
  "finco_participation_allowed": false
}
```

---

## Proof authority

| System | Authority |
|--------|-----------|
| `Data-Continuation/formalism-tests` | Stage 1–31 receipts and proof |
| `StegVerse-002/core-lite` | SV002 receipts and deployment proof |
| `StegVerse-Labs/Site` | Public mirror only — not proof authority |
