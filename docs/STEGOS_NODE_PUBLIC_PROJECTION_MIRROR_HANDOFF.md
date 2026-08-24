# StegOS Node Public Projection Mirror Handoff

Updated: 2026-08-24T09:20:00-05:00

```text
goal_id: SITE-STEGOS-NODE-REGISTRATION-OFFLINE-HISTORY-468
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#468
source_owner: StegVerse-Labs/StegOS#23
branch: main
source_pull_request: StegVerse-Labs/Site#469
source_merge_commit: d615e43222b40834fa599e256428ee4bc33cc1c5
live_observer_pull_request: StegVerse-Labs/Site#472
live_observer_merge_commit: c9bc4249f36397b486ad799158429169de71b9bd
evidence_export_pull_request: StegVerse-Labs/Site#475
evidence_export_merge_commit: b445cd35818510dd0eee81884b56ea8d549fe518
hosted_live_url_pull_request: StegVerse-Labs/Site#478
hosted_live_url_merge_commit: 72a13de33de7a9811194f7095223e61882fc8db6
independent_observer_pull_request: StegVerse-Labs/Site#479
independent_observer_merge_commit: e1008f923493121967a984864c5212315dff10e8
claim: data/session-work-claims.d/site-stegos-node-registration-offline-history-468.json
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
site_authority: PROJECTION_MATERIALIZATION_ONLY
model_output_authority: NONE
github_token_runtime_authority: NONE
render_authority: NONE
```

## Goal

Provide the public/offline-capable StegOS Node projection, exact public contract observation, privacy-bounded physical evidence export, and independently inspectable hosted deployment evidence before transferring the remaining physical proof back to StegOS#23.

## Installed Site surface

`stegos-node/index.html`
- exactly one explicit `Register Device` genesis action;
- Node state, Node ID, local receipt head;
- distinct `Last StegOS Network Sync` and `Last Personal KV Sync`;
- KnowledgeVault availability only after successful registration;
- Device History projection;
- post-registration `Export Node Evidence` control.

The evidence export is `stegos.node_physical_evidence_export.v1`. It carries commitment-derived Node/interlock identity, local receipt head, separate Personal-KV/Network heads, canonical-chain receipt projection, and explicit non-authority markers. It excludes raw registration random bytes and does not claim hardware attestation or activation.

## Direct public deployment observation — PASS

Canonical command:

```text
python scripts/check_stegos_node_projection.py --live-url https://stegverse.org/stegos-node/
```

The independent hosted observer ran from GitHub-hosted infrastructure and directly observed the exact public contract.

```text
workflow: StegOS Node Public Observation
run: 32738000838
job: 97465413849 SUCCESS
observed URL: https://stegverse.org/stegos-node/
STEGOS_NODE_PROJECTION_PASS
STEGOS_NODE_PUBLIC_OBSERVATION_PASS
AUTHORITY_EFFECT=NONE
PHYSICAL_NODE_ACTIVATION_CLAIMED=false
artifact: 9523975844
artifact zip sha256: 18c7344ff47a861c1e786feb61d261e236ed2dbb17e451d416b10cdf09fdc224
```

The workflow wrote `stegos.node_public_observation_receipt.v1` and uploaded both raw observer output and the JSON receipt. This satisfies the public deployment observation gate only. It does not satisfy physical Node, offline, HeartBeat/interlock, multi-node, or activation gates.

## Source integration evidence

```text
Site PR #469: MERGED @ d615e43222b40834fa599e256428ee4bc33cc1c5
Site PR #472: MERGED @ c9bc4249f36397b486ad799158429169de71b9bd
Site PR #475: MERGED @ b445cd35818510dd0eee81884b56ea8d549fe518
Site PR #478: MERGED @ 72a13de33de7a9811194f7095223e61882fc8db6
Site PR #479: MERGED @ e1008f923493121967a984864c5212315dff10e8
Site #479 independent observer: 32738000838 SUCCESS
Site Handoff Orchestrator: 32738000467 SUCCESS
Ecosystem Heartbeat Orchestration: 32738000501 SUCCESS
Site Bootstrap Validate: 32738000559 SUCCESS
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
independent hosted public-observation workflow: COMPLETE_MERGED_VALIDATED
Pages/public deployment evidence: PASS_DIRECT_OBSERVATION
physical Register Device -> Receipt #1: TRANSFERRED_TO_STEGOS_23
physical offline reload/history readability: TRANSFERRED_TO_STEGOS_23
exported physical evidence ingestion by StegOS#23: SOURCE_READY_PHYSICAL_INPUT_PENDING
controlled multi-node proof: SOURCE_READY_PHYSICAL_INPUT_PENDING
```

Site has satisfied its projection and deployment-evidence responsibilities. Remaining work belongs to StegVerse-Labs/StegOS#23 and must not be represented as Site activation evidence.
