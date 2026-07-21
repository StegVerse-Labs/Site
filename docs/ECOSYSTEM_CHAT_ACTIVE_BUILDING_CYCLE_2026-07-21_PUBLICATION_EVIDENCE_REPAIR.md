# Ecosystem Chat Active Building Cycle — Publication Evidence Repair

## Cycle date

2026-07-21

## Active goal

Complete the governed Ecosystem Chat vertical slice:

request → governed provider response → usage persistence → custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation.

## Proven state entering cycle

- Canonical StegDeploy runtime executed successfully through authoritative-source fallback in `StegVerse-org/core-node-runtime-demo` PR #8, merge `6f40cb7110823c48527efadd90c13d87b5cf2455`.
- Authoritative adapter checkout, canonical Dockerfile build, fail-closed gateway startup, live `/health`, and core-node compatibility passed.
- Existing retained image-publication receipt identifies `ghcr.io/stegverse-org/llm-adapter` digest `sha256:7fb9b072bcbbfa893e9db5981a9323d718271a9afee6d382891a3ab4ccffee58` from run `29866501493`.
- Cross-repository pull from `core-node-runtime-demo` was denied, so the consumer used `AUTHORITATIVE_SOURCE_BUILD`.

## Required capability

Retain exact canonical image publication and post-publication pull outcomes so package build/push/attestation/access failures are distinguishable and persistent-host readiness is evidence-bound.

## Existing candidate selected

Repository: `StegVerse-org/LLM-adapter`

Path: `.github/workflows/stegdeploy-image.yml`

Decision: bounded modification of the existing canonical image workflow.

No new image, registry, executor, host, deployment architecture, receipt authority, provider service, custody service, or heartbeat mechanism was created.

## Work performed

- Reused the existing canonical image workflow, image name, tags, Dockerfile, provenance, SBOM, GHCR registry, and repository receipt path.
- Added explicit stage outcomes for registry authentication, build/publish, attestation, and fresh post-publication pull verification.
- Added OCI source linkage metadata.
- Added an always-written `PUBLISHED` or `BLOCKED` v2 publication receipt.
- Added exact verification-pull output retention.
- Preserved fail-closed enforcement after evidence retention.
- Updated `StegVerse-org/LLM-adapter#18` to reflect the actual successful machine-execution state and current package/persistent-host boundaries.

## Runtime action

The workflow repair was committed on `main` as `a6663152d562710ff7438d1a968805bbd83bdf06`, which is within the existing workflow path trigger.

## State classification

- Canonical runtime source build: VERIFIED.
- Fail-closed gateway startup: VERIFIED.
- Gateway `/health`: VERIFIED.
- Core-node compatibility: VERIFIED.
- Canonical image publication: previously evidenced by retained v1 receipt.
- Cross-repository package pull: BLOCKED in the observed consumer run.
- Publication v2 outcome: TRIGGERED; not yet retained at cycle observation.
- Persistent public gateway: NOT LIVE.
- Real provider use: UNPROVEN.
- Provider usage persistence: UNPROVEN.
- Custody and reconstruction: UNPROVEN.
- Immutable activation receipt: UNPROVEN.
- Site activation: UNPROVEN.
- Downstream ingestion: UNPROVEN.

## Removals proposed but not performed

None.

No existing workflow, image, package, gateway, adapter, deployment path, portable-node path, receipt, custody path, Site consumer, downstream consumer, or heartbeat component was removed, disabled, renamed, replaced, or superseded.

## Goal delta

The canonical publication path now retains exact success or blocker evidence and independently verifies the resulting `main` image pull before declaring publication success.

## Reuse delta

The existing GHCR workflow, canonical Dockerfile, metadata, provenance, SBOM, receipt path, and source-build fallback eliminated the need for a new image, registry, deployment package, or host architecture.

## Runtime evidence

- Machine execution: `StegVerse-org/core-node-runtime-demo` PR #8 / merge `6f40cb7110823c48527efadd90c13d87b5cf2455`.
- Existing publication receipt: `StegVerse-org/LLM-adapter/receipts/stegdeploy-image-publication.json`.
- Publication evidence repair: `a6663152d562710ff7438d1a968805bbd83bdf06`.

## Non-progress

- The workflow repair does not create a persistent endpoint.
- Image publication does not authorize deployment, provider execution, custody, or release.
- Site record updates do not complete a runtime gate.

## Next executable step

Inspect the v2 retained publication receipt. If `PUBLISHED`, re-run the existing core-node intake against the published image. If `BLOCKED`, repair only the first retained publication blocker.

After package evidence is resolved, the next vertical-slice boundary is persistent authorized hosting of the existing canonical StegDeploy runtime. Applying Render or another paid/public host requires explicit deployment, cost, and secret-boundary authority and was not performed.

## Manual user action requirement

False for the publication-evidence path. Explicit approval is required before any live infrastructure attachment, paid hosting action, provider credential injection, Master-Records credential injection, or deployment-authority action.
