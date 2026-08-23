# StegOS Node Public Projection Mirror Handoff

Updated: 2026-08-23T16:25:00-05:00

```text
goal_id: SITE-STEGOS-NODE-REGISTRATION-OFFLINE-HISTORY-468
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#468
source_owner: StegVerse-Labs/StegOS#23
branch: feat/stegos-node-registration-offline-history-468
claim: data/session-work-claims.d/site-stegos-node-registration-offline-history-468.json
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
site_authority: PROJECTION_MATERIALIZATION_ONLY
model_output_authority: NONE
github_token_runtime_authority: NONE
render_authority: NONE
```

## Goal

Project the already-merged StegOS Node genesis, dual-interlock sync, and offline Device Node history contracts to a public/offline-capable Site surface without creating new credential, HeartBeat, device-continuity, model, or external execution authority.

## Source lineage

- StegOS Node/Manifold core: PR #24 / `09de722a4cf34fada6f58d8e1da52cd35ef5b672`
- Canonical HeartBeat interlock adapter: PR #25 / `14f3acddd61260c54ba8b3cbc6826d5fc4c6467d`
- Register Device genesis backend: PR #26 / `927595eff395e68a1af37557d5af4acbe2c20048`
- Personal KV + Network dual sync: PR #27 / `5e2393e238a4ce4f02a13bee1e315cf44bf69e25`
- Offline Device Node history: PR #28 / `942adfe9dd3f7768c09f4e979938d5aa9db99b09`

## Installed Site surface

`stegos-node/index.html`
- exactly one explicit `Register Device` action;
- Node state, Node ID, local receipt head;
- distinct `Last StegOS Network Sync` and `Last Personal KV Sync`;
- KnowledgeVault availability only after successful registration;
- Device History projection.

`stegos-node/stegos-node.js`
- generates a browser-local random registration value, hashes it to a device-binding commitment, then discards the raw random bytes;
- persists only the commitment-derived Node projection and canonical Receipt #1;
- derives distinct Node and Interlock IDs;
- creates/validates `stegos.node_handoff_receipt.v1` Receipt #1 with `UNREGISTERED -> REGISTERED`, `continuity_parent=GENESIS`, `authority_effect=NONE`, and TV/TVC credential authority;
- does not read serial numbers, user-agent identity, Apple account data, network hardware identifiers, or the separately owned `stegdevice-*` continuity root;
- keeps Personal KV and Network sync metadata distinct;
- renders sections only as filtered views of one local receipt chain;
- requires no current Network presence to render already-local history.

`stegos-node/service-worker.js`
- caches only the bounded Node shell for offline loading;
- grants no synchronization, HeartBeat, credential, or execution authority.

`manifest.webmanifest`
- standalone bounded PWA metadata.

## Authority and continuity boundaries

1. Site distributes/materializes the local Node code only.
2. This surface does not replace StegOS#19 device-continuity authority and does not claim browser hardware attestation.
3. HeartBeat remains `StegVerse-Labs/.github`; this projection does not generate HeartBeat references or observations.
4. TV/TVC remains sole credential/route authority.
5. Local Receipt #1 is evidence of this Node genesis contract; it is not evidence of physical multi-node Network activation.
6. Missing Personal KV or Network sync observations remain visibly absent rather than fabricated.
7. Wall-clock metadata is descriptive; receipt order is the local causal order.
8. Offline source capability is not yet physical offline validation.

## Validation

Repository-native checks:
- `scripts/check_stegos_node_projection.py`
- `tests/test_stegos_node_projection.py`
- canonical Site pre-work claim validation/orchestration

## Completion chain

```text
claim admission: COMPLETE
Site source projection: IMPLEMENTED_ON_BRANCH
repository validation: PENDING HOSTED EVIDENCE
merge: PENDING
Pages/public deployment evidence: PENDING
physical Register Device -> Receipt #1: PENDING
physical offline reload/history readability: PENDING
transfer to StegOS#23 multi-node proof: PENDING
```

Do not equate branch source, CI, merge, or Pages build with physical StegOS Network activation.
