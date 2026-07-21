# Ecosystem Chat Active Building Cycle — Core-Node Machine Executor

## Date

2026-07-21

## Goal delta

The canonical StegDeploy runtime can now be started and health-verified by a repository-owned machine executor in `StegVerse-org/core-node-runtime-demo`. Manual image pulling, installation, container startup, local health testing, core-node comparison execution, and compatibility receipt construction are removed from this boundary.

## Existing components reused

- `StegVerse-org/LLM-adapter` canonical StegDeploy image and gateway
- `StegVerse-org/core-node-runtime-demo/tools/run_all.py`
- Existing core-node comparison paths, witness-ready outputs, and governed result shapes
- GitHub-hosted machine runner and repository package token
- Existing Site build-goal and activation evidence boundaries

## Components added

- `StegVerse-org/core-node-runtime-demo/.github/workflows/stegdeploy-runtime-intake.yml`
  - pulls `ghcr.io/stegverse-org/llm-adapter:main`;
  - starts the canonical gateway fail-closed on a machine runner;
  - verifies live `/health`;
  - executes the existing core-node comparison pipeline;
  - writes and persists a hash-bound compatibility receipt;
  - grants no provider, custody, deployment, publication, or release authority.

## Durable records

- Core-node executor commit: `9eb2893cffd2fc4e8c7dfc8ae9dfb2b4d96344c2`
- Core-node task: `https://github.com/StegVerse-org/core-node-runtime-demo/issues/5`
- Adapter persistent-host task: `https://github.com/StegVerse-org/LLM-adapter/issues/18`
- Site goal update: `b7cd6133caf1f1753827b228a73214cf5bda0d92`

## Current evidence state

- Machine executor workflow: IMPLEMENTED
- Repository-authored compatibility receipt: EXECUTION PENDING
- Persistent public gateway: NOT LIVE
- Governed provider execution: UNPROVEN
- Provider-usage custody and reconstruction: UNPROVEN
- Transition custody and reconstruction: UNPROVEN
- Immutable VERIFIED activation receipt: UNPROVEN
- Site activation and downstream ingestion: UNPROVEN

## Exact blocker

`receipts/stegdeploy-runtime-intake.latest.json` has not yet been authored by the new core-node workflow. Even after compatibility passes, the machine runner is ephemeral and fail-closed. A persistent authorized host with governed provider and Master-Records configuration is still required for the full live activation chain.

## Manual user action requirement

False. No workflow dispatch, image pull, node start, health check, comparison run, credential copy, or receipt construction is assigned to the user.

## Removals

None proposed or performed.
