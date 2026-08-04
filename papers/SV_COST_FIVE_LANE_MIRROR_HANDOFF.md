# SV Cost Five-Lane Site Mirror Handoff

## Source of truth

This file is the current task and verification handoff for:

```text
papers/sv-cost-relational-analysis.html
```

Canonical result:

```text
GCAT-BCAT-Engine/workflows
experiments/sv-cost-program/five-lane-results/results/five_lane_results.json
```

Canonical publication:

```text
GCAT-BCAT-Engine/Publisher
papers/five-lane-reconstructable-governance-analysis.md
```

## Admission boundary

Publication is admitted only when the canonical result states:

```text
all_five_successful_equivalent_admissible = true
publication_status = RESULTS_READY_FOR_BOUNDED_PUBLICATION
```

This is a bounded publication projection only. It grants no execution, custody, validation, release, financial, or activation authority.

## Canonical evidence

```text
experiment_id: SV-COST-FIVE-LANE-RESULTS-001
task_id: SV-RECON-001
operation_class: governed_state_reconstruction
comparison_unit: successful equivalent admissible outcome
result_generated_at: 2026-08-04T01:41:10Z
canonical_result_commit: 3720211a1cfaaf2db697f3e26194d083db21e94f
canonical_publisher_commit: 0b897f782e72f76c4f7c6beb596c45bbe9d56b11
site_projection_commit: 9d4205f665956a01ea82e35abd098ecb9e814656
papers_index_commit: 31876f35ecbaa782780b3bcef673a1fb2055a2a6
task_contract_hash: sha256:2e9b4a4193669b6d8f1d3fea8639d2adcee6090c58246b8b99920ba2f08dfb6b
normalized_outcome_hash: sha256:155869baaef4bd023ad95e63c6a81d6ade921e92660cec351680e1aabd4d2597
price_card_status: VERSIONED_DECLARED_RATE_NOT_INVOICE_RECONCILED
```

## Exact admitted lane results

| Lane | Cost per successful equivalent admissible outcome | Latency | Status |
|---|---:|---:|---|
| OpenAI raw | $0.006875 | 3.424027735 s | PASS |
| OpenAI governed | $0.006880 | 2.867607194 s | PASS |
| Anthropic raw | $0.010656 | 7.939445812 s | PASS |
| Anthropic governed | $0.007116 | 5.459360124 s | PASS |
| StegVerse-only deterministic reconstruction | $0.000000002885 | 0.000000461 s | PASS |

## Claim boundary

The result measures one bounded deterministic reconstruction operation. It does not establish universal provider economics, company ROI, enterprise-wide savings, or fresh-inference equivalence.

Provider costs use retained token usage and a versioned declared price card; they are not invoice-reconciled charges. The StegVerse-only value combines measured runtime and output size with declared local runner and storage rates.

## Completed repository work

- Replaced the methodology-only Site page with the validated five-lane results.
- Preserved mobile-safe tables, long-hash wrapping, and bounded-claim callouts.
- Verified repository source contains all five exact lane values, the shared outcome hash, and the publication boundary.
- Preserved links to the canonical machine-readable result and Publisher source.
- Updated `Papers.html` to feature the validated five-lane results.
- Confirmed repository `CNAME` contains `stegverse.org`.
- Confirmed the authorized GitHub Pages deployment route is `Site Bootstrap Validate` followed by exact-SHA `Site Task Runner`, which uses `actions/deploy-pages@v4`.

## Fresh public observation — 2026-08-04

The public `Papers.html` response remained on the superseded methodology-only content even though `main` contains the corrected five-lane index and paper. This proves the public custom-domain deployment was stale at observation time.

The earlier Vercel project observation is not the authoritative custom-domain route. The repository CNAME and Pages deployment workflow identify GitHub Pages as the intended `stegverse.org` publication route.

This handoff update is a bounded repository mutation that triggers `Site Bootstrap Validate`; a successful bootstrap run should trigger exact-SHA `Site Task Runner`, upload the repository as a Pages artifact, and deploy it through `actions/deploy-pages@v4`.

## Required terminal verification

Verify both public URLs after the Pages run completes:

```text
https://stegverse.org/papers/sv-cost-relational-analysis.html
https://stegverse.org/Papers.html
```

Required public markers:

```text
Five-Lane Cost Results for Reconstructable Governance
OpenAI raw: $0.006875
OpenAI governed: $0.006880
Anthropic raw: $0.010656
Anthropic governed: $0.007116
StegVerse-only: $0.000000002885
```

## Completion state

```text
canonical_result: PASS
publisher_source: COMPLETE
site_source_projection: COMPLETE
site_source_verification: PASS
papers_index_update: COMPLETE
hosting_route_resolution: GITHUB_PAGES
pages_deployment_trigger: COMMITTED
public_custom_domain_verification: PENDING_PAGES_COMPLETION
```
