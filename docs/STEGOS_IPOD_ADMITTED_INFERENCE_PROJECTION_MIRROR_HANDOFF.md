# StegOS iPod Admitted Inference Projection Mirror Handoff

Updated: `2026-08-20T09:34:00-05:00`

## Active goal

```text
goal_id: SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#298 / REOPENED_FOR_UPSTREAM_DEVICE_LOCAL_REVISION
canonical_source_owner: StegVerse-Labs/StegOS#15
source_commit: f52ca9e1fac332a0ff6e79fb4a00579d1bbc95a9
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
render_production_authority: NONE
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
claim_registry_collision: data/session-work-claims.json remains owned by active Site#268 work and is NOT mutated by this lane
```

The prior #298 publication remains valid historical evidence for the old browser bundle, but it is not the current device-local source revision. The current source owner has removed the second-machine endpoint gap, added canonical browser model execution, portable TVC route evaluation, fenced device-local task execution, bounded automatic admission, and a Copy Text control for exported evidence bundles.

## Exact current projection

The current Site projection must match these StegOS blobs exactly:

```text
stegos-bootstrap/index.html                         561e21d38df310aee838716ab9f2a4a6175485d5
stegos-bootstrap/stegos-bootstrap.js                15343c398c168f3d5f8fe6933aaf3073e89dd5c0
stegos-bootstrap/admitted-inference.js              1cac8bc4d5a13a6596cd7f68b01e3a93be7536f0
stegos-bootstrap/device-local-autostart.js           d2aaffa033003cb6b031dbf30312c6104de989b2
stegos-bootstrap/service-worker.js                  3cba6ca48c8b093d0f0baa48aff000a544e93cc6
stegos-bootstrap/stegverse-reference-model.js        bd8e7553b61425386f6cf65db4766b952c148ed4
stegos-bootstrap/tvc-sovereign-local-model-route.js  3ca841310b904c2e09390512043f30f301976b1d
stegos-bootstrap/manifest.webmanifest                a223ec9454f46d0e9b91d4862f11de701792144a
```

Canonical upstream ownership remains split without duplication:

```text
browser reference model owner: StegVerse-002/micro-node-runtime@ce142a56bf4ac14c2fb075c78bcc413a02bc0f5e
browser model canonical blob: bd8e7553b61425386f6cf65db4766b952c148ed4
portable route authority owner: StegVerse-Labs/TVC@cf673ced2b0f13d0c2ef4fa581e477a660771a75
portable route canonical blob: 3ca841310b904c2e09390512043f30f301976b1d
physical consumer owner: StegVerse-Labs/StegOS#15
```

## Installed behavior required on the public path

`https://stegverse.org/stegos-bootstrap/local-model` is not a hosted model endpoint. The service worker intercepts the exact same-origin path on the physical node and executes the canonical browser reference model locally. The local branch must never call network `fetch(event.request)`.

Required behavior:

- service-worker import of the exact canonical model and TVC evaluator projections;
- `/canonical-evidence` produces local model proof plus TVC `ROUTE_ADMITTED` evidence;
- `/v1/chat/completions` executes on-device reference-model inference;
- every model execution performs an atomic device-local claim, monotonically increasing fence, terminal receipt, reconstruction receipt, and replay before success is returned;
- device-local task authority is constrained to `DEVICE_LOCAL_INFERENCE_ONLY` and does not claim global WorkerCoordinator/carrier authority;
- response header `X-StegVerse-Execution: SERVICE_WORKER_LOCAL_INTERCEPT` proves the device-local transport branch;
- automatic admission waits for node establishment and service-worker update, then retries within a bounded 60-second window;
- `credentials: omit`; no Authorization/Bearer/provider/GitHub/private-key credential path;
- `credential_requirement=NONE`, `github_token_required=false`, `third_party_execution_platform_required=false`;
- model output and Site projection have `authority_effect=NONE`;
- Show Evidence Bundle renders the exported JSON and enables a `Copy Text` button below the bundle;
- Copy Text uses `navigator.clipboard.writeText` with an iOS-compatible `document.execCommand("copy")` fallback.

## Physical one-task acceptance evidence

The physical node evidence supplied on 2026-08-20 satisfies the previously pending acceptance boundary:

```text
journal_replay.state: PASS
journal_replay.entries: 7
journal_replay.tail_sha256: 41210db81ee8f2aefcc235856e6a2968ab43e418e245daafc96da10aab996bf8
device task claim: stegos.web_task_claim_receipt.v1
fencing_token: 1
terminal state: COMPLETED
reconstruction: PASS
same_execution: true
admitted inference receipt: stegos.web_admitted_inference_receipt.v1
usage measured: true
prompt_tokens: 8
completion_tokens: 64
total_tokens: 72
latency_ms: 2
credential_authority: TV/TVC
credential_requirement: NONE
github_token_required: false
external_non_stegverse_machine_used: false
```

This is physical runtime evidence, not hosted CI evidence. The historical service-activation receipt inside the journal records fail-closed optional capabilities at its own earlier sequence; later journal entries 4-7 establish the subsequently admitted and executed device-local inference state.

## Validation

Canonical Site validator:

`./scripts/check_stegos_ipod_bootstrap_projection.py`

Current validator requires exact Git blob identity for all eight public assets plus no-network local interception, bounded automatic admission, device-local fenced task execution, authority neutrality, prohibited credential markers, and the Copy Text UI/clipboard fallback contract.

Hosted validation is source/publication evidence only. A workflow that does not execute a validation step is not a pass. Pages publication is also not the same thing as the physical inference evidence above.

## Collision boundary

Do not modify `data/session-work-claims.json` while the active Site#268 owner retains that coordination surface. The reopened #298 revision is confined to `stegos-bootstrap/**`, its exact projection validator, this scoped handoff, and issue evidence.

## Release condition

```text
exact current projection installed on Site main
-> projection validator PASS
-> exact Pages build from that merge observed
-> public current assets match the expected blobs
-> Site #298 closes again for this source revision
```

The physical one-task acceptance condition is now satisfied by the device-generated journal described above. Site remains transport/materialization only.

## Completion accounting

```text
old #298 publication: COMPLETE_HISTORICAL_REVISION
current source revision exact file set: 8 files
current projection source: PENDING_THIS_TREE_MERGE
current validator: INSTALLED_IN_THIS_TREE
current source/publication validation: PENDING
current Pages build: PENDING
physical one-task acceptance: PASS
physical admitted inference: PASS
scaffolding/stubs: 0
```

DO NOT ARCHIVE this reopened projection lane until current public materialization is proven and #298 is reclosed.
