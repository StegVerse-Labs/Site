# StegOS iPod Admitted Inference Projection Mirror Handoff

Updated: `2026-08-20T06:11:00-05:00`

## Active goal

```text
goal_id: SITE-STEGOS-IPOD-ADMITTED-INFERENCE-298
repository: StegVerse-Labs/Site
canonical_issue: StegVerse-Labs/Site#298 / REOPENED_FOR_UPSTREAM_DEVICE_LOCAL_REVISION
canonical_source_owner: StegVerse-Labs/StegOS#15
source_commit: 2dac60b43c4f7581666907569fbbed0c589e9146
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
render_production_authority: NONE
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
claim_registry_collision: data/session-work-claims.json remains owned by active Site#268 work and is NOT mutated by this lane
```

The prior #298 publication at Site merge `1f5ab3acde796d2787edf0493c19e193ca72eda4` / Pages build `1156543676` remains valid historical evidence for the old browser bundle, but it is not the current device-local source revision. The source owner has since removed the second-machine endpoint gap by adding a canonical browser model target, portable TVC route evaluation, service-worker local transport, and bounded automatic admission.

## Exact current projection

The current Site projection must match these StegOS blobs exactly:

```text
stegos-bootstrap/index.html                         fc64cb4a2ef5a4db5dbfe2e5222fbd05b986e879
stegos-bootstrap/stegos-bootstrap.js                15343c398c168f3d5f8fe6933aaf3073e89dd5c0
stegos-bootstrap/admitted-inference.js              1cac8bc4d5a13a6596cd7f68b01e3a93be7536f0
stegos-bootstrap/device-local-autostart.js           d2aaffa033003cb6b031dbf30312c6104de989b2
stegos-bootstrap/service-worker.js                  98c45c88b33c5c0d5cade19da7af6d951752c088
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

`https://stegverse.org/stegos-bootstrap/local-model` is not a hosted model endpoint. The v3 service worker intercepts the exact same-origin path on the physical node and executes the canonical browser reference model locally. The local branch must never call network `fetch(event.request)`.

Required behavior:

- service-worker import of the exact canonical model and TVC evaluator projections;
- `/canonical-evidence` produces local model proof plus TVC `ROUTE_ADMITTED` evidence;
- `/v1/chat/completions` executes on-device reference-model inference;
- response header `X-StegVerse-Execution: SERVICE_WORKER_LOCAL_INTERCEPT` proves the device-local transport branch;
- automatic admission waits for node establishment and service-worker update, then retries within a bounded 60-second window;
- `credentials: omit`; no Authorization/Bearer/provider/GitHub/private-key credential path;
- `credential_requirement=NONE`, `github_token_required=false`, `third_party_execution_platform_required=false`;
- model output and Site projection have `authority_effect=NONE`.

## Validation

Canonical Site validator:

`./scripts/check_stegos_ipod_bootstrap_projection.py`

Current validator blob in this tree:

`1581d28a82a843876752fbfc42ba51dd474ba7fa`

It checks exact Git blob identity for all eight public assets plus no-network local interception, bounded automatic admission, authority neutrality, and prohibited credential markers.

Hosted validation is source/publication evidence only. A workflow that does not execute a validation step is not a pass. Pages publication is also not physical inference activation.

## Collision boundary

Do not modify `data/session-work-claims.json` while the active Site#268 owner retains that coordination surface. The reopened #298 revision is confined to `stegos-bootstrap/**`, its exact projection validator, this scoped handoff, and issue evidence.

## Release condition

```text
exact current projection installed on Site main
-> projection validator PASS
-> exact Pages build from that merge observed
-> public current assets match the expected blobs
-> Site #298 closes again for this source revision
-> StegOS #15 performs physical device-local admitted inference
-> stegos.web_admitted_inference_receipt.v1 appended
-> local journal replay PASS
```

The Site lane closes at public-materialization proof. Physical inference remains a separate StegOS activation predicate and is never inferred from Site publication.

## Completion accounting

```text
old #298 publication: COMPLETE_HISTORICAL_REVISION
current source revision exact file set: 8 files
current projection source: PENDING_THIS_TREE_MERGE
current validator: INSTALLED_IN_THIS_TREE
current source/publication validation: PENDING
current Pages build: PENDING
physical inference: PENDING_STEGOS#15
scaffolding/stubs: 0
```

DO NOT ARCHIVE this reopened projection lane until current public materialization is proven and #298 is reclosed.
