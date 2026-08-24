# StegOS Node Physical Offline Proof Mirror Handoff

Updated: 2026-08-24T09:30:00-05:00

```text
goal_id: SITE-STEGOS-NODE-PHYSICAL-OFFLINE-PROOF-480
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#480
source_owner: StegVerse-Labs/StegOS#23
branch: feat/stegos-node-physical-offline-proof-480
claim: data/session-work-claims.d/site-stegos-node-physical-offline-proof-480.json
credential_authority: TV/TVC
heartbeat_authority: StegVerse-Labs/.github
site_authority: PROJECTION_MATERIALIZATION_ONLY
authority_effect: NONE
```

## Goal

Make the real-device `Register Device` + offline-reload portion of StegOS#23 machine-recordable on the device itself.

## Implemented proof semantics

A local offline proof is created only when:

```text
registered Node exists
AND canonical local receipt head exists
AND navigator.serviceWorker.controller is present
AND navigator.onLine == false
```

`stegos-node/stegos-node.js` now persists `stegos.node_offline_reload_proof.v1` in the existing local IndexedDB metadata store. The proof binds:
- Node ID;
- Interlock ID;
- persisted local receipt head;
- canonical-chain receipt count;
- service-worker-controlled observation;
- browser-offline observation;
- descriptive observation time;
- deterministic proof digest.

It explicitly states:

```text
current_network_required=false
network_topology_claimed=false
heartbeat_interlock_observation_verified=false
physical_activation_claimed=false
network_activation_claimed=false
authority_effect=NONE
credential_authority=TV/TVC
```

`navigator.onLine=false` is accepted only as evidence that this browser observed itself offline. It does not prove StegOS Network absence, fragmentation, or any external topology state.

The runtime validates proof schema, invariants, Node/Interlock identity, local receipt head, receipt count, and digest before the proof can be exported.

## Export integration

`stegos.node_physical_evidence_export.v1` now includes:

```text
offline_reload_proof: <validated proof or null>
network_activation_claimed: false
```

Absence remains `null`; the export never fabricates offline validation.

The Node UI exposes `Offline Reload Proof: Not yet observed | Recorded` as a human projection only.

## Source/deployment validation sequencing

`scripts/check_stegos_node_projection.py` always requires the new offline-proof source contract locally. `--require-offline-proof` additionally requires those markers from the exact deployed public route.

`.github/workflows/stegos-node-public-observation.yml` is staged to avoid false PR failure:
- pull requests validate the source contract only;
- push/main and manual observation retry the exact public URL and require the offline-proof capability after deployment;
- receipt remains non-authorizing and distinguishes source validation from deployed observation.

## Completion

```text
claim admission: COMPLETE
source implementation: COMPLETE_ON_BRANCH
source contract tests: INSTALLED
source/live validator extension: COMPLETE_ON_BRANCH
hosted observer deployment sequencing: COMPLETE_ON_BRANCH
hosted Site validation: PENDING
merge: PENDING
public offline-proof capability observation after merge: PENDING
real physical Receipt #1: PENDING
real physical offline reload proof: PENDING
real physical evidence export: PENDING
StegOS#23 validation of real exported proof: PENDING
```

Do not mark the physical/offline gate complete from source, CI, deployed capability, or simulated browser state alone.
