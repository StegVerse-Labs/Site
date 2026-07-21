# Ecosystem Chat Machine-Execution Cycle

Date: 2026-07-21

## Goal

Prove the existing canonical Ecosystem Chat runtime on a connected machine before expanding the deployment path.

## Reuse decision

Reused:

- `StegVerse-org/core-node-runtime-demo/.github/workflows/validate.yml`
- `StegVerse-org/core-node-runtime-demo/tools/run_all.py`
- the existing core-node receipt and evidence artifact paths
- `StegVerse-org/LLM-adapter@main`
- the existing canonical adapter `Dockerfile`
- the existing combined gateway and `/health` contract

No new runtime, gateway, scheduler, monitor, receipt schema, repository, image system, or heartbeat mechanism was created.

## Work performed

- Repaired five existing core-node scripts that could not import their existing `tools` modules when executed directly.
- Extended the existing compatibility receipt so the first failed pipeline or image-acquisition step is retained.
- Tried the existing GHCR package first.
- When that package path was denied, checked out the authoritative adapter source and built the existing canonical Dockerfile.
- Started the gateway with its existing fail-closed settings and verified live health.

## Runtime evidence

- Run `29839100748`: core-node pipeline, tests, artifacts, and boundary checks passed.
- Run `29839790061`: registry login passed; package acquisition failed; blocker retained.
- Run `29853616226`: exact package-acquisition output retained.
- Run `29853848999`: pipeline passed; authoritative source checkout passed; canonical Dockerfile build passed; gateway start passed; `/health` passed; compatibility enforcement passed; evidence upload passed.

Merged evidence:

- Core-node PR #6: `d8a4f82bfaa596b26463d3ea2ff11fd923477b08`
- Core-node PR #8: `6f40cb7110823c48527efadd90c13d87b5cf2455`
- Core-node Issue #5: https://github.com/StegVerse-org/core-node-runtime-demo/issues/5
- Adapter Issue #18: https://github.com/StegVerse-org/LLM-adapter/issues/18

## State

- Existing machine executor: INTEGRATED
- Canonical source acquisition: EXECUTED
- Canonical Dockerfile build: VERIFIED
- Fail-closed gateway start: VERIFIED
- Machine-runner gateway health: VERIFIED
- Authoritative-source runtime compatibility: VERIFIED
- Published package compatibility: BLOCKED / UNPROVEN
- Persistent public deployment: NOT DEPLOYED
- Public gateway: NOT LIVE
- Real provider response: UNPROVEN
- Persistence, custody, reconstruction, immutable activation receipt, Site activation, and downstream ingestion: UNPROVEN

## Goal delta

The canonical existing runtime now builds, starts, and returns healthy fail-closed evidence on a connected machine executor. This did not work before this cycle.

## Non-progress

The cycle did not execute a real provider request, custody, reconstruction, Site activation, or downstream propagation.

## Removals

None proposed or performed.

## Next executable step

Run the same existing canonical runtime on an already-authorized persistent host, execute one governed request, and pass the result through the existing verifier. Repair only the first concrete runtime failure.

Manual user action required for routine repository work: false.
