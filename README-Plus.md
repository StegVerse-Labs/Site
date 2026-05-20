# Stage 6 Site Publication Bundle

## Assumptions

1. `formalism-tests` remains the authoritative source for Stage 6 candidates, tests, receipts, and validation output.
2. `StegVerse-Labs/Site` is only the public presentation surface.
3. No GitHub Actions workflows are added or changed.
4. This bundle may be installed into the `StegVerse-Labs/Site` repository root.

## Done Definition

This bundle is done when:

1. `stage6-unified-gate-results.html` opens as a public Site page.
2. `transition-release-index.html` links to the Stage 6 public results page.
3. `transition-table-classes.html` links to the Stage 6 public results page.
4. The Site page describes all 10 completed Stage 6 candidates.
5. The page reports the first full test surface as 94 tests passing.
6. The footer/boundary text preserves the rule: `formalism-tests produces receipts. Site publishes receipts. Site must not become the authority for receipts.`

## Files Included

| Path | Purpose |
|---|---|
| `stage6-unified-gate-results.html` | New public Stage 6 results page. |
| `transition-release-index.html` | Full replacement adding a Stage 6 link in navigation and canonical pages. |
| `transition-table-classes.html` | Full replacement adding a Stage 6 link and decision-filter support for `RESET_BOUNDARY` and `EVOLVE_BOUNDARY`. |
| `bundle_manifest.json` | Bundle installation manifest. |
| `README.md` | Bundle explanation and verification checklist. |

## Stage 6 Public Result Summary

Stage 6 tests the Admissible Existence Unified Gate:

```text
ALLOW(u) iff IW_tau(S,u) subset A_total AND RE(S -> Phi(S,u)) <= RE_max
```

The completed candidate set contains 10 candidates and the first full test surface contains 94 tests.

## Candidate Coverage

| Candidate | Expected Decision | Purpose |
|---|---|---|
| `T-AE-UNIFIED-ALLOW-001` | `ALLOW` | Positive control for unified admissibility. |
| `T-AE-UNIFIED-IW-BREACH-001` | `FAIL_CLOSED` | IW containment failure. |
| `T-AE-UNIFIED-RE-BREACH-001` | `FAIL_CLOSED` | Reverse entropy bound failure. |
| `T-AE-UNIFIED-DUAL-BREACH-001` | `FAIL_CLOSED` | Dual IW and RE failure. |
| `T-AE-UNIFIED-RESET-001` | `RESET_BOUNDARY` | Recoverable non-convergence. |
| `T-AE-UNIFIED-EVOLVE-001` | `EVOLVE_BOUNDARY` | Purpose/coherence boundary failure. |
| `T-AE-UNIFIED-AI-BLOCK-ALLOW-001` | `ALLOW` | Valid AI Block admissibility. |
| `T-AE-UNIFIED-AI-BLOCK-ESCAPE-001` | `FAIL_CLOSED` | AI Block scope violation. |
| `T-AE-UNIFIED-FINCO-CHAIN-001` | `ALLOW` | Valid FinCo chain compliance. |
| `T-AE-UNIFIED-FINCO-CHAIN-BREAK-001` | `FAIL_CLOSED` | Broken FinCo chain failure. |

## Verification

After upload to `StegVerse-Labs/Site`, verify these pages:

```text
https://stegverse-labs.github.io/Site/stage6-unified-gate-results.html
https://stegverse-labs.github.io/Site/transition-release-index.html
https://stegverse-labs.github.io/Site/transition-table-classes.html
```

The Stage 6 page should be reachable from both linked pages.
