# Ecosystem Chat Active Building Cycle — Persistent Host Reuse Decision

Date: 2026-07-21

## Active goal

Complete the first hosted Ecosystem Chat vertical slice:

`request → governed provider response → usage persistence → custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation`

## Work performed

- Re-read the authoritative Site handoff, build-goal record, and active-building record.
- Inspected `StegVerse-org/LLM-adapter#18`, `StegVerse-org/core-node-runtime-demo#5`, and `StegVerse-Labs/Site#16`.
- Inspected the existing canonical `compose.stegdeploy.yaml`, the existing `render.yaml`, and the core-node repository's established `.github/workflows/validate.yml`.
- Evaluated reuse unchanged, bounded modification, adapter, and replacement options for the persistent-host boundary.
- Updated `StegVerse-org/LLM-adapter#18` with the full reuse evaluation and deployment-authority boundary.
- Opened `StegVerse-Labs/Site#24` as the explicit persistent-host authority decision.

## Existing ecosystem components reused

- `StegVerse-org/LLM-adapter/Dockerfile`
- `StegVerse-org/LLM-adapter/compose.stegdeploy.yaml`
- `StegVerse-org/LLM-adapter/scripts/container-entrypoint.sh`
- `StegVerse-org/LLM-adapter/scripts/stegdeploy_bootstrap.py`
- `StegVerse-org/LLM-adapter/.github/workflows/stegdeploy-image.yml`
- `StegVerse-org/LLM-adapter/render.yaml`
- `StegVerse-org/core-node-runtime-demo/.github/workflows/validate.yml`
- existing provider integration
- existing Master-Records custody and reconstruction binding
- existing verifier and immutable receipt retention
- existing Site activation and downstream consumers

## Existing candidates evaluated

### Canonical StegDeploy runtime

Classification: directly reusable unchanged.

Reusable behavior: durable storage contract, environment binding, health verification, provider-neutral image, fail-closed defaults, provenance, and deployment receipts.

Missing behavior: an already-authorized persistent host must execute it and supply provider and custody configuration through its existing secret boundary.

### Existing Render Blueprint

Classification: reusable with bounded modification.

Reusable behavior: existing service identity, hostname, build/start command, health path, and fail-closed environment structure.

Missing or incompatible behavior:

- `/tmp` database paths;
- `STEGVERSE_STORAGE_DURABLE_ACROSS_RESTARTS=false`;
- provider disabled;
- Master-Records directed to `127.0.0.1:9`;
- no server attached behind the existing Render hostname;
- application or modification may create paid infrastructure and exercises deployment authority.

### Core-node runtime demo

Classification: reusable for ephemeral compatibility execution only.

Reusable behavior: canonical image pull, fail-closed launch, health verification, comparison pipeline, tests, and hash-bound compatibility receipt.

Incompatibility: GitHub-hosted runners cannot provide the persistent public endpoint or provider/custody authority required by the active goal.

## Options and recommendation

1. Reuse canonical StegDeploy unchanged on an existing authorized persistent host.
   - Progress: directly enables the next runtime boundary.
   - Effort: low once the host exists.
   - Technical risk: low.
   - Governance impact: preserves existing authority boundaries.
   - Existing consumers: unchanged.
   - Reversibility: high.
   - Recommendation: preferred.

2. Apply a bounded modification to the existing Render Blueprint.
   - Progress: may restore the known public hostname.
   - Effort: low-to-medium.
   - Technical risk: medium because no service is attached.
   - Governance impact: requires explicit deployment and cost authority.
   - Existing consumers: public endpoint can remain stable.
   - Reversibility: repository changes are reversible; provider-side resource effects may not be.
   - Recommendation: viable only after explicit approval.

3. Add a hosting adapter.
   - Progress: none beyond the canonical bootstrap.
   - Effort and risk: unnecessary duplication.
   - Recommendation: do not build.

4. Build a new host architecture.
   - Progress: duplicates existing deployment capability.
   - Effort and risk: high.
   - Governance impact: creates a duplicate deployment-authority surface.
   - Recommendation: do not build.

## Components modified

- `StegVerse-org/LLM-adapter#18` — updated with exact candidate evaluation, options, and authority boundary.

## Adapters or new runtime components added

None.

## Runtime tests actually executed

- Queried commit status for `StegVerse-org/core-node-runtime-demo@62b87d6918977f6bcbc909955b4a765460e04238`.
- Result: no workflow status was published.
- Inspected the established workflow source and confirmed it is configured for `push` on `main`, `pull_request`, and `workflow_dispatch`.
- No provider request, deployment, custody operation, reconstruction, or live endpoint execution occurred.

## Observed results

- The canonical runtime is sufficient; no replacement gateway or host adapter is justified.
- The existing Render descriptor is a bounded deployment candidate, not a missing architecture.
- The exact remaining boundary is authority to attach an already-authorized persistent host.
- The core-node compatibility workflow remains IMPLEMENTED/INTEGRATED but not EXECUTED by published evidence.

## State classification

- Canonical StegDeploy runtime: IMPLEMENTED and INTEGRATED
- Existing Render Blueprint: IMPLEMENTED, NOT DEPLOYED
- Core-node compatibility intake: IMPLEMENTED and INTEGRATED, EXECUTION NOT OBSERVED
- Persistent public host: NOT DEPLOYED
- Real provider request/response: UNPROVEN
- Usage persistence: UNPROVEN
- Custody and reconstruction: UNPROVEN
- Immutable VERIFIED receipt: UNPROVEN
- Site activation: UNPROVEN
- Downstream propagation: UNPROVEN

## Durable evidence produced

- Deployment-owner evaluation: https://github.com/StegVerse-org/LLM-adapter/issues/18
- Persistent-host authority decision: https://github.com/StegVerse-Labs/Site/issues/24
- Existing core-node execution task: https://github.com/StegVerse-org/core-node-runtime-demo/issues/5

## Removals proposed but not performed

None.

The overlapping portable-node packaging remains retained. No file, workflow, gateway, deployment descriptor, heartbeat component, provider integration, custody path, receipt path, or downstream consumer was removed, disabled, renamed, replaced, or superseded.

## Goal delta

No runtime gate advanced. The remaining deployment boundary is now narrowed to a concrete authority decision between reuse of an existing authorized host and bounded alignment of the existing Render Blueprint.

## Reuse delta

The canonical StegDeploy runtime and existing Render service descriptor eliminated the need for a new gateway, hosting adapter, deployment schema, runtime service, or receipt mechanism.

## Runtime evidence

No live runtime evidence was produced. The exact negative evidence is that GitHub publishes no status for the integrated core-node workflow commit, while the configured Render endpoint remains unattached.

## Non-progress

- Issue and Site record updates do not complete a runtime gate.
- Candidate evaluation does not deploy the gateway.
- Existing workflow configuration does not prove execution.

## What was proposed but not changed

- Bounded alignment/application of `render.yaml`.
- Execution of canonical StegDeploy on an existing authorized persistent host.

Both remain unperformed because either action exercises deployment authority; Render may also incur cost.

## Next executable step

Obtain explicit selection at https://github.com/StegVerse-Labs/Site/issues/24:

- `AUTHORIZE_EXISTING_HOST`, or
- `AUTHORIZE_RENDER_ALIGNMENT`, or
- `NO_DEPLOYMENT_AUTHORITY`.

After authorization, reuse the canonical StegDeploy runtime, execute one governed request, retain the first exact verifier result, and repair only the first observed runtime failure.
