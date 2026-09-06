# HIL Final Activation Mirror Handoff

Updated: 2026-09-05
Repository: `StegVerse-Labs/Site`
Branch: `main`

## Source of truth

This file is the canonical HIL operational continuation record for Site. Read it with:

1. `docs/HIL_TV_TVC_AUTHORITY_MIRROR_HANDOFF.md`
2. `docs/HIL_SITE_MIRROR_HANDOFF.md`
3. `docs/HIL_EXECUTION_SESSION_PROMPT.md`
4. `docs/SV002_HIL_HB_INTR_CARRIER_MIRROR_HANDOFF.md`
5. `docs/CANONICAL_CARRIER_MATERIALIZATION_MIGRATION_MIRROR_HANDOFF.md`
6. `StegVerse-Labs/TVC/TVC_MIRROR_HANDOFF.md`
7. `StegVerse-Labs/TVC/docs/HIL_TVC_MIRROR_HANDOFF.md`
8. `StegVerse-Labs/TVC/config/hil_runtime_contract.json`
9. `StegVerse-Labs/TVC/config/package_registry.json`
10. `StegVerse-Labs/.github/handoffs/SHWP-HIL-SOVEREIGN-RECEIVER-001.json`
11. `StegVerse-Labs/.github/control/worker-registry.d/hil-sovereign-receiver-001.json`
12. `StegVerse-Labs/.github/control/cross-task-coordination.json#PRED-RESIDENT-REQUEST-CONSUMED-HIL-SOVEREIGN-RECEIVER-002`

Live repository state and authentic runtime evidence supersede older chat summaries, stale issue wording, and older deployment assumptions.

## Final goal

Activate the HIL v1.1 participant lifecycle end-to-end with governed intake, exact-byte preservation and verification, deterministic reconstruction, durable receipts, private review, separately authenticated publication, Site projection, Master Record release, release/tag evaluation, and authorized downstream verification.

## Current authority architecture

HIL activation does **not** use user-managed GitHub tokens or Site-held provider credentials.

Protected values and scoped credential authority belong to TV/TVC. Site is a participant-facing ingress/projection surface and must not store, export, resolve, or fall back to GitHub credentials or equivalent provider authority.

Canonical direction:

```text
Site participant surface
  -> Universal InTr materialization request
  -> shared HB/oscillator-derived carrier binding
  -> InTr/Interlock admissible transition
  -> same-device ESRL/runtime materialization
  -> local identity/readiness verification
  -> ESRL LEASE_OPEN
  -> WorkerCoordinator claim/fresh-fence execution ownership
  -> HIL sovereign receiver
  -> exact-byte verification + reconstruction + receipts
  -> TVC lifecycle
  -> private review
  -> separately authenticated publication
  -> Site projection
  -> CGE / Master Record / downstream release decisions
```

Authority separation remains:

```text
HB / oscillator: synchronization, timing/reference, freshness, liveness, state correlation, carrier/observability
InTr / Interlock: admissible transition semantics
WorkerCoordinator: execution ownership through claim/fresh fence
TV/TVC: sole credential authority
Site: participant ingress/projection
```

HB/oscillator carrier state grants no execution, admission, credential, routing, transition, claim/fence, publication, custody, or consequence authority by itself.

## Shared HB-derived carrier reconciliation — COMPLETE

The HIL browser path no longer has a missing runtime-carrier implementation problem.

Released repository evidence:

- Site issue `#808` — `Migrate SV002 and HIL to shared HB-derived InTr carrier`: CLOSED / COMPLETED.
- `docs/SV002_HIL_HB_INTR_CARRIER_MIRROR_HANDOFF.md`: `RELEASED_COMPLETE`.
- Site issue `#821` — `Use canonical generated carrier-bound materialization requests`: CLOSED / COMPLETED.
- `docs/CANONICAL_CARRIER_MATERIALIZATION_MIGRATION_MIRROR_HANDOFF.md`: `RELEASED_COMPLETE`.
- replacement PR `#826` merged as `a0efa5ef7abb5d4814c017b84703b14b82010edc`.
- HIL now derives carrier evidence through `StegVerseHBInTrCarrier` and passes the already-derived binding into the canonical generated `buildMaterializationRequest(..., carrierBinding)` path.

Therefore:

```text
MISSING_HIL_RUNTIME_CARRIER_IMPLEMENTATION = FALSE
HIL_SHARED_HB_DERIVED_CARRIER = RELEASED_COMPLETE
HIL_CANONICAL_CARRIER_BOUND_MATERIALIZATION = RELEASED_COMPLETE
```

Do not create another HIL heartbeat, scheduler, oscillator, carrier implementation, runtime owner, second user-operated machine requirement, or HIL-specific execution plane to address the remaining activation gap.

The remaining runtime denominator is **authentic materialization/execution evidence through the already-built shared carrier path**, not missing carrier source.

## Same-device ESRL LEASE_OPEN reconciliation — SOURCE SEMANTICS COMPLETE

The earlier HIL continuation text treated public/shared-Gateway readiness as part of the routine path to ESRL `LEASE_OPEN`. That requirement has been superseded by already-merged same-device source semantics and must not be reintroduced.

Canonical upstream evidence:

- `StegVerse-Labs/StegOS#179`: closed/completed same-device `LEASE_OPEN` implementation.
- `StegVerse-Labs/StegOS@95cb63a823ca86d6a04c44ef5140961ba9161d6a`: same-device local `LEASE_OPEN` source.
- `StegVerse-Labs/.github#889`: closed/completed removal of the required shared-Gateway other-machine dependency.
- `.github` runtime bridge now uses `RendezvousRequirement.NOT_REQUIRED` for routine HIL activation, verifies local runtime identity, and opens the lease after local verification.
- `.github` worker registry retains `SHWP-HIL-SOVEREIGN-RECEIVER-001` as `HANDOFF_READY`, with a fresh fence required and no active claim currently recorded.
- cross-task coordination already owns the exact resident-consumption predicate `PRED-RESIDENT-REQUEST-CONSUMED-HIL-SOVEREIGN-RECEIVER-002`; its state remains `UNKNOWN` until authentic consumption evidence exists.

Current semantics:

```text
same_device_execution_required = true
requires_other_machine = false
routine_HIL_public_gateway_required_for_LEASE_OPEN = false
local_identity_readiness_required_for_LEASE_OPEN = true
public_observation = downstream / optional for local LEASE_OPEN
public_observation_authority_effect = NONE
```

This source reconciliation does **not** prove an authentic `LEASE_OPEN`, WorkerCoordinator claim/fence, receiver READY state, custody, TVC lifecycle admission, reconstruction, publication, or Master Record release.

## Guided participant flow — COMPLETE SOURCE IMPLEMENTATION

`humans-as-interoperability-layer.html` presents HIL as a seven-step evidence-aware participant workflow while retaining the existing governed receiver implementation and authority boundaries.

Current participant sequence:

1. Get the canonical experiment.
2. Open it with an LLM using the exact canonical prompt.
3. Receive one complete response PDF.
4. Preserve the artifact unchanged and calculate local SHA-256 identity.
5. Identify the submission and complete participant assertions.
6. Submit through governed intake, which may preserve the canonical Universal InTr transport/materialization intent before a receiver is READY; receiver readiness and execution remain downstream observations rather than prerequisites to transport initiation.
7. Verify the governed result without overclaiming publication, Master Record release, downstream verification, or product activation.

The page distinguishes participant-confirmed, machine-verified, and governed-accepted states. Local selection/hash validation is explicitly not governed acceptance or StegVerse custody.

Implementation commit: `46be8ce88fb572943d301412f664c3dc8f251967`.

The receipt retry diagnostics/transport-identity coverage gap tracked in Site issue `#1006` is CLOSED / COMPLETED. The current `hil-receipt.html` retry path uses bounded response diagnostics, remains fail-closed on invalid ingress, and validates reuse of the stored `intr_transport_intent.operation_id` before transport retry.

## Historical Cloudflare evidence

The July Cloudflare deployment evidence remains valid historical evidence of a path that failed before provider execution because required Actions values were absent. It is **not** the current activation dependency and must not be used to reintroduce Site-owned secrets.

Historical evidence includes:

```text
data/hil-cloudflare-deployment-failure-evidence-30573565667.json
data/hil-public-runtime-probe-latest.json
data/hil-receiver-deployment-latest.json
```

Those artifacts are retained for provenance only.

## Current verified implementation state

Site authority boundary:

```text
Site may validate participant input: true
Site may hash participant PDF: true
Site may construct bounded non-secret capability/request metadata: true
Site may use canonical shared HB-derived carrier binding: true
Site may use canonical generated carrier-bound InTr materialization request: true
Site may hold GitHub token or equivalent provider authority: false
Site may silently fall back to browser/Vercel/participant credentials: false
```

TVC/runtime source state:

```text
HIL runtime contract: present
HIL package registry entry: present
registered package: hil.site.participant-record.v1
private-review task catalog entry: present
private-review validator/task: present
Site projection receipt builder: present
shared HB-derived HIL carrier integration: RELEASED_COMPLETE
canonical generated carrier-bound materialization: RELEASED_COMPLETE
same-device ESRL LEASE_OPEN source: MERGED + VALIDATED
sovereign receiver source/admission: MERGED + VALIDATED
full authentic participant end-to-end proof: not yet complete
```

## Canonical HIL runtime contract

Current TVC runtime contract identity:

```text
schema_version: TVC-HIL-RUNTIME-CONTRACT-v1
contract_id: tvc.hil.runtime.controlled-cycle.v1
platform_model: PLATFORM_AGNOSTIC_GOVERNED_RUNTIME
runtime package repository: StegVerse-org/LLM-adapter
runtime minimum commit: b2e612dd74d311e0cbe66cd1c1d4758bff129fd4
runtime entrypoint: llm_adapter.combined_gateway:app
transport binding: RESOLVED_BY_TVC
host binding: NONE_REQUIRED
provider binding: NONE_REQUIRED
```

Required controlled-cycle evidence includes runtime package identity, state allocation, distinct capability-role fingerprints, readiness before/after, receiver receipt, runtime transition receipt, exact-byte persistence, provenance persistence, private review receipt, publication record, and stable lookup receipt.

## StegGate / common-runtime integration

HIL remains part of `StegVerse-Labs/StegCore#70` / `StegVerse-Labs/Site#239`.

The HIL consumer must bind to the canonical StegGate runtime identity without creating a HIL-specific evaluator:

```text
runtime_identity: stegverse:steggate:canonical:three-layer:v1
canonical_admissibility_runtime: stegcore.three_layer.evaluate_three_layer
```

Common-runtime evidence remains distinct from the completed HB-carrier and same-device ESRL source reconciliation. Do not reinterpret a missing authentic StegGate/receiver receipt as permission to create a duplicate evaluator, carrier, runtime, or rendezvous dependency.

## Current activation state

```text
HIL package registered in TVC: true
TVC HIL runtime contract present: true
TVC private-review validation path present: true
Site projection receipt builder present: true
shared HB-derived carrier source integration: complete
canonical carrier-bound materialization source integration: complete
guided seven-step participant UX source: complete
receipt retry bounded diagnostics + transport-identity continuity source: complete
same-device local LEASE_OPEN source: complete
resident request: RESIDENT-EXEC-HIL-SOVEREIGN-RECEIVER-002
resident request consumption predicate: UNKNOWN
authentic same-device event -> ESRL LEASE_OPEN: not proven
HIL WorkerCoordinator real claim/fresh fence: not proven
sovereign HIL receiver READY: not proven
public observation/rendezvous: downstream optional for local LEASE_OPEN; not proven
canonical StegGate HIL direct execution evidence: pending
public participant end-to-end proof: pending
exact-byte live controlled-cycle proof: pending
successor-runtime continuity proof: pending
automatic TVC lifecycle receiving receipt: pending
authenticated publication proof: pending
Master Record release: pending
release/tag authority: false
```

## Required continuation path

The next legitimate continuation is authentic execution/evidence through the existing same-device runtime path, not new HIL runtime implementation:

1. Observe authentic consumption of the already-issued `RESIDENT-EXEC-HIL-SOVEREIGN-RECEIVER-002` request or an admitted HIL Universal InTr event on the existing same-device task-control path.
2. Observe same-device ESRL runtime materialization, local identity/readiness verification, and authentic `LEASE_OPEN`. Public/shared-Gateway readiness is not a prerequisite to this transition.
3. Observe the independent HIL WorkerCoordinator claim and fresh fence; do not synthesize or manually mint them.
4. Observe the sovereign HIL receiver report the canonical ready/active state and exact v1.1 readiness.
5. Preserve receiver/custody evidence and, separately, observe any public Site readiness/identity evidence needed for a public participant path. Public observation does not retroactively grant local execution authority.
6. Perform one real participant browser submission or controlled retry only after the relevant public path is actually published/observable, and retain `HIL-RECEIVER-RECEIPT-v2` when authentically returned.
7. Retain exact-byte hash/size/retrieval/restart reconstruction evidence.
8. Observe automatic admission/receiving receipt into the existing TVC HIL lifecycle.
9. Execute and retain private-review evidence through its existing authority.
10. Execute separately authenticated publication and retain append-only publication evidence.
11. Emit and verify Site projection evidence.
12. Continue through CGE/Master Record release and required downstream verification.

Source, merge, CI, handoff readiness, heartbeat progression, request issuance, carrier binding, or publication alone do not satisfy these authentic runtime predicates.

## Remaining modules and destinations

```text
StegVerse-Labs/.github / canonical resident runtime lane
- authentic consumption of RESIDENT-EXEC-HIL-SOVEREIGN-RECEIVER-002 or admitted HIL event
- same-device ESRL LEASE_OPEN evidence
- independent WorkerCoordinator claim/fresh-fence receipt
- sovereign HIL receiver READY evidence
- optional downstream public-observation evidence when a public participant path is exercised

StegVerse-Labs/TVC
- authentic HIL lifecycle receiving/admission receipt
- private-review execution evidence
- publication lifecycle evidence
- canonical StegGate runtime-identity evidence where required

StegVerse-Labs/Site
- deployed observation of the current participant/receipt source
- public route/readiness observation when needed for the participant path
- one real participant end-to-end browser submission or controlled retry
- durable returned receiver receipt projection
- exact-byte post-restart verification projection

master-records/orchestration
- custody/reconstruction and Master Record release after authentic upstream evidence exists

After verified activation/release
- GCAT-BCAT-Engine/Publisher
- StegVerse-Labs/admissibility-wiki
- StegVerse-002/stegguardian-wiki
- StegVerse-Labs/Sit only after repository identity and role are independently verified
```

## Master Records boundary

`docs/HIL_FIRST_MASTER_RECORD_RELEASE_PREPARATION.md` remains authoritative for first-release preparation. Its readiness ledger must remain `WAITING_FOR_AUTHORIZED_EXTERNAL_CYCLE` until authentic external-cycle and Site-import evidence exists. Same-device source completion, CI, source publication, screenshots, manually entered hashes, or fixture values cannot substitute for the required custody/reconstruction/review/publication evidence.

## Release posture

No HIL tag or release is authorized yet. Release requires authentic live controlled-cycle evidence, genuine participant completion, private review, authenticated publication, Site projection, Master Record release, and required downstream verification.

## User-machine boundary

No second user-operated machine is required or authorized as an activation prerequisite. Same-device execution is the canonical routine HIL activation model. Remote/public peers may be used only as optional downstream observation or participant transport surfaces; they may not become a required second-machine execution dependency or production authority. No GitHub token, NON-TV/TVC credential, manual third-party hosting setup, or separate developer machine is a legitimate HIL activation requirement.

## Archive readiness

The current authority architecture, completed HB/oscillator carrier migration, canonical generated InTr materialization migration, same-device ESRL LEASE_OPEN source semantics, guided participant UX, receipt retry diagnostics/continuity repair, remaining authentic runtime evidence denominator, downstream destinations, and continuation sequence are repository-resident. The complete prior conversation thread is not required to continue.
