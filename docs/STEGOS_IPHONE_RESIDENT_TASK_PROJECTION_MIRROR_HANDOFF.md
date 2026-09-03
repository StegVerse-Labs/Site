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
claim: RELEASED
exact projection: MERGED_EXACT_UPSTREAM_BLOBS
validation: PASS_EXACT_BLOB_AND_JAVASCRIPT_SYNTAX
merge: PR #940 / 13baddb05104729fb85c41e029c675add07a4107
publication source: RELEASED
physical iPhone execution: NOT OBSERVED
```


## Exact projection validation — 2026-09-02

Validated branch bytes:

```text
stegos-bootstrap/service-worker.js
  git blob: 0bf8c8df1ae678bc73170978f6c6fdae7b9341f1
  matches StegOS merged source: true
  JavaScript syntax: PASS

stegos-bootstrap/external-resident-task.js
  git blob: 87dbfdf156224df80ab5f24ae263ed13cb7577c9
  matches StegOS merged source: true
  JavaScript syntax: PASS
```

The projection contains no Site-local reimplementation. Runtime execution remains unobserved.


## Cumulative Site application validator integration

The canonical existing `scripts/check_stegos_ipod_bootstrap_projection.py` remains the cumulative StegOS public-surface guard. Issue #938 advances it rather than bypassing it:

- service-worker expected blob advances from the historical v4 projection to merged StegOS v6 blob `0bf8c8df1ae678bc73170978f6c6fdae7b9341f1`;
- `stegos-bootstrap/external-resident-task.js` is required at exact blob `87dbfdf156224df80ab5f24ae263ed13cb7577c9`;
- all prior continuity, admitted-inference, local-model, credential, and fail-closed checks remain;
- the new SV001 profile/transition/endpoint and non-promotion authority markers are additionally required.


## Release reconciliation — 2026-09-03

The source-state block above was stale after the implementation merged.

Canonical release:

```text
claim: SITE-STEGOS-IPHONE-RESIDENT-TASK-938-20260902
state: RELEASED
Site PR: #940
release commit: 13baddb05104729fb85c41e029c675add07a4107
execution surface: CURRENT_USER_IPHONE
second_user_device_required: false
external_non_stegverse_machine_required: false
```

This capability is the canonical answer when a bounded StegOS task must execute on the current iPhone rather than requiring a second user-operated computer.

Remaining runtime predicates are not a source-implementation gap: an exact externally admitted task envelope, its applicable WorkerCoordinator admission/claim/fence and TV/TVC lease, current-iPhone consumption, and the task-specific terminal/reconstruction receipts must all refer to the same execution.

Do not substitute the separate Service-Gateway resident-request chain as a mandatory second-machine requirement for tasks that are admitted by this iPhone resident-task adapter.
