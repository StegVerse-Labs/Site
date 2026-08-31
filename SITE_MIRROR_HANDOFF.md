# Site Mirror Handoff

## Current source of truth

This file is the authoritative continuation record for `StegVerse-Labs/Site`.

## Primary Site application goal

```text
Goal: governed Ecosystem Chat and AI Entry application with fail-closed live activation, recoverability, release, and downstream evidence boundaries
Repository-local result: COMPLETE
Manual user tasks: NONE
Recursive repository-local goal expansion: DISABLED
```

The completed primary Site application implementation remains governed by its existing validation, custody, reconstruction, release, and downstream evidence boundaries. Absent live evidence never becomes success.

## Session pre-work orchestration enforcement

```text
goal_id: SITE-259-PREWORK-CLAIM-ENFORCEMENT
canonical_issue: StegVerse-Labs/Site#259
implementation_branch: fix/session-prework-claims-259
claim_registry: data/session-work-claims.json
claim_validator: scripts/check_session_work_claims.py
claim_tests: tests/test_session_work_claims.py
orchestrator: scripts/site_handoff_orchestrator.py
heartbeat_gate: .github/workflows/ecosystem-heartbeat-orchestration.yml
bounded_handoff: docs/SESSION_PREWORK_CLAIMS_MIRROR_HANDOFF.md
state: HOSTED_VALIDATION_IN_PROGRESS
```

Every mutable Site pull-request execution lane must resolve to exactly one active machine-readable pre-work claim. Task collisions and dependency/work-surface collisions fail closed. Distinct support roles require explicit non-overlap. Fuzzy issue-title overlap is diagnostic only and does not itself mint execution ownership. An incidental dependency, including Render, cannot become a governing objective unless canonical task evidence explicitly marks it critical and unowned.

The heartbeat/orchestration workflow must not suppress `site_handoff_orchestrator.py` failures. Pull requests are gated by the claim registry, and the heartbeat worker revalidates the registry on repository events, explicit dispatch, and scheduled heartbeat observation.

## Adjacent active goal — SV-DN-1 governed browser evidence egress

```text
goal_id: SITE-SV-DN1-BROWSER-EVIDENCE-INTR-EGRESS-001
handoff: docs/SV_DN1_BROWSER_EVIDENCE_INTR_EGRESS_MIRROR_HANDOFF.md
implementation_pr: 749
implementation_merge: 8fff6f9d18c18fcb6fd75d47557de74825d5c74d
claim_release_pr: 752
claim_release_merge: dc9b61428a0588b507b0f4ae3861322f7d371228
source_state: MERGED_VALIDATED
runtime_ingress_admission: NOT_OBSERVED
governed_request: RESIDENT-EXEC-SV-DN1-FIRST-ROUND-007
authority_effect: NONE
```

The established `stegnode-web-*` SV-DN-1 observation surface now has the browser-side half of the canonical Universal InTr handoff. After an authentic observation freezes `bundleOut`, the page automatically attempts the exact `DEVICE_SYSTEM -> STEGOS_ECOSYSTEM` transport, preserves the existing node/device continuity, builds a source-side Interlock receipt from the journal tail, and accepts only an exact `INGRESS_ADMITTED` sovereign receipt. The merged target remains fail-closed until independently observed HTTPS `/intr/profile` evidence explicitly advertises `SV-DN1:BrowserObservation` and `STEGOS_WEB_BOOTSTRAP_EGRESS`.

Source completion does not establish that the shared Gateway currently has an open ESRL lease, that `/intr/materialization` accepted this bundle, or that SDK/StegCore/Master Records/public promotion/repository persistence completed. Those remain authentic runtime evidence gates.

## Adjacent active goal — My KV multi-email Personal Information

```text
goal_id: SITE-MY-KV-MULTI-EMAIL-558
canonical_issue: StegVerse-Labs/Site#558
claim: SITE-MY-KV-MULTI-EMAIL-558-20260828
branch: claim/site-my-kv-multi-email-558
handoff: docs/MY_KV_MULTI_EMAIL_MIRROR_HANDOFF.md
state: IMPLEMENTED_VALIDATED_MERGED_PUBLICATION_VERIFY_PENDING
authority_effect: NONE
activation_effect: false
```

This lane projects the canonical `continuity-vault-kit` multi-email personal-contact profile into a new `my-kv.html` surface. Multiple addresses, one optional primary preference, profile-only addresses, per-address connection state, and SKAP completion guidance are implemented. Site does not accept provider secrets and does not fabricate mailbox mapping: `Connect this email` fails closed when the canonical KV email bridge is unavailable.

Live mailbox mapping, SKAP credential installation, provider verification, and governed email ingestion remain upstream owner-authorized activation gates.

Exact implementation validation for Site #558:
- My KV Personal Information `33145133095`: PASS
- Site Bootstrap Validate `33145133097`: PASS
- Ecosystem Heartbeat Orchestration `33145133112`: PASS
- Site Handoff Orchestrator `33145133122`: PASS

Merge evidence: PR #560 -> `37c304a4d0ecdfa2e648177452c80ec7ddb52860`; claim released at `70d6e4f00fa61da6b0e19034c99cca82eeabe3c9`. Final handoff-bearing validation head `93e1e480a92ceb290fa5ab17655241bdfcd73e0a` also passed all four Site/My KV gates. Public route verification remains separate.

## Adjacent active goal — StegGate tunnel-native rendezvous

```text
goal_id: STEGGATE-TUNNEL-NATIVE-RENDEZVOUS
canonical_owner: StegVerse-Labs/Site#24 + StegVerse-Labs/StegCore heartbeat tunnel runtime
originating_completed_dependencies:
  - StegVerse-Labs/StegCore#68 — functional StegGate COMPLETE
  - StegVerse-Labs/StegCore#75 — heartbeat/credential integration COMPLETE
state: CURRENT_HEARTBEAT_TUNNEL_VERIFIED
scheduler_authority: single StegVerse heartbeat
wall_clock_scheduler_authority: false
persistent_third_party_host_required: false
```

The active path is the heartbeat-owned StegGate micro-node plus its verified ephemeral public tunnel. Render is not authoritative and is not an activation prerequisite. A provider-specific stable-domain route such as `https://stegverse.org/api/steggate` is optional availability/discovery hardening only.

## Installed tunnel/discovery surfaces

```text
StegVerse-Labs/.github/.github/workflows/steggate-heartbeat-integration.yml
StegVerse-Labs/.github/management/STEGGATE_HEARTBEAT_CREDENTIAL_INTEGRATION_001.json
StegVerse-Labs/StegCore/.github/workflows/steggate-heartbeat-worker-reusable.yml
StegVerse-Labs/StegCore/.github/workflows/steggate-fallback-public-runtime.yml
StegVerse-Labs/StegCore/src/stegcore/endpoint_discovery.py
StegVerse-Labs/StegCore/management/steggate-heartbeat-credential-integration.json
StegVerse-Labs/Site/src/steggate-rendezvous-worker.js
StegVerse-Labs/Site/data/steggate-rendezvous-activation.json
```

`src/steggate-rendezvous-worker.js` contains no StegGate policy engine. It resolves only a registry-declared live StegGate micro-node, independently verifies canonical health, proxies the bounded HTTP contract, and fails closed when no verified node exists.

## Canonical tunnel acceptance

A tunnel is usable only after independent verification of:

```text
/health                  state=healthy; canonical_three_layer_bound=true
/v1/self-test            exact ALLOW / DENY / REVIEW / FAIL_CLOSED
/v1/evaluate             deterministic complete-matrix acceptance
```

Historical tunnel success does not assert current liveness. Tunnel endpoints are lease-bound and must be re-resolved and reverified for current use.

## Current heartbeat tunnel proof

Fresh canonical proof:

```text
StegVerse-Labs/.github workflow run: 31325104576
heartbeat job: 93274099310 SUCCESS
StegGate micro-node job: 93274112655 SUCCESS
heartbeat id: HB-31325104576-5
heartbeat epoch: 5
StegCore commit executed: f0d764b2b5b48987d75ea4efd1da1fafde04b406
current observed tunnel origin: https://owners-recipes-catherine-laid.trycloudflare.com
/health: PASS
/v1/self-test: PASS
/v1/evaluate: PASS
heartbeat artifact: 9041292966
heartbeat digest: sha256:bc0c6d498f0f270f2fa1ec2de29444b4d2cd809d726287fb70f36f2decb9e919
micro-node artifact: 9041297862
micro-node digest: sha256:a1222757e3fe0187b58ce2bd26c32600c70087c14c5f9e48f68ee7ffa2473b69
observed_at: 2026-08-09T16:57:13.142713Z
```

The deterministic evaluation returned canonical `ALLOW` with all required matrix predicates PASS, permission/admissibility separation preserved, no external execution, and no continuity receipt minted by the observer.

The older issue-comment registry origin from 09:14 UTC remains historical rotating-endpoint evidence only. Consumers must not equate that declaration with current liveness.

## Stable-domain / provider-specific lane

The Cloudflare Worker stable-domain lane remains optional hardening. It is now an **actually activated StegVerse heartbeat worker task**, not merely a documented blocker.

Canonical worker continuation:

```text
task: STEGGATE-STABLE-RENDEZVOUS-WORKER-001
registry: StegVerse-Labs/.github/control/worker-registry.json
handoff: StegVerse-Labs/.github/handoffs/STEGGATE-STABLE-RENDEZVOUS-WORKER-001.json
authorization: StegVerse-Labs/.github/authorizations/STEGGATE-STABLE-RENDEZVOUS-WORKER-001.json
worker: steggate-rendezvous-deployment-worker
adapter: process:steggate-rendezvous-deployment-v1
claim: SHWP-STEGGATE-STABLE-RENDEZVOUS-WORKER-001-G13
worker_instance: steggate-rendezvous-deployment-worker-HB7-G13
heartbeat_epoch: 7
fencing_token: 13
state: BLOCKED
current_transition: CREDENTIAL_VALUES_ABSENT
expected_next_transition: CREDENTIAL_RECHECK
checkpoint: checkpoints/workers/STEGGATE-STABLE-RENDEZVOUS-WORKER-001/HB7-G13.json
worker_receipt: receipts/steggate-rendezvous-worker/STEGGATE-STABLE-RENDEZVOUS-WORKER-001.json
heartbeat_run: 31325420776
heartbeat_job: 93274879376 SUCCESS
heartbeat_artifact: 9041376225
heartbeat_artifact_digest: sha256:590af345db1d942993345f7d5ecff50998ddc4d6898331d7bcf6d3adabd94756
```

The canonical heartbeat status projection independently classified this unfinished worker as `archive_eligible=true`, with `executor_binding=BOUND`, heartbeat timing established, authority resolved, a live claim/fence, and a canonical checkpoint. This means the remaining provider-specific hardening is now worker-owned in the precise sense required by the session-consolidation rule; it is not merely durably assigned.

The worker performs no wall-clock polling. On admitted heartbeat execution it re-evaluates the bounded provider credential references. Missing values return `BLOCKED` and remain claimed/checkpointed. When values are present, the same worker validates the exact Cloudflare Workers capability, verifies the pinned canonical Site rendezvous source blob, deploys only the non-authorizing `stegverse-steggate-rendezvous` route, and requires readiness/health/four-disposition live acceptance before returning `COMPLETED`.

```text
optional stable origin: https://stegverse.org/api/steggate
CLOUDFLARE_API_TOKEN value present: NO
CLOUDFLARE_ACCOUNT_ID value present: NO
impact on tunnel-native activation: NONE
release condition for worker transition: both values are present in the authorized heartbeat execution environment
```

TV/TVC credential-reference contracts remain valid boundaries for provider-specific publication. They do not manufacture secret values and they do not own StegGate execution.

## Current execution rule

Machine-observable current-use condition:

```text
A heartbeat-owned StegGate tunnel is freshly discoverable
AND it independently passes canonical health
AND it passes exact self-test
AND deterministic /v1/evaluate passes the acceptance contract.
```

This condition is satisfied by heartbeat epoch 5 evidence above. Consumers may use a verified tunnel only within its actual live lease. If no current tunnel is discoverable, the system fails closed and the next admitted heartbeat worker is the canonical recovery path. Do not wait on Render build minutes or provider-specific hosting credentials.

## Collision and authority boundaries

```text
heartbeat != execution authority
tunnel availability != StegGate admissibility
registry declaration != current health
provider transport != policy authority
rendezvous routing != StegGate policy authority
SDK validation != execution
local persistence != custody
custody receipt != execution authority
reconstruction PASS != execution authority
workflow artifact != current endpoint evidence
```

Canonical owners:

```text
single heartbeat: StegVerse-Labs/.github#12
StegGate runtime/tunnel: StegVerse-Labs/StegCore
Site tunnel consumption/rendezvous: StegVerse-Labs/Site#24
stable-domain hardening worker: StegVerse-Labs/.github/control/worker-registry.json#STEGGATE-STABLE-RENDEZVOUS-WORKER-001
TV credential-reference packaging: StegVerse-Labs/TV
TVC secret-reference authority: StegVerse-Labs/TVC
```


## Active sequenced goal — third-party dependency eradication

```text
goal_id: SITE-497-THIRD-PARTY-DEPENDENCY-ERADICATION
canonical_issue: StegVerse-Labs/Site#497
state: INVENTORY_AND_REPLACEMENT_SEQUENCE_ACTIVE
target_invariant: NO_REQUIRED_THIRD_PARTY_AUTHORITY_OR_CONTINUITY_DEPENDENCY
```

This goal expands the former Vercel-only removal lane to every required third-party dependency, including Render, Cloudflare, PyPI/package registries, GitHub-hosted publication/source/CI surfaces, external CDNs/container registries, provider-specific tunnels, model/API SaaS, identity/notification transports, external databases/queues/object stores, and any equivalent provider discovered by inventory.

A third-party service may remain usable as optional transport, fallback, interoperability, discovery, or update source only when its outage, deletion, credential loss, account suspension, quota/pricing change, API change, DNS failure, package disappearance, or policy change cannot destroy StegVerse authority, canonical state, build reproducibility, recovery, activation, custody, reconstruction, or release continuity.

Canonical per-provider state progression:

```text
DISCOVERED
-> CLASSIFIED
-> REPLACEMENT_DESIGNED
-> SOVEREIGN_COPY_OR_RUNTIME_READY
-> DUAL_RUN_VERIFIED
-> PROVIDER_FAILURE_PROVEN
-> CUTOVER_COMPLETE
-> CREDENTIALS_REVOKED
-> ORPHAN_RESOURCE_RETIRED
-> REGRESSION_GUARDED
```

Sequenced build/event plan:

```text
0 FREEZE_INVARIANT
  no new required third-party dependency

1 INVENTORY
  source/CI/build/DNS/TLS/publication/runtime/tunnels/packages/
  containers/data stores/secrets/APIs/observability/custody/recovery/release

2 CLASSIFY
  REQUIRED_CURRENTLY | OPTIONAL_FALLBACK | HISTORICAL_ONLY |
  NEGATIVE_ASSERTION_ONLY | REPLACEABLE_BUILD_INPUT |
  UNAVOIDABLE_EXTERNAL_INTEROP

3 PACKAGE_SOVEREIGNTY
  pin+hash+mirror/vendor PyPI/npm/container/base-image inputs
  prove clean install/build with public registries unavailable

4 RUNTIME_SOVEREIGNTY
  remove Vercel/Render/provider-hosted runtime authority
  Cloudflare Workers/tunnels and equivalents become optional transport only
  dynamic execution remains StegVerse/heartbeat owned

5 PUBLICATION_EDGE_DNS_SOVEREIGNTY
  replace single-provider publication/redirect/DNS dependency
  dual-run sovereign static origin + redirect/routing + deterministic DNS restore
  preserve working current path until replacement is directly verified

6 SOURCE_CI_RELEASE_SOVEREIGNTY
  StegVerse-controlled canonical repository/recovery mirror
  validators/workers runnable without GitHub Actions
  mirrored release artifacts/evidence
  prove reconstruction/build/release preparation with GitHub unavailable

7 EXTERNAL_API_IDENTITY_RESILIENCE
  enumerate production provider calls
  separate interoperability from authority
  local/StegVerse alternative or admitted multi-provider path for required functions
  receipt continuity across provider loss

8 FAILURE_INJECTION
  per-provider and simultaneous optional-provider outage:
  NXDOMAIN/5xx/credential removal/project deletion/quota exhaustion/
  registry unavailable/artifact unavailable

9 CUTOVER_AND_RETIRE
  switch canonical path only after failure proof
  revoke credentials/remove secrets/retire orphan resources
  retain immutable provenance

10 CONTINUOUS_ANTI_REGRESSION
  validator rejects new provider-required gates, provider credential authority,
  unmanaged provider SDK/API authority, and unmirrored required package/runtime targets
```

Installed dependency-eradication control surfaces:

```text
claim: data/session-work-claims.d/site-third-party-dependency-eradication-497-20260826.json
inventory: data/third-party-dependency-inventory.json
canonical issue: StegVerse-Labs/Site#497
phase: PHASE_1_INVENTORY_IN_PROGRESS
```

Important classification correction:

```text
Render execution/policy authority: NO
Render current availability dependency: YES for the enabled Ecosystem Chat gateway
evidence: data/ecosystem-chat-gateway.json
current endpoint: https://stegverse-ecosystem-chat-gateway.onrender.com/api/ecosystem-chat
replacement required before retirement: YES
```

This distinction is mandatory: `provider_not_authority` does not imply `provider_not_dependency`. A provider remains a dependency whenever its loss blocks a required function even if it grants no execution or governance authority.

Current provider posture:

```text
Vercel:
  production/publication dependency: NO
  residual historical/negative references: YES
  formal outage/deletion + anti-regression proof: OPEN

Render:
  canonical authority/activation prerequisite: NO
  formal repo-wide outage/deletion proof: OPEN

Cloudflare:
  current stegverse.ai DNS/edge redirect use: YES
  optional StegGate tunnel/stable-domain concepts: YES
  removable today without replacement: NO
  target: optional/migration-ready transport, never authority

PyPI / npm / public package registries:
  offline/mirrored clean-build proof: OPEN
  target: update/discovery source only; exact required artifacts StegVerse-controlled

GitHub:
  current source hosting / Pages / workflow use: YES
  removable today without replacement: NO
  target: collaboration/public mirror only after sovereign source, CI, artifact,
  recovery, publication, and worker-continuation proof
```

Current public route evidence:

```text
stegverse.ai -> Cloudflare edge 301 -> stegverse.org -> GitHub Pages
state: LIVE_AND_VERIFIED
authority effect: TRANSPORT/PUBLICATION ONLY
dependency-eradication effect: demonstrates Vercel removal but exposes Cloudflare/GitHub
as later replacement targets
```

No current working provider path is removed before its sovereign replacement is directly observed, dual-run verified, and provider-failure proven. Historical provider records remain immutable provenance and cannot reactivate provider authority.


### Dependency-eradication execution checkpoint — 2026-08-26

```text
claim:
  data/session-work-claims.d/site-third-party-dependency-eradication-497-20260826.json

executable controls:
  scripts/check_third_party_dependency_invariant.py
  scripts/build_package_dependency_census.py

machine-readable state:
  data/third-party-dependency-inventory.json
  data/package-dependency-census.json
  data/render-gateway-replacement-plan.json
```

Executed findings and transitions:

```text
initial provider nodes classified: 10/10
UNKNOWN_PENDING_INVENTORY among initial nodes: 0

Vercel:
  event: CLASSIFIED
  current required use: false
  remaining: failure-equivalence + anti-regression proof

Render Ecosystem Chat gateway:
  event: REPLACEMENT_DESIGNED
  current required use: true
  sovereign replacement implementation: already COMPLETE_RELEASED in StegVerse-org/LLM-adapter
  exact Site cutover plan: data/render-gateway-replacement-plan.json
  live mutation collision: Site #501 owns scripts/check_ecosystem_chat_gateway_activation.py
  action while collision exists: preserve working Render fallback; do not duplicate gateway/runtime

Python package supply:
  classification: REQUIRED_CURRENTLY
  direct observed packages: jsonschema, requests, beautifulsoup4
  root requirements/pyproject/lockfile: absent
  exact version/hash/offline mirror proof: open

npm:
  classification: HISTORICAL_ONLY
  active Site manifest/lockfile: absent

container registries:
  classification: HISTORICAL_ONLY for current Site build
  active Site Docker/compose/build file: absent

external model/API providers:
  classification: OPTIONAL_FALLBACK
  Site client direct provider call: none
  same-origin gateway + StegVerse-owned local-provider architecture: canonical

registrar/DNS registry class:
  classification: UNAVOIDABLE_EXTERNAL_INTEROP
  target: migration-ready/redundant, never canonical authority
```

Render replacement invariant now recorded:

```text
verified sovereign node advertisement
-> discovery result enables governed gateway
-> dual-run against still-present Render fallback
-> inject Render failure
-> static Render endpoint removed
-> no sovereign node => LOCAL_CLASSIFICATION fail-closed
-> retire Render credentials/resources
-> regression guard
```

The dependency invariant validator is intentionally not yet wired into the shared Site bootstrap workflow because Site #501 currently owns a colliding validation/task-runner surface. Source installation is complete; hosted/strict-scan proof remains pending ownership-safe execution.



### Dependency-eradication execution checkpoint — 2026-08-27

Implemented on canonical `main`:

```text
repository-local schema validator:
  scripts/stegverse_jsonschema.py
  commit: 62255f8e6446576ad8102b73d8d4682df2b52c2f

migrated from external jsonschema package:
  scripts/validate_hil_pilot_ledger.py
  scripts/test_hil_pilot_validation.py
  scripts/capture_validation_manifest.py
  .github/workflows/hil-announcement-contract.yml
  .github/workflows/capture-validation-evidence.yml
  .github/workflows/observe-rtg-formalism-projection.yml

remaining current Python package-network surfaces:
  .github/workflows/validate.yml -> jsonschema
  .github/workflows/site-task-runner.yml -> pip upgrade + requests + beautifulsoup4

ownership boundary:
  validate.yml / Site Task Runner remain collision-owned by other active Site lanes
  #497 does not mutate them until ownership releases or transfers
```

Python package dependency transition:

```text
previous: broad public-registry dependence across HIL/receipt/RTG validation
current: reduced to two collision-owned workflow surfaces
inventory event: REPLACEMENT_DESIGNED
hosted proof of repository-local validator: PENDING
full public-registry independence: NOT YET PROVEN
```

Cloudflare reconciliation:

```text
legacy HIL Cloudflare/D1 deploy:
  state: HISTORICAL_SUPERSEDED
  current dependency: false
  retry authority: false
  stale secret-population instruction removed
  reconciliation commit: a8255cdcff9ac8c5318c265ca8a5935ac5144048

Cloudflare roles are now decomposed:
  .ai DNS/edge redirect: REQUIRED_CURRENTLY
  StegGate rotating tunnel carrier: REQUIRED_CURRENTLY for currently evidenced public tunnel
  stable-domain Worker hardening: OPTIONAL_FALLBACK
  retired HIL Cloudflare/D1 path: HISTORICAL_ONLY
  StegFin rotating SKAP carrier contract: OPTIONAL_FALLBACK / NOT_PROVISIONED
```

Render coupling reduction:

```text
hard-coded Render removed from:
  assets/hil-experiment.js
  math-solver/index.html
  scripts/advance_math_solver_public_activation.py

current exact Render endpoint concentration:
  data/ecosystem-chat-gateway.json
  data/hil-gateway-config.json
  .github/workflows/site-task-runner.yml activation-evidence environment

HIL client:
  resolves declared candidates through data/hil-gateway-config.json
  does not hard-code a provider origin

Math Solver:
  resolves runtime origin through data/ecosystem-chat-gateway.json
  no provider-specific URL in the client
  sovereign runtime receipt remains BLOCKED when local carrier is unavailable
  fail-closed behavior preserved
```

Additional provider classification:

```text
Coinbase:
  classification: UNAVOIDABLE_EXTERNAL_INTEROP
  current Site SKAP runtime use: false / NOT_PROVISIONED
  provider authority effect: false

StegFin Cloudflare fallback:
  classification: OPTIONAL_FALLBACK
  current route: NOT_PROVISIONED
  hard provider origin in repository route state: none
```

Anti-regression validator update:

```text
scripts/check_third_party_dependency_invariant.py
active-surface strict scan:
  .github/workflows/
  api/
  assets/
  scripts/
  src/
  active config/gateway/activation/deployment/runtime/route/profile/endpoint/provider JSON
historical documentation is not itself an active-runtime failure
strict hosted/current-checkout PASS: PENDING
```

Current #497 machine boundary:

```text
Render actual cutover:
  blocked from mutation by active Site #501 ownership of gateway/task-runner validator surface
  replacement design already complete
  no duplicate gateway implementation authorized

next non-colliding work:
  continue active-reference census
  internalize additional public package/network dependencies
  design .ai DNS/redirect migration-ready sovereign replacement
  install provider-failure evidence contracts
```

## Archive posture — completion / continuation

Primary Site application work remains complete. The StegGate architecture correction has hosted proof: tunnel-native heartbeat execution is the active path; persistent third-party hosting is optional hardening rather than a prerequisite.

The optional stable-domain hardening itself is not complete because the Cloudflare credential values are absent, but its continuation is no longer chat-owned or merely documented. It is actively claimed by the single-heartbeat worker registry with a bound executor, heartbeat-relative timing, fencing token, live BLOCKED transition, worker receipt, and canonical checkpoint. Current-liveness remains lease-sensitive by design; the heartbeat remains the recovery/refresh mechanism and no wall-clock scheduler owns the lane.

The issue #259 pre-work-claim goal is not archive-complete until its hosted workflow passes, PR #260 merges, its active claim is released or transferred to the scheduled heartbeat observer, and the resulting main-branch evidence is recorded here or in its bounded sub-handoff.


## HeartBeat public visibility repair — 2026-08-26

The canonical HB32 heartbeat status existed at `heartbeat-transition/index.html` but was not discoverable from the public Home or Version & Status surfaces. That visibility gap is now repaired.

Machine-readable/public surfaces:
- `index.html` now links to HeartBeat in navigation, transition routing, and Current proof status.
- `ecosystem-version.html` now links to HeartBeat in navigation and exposes an explicit HB32 operational-proof card.
- `data/heartbeat-public-visibility.json` defines the visibility contract.
- `scripts/check_heartbeat_public_visibility.py` fails closed if Home, Version & Status, or the dedicated status page loses the required HB32 semantics/link.
- `.github/workflows/heartbeat-public-visibility.yml` validates only this public visibility boundary and has `contents: read` with no execution/activation authority.

Exact source/publication evidence:

```text
head: 18a2fb7254f78661fb93d2c0c69d5f1ed41df8c9
HeartBeat Public Visibility 33029168537: SUCCESS
pages build and deployment 33029168082: SUCCESS
```

Current HB semantics exposed publicly:

```text
protocol: HB32
progression: OSCILLATOR_ONLY
period: 10 ms
reference rate: 100 Hz
continuous reference stream: true
LIVE-009: COMPLETED / INDEPENDENT_HEARTBEAT_LIVE_PROOF_VERIFIED
authority effect: NONE
```

Publication distinction: the exact Pages deployment for the visibility head succeeded. The external crawler available in this session still returned a cached pre-change Home snapshot immediately after deployment, so `data/heartbeat-public-visibility.json` records `PUBLIC_HTTP_REOBSERVATION_PENDING_CACHE_REFRESH` rather than treating a stale crawler cache as contradictory runtime evidence.


## HeartBeat route correction — 2026-08-26

User-observed public evidence showed a semantic routing defect: the Home card labeled **Observe HeartBeat** promised the current HB32 / 100 Hz status but routed to `heartbeat-transition/`, whose primary identity is the historical HB29 → HB30 transition capsule. The page did contain current HB32 text, but the destination identity was misleading.

Implemented correction:

```text
current public HeartBeat status: heartbeat-status/
historical compatibility capsule: heartbeat-transition/
Home HeartBeat links: heartbeat-status/
Version & Status HeartBeat links: heartbeat-status/
current status authority effect: NONE
historical capsule authority effect: NONE
```

A dedicated `heartbeat-status/index.html` now presents only current canonical HB32 status as the primary surface and links explicitly to the historical capsule as compatibility evidence. The machine-readable visibility contract now fails closed on the corrected route split. Source implementation is complete; public deployment/re-observation remains a separate evidence state and must not be inferred from source mutation alone.


## Generated StegPay latest-evidence reconciliation — 2026-08-27

The completed historical task `SITE-0001-GENERATED-STEGPAY-PROPAGATION-IMPORT` remains closed. The `latest` generated StegPay evidence pointer is reconciled to StegOps generation `2026-08-27T11:58:18Z` with propagation SHA-256 `e59e71bf31879f0bf29a8356f8027304a94a4dee59d3c0be35c3ecc505e7cec9` and consumer receipt SHA-256 `b8084ecc9821eb7738e4dccffd239185a072e0bc630e71c72906098a830cf515`.

The associated workflow is validation-only with read-only repository permissions. It no longer admits/completes tasks or commits/pushes controller state. Generated StegPay remains bounded test evidence only, with no payment, deployment, publication, release, activation, or admissibility authority.

Canonical detailed handoff: `docs/GENERATED_STEGPAY_INTEGRATION_MIRROR_HANDOFF.md`.


## HeartBeat public HTTP re-observation — 2026-08-27

Fresh public HTTP observation now confirms the repaired current-status routing is externally visible:

```text
Home: https://stegverse.org/
  exposes HeartBeat -> heartbeat-status/
  HB32 / OSCILLATOR_ONLY / 10 ms / 100 Hz / LIVE-009 / authority effect NONE

Dedicated current status: https://stegverse.org/heartbeat-status/
  HB32 / OSCILLATOR_ONLY
  LIVE-009 COMPLETED / INDEPENDENT_HEARTBEAT_LIVE_PROOF_VERIFIED
  observation authority effect NONE
  execution authority NONE
  activation effect false
```

`data/heartbeat-public-visibility.json` now records `PUBLIC_HTTP_REOBSERVED_CURRENT_HB32_STATUS`. This closes the stale-crawler re-observation gap only; it does not change heartbeat progression, execution authority, activation authority, or any crypto/TVC runtime predicate.


## Adjacent active goal — evaluator manifest review / freeze UI

```text
goal_id: SITE-EVALUATOR-MANIFEST-REVIEW-575
canonical_issue: StegVerse-Labs/Site#575
claim: SITE-EVALUATOR-MANIFEST-REVIEW-575-20260828
branch: feature/evaluator-manifest-review-ui
handoff: docs/EVALUATOR_REVIEW_UI_MIRROR_HANDOFF.md
source_contract: StegVerse-org/StegVerse-SDK PR #94
state: VALIDATED_MERGED_PUBLICATION_VERIFY_PENDING
authority_effect: NONE
activation_effect: false
```

This lane installs a generic mobile-first human review surface above the existing SDK evaluator-neutral manifest contract. Site renders review state but does not become test, approval, freeze, execution, credential, signing, custody, replay, or reconstruction authority. PUBLIC_READ works without credentials; comments, change requests, approvals, and freeze transitions require the authorized StegVerse review runtime bridge and fail closed when absent.

Current cross-framework fixture remains `DRAFT_PRE_FREEZE`. No external approval, canonical freeze, execution, result, deployment, activation, or public-route observation is claimed. Approval matching is exact-version + exact-manifest-SHA-256; any revision/hash drift makes prior approval stale for freeze readiness.


### Evaluator review v0.2 projection continuation — 2026-08-28

```text
canonical project: SITE-EVALUATOR-MANIFEST-REVIEW-575
continuation issue: StegVerse-Labs/Site#589
task: data/tasks/SITE-EVALUATOR-REVIEW-V02-SYNC-589.json
claim: SITE-EVALUATOR-REVIEW-V02-SYNC-589-20260828
SDK source: StegVerse-org/StegVerse-SDK PR #94 head c9b8935309e69d3a6f70e4ad4ef5dd55fb8a9aac
state: VALIDATED_MERGED_PUBLICATION_VERIFY_PENDING
```

The earlier public projection was stale relative to the externally reviewed SDK v0.2 draft. Issue #589 updates only the projection, guard, handoff, and state records. SDK v0.2 source validation is PASS (run 33196691745), while approval, freeze, execution, replay, reconstruction, and results remain absent. Public publication observation remains a separate post-merge gate.


### Evaluator v0.2 projection merge evidence

```text
Site issue: #589
Site PR: #590
validated head: b92b2700742f4b12bca4eb3e95454cf46bb6c406
merge: dd7e6d5685abea6c87429e90e36b1069bd9c9b9d
Evaluator Review UI Source Validation 33222852501: SUCCESS
Site Bootstrap 33222852459: SUCCESS
Site Handoff Orchestrator 33222852526: SUCCESS
Ecosystem Heartbeat 33222852590: SUCCESS
My KV regression 33222852475: SUCCESS
public route observation: PENDING
```

The exact SDK v0.2 projection is now merged. The first #590 hosted validation attempt failed closed only because the new claim lacked required `handoff_revision`; that defect was corrected before merge and the full exact-head gate passed. This does not advance the SDK manifest beyond DRAFT_PRE_FREEZE and does not establish external approval, freeze, execution, replay, reconstruction, release, activation, or completion.


## Site #562 refreshed diagnostic contract merge

State: IMPLEMENTED_VALIDATED_MERGED / POST_MERGE_ALL_LOCAL_PENDING

The stale `scripts/check_site_task_diagnostic_contract.py` hosted-authority contract was refreshed on current main and merged via PR #564 at `8c3b2cd280a2dcefca26fa2980a8c6492199e510`.

Validated head `af71ab968c9c2c555371c1cccd3f0f49e2cf5c2c` passed:
- Site Task Diagnostic Contract `33227836176`
- Site Bootstrap Validate `33227836075`
- Site Handoff Orchestrator `33227836133`
- Ecosystem Heartbeat Orchestration `33227836462`

The repair requires current validation-only activation retention and forbids retired GitHub-hosted secret/writeback authority. A successor `all-local` Site Task Runner is the remaining completion gate for this lane.


## Clean all-local baseline — 2026-08-28

State: VALIDATED / ALL_LOCAL_PASS

After the sequential stale-validator repairs (#586, #562, #521, #594), the canonical Site Task Runner completed a full `all-local` cycle successfully:

```text
run: 33228509129
head: aae871d97074be8e56df184ca6d3ff1881f6aea6
job: 99036820468
result: SUCCESS
SITE_TASK_DIAGNOSTIC_CONTRACT_PASS: observed
SITE UNIFIED GOVERNED EXPERIENCE: PASS: observed
SITE HOMEPAGE GOVERNED ECOSYSTEM: PASS: observed
Site Governance Observatory status mirror: validated
terminal orchestration receipt: COMPLETED
```

Current main subsequently advanced through generated-state persistence to `290c5ab41e6aa164579bf8946341e764e2f0a68c`.

This proves the repository-local `all-local` validation/orchestration path is currently clean. It does not itself prove every external runtime, public route, provider, credential, or activation lane complete.


## Evaluator review v0.2 public observation — complete

```text
issue: #589
state: COMPLETE_VALIDATED_MERGED_PUBLICLY_OBSERVED
PR: #598
merge: 1d1e5f0535db5a967fc75f8acd92fb2e0a0d0165
main public verifier: 33228826510 SUCCESS
artifact: 9707785332
artifact digest: sha256:27a64910d7a137313cc790c6a4df69ae6977b1a3ccaaad6d96cf18c3ae470354
public HTML: https://stegverse.org/evaluator-review.html
public projection: https://stegverse.org/data/evaluator-review/cross-framework-current-basis-001.json
SDK head: c9b8935309e69d3a6f70e4ad4ef5dd55fb8a9aac
source blob: 2dd0468779975d18ad53dfe400e1d2fcf83650c3
DRAFT_PRE_FREEZE: observed
approval/freeze/execution/results: absent
authority effect: NONE
activation effect: false
```

This is publication/public-read observation only. Consequential evaluator review actions remain fail-closed until an authorized StegVerse review bridge exists; approval, freeze, execution, replay, reconstruction, and results remain separate gates.

## Pre-work claim terminalization maintenance — 2026-08-29

Site issue #611 repairs a governance dead-end in the pre-work claim system.

Observed defect:

```text
implementation PR completes
-> claim should become terminal
-> release-only PR changes only its claim fragment
-> proposed tree no longer has an active claim for that branch
-> orchestrator rejects the PR solely because the claim is correctly terminal
```

The repaired rule remains fail-closed. A pull request without a current active branch claim is admitted only when all changed files are under `data/session-work-claims.d/*.json`, no claim is added or removed, exactly one existing claim changes, its base state is active, its proposed state is terminal, protected identity/ownership/dependency/handoff/credential/authority fields are byte-equivalent as parsed JSON, and required release evidence is present.

Allowed terminalization-only mutable fields:

```text
state
role
pull_request
release_commit
claim_released_at
archive_eligible
```

Authority constraints remain:

```text
authority_effect = false
activation_effect = false
exactly-one-active-claim rule for implementation PRs = unchanged
branch-name exemption = not sufficient
claim add/remove through terminalization path = rejected
non-claim file through terminalization path = rejected
```

Source:

```text
issue: StegVerse-Labs/Site#611
claim: SITE-PREWORK-CLAIM-TERMINALIZATION-611-20260829
script: scripts/site_handoff_orchestrator.py
tests: tests/test_site_handoff_orchestrator_claim_release.py
state: IMPLEMENTED_ON_BRANCH_VALIDATION_PENDING
```

After this repair merges, the pending completed #607 HIL pretransport-staging claim must be re-terminalized through this exact maintenance path and its release PR must pass the normal Site orchestration/bootstrap/heartbeat gates.

### Shallow-checkout compatibility continuation

Real release PR #613 proved the terminalization-only rule under the dedicated Site Handoff Orchestrator workflow, but Ecosystem Heartbeat exposed a different checkout shape: its default shallow checkout does not guarantee `HEAD^1` is locally available.

The detector now preserves the same fail-closed semantics with two evidence paths:

```text
full-history checkout:
  git diff HEAD^1..HEAD
  git show HEAD^1:<claim-fragment>

shallow pull-request checkout:
  pull_request event number/base SHA
  GitHub PR files API
  exact base claim fragment from contents API at pull_request.base.sha
```

The API fallback is used only when local git parent evidence is unavailable. It still requires claim-registry-only changed files, fewer than 100 returned PR-file rows in the bounded single-page fallback, no claim add/remove, exactly one active-to-terminal claim transition, protected-field equality, existing handoff, release evidence, and zero authority/activation effect.

Focused regression tests explicitly force local git parent failure and prove both changed-file and base-fragment fallback paths.


## Resident rendezvous request client — issue #768

Site now has a bounded browser client lane for submitting the exact already-defined StegOS/KV resident execution request to the StegVerse Service Gateway rendezvous. The browser does not accept arbitrary tasks/commands/argv or credential values, computes the exact request digest with WebCrypto, limits the lease to one hour, omits cross-origin credentials, and marks ambiguous POST outcomes `VERIFY_EXTERNALLY` with blind retry disabled.

Scoped handoff: `docs/RESIDENT_RENDEZVOUS_CLIENT_MIRROR_HANDOFF.md`.
Source: `assets/kv-ui/resident-rendezvous-client.js`.

This is a request carrier only. WorkerCoordinator remains the execution admission authority and live Gateway/resident consumption remain separate evidence gates.


## Legacy claim terminalization zero-effect compatibility — issue #824

A legacy Site claim can predate the explicit `authority_effect` and `activation_effect` fields. The terminalization-only maintenance path previously required those fields to be literally `false` while also forbidding addition of protected fields, making a legacy omitted-field claim impossible to release.

The compatibility rule is now:
```text
base omits authority_effect AND current omits authority_effect -> zero-effect compatible
base omits activation_effect AND current omits activation_effect -> zero-effect compatible
present false -> accepted under existing protected-field equality
present true -> rejected
field introduced/removed during terminalization -> rejected as protected-field drift
```

All other terminalization constraints remain unchanged: claim-registry-only delta, exactly one active-to-terminal claim, protected ownership/dependency/handoff fields unchanged, release PR/commit/time evidence required, and no activation or authority creation.

This repair exists specifically so already-completed legacy claims can be released without weakening collision enforcement. It does not make implementation work or runtime activation manually startable.


## 2026-08-31 request-003 shared-HB terminal propagation — issue #829

The current browser/iPhone rendezvous producer emits exactly:
```text
RESIDENT-EXEC-STEGOS-KV-INTR-CHAIN-003
```

The request retains the canonical three-step chain and does not reintroduce endpoint fanout. Request 003 reflects the stronger resident terminal boundary: a DEVICE_KV terminal must retain and independently validate both exact shared HB carrier signals in addition to the underlying exact transport/recovery predicates.

This browser surface remains a request carrier only. It grants no claim, fence, WorkerCoordinator execution authority, heartbeat progression authority, credential, route, transition, receiving, KV mutation, repository, deployment, or release authority. Ambiguous submission still forbids blind retry.
