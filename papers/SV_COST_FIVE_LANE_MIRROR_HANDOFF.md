# SV Cost Five-Lane Site Mirror Handoff

## Source of truth

This file is the current task and verification handoff for the public Site projection at:

```text
papers/sv-cost-relational-analysis.html
```

Canonical result source:

```text
GCAT-BCAT-Engine/workflows
experiments/sv-cost-program/five-lane-results/results/five_lane_results.json
```

Canonical publication source:

```text
GCAT-BCAT-Engine/Publisher
papers/five-lane-reconstructable-governance-analysis.md
```

## Admission boundary

This is a bounded publication projection only. It grants no execution, custody, validation, release, financial, or activation authority.

Publication is admitted only when the canonical result states:

```text
all_five_successful_equivalent_admissible = true
publication_status = RESULTS_READY_FOR_BOUNDED_PUBLICATION
```

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

Provider costs are computed from retained token usage using a versioned declared price card and are not invoice-reconciled charges. The StegVerse-only value combines measured runtime and output size with declared local runner and storage rates.

## Completed mirror work

- Replaced the earlier methodology/relational-analysis Site page with the validated five-lane results publication.
- Preserved mobile-safe tables, long-hash wrapping, and bounded-claim callouts.
- Verified repository source contains all five exact lane values, the shared outcome hash, and the publication boundary.
- Preserved links to the canonical machine-readable result and Publisher source.

## Remaining work

Destination `StegVerse-Labs/Site`:

```text
Update Papers.html featured title and description after the active index owner admits the change.
Observe the custom-domain deployment serving Site commit 9d4205f665956a01ea82e35abd098ecb9e814656.
Verify https://stegverse.org/papers/sv-cost-relational-analysis.html contains the five-lane title and exact results.
```

The current environment could not independently retrieve the custom-domain page; public verification therefore remains fail-closed rather than inferred from the committed source.

## Completion state

```text
publisher_source: COMPLETE
site_source_projection: COMPLETE
site_source_verification: PASS
papers_index_update: PENDING_ACTIVE_OWNER_ADMISSION
public_custom_domain_verification: PENDING_DEPLOYMENT_OBSERVATION
```
