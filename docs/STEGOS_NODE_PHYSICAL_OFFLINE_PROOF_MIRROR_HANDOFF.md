# StegOS Node Physical Offline Proof Mirror Handoff

Updated: 2026-08-24T09:25:00-05:00

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

## Required proof semantics

A local offline proof may be created only when:

```text
registered Node exists
AND canonical local receipt head exists
AND navigator.serviceWorker.controller is present
AND navigator.onLine == false
```

The proof schema is `stegos.node_offline_reload_proof.v1` and must contain the persisted Node/Interlock identity, local receipt head, receipt-count commitment, service-worker control observation, offline observation, and a digest.

It must also state:

```text
network_topology_claimed=false
heartbeat_interlock_observation_verified=false
physical_activation_claimed=false
network_activation_claimed=false
authority_effect=NONE
credential_authority=TV/TVC
```

`navigator.onLine=false` is accepted only as evidence that this browser observed itself offline. It does not prove StegOS Network absence, fragmentation, or any external topology state.

## Export integration

`stegos.node_physical_evidence_export.v1` will include the latest validated local offline proof when one exists. Absence remains `null`; the export must never fabricate offline validation.

## Completion

```text
claim admission: COMPLETE
source implementation: PENDING
source tests: PENDING
hosted Site validation: PENDING
merge: PENDING
public deployment observation after merge: PENDING
real physical offline proof: PENDING
StegOS#23 validation of real exported proof: PENDING
```

Do not mark the physical/offline gate complete from source, CI, or simulated browser state alone.
