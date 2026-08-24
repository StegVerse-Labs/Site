# StegOS Node Public Projection Mirror Handoff

Updated: 2026-08-24T09:15:00-05:00

```text
goal_id: SITE-STEGOS-NODE-REGISTRATION-OFFLINE-HISTORY-468
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#468
source_owner: StegVerse-Labs/StegOS#23
branch: feat/stegos-node-independent-public-observer-468
source_pull_request: StegVerse-Labs/Site#469
source_merge_commit: d615e43222b40834fa599e256428ee4bc33cc1c5
live_observer_pull_request: StegVerse-Labs/Site#472
live_observer_merge_commit: c9bc4249f36397b486ad799158429169de71b9bd
evidence_export_pull_request: StegVerse-Labs/Site#475
evidence_export_merge_commit: b445cd35818510dd0eee81884b56ea8d549fe518
hosted_live_url_pull_request: StegVerse-Labs/Site#478
hosted_live_url_merge_commit: 72a13de33de7a9811194f7095223e61882fc8db6
claim: data/session-work-claims.d/site-stegos-node-registration-offline-history-468.json
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
site_authority: PROJECTION_MATERIALIZATION_ONLY
model_output_authority: NONE
github_token_runtime_authority: NONE
render_authority: NONE
```

## Goal

Provide the public/offline-capable StegOS Node projection, exact public contract observation, privacy-bounded physical evidence export, and an independently inspectable hosted observation receipt so deployment evidence does not depend on search indexing or an opaque workflow_run lookup.

## Installed Site surface

`stegos-node/index.html`
- exactly one explicit `Register Device` genesis action;
- Node state, Node ID, local receipt head;
- distinct `Last StegOS Network Sync` and `Last Personal KV Sync`;
- KnowledgeVault availability only after successful registration;
- Device History projection;
- post-registration `Export Node Evidence` control.

The evidence export is `stegos.node_physical_evidence_export.v1`. It carries commitment-derived Node/interlock identity, local receipt head, separate Personal-KV/Network heads, canonical-chain receipt projection, and explicit non-authority markers. It excludes raw registration random bytes and does not claim hardware attestation or activation.

## Exact public observer

Canonical command:

```text
python scripts/check_stegos_node_projection.py --live-url https://stegverse.org/stegos-node/
```

The observer requires HTTPS, HTTP 200 for index/JS/service worker/manifest, and exact canonical source-contract markers. Search-engine presence is neither required nor accepted as deployment proof.

PR #478 merged the observer into Site's existing hosted `live-url` task. Because the connector cannot directly enumerate the resulting post-merge `workflow_run`, this lane adds a second independently inspectable workflow:

```text
.github/workflows/stegos-node-public-observation.yml
```

That workflow:
- runs without credentials;
- observes the exact public URL;
- requires the same task-specific validator to pass;
- writes `stegos.node_public_observation_receipt.v1`;
- records `authority_effect=NONE`;
- records `physical_node_activation_claimed=false` and `network_activation_claimed=false`;
- uploads the text observation plus JSON receipt as an artifact.

A successful run satisfies only the direct public deployment observation gate. It does not satisfy physical Node, offline, HeartBeat/interlock, multi-node, or activation gates.

## Source integration evidence

```text
Site PR #469: MERGED @ d615e43222b40834fa599e256428ee4bc33cc1c5
Site PR #472: MERGED @ c9bc4249f36397b486ad799158429169de71b9bd
Site PR #475: MERGED @ b445cd35818510dd0eee81884b56ea8d549fe518
Site PR #478: MERGED @ 72a13de33de7a9811194f7095223e61882fc8db6
associated claim/orchestration/bootstrap gates: SUCCESS
independent public-observation workflow: IMPLEMENTED_ON_BRANCH
independent public-observation hosted result: PENDING
```

## Authority boundaries

1. Site distributes/materializes local Node code only.
2. Export and observation receipts are evidence transport, not state-transition or execution authority.
3. No browser hardware-attestation claim.
4. HeartBeat authority remains `StegVerse-Labs/.github`.
5. TV/TVC remains sole credential/route authority.
6. Public observation/export do not establish physical multi-node Network activation.
7. Wall-clock metadata is descriptive only.

## Completion chain

```text
claim admission: COMPLETE
Site source projection: COMPLETE_MERGED_VALIDATED
exact live observer source: COMPLETE_MERGED_VALIDATED
bounded physical Node evidence export: COMPLETE_MERGED_VALIDATED
hosted live-url task integration: COMPLETE_MERGED_VALIDATED
independent hosted public-observation workflow: IMPLEMENTED_ON_BRANCH
Pages/public deployment evidence: PENDING_DIRECT_OBSERVATION
physical Register Device -> Receipt #1: PENDING
physical offline reload/history readability: PENDING
exported physical evidence ingestion by StegOS#23: SOURCE_READY_PHYSICAL_INPUT_PENDING
controlled multi-node proof: SOURCE_READY_PHYSICAL_INPUT_PENDING
```

Do not release this claim until direct deployed observation succeeds and continuation returns to StegOS#23 for the real physical proof sequence.
