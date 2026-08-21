# StegOS iPod Browser Bootstrap Projection Mirror Handoff

Updated: `2026-08-20T22:08:00-05:00`

## Canonical scope

```text
goal_id: SITE-STEGOS-IPOD-BROWSER-BOOTSTRAP-294
repository: StegVerse-Labs/Site
source_owner: StegVerse-Labs/StegOS#13
site_issue: StegVerse-Labs/Site#294 / CLOSED_COMPLETED
claim_id: SITE-STEGOS-IPOD-BROWSER-BOOTSTRAP-294-20260816
claim_state: MERGED_INTO_CANONICAL_WORKSTREAM
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_used: false
github_token_runtime_authority: NONE
render_production_authority: false
canonical_public_path: https://stegverse.org/stegos-bootstrap/
```

This Site lane remains a projection/materialization surface. It does not own StegOS node identity, physical activation, heartbeat, model, route, credential, wallet, signing, broadcast, custody, or execution authority.

## Current exact source binding

The bootstrap evolved after the original #294 projection. Current Site files are bound to the exact canonical StegOS tree at:

```text
StegVerse-Labs/StegOS@7f175d9e61e8d3e521e18ca7a3edb183fdcedd2a
```

Current exact blobs:

```text
Site path                                      StegOS source path                                      Git blob
stegos-bootstrap/index.html                    mobile/web-bootstrap/index.html                         f2e9aa2a994acb9b259388b7b876be5ec5487c92
stegos-bootstrap/stegos-bootstrap.js            mobile/web-bootstrap/stegos-bootstrap.js                15343c398c168f3d5f8fe6933aaf3073e89dd5c0
stegos-bootstrap/admitted-inference.js          mobile/web-bootstrap/admitted-inference.js              1cac8bc4d5a13a6596cd7f68b01e3a93be7536f0
stegos-bootstrap/device-local-autostart.js      mobile/web-bootstrap/device-local-autostart.js          ef8d0c0da429365589d7559bfbcdc77cc3452ebd
stegos-bootstrap/service-worker.js             mobile/web-bootstrap/service-worker.js                 3cba6ca48c8b093d0f0baa48aff000a544e93cc6
stegos-bootstrap/stegverse-reference-model.js   mobile/web-bootstrap/stegverse-reference-model.js       bd8e7553b61425386f6cf65db4766b952c148ed4
stegos-bootstrap/tvc-sovereign-local-model-route.js mobile/web-bootstrap/tvc-sovereign-local-model-route.js 3ca841310b904c2e09390512043f30f301976b1d
stegos-bootstrap/manifest.webmanifest           mobile/web-bootstrap/manifest.webmanifest               a223ec9454f46d0e9b91d4862f11de701792144a
```

`Site` does not fork these semantics. A changed projected byte requires exact canonical StegOS provenance before the Site validator may advance.

## 2026-08-20 projection-binding repair

Site Bootstrap Validate run `32434679078` reached the canonical application aggregate after all credential-neutral bootstrap, HIL, Master Records, continuity, VA-guided, child-safety, workflow-inventory, claim, and orchestration checks passed. It then failed only because `scripts/check_stegos_ipod_bootstrap_projection.py` still expected the older `index.html` blob:

```text
observed Site blob:  f2e9aa2a994acb9b259388b7b876be5ec5487c92
stale expected blob: 561e21d38df310aee838716ab9f2a4a6175485d5
```

Direct canonical inspection proved `f2e9aa2a994acb9b259388b7b876be5ec5487c92` is the exact current `StegVerse-Labs/StegOS:mobile/web-bootstrap/index.html` blob. The remaining seven projected files also match the exact StegOS tree at `7f175d9e61e8d3e521e18ca7a3edb183fdcedd2a`.

Repair commit:

```text
a6be9d9f05f321838a7d8ea0fab8b583d15e0e50
```

The repair advances provenance only. It does not weaken marker validation, credential prohibitions, service-worker local-model confinement, continuity-root separation, or any authority boundary. A hosted Site Bootstrap PASS for the repair is still required before calling the validation regression closed.

## Physical downstream state

The original physical continuation was transferred to `StegVerse-Labs/StegOS#13`. The canonical StegOS handoff now records that first-node physical goal as complete:

```text
secure browser capabilities: PASS
node establishment and persistence: PASS
Ecosystem Chat local activation: PASS
local evidence bundle: PASS
journal replay: PASS
offline shell and offline replay: PASS
second non-StegVerse machine required: false
credential authority: TV/TVC
```

This is downstream StegOS physical evidence. It does not grant Site runtime or execution authority.

StegOS has also advanced admitted inference and browser continuity beyond the original #294 denominator. Those newer goals remain owned by their respective StegOS handoffs and must not be collapsed into this historical first-node projection claim.

## Runtime boundary

```text
Site HTTPS materialization
  -> exact canonical StegOS browser shell
  -> physical secure browser context
  -> persistent local StegVerse node / continuity state
  -> local hash-bound receipt journal
  -> StegOS-owned local activation and replay evidence
```

## Authority invariants

```text
activation_authority_plane: STEGVERSE
credential_authority: TV/TVC
requires_external_non_stegverse_machine: false
github_token_runtime_authority: NONE
hosted_ci_activation_authority: NONE
render_production_authority: false
non_tv_tvc_secret_or_token_used: false
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
```

## Original release evidence retained

The original Site #294 integration remains historical provenance:

```text
StegOS source merge: 799e0f3fd2766a32cbf0720384db11f066d8e9b8
Site PR #295 merge: 312261808b1e98927a66488ffa066d5a3abd475f
Site Bootstrap Validate: 31988655831 SUCCESS
Ecosystem Heartbeat Orchestration: 31988655786 SUCCESS
Site Handoff Orchestrator: 31988655803 SUCCESS
Check StegFin Phone Projection: 31988655790 SUCCESS
GitHub Pages build: 1156080325 / built
```

Historical success does not substitute for validating later canonical StegOS source changes.

## Collision / continuation

- The #294 Site claim remains released; do not reopen it as a competing implementation owner.
- `StegVerse-Labs/StegOS` remains canonical source and physical browser owner.
- `StegVerse-002/micro-node-runtime` remains formal local-model owner.
- `StegVerse-Labs/TV` + `StegVerse-Labs/TVC` remain protected credential/route authority.
- `StegVerse-Labs/.github` owns heartbeat/control-plane continuation.
- The next active StegOS continuation is browser command ingress under `StegVerse-Labs/StegOS#17`; any Site projection for that capability requires its own fresh collision-safe Site claim rather than extending #294 implicitly.

## Completion accounting

```text
historical #294 developed projection files: COMPLETE
current validator-covered projection files: 8/8 present
scaffolding_or_stubs: 0
missing_required_projection_files: 0
first-node Site publication/materialization: COMPLETE
first-node physical StegOS downstream goal: COMPLETE
current exact-source validator repair: INSTALLED / HOSTED REVALIDATION PENDING
release/tag authority from this repair: NONE
```

## Next executable action

1. Observe a fresh Site Bootstrap run containing `a6be9d9f05f321838a7d8ea0fab8b583d15e0e50` or a descendant and require `scripts/check_stegos_ipod_bootstrap_projection.py` to PASS.
2. If it passes, preserve #294 as completed and do not create more first-node work.
3. Continue the distinct StegOS #17 command-ingress Site projection only through a fresh claim admitted by the existing Site pre-work gate.

## Archive condition

The historical #294 implementation and physical first-node continuation are durably complete and recoverable from repository state. This handoff remains the Site-side provenance record for exact bootstrap projection maintenance; no earlier chat is required to continue.
