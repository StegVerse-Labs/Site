# Ecosystem Chat Active Building Cycle — Portable-Node Singleton Repair

## Cycle date

2026-07-21

## Active goal

Complete the existing governed Ecosystem Chat vertical slice:

request → governed provider response → usage persistence → authenticated custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation.

The portable-node runtime remains an existing deployment-recovery path for this same goal. It is not a replacement gateway or separate architecture.

## Current proven state

- Canonical provider-neutral StegDeploy runtime: IMPLEMENTED and MERGED.
- Zero-touch portable-node bootstrap: IMPLEMENTED and MERGED.
- Autonomous portable-node lifecycle: IMPLEMENTED and MERGED.
- User-level portable-node autostart: IMPLEMENTED and MERGED.
- Atomic state and lifecycle receipt persistence: IMPLEMENTED and MERGED.
- Active health verification and bounded reconstruction backoff: IMPLEMENTED and MERGED.
- Singleton portable-node ownership and stale-lock repair: IMPLEMENTED, VALIDATED, and MERGED as adapter PR #20.
- Real governed provider request/response: NOT VERIFIED.
- Provider-usage custody and reconstruction: NOT VERIFIED.
- Transition custody and reconstruction: NOT VERIFIED.
- Immutable zero-blocker VERIFIED activation receipt: NOT OBSERVED.
- Site ACTIVATION_COMPLETE: NOT OBSERVED.
- Verified downstream ingestion: NOT OBSERVED.

## Next missing runtime step

Use the existing repository-owned machine execution and persistent-deployment recovery paths to run the canonical StegDeploy runtime with already-authorized provider and Master-Records environment, expose a reachable endpoint, and allow the existing verifier, receipt retention, Site activation, and downstream consumers to proceed automatically.

## Existing components evaluated for reuse

### Directly reused

- `StegVerse-org/LLM-adapter/llm_adapter/node_service.py`
- `StegVerse-org/LLM-adapter/tests/test_node_service.py`
- Existing portable-node state file and lifecycle receipt paths
- Existing cross-platform capability-runtime test matrix
- Existing Architecture Guard and validation workflows
- Existing canonical StegDeploy runtime from adapter PR #14
- Existing live verifier and validation-owned evidence retention
- Existing Site activation consumers
- Existing Master-Records custody and reconstruction path
- Existing machine-execution task in `StegVerse-org/core-node-runtime-demo#5`
- Existing persistent deployment recovery task in `StegVerse-org/LLM-adapter#18`

### Reused with bounded modification

- `node_service.py`: extended with an atomic per-node ownership claim, stale-lock recovery, duplicate-daemon refusal receipt, and ownership-safe release.
- `test_node_service.py`: extended with live-owner refusal, stale-owner recovery, and active-state idempotency tests.

### Adapter considered

A separate singleton service or lock-manager adapter was unnecessary. The existing node service already owned the process lifecycle and durable node root, so a bounded extension was lower risk and preserved existing consumers.

### New or replacement component considered

A replacement supervisor, external scheduler, new repository, new heartbeat mechanism, or duplicate runtime was rejected as unnecessary. No new core component was created.

## Work performed

- Read the authoritative Site mirror handoff, build-goal record, and active-building record.
- Inspected the active portable-node service implementation and its existing tests.
- Confirmed that concurrent direct start, native autostart, and fallback start could race before the durable state file was written.
- Extended the existing node service rather than creating a second supervisor or lock service.
- Added an atomic ownership claim scoped to the existing node root.
- Added automatic stale-owner detection and repair.
- Added fail-closed duplicate-daemon refusal with a machine-readable receipt.
- Added ownership-safe lock release so one process cannot release another process's claim.
- Preserved the existing heartbeat boundary; no GitHub workflow or process supervisor was designated as the StegVerse heartbeat.
- Ran the existing Architecture Guard, validation workflow, and complete cross-platform capability-runtime matrix.
- Merged adapter PR #20 only after all required gates succeeded.

## Components modified

- `StegVerse-org/LLM-adapter/llm_adapter/node_service.py`
- `StegVerse-org/LLM-adapter/tests/test_node_service.py`

## Adapters added

None.

## New components and decision rationale

None.

Required capability: prevent duplicate portable-node daemons and recover automatically from stale process ownership.

Options evaluated:

1. Reuse unchanged: no implementation effort, but leaves a real race between direct start, autostart, and fallback paths.
2. Modify the existing node service: direct progress, bounded effort, low authority risk, preserves all consumers, and is fully reversible through repository history.
3. Add a bounded lock-manager adapter: additional process and interface complexity without improving the node-root ownership model.
4. Build a replacement supervisor: duplicates a core lifecycle capability and would require explicit architectural approval.

Selected option: bounded modification of the existing node service.

## Runtime tests actually executed

Adapter head `5d062919825f757f3ab9bedf2543336f140e590a` completed:

- Architecture Guard: SUCCESS.
- `validate`: SUCCESS.
- `capability-runtime`: SUCCESS across Linux, macOS, Windows, Python 3.11, and Python 3.12.

The change was merged as `3d10487535c0005fd398214b7ef04cc5d89ef2ab`.

## Observed results

- A live ownership claim now prevents a second daemon from becoming the node owner.
- A stale ownership claim is repaired automatically without user intervention.
- Duplicate launch attempts remain fail-closed and emit durable evidence.
- Existing active lifecycle states remain idempotent.
- No manual recovery, backend selection, workflow dispatch, credential copying, or node-start task was assigned to the user.

## Exact failures and unproven boundaries

- Persistent public machine execution: NOT YET OBSERVED.
- Reachable governed gateway endpoint: NOT YET OBSERVED.
- Real provider response: NOT VERIFIED.
- Provider usage persistence: NOT VERIFIED.
- Provider-usage custody and reconstruction: NOT VERIFIED.
- Transition custody and reconstruction: NOT VERIFIED.
- Immutable VERIFIED receipt: NOT OBSERVED.
- Site activation: NOT OBSERVED.
- Downstream verified ingestion: NOT OBSERVED.

## Durable evidence produced

- Adapter PR #20: https://github.com/StegVerse-org/LLM-adapter/pull/20
- Adapter merge commit: https://github.com/StegVerse-org/LLM-adapter/commit/3d10487535c0005fd398214b7ef04cc5d89ef2ab
- Validated head commit: https://github.com/StegVerse-org/LLM-adapter/commit/5d062919825f757f3ab9bedf2543336f140e590a
- Persistent deployment owner: https://github.com/StegVerse-org/LLM-adapter/issues/18
- Machine-execution compatibility owner: https://github.com/StegVerse-org/core-node-runtime-demo/issues/5

## State classification

- Singleton ownership design: DESIGNED.
- Singleton ownership implementation: IMPLEMENTED.
- Existing lifecycle integration: INTEGRATED.
- Cross-platform tests: EXECUTED and VERIFIED.
- Merge to adapter `main`: DEPLOYED to repository source.
- Persistent public runtime: NOT LIVE.
- Site activation: NOT PROPAGATED.

Repository merge is not equivalent to a live public deployment.

## Removals proposed but not performed

None.

No repository, file, workflow, runtime, receipt path, provider integration, custody path, heartbeat component, or downstream consumer was removed, renamed, disabled, superseded, or replaced.

## Goal delta

Portable-node startup can no longer create competing daemon owners through concurrent start paths, and stale ownership repairs itself automatically. This secures the existing local execution boundary but does not complete the provider/custody vertical slice.

## Reuse delta

The existing node supervisor, node-root state, lifecycle receipts, test matrix, and validation workflows eliminated the need for a new lock service, scheduler, supervisor, repository, schema, or heartbeat mechanism.

## Runtime evidence

All existing required adapter gates passed on the exact PR #20 head, and the validated change was merged. No real provider, custody, reconstruction, immutable activation receipt, Site activation, or downstream-ingestion evidence was produced by this cycle.

## Non-progress

- This Site record does not complete a runtime gate.
- Singleton hardening does not itself provide a persistent public machine.
- Passing CI does not establish runtime heartbeat authority or prove live provider execution.

## Next critical executable step

Run the existing canonical StegDeploy image through the already-created repository-owned machine execution path, retain its compatibility receipt, then bind the same canonical runtime to an already-authorized persistent host through adapter issue #18. Point the existing verifier at that endpoint and repair only the first concrete provider, persistence, custody, reconstruction, or receipt failure.

## Manual user action requirement

False. Routine deployment recovery, machine execution, verification, receipt retention, Site activation, and downstream propagation remain repository-owned tasks.