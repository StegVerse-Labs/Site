# StegOS Node Public Projection Mirror Handoff

Updated: 2026-08-23T17:07:00-05:00

```text
goal_id: SITE-STEGOS-NODE-REGISTRATION-OFFLINE-HISTORY-468
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#468
source_owner: StegVerse-Labs/StegOS#23
branch: feat/stegos-node-live-observer-468
source_pull_request: StegVerse-Labs/Site#469
source_merge_commit: d615e43222b40834fa599e256428ee4bc33cc1c5
claim: data/session-work-claims.d/site-stegos-node-registration-offline-history-468.json
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
site_authority: PROJECTION_MATERIALIZATION_ONLY
model_output_authority: NONE
github_token_runtime_authority: NONE
render_authority: NONE
```

## Goal

Project the merged StegOS Node genesis, dual-interlock sync, and offline Device Node history contracts to a public/offline-capable Site surface, then prove the deployed surface by exact credential-free contract observation without promoting publication evidence to physical Node or Network activation.

## Installed Site surface

`stegos-node/index.html`
- exactly one explicit `Register Device` action;
- Node state, Node ID, local receipt head;
- distinct `Last StegOS Network Sync` and `Last Personal KV Sync`;
- KnowledgeVault availability only after successful registration;
- Device History projection.

`stegos-node/stegos-node.js`
- browser-local random registration value is hashed to a device-binding commitment and raw random bytes are discarded;
- persists only commitment-derived Node projection and canonical Receipt #1;
- distinct Node and Interlock IDs;
- `UNREGISTERED -> REGISTERED`, `continuity_parent=GENESIS`, `authority_effect=NONE`, TV/TVC credential authority;
- no serial number, user-agent identity, Apple account data, network hardware identifier, or separately owned `stegdevice-*` continuity root;
- separate Personal KV and Network sync metadata;
- section views are filtered views of one receipt chain;
- already-local history requires no current Network presence.

`stegos-node/service-worker.js`
- caches only the bounded Node shell for offline loading;
- grants no synchronization, HeartBeat, credential, or execution authority.

## Source integration evidence

```text
Site PR #469: MERGED
merge_commit: d615e43222b40834fa599e256428ee4bc33cc1c5
Site Handoff Orchestrator 32667617880: SUCCESS
Ecosystem Heartbeat Orchestration 32667617897: SUCCESS
Site Bootstrap Validate 32667617883: SUCCESS
```

These are source/integration evidence only.

## Exact public observer

The active claim now continues as validation rather than implementation. `scripts/check_stegos_node_projection.py` supports:

```text
python scripts/check_stegos_node_projection.py --live-url https://stegverse.org/stegos-node/
```

The live path is accepted only when:
- the URL is absolute HTTPS;
- the exact public index returns HTTP 200;
- the public JavaScript and service worker return HTTP 200;
- the public manifest returns HTTP 200;
- the public objects contain the same canonical Node/Receipt #1/offline-history markers required by the local source contract;
- prohibited identity/token/runtime-authority markers remain absent.

Success emits `STEGOS_NODE_PUBLIC_OBSERVATION_PASS`, `AUTHORITY_EFFECT=NONE`, and `PHYSICAL_NODE_ACTIVATION_CLAIMED=false`.

Search-engine absence is neither deployment PASS nor deployment FAIL. Only direct exact-URL observation satisfies the deployment gate.

## Authority boundaries

1. Site distributes/materializes local Node code only.
2. No browser hardware-attestation claim.
3. HeartBeat authority remains `StegVerse-Labs/.github`.
4. TV/TVC remains sole credential/route authority.
5. Public observation does not establish Receipt #1 on a physical device.
6. Public observation does not establish offline persistence or multi-node Network presence.
7. Wall-clock metadata remains descriptive; receipt relationships remain causal order.

## Completion chain

```text
claim admission: COMPLETE
Site source projection: COMPLETE_MERGED
repository hosted validation: PASS
merge: COMPLETE
exact live observer source: IMPLEMENTED_ON_BRANCH
exact live observer hosted validation: PENDING
Pages/public deployment evidence: PENDING_DIRECT_OBSERVATION
physical Register Device -> Receipt #1: PENDING
physical offline reload/history readability: PENDING
transfer to StegOS#23 multi-node proof: PENDING
```

The claim remains active until direct deployed observation succeeds and continuation returns to StegOS#23.
