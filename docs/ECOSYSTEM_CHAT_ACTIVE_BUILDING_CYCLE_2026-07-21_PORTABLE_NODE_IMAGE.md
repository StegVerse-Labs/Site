# Ecosystem Chat Active Building Cycle — Portable-Node Image

## Cycle date

2026-07-21

## Work performed

- Re-read the current Site goal and the machine-owned adapter deployment task.
- Searched the adapter repository for an existing container, GHCR publication path, or self-hosted deployment runner.
- Confirmed no existing repository-owned container or host runner was present.
- Reused the repaired `stegnode` runtime instead of creating a replacement gateway or hosting architecture.
- Packaged the existing runtime as a non-root, health-checked OCI image with an external durable state volume.
- Added repository-owned, multi-architecture GHCR publication using the repository token, provenance, and SBOM generation.
- Extended the existing live-activation validation contract to enforce packaging boundaries and absence of embedded secrets.
- Updated machine-owned adapter issue #18 and the Site build-goal record.

## Existing ecosystem components reused

- `llm_adapter.combined_gateway:app`
- `llm_adapter.custody_worker`
- `llm_adapter.node_bootstrap`
- `llm_adapter.node_service`
- `stegnode-bootstrap`
- `stegnode`
- Existing provider integration
- Existing Master-Records submission and reconstruction path
- Existing live verifier and immutable receipt path
- Existing Site activation importers and downstream consumers

## Components added

- `StegVerse-org/LLM-adapter/Dockerfile.portable-node`
- `StegVerse-org/LLM-adapter/.github/workflows/publish-portable-node-image.yml`

These package and distribute the existing runtime. They do not create a new gateway, provider integration, custody system, receipt system, heartbeat, or authority path.

## Components modified

- `StegVerse-org/LLM-adapter/tests/test_live_activation_automation_contract.py`
  - Enforces non-root image execution.
  - Enforces durable node-state volume and health checking.
  - Enforces multi-architecture GHCR publication, provenance, and SBOM.
  - Rejects embedded provider or Master-Records credentials and enabled-provider defaults.
- `StegVerse-Labs/Site/docs/ECOSYSTEM_CHAT_BUILD_GOAL.md`
  - Records the OCI image as part of the active deployment-recovery path.
  - Preserves fail-closed runtime completion accounting.

## Runtime and validation posture

- Portable-node source runtime: IMPLEMENTED
- Authorized host binding: IMPLEMENTED
- Authorized runtime environment inheritance: IMPLEMENTED
- OCI packaging: IMPLEMENTED
- Repository-owned image publication workflow: IMPLEMENTED
- Packaging contract validation: IMPLEMENTED
- Published image execution on an authorized host: NOT YET OBSERVED
- Live provider response: UNPROVEN
- Durable provider usage: UNPROVEN
- Provider-usage custody and reconstruction: UNPROVEN
- Transition custody and reconstruction: UNPROVEN
- Immutable VERIFIED receipt: UNPROVEN
- Site activation: UNPROVEN
- Downstream verified ingestion: UNPROVEN

## Durable evidence

- Portable-node OCI package: `0eaac3abc6c3691dae73916b1bd6f135e0a9955f`
- GHCR publication workflow: `ea9efe1c621552f609e1a6d929964135b52476e8`
- Packaging contract enforcement: `4f2e56913462a74944d67c0e91afb484fe0df643`
- Site build-goal update: `256b094cc9ed561b01d1a4fd3530c20b7eb4399c`
- Machine-owned continuation: `https://github.com/StegVerse-org/LLM-adapter/issues/18`

## Removals proposed or performed

None.

No existing Render configuration, gateway, workflow, portable-node runtime, provider integration, custody path, Site consumer, downstream consumer, or heartbeat component was removed, disabled, renamed, replaced, or superseded.

## Goal delta

The existing sovereign portable-node runtime can now be built and distributed automatically as a reproducible, multi-architecture repository-owned image. Platform-specific installation and manual image construction are no longer part of the deployment path.

No runtime gate is upgraded because the image has not yet been observed running on an authorized machine host.

## Exact blocker

No currently connected machine-owned host has scheduled the repository-owned portable-node image and exposed a live endpoint with authorized provider and Master-Records configuration.

## Next executable step

Machine-owned task #18 must bind the published image to an already-authorized machine runtime or restore the existing Render service, then point the existing verifier at the resulting endpoint. The existing validation path will retain the exact provider, persistence, custody, reconstruction, and receipt result automatically.

## Manual user action requirement

False.
