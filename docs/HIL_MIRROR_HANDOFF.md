# HIL Final Activation Mirror Handoff

Updated: 2026-09-03
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
  -> ESRL/runtime materialization
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

## Guided participant flow — COMPLETE SOURCE IMPLEMENTATION

`humans-as-interoperability-layer.html` now presents HIL as a seven-step evidence-aware participant workflow while retaining the existing governed receiver implementation and authority boundaries.

Current participant sequence:

1. Get the canonical experiment.
2. Open it with an LLM using the exact canonical prompt.
3. Receive one complete response PDF.
4. Preserve the artifact unchanged and calculate local SHA-256 identity.
5. Identify the submission and complete participant assertions.
6. Submit through governed intake only after the existing receiver readiness/identity boundary permits it.
7. Verify the governed result without overclaiming publication, Master Record release, downstream verification, or product activation.

The page distinguishes participant-confirmed, machine-verified, and governed-accepted states. Local selection/hash validation is explicitly not governed acceptance or StegVerse custody.

Implementation commit: `46be8ce88fb572943d301412f664c3dc8f251967`.

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

Common-runtime evidence remains distinct from the completed HB-carrier migration. Do not reinterpret a missing authentic StegGate/receiver receipt as permission to create a duplicate evaluator or carrier.

## Current activation state

```text
HIL package registered in TVC: true
TVC HIL runtime contract present: true
TVC private-review validation path present: true
Site projection receipt builder present: true
shared HB-derived carrier source integration: complete
canonical carrier-bound materialization source integration: complete
guided seven-step participant UX source: complete
public receiver READY: not proven
authentic event -> ESRL LEASE_OPEN: not proven
authentic public /intr/materialization execution: not proven
HIL WorkerCoordinator real claim/fresh fence: not proven
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

The next legitimate continuation is evidence/execution through the existing shared runtime path, not new HIL runtime implementation:

1. Observe an authentic event carried through the canonical HB/oscillator-derived binding into Universal InTr materialization.
2. Observe ESRL runtime materialization and `LEASE_OPEN` through the existing shared runtime/Gateway path.
3. Observe the independent HIL WorkerCoordinator claim and fresh fence; do not synthesize or manually mint it.
4. Observe the sovereign HIL receiver report `ACTIVE_SOVEREIGN_RECEIVER` and exact v1.1 readiness.
5. Observe the public Site control become `READY` from that receiver evidence.
6. Perform one real participant browser submission and retain `HIL-RECEIVER-RECEIPT-v2`.
7. Retain exact-byte hash/size/retrieval/restart reconstruction evidence.
8. Observe automatic admission/receiving receipt into the existing TVC HIL lifecycle.
9. Execute and retain private-review evidence through its existing authority.
10. Execute separately authenticated publication and retain append-only publication evidence.
11. Emit and verify Site projection evidence.
12. Continue through CGE/Master Record release and required downstream verification.

Source, merge, CI, handoff readiness, heartbeat progression, request issuance, or carrier binding alone do not satisfy these authentic runtime predicates.

## Remaining modules and destinations

```text
StegVerse-Labs/.github / canonical resident runtime lane
- authentic event-driven consumption of the already-issued HIL resident/runtime request
- ESRL LEASE_OPEN evidence
- shared Gateway READY evidence
- independent WorkerCoordinator claim/fresh-fence receipt
- sovereign HIL receiver READY evidence

StegVerse-Labs/TVC
- authentic HIL lifecycle receiving/admission receipt
- private-review execution evidence
- publication lifecycle evidence
- canonical StegGate runtime-identity evidence where required

StegVerse-Labs/Site
- deployed observation of the seven-step participant UX after publication of current main
- public receiver READY observation
- one real participant end-to-end browser submission
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

## Release posture

No HIL tag or release is authorized yet. Release requires authentic live controlled-cycle evidence, genuine participant completion, private review, authenticated publication, Site projection, Master Record release, and required downstream verification.

## User-machine boundary

No second user-operated machine is required or authorized as an activation prerequisite. The current participant device may participate in the browser experiment, but the participant device does not become the sovereign receiver/runtime authority. No GitHub token, NON-TV/TVC credential, manual third-party hosting setup, or separate developer machine is a legitimate HIL activation requirement.

## Archive readiness

The current authority architecture, completed HB/oscillator carrier migration, canonical generated InTr materialization migration, guided seven-step participant UX, remaining authentic runtime evidence denominator, downstream destinations, and continuation sequence are repository-resident. The complete prior conversation thread is not required to continue.
