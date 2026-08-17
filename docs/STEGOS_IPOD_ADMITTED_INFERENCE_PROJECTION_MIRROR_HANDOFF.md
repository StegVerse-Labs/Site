# StegOS iPod Admitted Inference Projection Mirror Handoff

Updated: `2026-08-17T00:25:00-05:00`

## Active goal

```text
goal_id: SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298
originating_goal: project the exact merged StegOS admitted-inference browser consumer to the established physical iPod surface without a second non-StegVerse machine or any NON-TV/TVC secret/token
repository: StegVerse-Labs/Site
branch: feat/stegos-ipod-canonical-inference-298
canonical_issue: StegVerse-Labs/Site#298
canonical_source_owner: StegVerse-Labs/StegOS#15
source_merge: 441b72a467753a753f3cb9ac1dbced99f10de884
claim: SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298-20260817
claim_state: CLAIMED_FOR_INTEGRATION
claim_release_condition: merge exact projection, pass Site gates, observe Pages built from merge, then transfer physical execution to StegVerse-Labs/StegOS#15
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
render_production_authority: NONE
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
```

## Authoritative handoffs read

- `docs/SITE_MIRROR_HANDOFF.md`
- `StegVerse-Labs/StegOS/docs/STEGOS_MIRROR_HANDOFF.md`
- `StegVerse-Labs/StegOS/docs/IPOD_ADMITTED_INFERENCE_MIRROR_HANDOFF.md`
- canonical model/runtime and TVC route handoffs were read in the source integration lane before StegOS PR #16.

## Convergence / branch reconciliation

Initial Site PR #299 was created from main `5f9a9a2f...`. Site main then advanced independently to `ddcc370b...` through the Math Solver public-activation observer. The first PR's handoff-orchestrator run also exposed that its branch name did not resolve to a token in the broad root remaining-work inventory. No product collision occurred; pre-work claim validation itself passed.

Rather than force or overwrite concurrent Site state, this canonical replacement branch was created from current main `ddcc370bdf9060b7071e4d2bb212e40f4a9e6718`. The exact product blobs and the admitted-inference claim were reapplied. The branch name deliberately preserves the canonical-inference relationship to the root Site workload while the scoped handoff remains the detailed owner record. PR #299 is superseded by the replacement PR for this branch.

The active VACC PR #263 owns `site:vacc-document-evidence-awareness` and distinct files. It does not overlap this claim's dependency surface `site:stegos-ipod-bootstrap:admitted-inference` or product paths. The machine pre-work claim owns orchestration admission, not this product integration. Older StegOS bootstrap claim #294 is released/merged.

## Exact source projection

Expected upstream Git blob identities:

```text
stegos-bootstrap/index.html                018c97360e7064bf677944b79c1a3ba72dc64f51
stegos-bootstrap/stegos-bootstrap.js       15343c398c168f3d5f8fe6933aaf3073e89dd5c0
stegos-bootstrap/admitted-inference.js     7f4773757a8d1a81ad2a29e0dbed8662e5b89194
stegos-bootstrap/service-worker.js         00de0178f5bfc881b5d3e729734d519035de9901
stegos-bootstrap/manifest.webmanifest       a223ec9454f46d0e9b91d4862f11de701792144a
```

The first-node bootstrap JS and manifest are unchanged. The index, admitted-inference consumer and service worker are exact projections of the merged StegOS source.

## Validation

`scripts/check_stegos_ipod_bootstrap_projection.py` pins all five exact blobs and checks the admitted-inference authority boundaries. It remains wired as the second command in `scripts/check_ecosystem_chat_application.py`.

Validation state:

```text
claim registry static admission: PENDING_REPLACEMENT_PR_VALIDATION
exact projection validator: PENDING_REPLACEMENT_PR_VALIDATION
canonical Site aggregate: PENDING_REPLACEMENT_PR_VALIDATION
Site Handoff Orchestrator: PENDING_REPLACEMENT_PR_VALIDATION
Ecosystem Heartbeat Orchestration: PENDING_REPLACEMENT_PR_VALIDATION
Pages build: PENDING_AFTER_MERGE
physical admitted inference: OUTSIDE_SITE / StegVerse-Labs/StegOS#15
```

Hosted Site CI is source/publication evidence only and does not become activation, credential, route, model or custody authority.

## Completion / archive boundary

This Site lane is complete only when exact projection validation and required Site gates pass, the Site PR merges, Pages reports `built` from the merged projection, the claim is released, and #298 is closed. Publication does not prove physical admitted inference.
