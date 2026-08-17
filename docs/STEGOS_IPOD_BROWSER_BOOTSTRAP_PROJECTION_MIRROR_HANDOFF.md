# StegOS iPod Browser Bootstrap Projection Mirror Handoff

Updated: `2026-08-16T21:34:00-05:00`

## Canonical scope

```text
goal_id: SITE-STEGOS-IPOD-BROWSER-BOOTSTRAP-294
originating_goal: allow the physical iPod touch 7 / iOS 15.8.8 to establish the first StegVerse node and activate Ecosystem Chat without a second user-operated machine
repository: StegVerse-Labs/Site
branch: claim/stegos-ipod-browser-bootstrap-294
issue: StegVerse-Labs/Site#294
source_owner: StegVerse-Labs/StegOS#13
source_merge: 799e0f3fd2766a32cbf0720384db11f066d8e9b8
claim_registry: data/session-work-claims.json
claim_id: SITE-STEGOS-IPOD-BROWSER-BOOTSTRAP-294-20260816
implementation_claim: CLAIMED_FOR_IMPLEMENTATION
validation_claim: SOURCE_AND_SITE_GATES_PENDING
integration_claim: PAGES_PUBLICATION_PENDING
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_allowed: false
render_production_authority: false
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
```

## Exact source projection

The following Site files are exact byte projections of the released StegOS browser bootstrap at merge `799e0f3fd2766a32cbf0720384db11f066d8e9b8`:

```text
Site path                              StegOS source path                                 Git blob
stegos-bootstrap/index.html            mobile/web-bootstrap/index.html                   0b3ca0df4f1c2e115f1a7040ab981ff5c7b67db0
stegos-bootstrap/stegos-bootstrap.js    mobile/web-bootstrap/stegos-bootstrap.js          0f58bf5b8dd7b5de02c4113aebf798005f2e5808
stegos-bootstrap/service-worker.js     mobile/web-bootstrap/service-worker.js           d489341a69185a33e36c517177a2049a0b160ead
stegos-bootstrap/manifest.webmanifest  mobile/web-bootstrap/manifest.webmanifest        a223ec9454f46d0e9b91d4862f11de701792144a
```

Site does not fork the StegOS semantics. Any source change must originate in the canonical StegOS owner and be re-projected with a new exact provenance record.

## Runtime boundary

The public Site surface provides only HTTPS materialization of the exact StegOS files. Once materialized in Safari, node establishment and Ecosystem Chat activation execute on the iPod through local WebCrypto/IndexedDB/service-worker capabilities.

```text
Site HTTPS transport
  -> exact StegOS browser shell
  -> iPod secure browser context
  -> persistent local StegVerse node id
  -> local hash-bound receipt journal
  -> local Ecosystem Chat activation
```

Site does not become node identity, activation, heartbeat, model, route, TV/TVC, wallet, signing, broadcast, custody, Apple-signing, or publication authority.

## Activation invariants

```text
activation_authority_plane: STEGVERSE
credential_authority: TV/TVC
requires_external_non_stegverse_machine: false
external_non_stegverse_machine_used_for_activation: false
github_token_runtime_authority: NONE
hosted_ci_activation_authority: NONE
render_production_authority: false
non_tv_tvc_secret_or_token_used: false
```

Ecosystem Chat surface activation requires only local node/runtime and local receipt-journal readiness. TVC route and sovereign inference remain optional StegVerse capabilities. Routed and inference actions fail closed until canonical evidence is available.

## Validation

Repository validator:

```text
python scripts/check_stegos_ipod_bootstrap_projection.py
python -m pytest tests/test_stegos_ipod_bootstrap_projection.py
python scripts/check_session_work_claims.py
python scripts/site_handoff_orchestrator.py
```

Required PR gates:

```text
exact StegOS projection validator: PASS
session pre-work claims: PASS
Site Handoff Orchestrator: PASS
Ecosystem Heartbeat Orchestration: PASS
Site Bootstrap Validate: PASS
```

Hosted GitHub workflows remain validation/evidence surfaces only. They grant no StegOS activation or TV/TVC authority and must not become a runtime dependency.

## Integration and publication

After all source and orchestration gates pass:

1. merge the claim branch;
2. verify the exact GitHub Pages build/deployment is descended from the merge commit;
3. record the exact deployed path for `stegos-bootstrap/`;
4. release this Site implementation claim;
5. transfer physical continuation to `StegVerse-Labs/StegOS#13`.

## Physical continuation

The physical iPod proof is not owned by Site. StegOS #13 closes only after the registered iPod directly demonstrates:

```text
load exact canonical HTTPS bootstrap
Establish StegVerse Node -> ESTABLISHED
persistent node_id observed across reload
Activate Ecosystem Chat -> ACTIVATED
local journal replay -> PASS
evidence bundle shown/exported
no second non-StegVerse machine participates in node/service activation
missing TVC/model evidence leaves routed/inference actions fail closed
```

## Collision/convergence

This work is distinct from the active StegFin freshness projection claim `SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292-20260816`. The dependency surfaces and product files do not overlap except the shared claim registry itself. The machine-owned pre-work gate remains the canonical collision-control owner.

The local-model/runtime implementation is already canonical in `StegVerse-002/micro-node-runtime`; this Site task does not duplicate it. The heartbeat/runtime is canonical in `StegVerse-Labs/.github`; this task does not duplicate it.

## Completion accounting

```text
developed_files: 7/7
scaffolding_or_stubs: 0
missing_required_files: 0
validation: 0/5 required gate groups at handoff creation
integration: 1/3 exact source projected; merge + Pages publication pending
goal_activation: 0/2 physical predicates (node established, Ecosystem Chat activated)
session_consolidation: requirement transferred to Site #294 + this handoff + StegOS #13
```

## Archive condition

Site implementation ownership can be released after exact merge + Pages publication evidence. The originating session remains non-archiveable while physical iPod node establishment/service activation or other unique session work remains untransferred.
