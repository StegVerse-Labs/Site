# StegOS iPhone Resident Task Projection Mirror Handoff

Updated: 2026-09-02
Repository: `StegVerse-Labs/Site`
Issue: #938
Claim: `SITE-STEGOS-IPHONE-RESIDENT-TASK-938-20260902`

## Goal

Project the exact merged StegOS externally admitted resident-task adapter to the public `stegverse.org/stegos-bootstrap/` surface so the current iPhone can execute a bounded resident task without any second user-operated machine.

Canonical source owner:
- `StegVerse-Labs/StegOS#162`
- merge `835372a69af23dc73b6f75591ced6281c43ffa8d`

Exact source files:
- `StegOS:mobile/web-bootstrap/service-worker.js` blob `0bf8c8df1ae678bc73170978f6c6fdae7b9341f1`
- `StegOS:mobile/web-bootstrap/external-resident-task.js` blob `87dbfdf156224df80ab5f24ae263ed13cb7577c9`

Destination:
- `stegos-bootstrap/service-worker.js`
- `stegos-bootstrap/external-resident-task.js`

## Authority boundary

```text
Site role: MATERIALIZATION / PUBLICATION ONLY
execution surface: CURRENT_USER_IPHONE
global_workercoordinator_authority: false
external_claim_promoted_to_browser_authority: false
carrier_granted_authority: false
credential_authority: TV/TVC
github_token_runtime_authority: NONE
second_user_device_required: false
external_non_stegverse_machine_required: false
```

Site does not issue WorkerCoordinator claims/fences, TVC leases, credentials, execution authority, or runtime truth.

## Runtime distinction

Publication of the adapter is not SV001 execution.

Authentic runtime completion requires:
1. an external WorkerCoordinator admission/claim/fence;
2. a valid TV/TVC single-cycle SV001 lease;
3. the current iPhone to consume the envelope through the service worker;
4. `SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED`;
5. terminal + reconstruction receipts with `same_execution=true`;
6. downstream Master Records and SV002 evidence independently.

## Source state

```text
claim: ACTIVE
exact projection: PENDING
validation: PENDING
merge: PENDING
publication: PENDING
physical iPhone execution: NOT OBSERVED
```
