# StegOS Node Public Projection Mirror Handoff

Updated: 2026-08-23T17:12:00-05:00

```text
goal_id: SITE-STEGOS-NODE-REGISTRATION-OFFLINE-HISTORY-468
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#468
source_owner: StegVerse-Labs/StegOS#23
branch: feat/stegos-node-evidence-export-468
source_pull_request: StegVerse-Labs/Site#469
source_merge_commit: d615e43222b40834fa599e256428ee4bc33cc1c5
live_observer_pull_request: StegVerse-Labs/Site#472
live_observer_merge_commit: c9bc4249f36397b486ad799158429169de71b9bd
claim: data/session-work-claims.d/site-stegos-node-registration-offline-history-468.json
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
site_authority: PROJECTION_MATERIALIZATION_ONLY
model_output_authority: NONE
github_token_runtime_authority: NONE
render_authority: NONE
```

## Goal

Provide the public/offline-capable StegOS Node projection, direct public contract observer, and a privacy-bounded evidence export that lets a physical Node run feed exact local evidence into StegOS#23 without manual transcription.

## Installed Site surface

`stegos-node/index.html`
- exactly one explicit `Register Device` genesis action;
- Node state, Node ID, local receipt head;
- distinct `Last StegOS Network Sync` and `Last Personal KV Sync`;
- KnowledgeVault availability only after successful registration;
- Device History projection;
- post-registration `Export Node Evidence` control.

The evidence export is `stegos.node_physical_evidence_export.v1` and contains the Node/interlock IDs, binding commitment, local receipt head, separate Personal-KV/Network heads, canonical-chain receipt count, and the receipt-section projection. It explicitly records:

```text
raw_registration_random_bytes_included=false
hardware_attestation_claimed=false
credential_authority=TV/TVC
heartbeat_authority=StegVerse-Labs/.github
authority_effect=NONE
physical_activation_claimed=false
```

The export is unavailable until local state is `REGISTERED`; attempting export without Receipt #1 fails closed.

## Exact public observer

`python scripts/check_stegos_node_projection.py --live-url https://stegverse.org/stegos-node/`

The observer requires HTTPS, HTTP 200 for index/JS/service worker/manifest, and exact canonical source-contract markers. Search-engine presence is neither required nor accepted as deployment proof. Success remains publication evidence only and emits `AUTHORITY_EFFECT=NONE` and `PHYSICAL_NODE_ACTIVATION_CLAIMED=false`.

## Source integration evidence

```text
Site PR #469: MERGED @ d615e43222b40834fa599e256428ee4bc33cc1c5
Site Handoff Orchestrator 32667617880: SUCCESS
Ecosystem Heartbeat Orchestration 32667617897: SUCCESS
Site Bootstrap Validate 32667617883: SUCCESS

Site PR #472: MERGED @ c9bc4249f36397b486ad799158429169de71b9bd
Site Handoff Orchestrator 32669681269: SUCCESS
Ecosystem Heartbeat Orchestration 32669681347: SUCCESS
Site Bootstrap Validate 32669681218: SUCCESS
```

## Authority boundaries

1. Site distributes/materializes local Node code only.
2. Export is evidence transport, not state-transition or execution authority.
3. No browser hardware-attestation claim.
4. HeartBeat authority remains `StegVerse-Labs/.github`.
5. TV/TVC remains sole credential/route authority.
6. Public observation/export do not establish physical multi-node Network activation.
7. Wall-clock export time is descriptive only.

## Completion chain

```text
claim admission: COMPLETE
Site source projection: COMPLETE_MERGED_VALIDATED
exact live observer source: COMPLETE_MERGED_VALIDATED
bounded physical Node evidence export: IMPLEMENTED_ON_BRANCH
bounded export hosted validation: PENDING
Pages/public deployment evidence: PENDING_DIRECT_OBSERVATION
physical Register Device -> Receipt #1: PENDING
physical offline reload/history readability: PENDING
exported physical evidence ingestion by StegOS#23: PENDING
controlled multi-node proof: PENDING
```

Do not release this claim until the deployment gate is directly observed and the physical evidence path has been transferred back to StegOS#23.
