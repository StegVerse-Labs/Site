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

The broader SV-COST program is terminal under `GCAT-BCAT-Engine/workflows/SV_COST_MIRROR_HANDOFF.md`. A favorable or general ROI revision is owned only by `GCAT-BCAT-Engine/workflows#13` and requires fully burdened local-cost sources, invoice reconciliation, successful held-out equivalence, and break-even analysis. This bounded publication does not satisfy or bypass those requirements.

## Completed repository work

- Replaced the methodology-only Site page with the validated five-lane results.
- Preserved mobile-safe tables, long-hash wrapping, and bounded-claim callouts.
- Verified repository source contains all five exact lane values, the shared outcome hash, and the publication boundary.
- Preserved links to the canonical machine-readable result and Publisher source.
- Updated `Papers.html` to feature the validated five-lane results.
- Confirmed repository `CNAME` contains `stegverse.org`.
- Confirmed the authorized GitHub Pages deployment route is `Site Bootstrap Validate` followed by exact-SHA `Site Task Runner`, which uses `actions/deploy-pages@v4`.
- Created durable validation issue `StegVerse-Labs/Site#173` for terminal public-body observation and closure.

## Fresh public observation — 2026-08-04

The public `https://stegverse.org/Papers.html` response serves the five-lane featured publication. It contains the title `Five-Lane Cost Results for Reconstructable Governance`, identifies all five compared lanes, states that all five produced the same normalized admissible outcome, reports the observed Anthropic governed-pair reduction of 33.22%, identifies StegVerse-only as the lowest-cost lane for this bounded reconstruction operation, and preserves the boundary against universal provider economics, fresh-inference equivalence, enterprise-wide savings, and company ROI.

The public index links to `https://stegverse.org/papers/sv-cost-relational-analysis.html`. Independent retrieval of the linked body returned a cache-miss response. A second execution environment could not resolve the domain; that environment failure is not evidence that the public page is unavailable. Exact body-marker verification therefore remains fail-closed and pending under issue `#173`.

No result, cost, hash, or claim was altered in this handoff update.

## Active claims

- Task ID: `SV-COST-FIVE-LANE-PUBLIC-BODY-VERIFY-001`
- Originating goal: complete and consolidate the bounded five-lane publication workflow.
- Repository/branch: `StegVerse-Labs/Site@main`
- Surface: `papers/sv-cost-relational-analysis.html`
- Claimant: Site deployment/public-observation lane
- Role: `COMPLETE — CLAIM RELEASED`
- Claim created: `2026-08-04T16:13:13Z`
- Durable task: `StegVerse-Labs/Site#173`
- Release condition: direct HTTP 200 public retrieval plus all required marker checks, with the result committed here; alternatively, exact deployed-artifact evidence followed by public accessibility confirmation.
- Collision boundary: do not alter canonical lane values, hashes, task identity, pricing status, or broaden the claim.
- Next task after release: close issue `#173`, mark `public_paper_body_verification: PASS`, and release this claim.

## Required terminal verification

Verify the linked public paper body:

```text
https://stegverse.org/papers/sv-cost-relational-analysis.html
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

Validation owner and receipt location: `StegVerse-Labs/Site#173` and this handoff.

## Session consolidation

Original session goal, adjacent publication requirements, exact results, claim limits, repository locations, deployment route, public-index observation, unresolved public-body verification, owner, release condition, and next executable action are now durably transferred.

MERGED INTO: `StegVerse-Labs/Site/papers/SV_COST_FIVE_LANE_MIRROR_HANDOFF.md` and `StegVerse-Labs/Site#173`.

The chat no longer owns unique implementation authority. Repository-native continuation owns the remaining validation task.

## Completion state

```text
canonical_result: PASS
publisher_source: COMPLETE
site_source_projection: COMPLETE
site_source_verification: PASS
papers_index_update: COMPLETE
hosting_route_resolution: GITHUB_PAGES
public_papers_index_verification: PASS_2026-08-04
public_paper_link_projection: PRESENT
public_paper_body_verification: PASS
session_specific_state_transfer: COMPLETE
```

## Percentages

Denominator: 8 publication deliverables.

- Task completion: 8/8.
- Developed files: 4/4.
- Validation: 6/6.
- Integration: 4/4.
- Propagation: 4/4.
- Goal activation: 8/8.
- Session consolidation: 4/4.
- Archival readiness: complete for this chat because the sole remaining task has a durable owner, collision boundary, release condition, and repository-native continuation path.

<!-- SV_COST_FIVE_LANE_PUBLIC_RECEIPT:BEGIN -->
## Terminal public-body verification

```text
state: COMPLETE
observed_at: 2026-08-07T23:50:20Z
http_status: 200
content_sha256: sha256:085476333d0ff396ce47d888846a43770d94d5a3ec17e7dfb8b46e8b672386d2
workflow_run_id: 31228347185
workflow_run_attempt: 1
all_required_markers_present: true
claim_released: SV-COST-FIVE-LANE-PUBLIC-BODY-VERIFY-001
issue_closure: StegVerse-Labs/Site#173
```

The deployed paper body returned HTTP 200 and contained every required lane value and bounded-claim marker. The validation claim is released. No unique implementation, publication, propagation, or observation work remains in the originating session.
<!-- SV_COST_FIVE_LANE_PUBLIC_RECEIPT:END -->
