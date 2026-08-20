# StegOS iPod Admitted Inference Projection Mirror Handoff

Updated: `2026-08-20T07:04:00-05:00`

## Active goal

```text
goal_id: SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#298 / OPEN
canonical_source_owner: StegVerse-Labs/StegOS#15
source_commit: ec41956ac6fd114468a302aaf1d0eaff884ab80e
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
render_production_authority: NONE
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
claim_registry_collision: data/session-work-claims.json remains owned by active Site#268 work and is NOT mutated by this lane
```

## Current source revision

StegOS now wraps every admitted on-device `/v1/chat/completions` request in a bounded device-local task lifecycle before the result is returned. The service worker performs atomic local claim + monotonic fence, writes claim/terminal/reconstruction receipts into the established StegOS journal, requires replay PASS, and returns `stegos.device_task_execution_proof.v1` only after same-execution reconstruction.

This does not transfer `.github` global WorkerCoordinator authority into Site or the browser. The scope is `DEVICE_LOCAL_INFERENCE_ONLY`; model authority remains `StegVerse-002/micro-node-runtime`; TVC/TV remains route and credential authority; Site remains transport materialization only.

## Exact projection

The Site public bundle must match these current StegOS blobs:

```text
stegos-bootstrap/index.html                         fc64cb4a2ef5a4db5dbfe2e5222fbd05b986e879
stegos-bootstrap/stegos-bootstrap.js                15343c398c168f3d5f8fe6933aaf3073e89dd5c0
stegos-bootstrap/admitted-inference.js              1cac8bc4d5a13a6596cd7f68b01e3a93be7536f0
stegos-bootstrap/device-local-autostart.js           d2aaffa033003cb6b031dbf30312c6104de989b2
stegos-bootstrap/service-worker.js                  3cba6ca48c8b093d0f0baa48aff000a544e93cc6
stegos-bootstrap/stegverse-reference-model.js        bd8e7553b61425386f6cf65db4766b952c148ed4
stegos-bootstrap/tvc-sovereign-local-model-route.js  3ca841310b904c2e09390512043f30f301976b1d
stegos-bootstrap/manifest.webmanifest                a223ec9454f46d0e9b91d4862f11de701792144a
```

Canonical upstream ownership remains:

```text
browser reference model: StegVerse-002/micro-node-runtime@ce142a56bf4ac14c2fb075c78bcc413a02bc0f5e
portable TVC evaluator: StegVerse-Labs/TVC@cf673ced2b0f13d0c2ef4fa581e477a660771a75
physical task/inference consumer: StegVerse-Labs/StegOS@ec41956ac6fd114468a302aaf1d0eaff884ab80e / issue #15
```

## Required public behavior

The same-origin `/stegos-bootstrap/local-model` path remains device-local service-worker execution, not a hosted model endpoint. The service worker must:

- intercept local model traffic without network fallback;
- admit the canonical model/TVC route;
- require an established StegVerse node id;
- atomically persist local task generation + task claim;
- use the new generation as the task fencing token;
- explicitly retain `global_workercoordinator_authority=false` and `carrier_granted_authority=false`;
- append task claim, terminal, and reconstruction receipts to the existing journal;
- replay the journal before successful result return;
- return `X-StegVerse-Task-Control: DEVICE_LOCAL_FENCED` and `stegos.device_task_execution_proof.v1`;
- fail closed on stale fence, execution failure, or replay failure;
- require no GitHub/provider credential and no second non-StegVerse machine.

## Validation

Canonical Site validator:

`./scripts/check_stegos_ipod_bootstrap_projection.py`

The current validator pins all eight public Git blobs to StegOS `ec41956...` and additionally requires the device-task claim/fence/terminal/reconstruction markers and verifies that local chat completions call `executeDeviceTask(body)`.

Hosted CI is source/publication evidence only. A workflow that never executes its validation step is not a pass, and GitHub-hosted Actions has no StegVerse runtime authority.

## Collision boundary

Do not modify `data/session-work-claims.json` while active Site#268 owns that coordination surface. This lane is confined to the exact `stegos-bootstrap/**` projection, its validator, this scoped handoff, and issue evidence.

## Release condition

```text
exact current projection installed on Site main
-> exact blob validation PASS
-> public/Pages materialization of this revision observed
-> physical StegOS node issues one admitted inference task
-> returned stegos.device_task_execution_proof.v1 state=COMPLETED
-> reconstruction_state=PASS and same_execution=true
-> physical local journal replay PASS
```

Source/publication does not equal physical activation. The binary operational acceptance boundary is the physical one-task run.

## Completion accounting

```text
current StegOS task-control source: BUILT / ec41956...
current Site projection source: PENDING_THIS_ATOMIC_COMMIT
current exact projection validator: PENDING_THIS_ATOMIC_COMMIT
current public materialization: PENDING
physical one-task execution: PENDING_STEGOS#15
scaffolding/stubs: 0
archive_state: NOT_READY
```
