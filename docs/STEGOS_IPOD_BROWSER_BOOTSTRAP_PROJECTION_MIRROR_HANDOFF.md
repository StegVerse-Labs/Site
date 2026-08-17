# StegOS iPod Browser Bootstrap Projection Mirror Handoff

Updated: `2026-08-16T21:42:00-05:00`

## Canonical scope

```text
goal_id: SITE-STEGOS-IPOD-BROWSER-BOOTSTRAP-294
originating_goal: allow the physical iPod touch 7 / iOS 15.8.8 to establish the first StegVerse node and activate Ecosystem Chat without a second user-operated machine
repository: StegVerse-Labs/Site
source_owner: StegVerse-Labs/StegOS#13
source_merge: 799e0f3fd2766a32cbf0720384db11f066d8e9b8
site_issue: StegVerse-Labs/Site#294
site_pr: StegVerse-Labs/Site#295
site_merge: 312261808b1e98927a66488ffa066d5a3abd475f
claim_id: SITE-STEGOS-IPOD-BROWSER-BOOTSTRAP-294-20260816
claim_state: MERGED_INTO_CANONICAL_WORKSTREAM
implementation_state: COMPLETE_MERGED
validation_state: COMPLETE_SOURCE_BEHAVIOR
publication_state: GITHUB_PAGES_BUILT_EXACT_MERGE
physical_activation_state: PENDING_STEGOS_13
credential_authority: TV/TVC
non_tv_tvc_secret_or_token_used: false
render_production_authority: false
site_authority_effect: TRANSPORT_MATERIALIZATION_ONLY
canonical_public_path: https://stegverse.org/stegos-bootstrap/
```

## Released exact source projection

The following Site files are exact byte projections of the released StegOS browser bootstrap at merge `799e0f3fd2766a32cbf0720384db11f066d8e9b8`:

```text
Site path                              StegOS source path                                 Git blob
stegos-bootstrap/index.html            mobile/web-bootstrap/index.html                   0b3ca0df4f1c2e115f1a7040ab981ff5c7b67db0
stegos-bootstrap/stegos-bootstrap.js    mobile/web-bootstrap/stegos-bootstrap.js          0f58bf5b8dd7b5de02c4113aebf798005f2e5808
stegos-bootstrap/service-worker.js     mobile/web-bootstrap/service-worker.js           d489341a69185a33e36c517177a2049a0b160ead
stegos-bootstrap/manifest.webmanifest  mobile/web-bootstrap/manifest.webmanifest        a223ec9454f46d0e9b91d4862f11de701792144a
```

Site does not fork StegOS semantics. Changes originate in the canonical StegOS owner and must be re-projected with new exact provenance.

## Runtime boundary

```text
Site HTTPS materialization
  -> exact StegOS browser shell
  -> iPod secure browser context
  -> persistent local StegVerse node id
  -> local hash-bound receipt journal
  -> local Ecosystem Chat activation
```

Site does not become node identity, activation, heartbeat, model, route, TV/TVC, wallet, signing, broadcast, custody, Apple-signing, or model authority.

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

Ecosystem Chat activation requires only local node/runtime and local receipt-journal readiness. TVC route and sovereign inference are optional StegVerse capabilities. Routed and inference actions remain fail closed until canonical evidence exists.

## Validation evidence

PR #295 final head: `e87c09db83def358c6a88f4b2d30c200deff21f8`.

All final-head repository gates passed:

```text
Check StegFin Phone Projection: run 31988655790 SUCCESS
Ecosystem Heartbeat Orchestration: run 31988655786 SUCCESS
Site Handoff Orchestrator: run 31988655803 SUCCESS
Site Bootstrap Validate: run 31988655831 SUCCESS
bootstrap-validate job: 95268074578 SUCCESS
```

The canonical application aggregate directly executed and passed:

```text
scripts/check_stegos_ipod_bootstrap_projection.py
```

The same validation job generated artifact `site-application-validation-result`, artifact ID `9274581050`, ZIP SHA-256 `275c55326e826f939f91ab702bcecb32be5660fb44a43a91385507dc8e185076`.

Hosted GitHub validation exposed GitHub Actions credential material during checkout/setup. It is therefore source/integration evidence only and has **zero activation-authority effect**. No such token is required by or embedded in the iPod bootstrap runtime.

## Publication evidence

PR #295 merged as:

```text
312261808b1e98927a66488ffa066d5a3abd475f
```

GitHub Pages build:

```text
build_id: 1156080325
status: built
source_commit: 312261808b1e98927a66488ffa066d5a3abd475f
created_at: 2026-08-17T02:40:27Z
updated_at: 2026-08-17T02:40:45Z
source: main /
custom_domain: stegverse.org
certificate_state: approved
```

This proves the canonical Pages build consumed the exact merge containing `stegos-bootstrap/`. The canonical HTTPS path for physical validation is:

```text
https://stegverse.org/stegos-bootstrap/
```

## Claim release and continuation transfer

The Site implementation claim has been released as `MERGED_INTO_CANONICAL_WORKSTREAM` in `data/session-work-claims.json` after source validation, merge, and Pages build completed.

```text
MERGED INTO: StegVerse-Labs/StegOS#13
transferred: physical iPod node-establishment and Ecosystem Chat activation proof
already_complete: browser bootstrap implementation, exact Site projection, repository validation, Pages build
remaining_owner: StegVerse-Labs/StegOS#13
```

## Physical continuation — now the next executable action

On the registered iPod touch 7 / iOS 15.8.8, using Safari only:

```text
open https://stegverse.org/stegos-bootstrap/
confirm secure runtime capabilities
select Establish StegVerse Node
observe ESTABLISHED + persistent node_id
select Activate Ecosystem Chat
observe ACTIVATED
select Replay Local Journal
observe PASS
select Show Evidence Bundle
preserve/show the resulting evidence
reload and confirm the same node_id persists
```

If the Service Worker is available and registers on this iOS/Safari build, offline-shell persistence can then be tested by removing network access and reloading. Service Worker availability is not authority and is not required to fabricate success; unsupported behavior is recorded as unavailable.

Missing TVC/model evidence must leave routed/inference actions fail closed. No Mac, Xcode, Render, GitHub token, non-TV/TVC secret/token, wallet operation, signing, or broadcast participates in node or Ecosystem Chat activation.

## Collision/convergence

- `StegVerse-002/micro-node-runtime` already owns the actual local-model discovery/launch/inference/proof path and formal local-model work; this lane does not duplicate it.
- `StegVerse-Labs/.github` owns sovereign heartbeat/runtime and worker continuation.
- `StegVerse-Labs/TV` + `StegVerse-Labs/TVC` own protected credential and route authority.
- the concurrent Site StegFin freshness work owns a distinct dependency surface and remains separate.

## Completion accounting

```text
developed_files: 9/9
scaffolding_or_stubs: 0
missing_required_files: 0
validation: 5/5 gate groups PASS
integration: 3/3 exact projection + merge + Pages build COMPLETE
site_goal_activation: 100% publication/materialization ready
physical_goal_activation: 0/2 until iPod node establishment + Ecosystem Chat activation are directly observed
session_consolidation: Site lane transferred completely to StegOS #13
```

## Archive condition

The Site projection lane itself is complete and transferred. The originating session is not archive-ready because direct physical iPod activation evidence and adjacent session goals remain active or machine-owned elsewhere.
