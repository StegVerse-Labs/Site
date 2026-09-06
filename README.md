# StegVerse-Labs / Site

Public mirror for the StegVerse ecosystem. Renders proof surfaces, transition status,
governance documentation, and product information from canonical source data.

**Live site:** https://stegverse-labs.github.io/Site/

---

## Boundary

```
formalism-tests    =  proof/test authority
StegVerse-002      =  governed deployment authority
Site               =  public mirror only
Ecosystem Chat     =  text-only user advancement surface, not proof authority or shell authority

Site publishes receipts. Site does not generate them.
Site must never become the authority for receipts, transitions, accreditation, shell execution, credentials, or repository administration.
```

### Ecosystem Chat boundary markers

```text
raw_shell_allowed=false
authority_required=true
rate_limit_required=true
receipt_required_for_execution=true
Restricted admin=false for public Site runtime
```

---

## Site structure

### Public pages

| Page | Purpose |
|------|---------|
| [`index.html`](index.html) | Home — proof status, product overview, live evidence |
| [`ecosystem-chat.html`](ecosystem-chat.html) | User advancement console — local route scaffold, no shell, no credential authority, no proof authority |
| [`tga-reexamine.html`](tga-reexamine.html) | Temporal Governed Analysis “Re-examine” projection — exact source/time/rule-context/provenance/variance display with local-only media binding; projection is not ground truth or adjudicative authority |
| [`demo.html`](demo.html) | Execution demo — commit-boundary decision with receipt hash |
| [`stegverse-002.html`](stegverse-002.html) | StegVerse-002 / core-lite mirror — gate map, live evidence |
| [`formalism-tests-stage-1-to-31.html`](formalism-tests-stage-1-to-31.html) | Stage 1–31 proof mirror — Beta_Orionis / StegVerse-001 |
| [`stegfinco.html`](stegfinco.html) | StegFinCo — governed financial execution layer |
| [`product.html`](product.html) | Trust & Risk Systems Audit — product details |
| [`pricing.html`](pricing.html) | Pricing — rendered from canonical manifest |
| [`methodology.html`](methodology.html) | Methodology — evidence over self-attestation |
| [`about.html`](about.html) | About StegVerse |
| [`support.html`](support.html) | Support StegVerse Research |
| [`Papers.html`](Papers.html) | Papers and research |

### StegOS same-device operational cards

`stegos-bootstrap/` provides the same-device operational-card UX used to retain and
reuse completed local workflow data without turning Site into an authority plane.
The explicit offline shell now includes `persistent-card-ux.js` and all eleven
card-help routes. The service-worker cache generation is
`stegos-web-bootstrap-v12`, so an installed client that receives this source can
replace the prior shell generation and receive the governed SV001 Master Records
custody path rather than retaining the previous shell behavior.

The normal Master Records path reuses an exact same-device persisted SV001 proof
when one is available. Exact manual proof import remains a fallback for legacy
pre-persistence evidence. The terminal SV001 bounded-autonomy cycle must not be
rerun merely to obtain Master Records custody.

SV001 Master Records custody/reconstruction is a machine-owned transition even when
the execution surface is the current iPhone. Before the Site same-device carrier may
invoke the canonical Master Records portable custody module or append custody and
reconstruction state, the exact
`SV001_MASTER_RECORDS_CUSTODY_AND_RECONSTRUCTION` transition must receive a fresh,
write-once admission from the existing root Universal InTr service worker. The
admission is bound to the registered Node/Interlock, exact canonical G23 source
receipt hash, machine-governed authority class, and current HB-derived carrier
reference. A prior SV001 receipt is evidence input only and never authorizes custody.
Missing, mismatched, stale, or partial admission fails closed before Master Records
mutation. This path adds no human approval checkpoint and does not create a second
InTr runtime, scheduler, WorkerCoordinator, credential path, or custody authority.

Offline caching and same-device UI persistence do not establish Master Records custody,
reconstruction PASS, SV002 disposition, deployment, or device activation. Site remains
an exact materialization/persistence carrier only; WorkerCoordinator claim/fence
ownership, TV/TVC credential authority, Master Records custody authority, and InTr
transition authority are unchanged. Source, merge, validation, cache generation, or
publication must not be substituted for authentic current-device evidence.

Relevant source surfaces:

| File | Purpose |
|------|---------|
| [`stegos-bootstrap/persistent-card-ux.js`](stegos-bootstrap/persistent-card-ux.js) | Same-device card persistence, completed/incomplete presentation, Copy Text controls, help links, and exact retained SV001-proof discovery |
| [`stegos-bootstrap/stegos-bootstrap.js`](stegos-bootstrap/stegos-bootstrap.js) | Same-device browser carrier that constructs the exact Node-bound machine-governed SV001 custody trigger and obtains root Universal InTr admission before nested custody execution |
| [`stegos-bootstrap/service-worker.js`](stegos-bootstrap/service-worker.js) | Explicit offline-shell cache plus existing device-local governed endpoints; cache generation `stegos-web-bootstrap-v12`; validates and retains the root InTr admission before new Master Records custody/reconstruction mutation |
| [`intr-service-worker.js`](intr-service-worker.js) | Existing root Universal InTr runtime, including bounded `MasterRecords:SV001Custody` admission alongside the existing KV and HIL profiles |
| [`stegos-bootstrap/help/`](stegos-bootstrap/help/) | Per-card purpose, remediation, and troubleshooting pages cached for offline use |
| [`docs/STEGOS_PERSISTENT_CARD_UX_MIRROR_HANDOFF.md`](docs/STEGOS_PERSISTENT_CARD_UX_MIRROR_HANDOFF.md) | Canonical bounded handoff and completion predicates for Site issue #1000 |
| [`docs/MR_SV001_CURRENT_IPHONE_CUSTODY_MIRROR_HANDOFF.md`](docs/MR_SV001_CURRENT_IPHONE_CUSTODY_MIRROR_HANDOFF.md) | Master Records same-device custody authority boundary and authentic-runtime requirements |
| [`scripts/validate_stegos_persistent_card_ux.py`](scripts/validate_stegos_persistent_card_ux.py) | Deterministic source/offline-shell completeness validator |
| [`scripts/check_mr_sv001_intr_governance.py`](scripts/check_mr_sv001_intr_governance.py) | Deterministic fail-closed validator for the root-InTr-to-Master-Records custody governance chain |

### Temporal Governed Analysis projection

The TGA Site surface projects canonical Temporal Governed Analysis records without becoming their truth or adjudication authority.

| File | Purpose |
|------|---------|
| [`tga-reexamine.html`](tga-reexamine.html) | Human-readable projection separating observed/encoded events, governing context, evaluation, uncertainty, and provenance |
| [`assets/tga-reexamine.js`](assets/tga-reexamine.js) | Browser renderer and user-local video binding via `URL.createObjectURL`; no external media acquisition |
| [`data/tga/tga-site-sample.json`](data/tga/tga-site-sample.json) | Synthetic bounded counterfactual sample preserving exact temporal window, unresolved evidence, authority effect, and custody posture |
| [`scripts/check_tga_site_projection.py`](scripts/check_tga_site_projection.py) | Deterministic validator for the projection contract and non-authorizing boundaries |
| [`docs/TGA_SITE_PROJECTION_MIRROR_HANDOFF.md`](docs/TGA_SITE_PROJECTION_MIRROR_HANDOFF.md) | Canonical goal handoff, merge/validation evidence, invariants, and downstream continuation |

TGA boundary rules:

```text
canonical_representation != canonical_reality
encoding_precision != correctness
media_reference != media_custody
counterfactual_projection != historical_applicability
unresolved_evidence = unresolved
Site_TGA_authority_effect = NONE_PROJECTION_ONLY
```

The Site renderer does not grant legal, officiating, enforcement, publication, custody, or adjudicative authority. Public deployment/reachability is separate evidence and must not be inferred from source merge.

### Ecosystem chat activation

| File | Purpose |
|------|---------|
| [`assets/ecosystem-chat.js`](assets/ecosystem-chat.js) | Browser-side text-only console logic, local route scaffold, restricted-admin detection, fail-closed gateway adapter |
| [`docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md`](docs/ECOSYSTEM_CHAT_GATEWAY_CONTRACT.md) | Backend activation contract for `POST /api/ecosystem-chat`, allowed-task routing, and receipt boundary rules |
| [`docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md`](docs/ECOSYSTEM_CHAT_FORM_GATEWAY_MODEL.md) | Browser form model for StegVerse-org/SDK entry, manifest window, receipt window, and dropdown-limited fields |
| [`docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md`](docs/ECOSYSTEM_CHAT_BOUNDARY_CHECK.md) | Local verification task for public links, no-shell/no-credential language, authority-required state, and receipt-required fixtures |
| [`docs/ECOSYSTEM_CHAT_SDK_BACKEND_HANDOFF.md`](docs/ECOSYSTEM_CHAT_SDK_BACKEND_HANDOFF.md) | Backend handoff for SDK intake checks over fields, manifest, and receipt_window layers |
| [`docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md`](docs/ECOSYSTEM_CHAT_ACTIVATION_STATUS.md) | Current local-simulation status, installed surfaces, and next backend milestone |
| [`fixtures/ecosystem-chat/request.example.json`](fixtures/ecosystem-chat/request.example.json) | Example gateway request payload for backend implementers |
| [`fixtures/ecosystem-chat/response.example.json`](fixtures/ecosystem-chat/response.example.json) | Example gateway response payload with null receipt state before backend activation |
| [`fixtures/ecosystem-chat/sdk-form-payload.example.json`](fixtures/ecosystem-chat/sdk-form-payload.example.json) | Canonical SDK form payload preserving fields, manifest, and receipt_window layers |
| [`fixtures/ecosystem-chat/sdk-backend-response.example.json`](fixtures/ecosystem-chat/sdk-backend-response.example.json) | Canonical SDK backend response payload with receipt_id null before backend activation |
| [`scripts/check_ecosystem_chat_boundary.py`](scripts/check_ecosystem_chat_boundary.py) | Static checker for the public boundary across page, JavaScript, docs, public links, and fixtures |
| [`scripts/check_ecosystem_chat_contract.py`](scripts/check_ecosystem_chat_contract.py) | Static checker for the console page, gateway adapter, README index, and receipt boundary contract |
| [`data/headless-tasks/ecosystem-chat-boundary-check-v1.json`](data/headless-tasks/ecosystem-chat-boundary-check-v1.json) | Declared task wrapper for `python scripts/check_ecosystem_chat_boundary.py` using the existing headless task registry |
| [`data/headless-task-registry-v1.json`](data/headless-task-registry-v1.json) | Registry containing `ecosystem-chat-boundary-check-v1` |
| `github/workflows/check-ecosystem-chat.yml` | Workflow path shown without leading dot; runs the Ecosystem Chat contract checker on relevant pushes, pull requests, and manual dispatch |
| [`iosnoperiod/iosnoperiod.md`](iosnoperiod/iosnoperiod.md) | iOS no-leading-dot handling note for workflow paths |
| [`iosnoperiod/workflow-map.json`](iosnoperiod/workflow-map.json) | Canonical-to-iOS workflow path manifest |

Direct contract verification command:

```bash
python scripts/check_ecosystem_chat_contract.py
```

Direct boundary verification command:

```bash
python scripts/check_ecosystem_chat_boundary.py
```

### Ecosystem visual render transport

The visual-render transport is a provider-neutral interface between the canonical
`stegverse.ecosystem_visual_projection/v1` document and an optional 2D/3D renderer.
A request binds the exact projection ID/hash, exact source event IDs, requested
renderer capabilities, correlation refs, and intent-only interaction policy. A
receipt binds the request hash, projection hash, renderer/provider identity,
capabilities actually used, render artifact identity/hash or bounded locator,
status, provenance, and selection/refinement intents.

The renderer role is always `PROJECTION_ONLY`. The transport fails closed on
projection or request hash mismatch, source-event mismatch, capability escalation,
missing rendered-artifact identity, or any attempted admission, credential,
publication, custody, execution, evidence, or canonical-event mutation authority.
Provider endpoints and credentials are deployment configuration and are not embedded
in canonical request fixtures.

| File | Purpose |
|------|---------|
| [`schemas/ecosystem-visual-render-request.schema.json`](schemas/ecosystem-visual-render-request.schema.json) | Canonical render-request binding and non-authorizing interaction policy |
| [`schemas/ecosystem-visual-render-receipt.schema.json`](schemas/ecosystem-visual-render-receipt.schema.json) | Returned render receipt, artifact/provenance binding, and all-false authority contract |
| [`assets/ecosystem-visual-render-transport.js`](assets/ecosystem-visual-render-transport.js) | Deterministic hashing, request construction, and fail-closed request/receipt validation |
| [`scripts/check_ecosystem_visual_render_transport.py`](scripts/check_ecosystem_visual_render_transport.py) | Source/README completeness and deterministic Node contract verifier |
| [`docs/ECOSYSTEM_VISUAL_RENDER_TRANSPORT_MIRROR_HANDOFF.md`](docs/ECOSYSTEM_VISUAL_RENDER_TRANSPORT_MIRROR_HANDOFF.md) | Focused continuation, runtime boundary, and next live-integration seam |

Source or CI validation does not prove a live renderer endpoint, Site#242 runtime
activation, Master Records custody, public rendering, or downstream publication.

### Public positioning

| Document | Purpose |
|----------|---------|
| [`docs/public-positioning/ai-safety-to-transition-admissibility.md`](docs/public-positioning/ai-safety-to-transition-admissibility.md) | External bridge from AI safety framing to StegVerse transition admissibility, GLM, EVIDE, and runtime governance |

### Publisher-to-Site paper mirror

| File | Purpose |
|------|---------|
| [`docs/SITE_MIRROR_HANDOFF.md`](docs/SITE_MIRROR_HANDOFF.md) | Current handoff and task source of truth for Publisher-to-Site mirror activation |
| [`docs/SITE_ECOSYSTEM_MANAGEMENT_HANDOFF.md`](docs/SITE_ECOSYSTEM_MANAGEMENT_HANDOFF.md) | Ecosystem-managed continuation handoff for selecting the next safe build action without prior chat context |
| [`docs/SITE_MIRROR_LIVE_VERIFICATION.md`](docs/SITE_MIRROR_LIVE_VERIFICATION.md) | Live verification packet and evidence requirements before activation |
| [`docs/SITE_MIRROR_ACTIVATION_STATUS.md`](docs/SITE_MIRROR_ACTIVATION_STATUS.md) | Activation-state tracker for the mirror system |
| [`docs/README_SITE_PAPERS_MIRROR.md`](docs/README_SITE_PAPERS_MIRROR.md) | Mirror protocol and operational notes |
| [`docs/SITE_PAPER_DISPLAY_POLICY.md`](docs/SITE_PAPER_DISPLAY_POLICY.md) | Public display policy and source-of-truth boundary |
| [`scripts/mirror_papers.py`](scripts/mirror_papers.py) | Mirror generator for paper files, aliases, indexes, and manifest metadata |
| [`scripts/check_paper_display_policy.py`](scripts/check_paper_display_policy.py) | Policy/config checker for mirror readiness |
| [`scripts/check_papers_manifest_metadata.py`](scripts/check_papers_manifest_metadata.py) | Manifest metadata checker for live mirror activation |
| [`scripts/check_site_ecosystem_management_handoff.py`](scripts/check_site_ecosystem_management_handoff.py) | Verifies the ecosystem-managed continuation handoff, pending activation boundary, and next-action rules |
| [`papers/papers_manifest.json`](papers/papers_manifest.json) | Current checked-in paper manifest; must be regenerated by the live mirror before activation |

Current mirror state:

```text
Goal: Continue building without manual actions needed through completion OR until task handoff and task completion is capable of being handled by the ecosystem's own management.
Source of truth: GCAT-BCAT-Engine/Publisher/papers
Target mirror: StegVerse-Labs/Site/papers
Activation state: pending Publisher/Site closure evidence
Management state: ecosystem-managed continuation ready after docs/SITE_ECOSYSTEM_MANAGEMENT_HANDOFF.md and scripts/check_site_ecosystem_management_handoff.py pass
Current delta: checked-in manifest remains pending live Publisher dispatch and Site mirror evidence before activation can be claimed
```

Note: the workflow path starts with a leading dot in the repository. It is shown here without the leading dot as requested: `github/workflows/mirror-papers.yml`.
Note: the Ecosystem Chat workflow path also starts with a leading dot in the repository. It is shown here without the leading dot as requested: `github/workflows/check-ecosystem-chat.yml`.

### Transition pages

| Page | Purpose |
|------|---------|
| [`transition-proof-surface.html`](transition-proof-surface.html) | Proof progression, verified task chain, source artifacts |
| [`transition-release-index.html`](transition-release-index.html) | Release index — all 31 stages, current release state |
| [`transition-development-status.html`](transition-development-status.html) | Current gate, next integration target, SV002 status |
| [`transition-verification-guide.html`](transition-verification-guide.html) | How to verify receipts, task chains, proof artifacts |

### Coherent transition threshold

The coherent-transition threshold posture is derived from committed heartbeat,
repository-orchestration, and repository-task evidence. The threshold activation
task's own expected pre-threshold validator failure is observation evidence, not an
independent readiness blocker; counting it as one would create a circular condition
where the threshold could never become established because it was not already
established.

Only that self-observation is excluded from the independent blocker set. All other
heartbeat, repository-task, runtime, provider-usage, Master Records custody, and
reconstruction blockers remain fail-closed. Removing the circular self-block does
not establish `THRESHOLD_ESTABLISHED`, does not prove runtime execution, and grants
no execution, activation, publication, custody, scientific-claim, or biological-
classification authority. Authentic sovereign-carrier execution and required
custody/reconstruction evidence must still satisfy their canonical predicates before
any dependent activation transition can advance.

### Sovereign endpoint activation readiness

The canonical Ecosystem Chat production route is the StegVerse-owned local/private
runtime carried through the existing WorkerCoordinator/heartbeat lane and TV/TVC
route authority. For that local route, credential authority remains `TV/TVC` and the
credential requirement is `NONE`.

Provider API tokens, Master Records bearer tokens, GitHub tokens, hosted inference,
or a provider-specific stable domain are not canonical activation prerequisites.
The legacy readiness state string `CONFIGURATION_AND_PERSISTENT_EXECUTION_REQUIRED`
is retained only as compatibility vocabulary for existing Site consumers; it must
not be interpreted as requiring those superseded credentials.

Current activation remains fail-closed on authentic sovereign-carrier execution,
private endpoint observation, same-execution E1/E2 evidence, measured usage
persistence, provider-usage reconstruction PASS, transition reconstruction PASS,
an immutable zero-blocker verified receipt, Site activation completion, and verified
downstream propagation. Source, CI, local-model implementation, route-admission
source, or a readiness-record update does not satisfy those predicates.