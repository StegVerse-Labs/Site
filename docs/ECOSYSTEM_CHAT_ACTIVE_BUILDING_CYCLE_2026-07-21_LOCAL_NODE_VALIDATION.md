# Ecosystem Chat Active Building Cycle — StegVerse Local-Node Validation

Date: 2026-07-21

## Active goal

Complete the first real governed Ecosystem Chat vertical slice through StegVerse-owned runtime capabilities:

`request → governed provider response → usage persistence → custody → reconstruction → immutable VERIFIED receipt → Site activation → downstream propagation`

## Work performed

### Adapter

- Merged health-bound node advertisement implementation:
  - https://github.com/StegVerse-org/LLM-adapter/pull/24
- Added a clean follow-up validation PR:
  - https://github.com/StegVerse-org/LLM-adapter/pull/26
- Bound `tests/test_node_advertisement.py` into both canonical and iOS-safe validation workflows.
- Repaired stale StegDeploy validators that still asserted publication receipt schema `v1` after the canonical workflow moved to `v2`.
- Preserved compatibility with the repository-retained `v1` receipt until the next successful image publication retains `v2` evidence.

### Site

- Implemented verified loopback StegVerse-node discovery:
  - https://github.com/StegVerse-Labs/Site/pull/29
- Removed the hard-coded Render endpoint from the active binding.
- Limited discovery to `127.0.0.1:8000` and `localhost:8000`.
- Required advertisement schema, SHA-256 verification, health binding, and false authority/publication/execution flags before routing.
- Bound the focused local-node validator into the existing canonical and iOS-safe Site validation workflows.

## Existing capabilities reused

- canonical StegDeploy runtime;
- portable-node bootstrap and node identity;
- autonomous node lifecycle and reconstruction;
- existing `/health` endpoint;
- existing Site live-binding layer and fail-closed classifier;
- provider integration;
- provider-usage persistence;
- Master-Records custody and reconstruction;
- immutable activation receipt path;
- canonical and iOS-safe validation mirrors.

No new gateway, host platform, central registry, scheduler, heartbeat mechanism, custody service, or receipt authority was created.

## State separation

### IMPLEMENTED

- health-bound node advertisement;
- browser advertisement verification;
- loopback-only Site discovery;
- focused adapter and Site validators;
- canonical/iOS validation wiring.

### INTEGRATED

- adapter advertisement is merged on `main` through PR #24;
- Site binding remains open in PR #29;
- adapter validation completion remains open in PR #26.

### EXECUTED

Adapter CI run https://github.com/StegVerse-org/LLM-adapter/actions/runs/29867198411 executed:

- StegDeploy runtime contract — PASS;
- retained image receipt compatibility — PASS;
- provider and endpoint checks — PASS;
- Master-Records provider-usage custody-submission tests — PASS;
- node advertisement contract — PASS.

The external live probe is a separate later step and remained in progress when this record was written.

### VERIFIED

The node advertisement contract is VERIFIED by CI.

The complete live Ecosystem Chat vertical slice is not VERIFIED.

### DEPLOYED / LIVE / PROPAGATED

Not proven.

## Observed failures and repairs

1. StegDeploy verifier required publication schema `v1` while the canonical workflow emits `v2`.
   - Repaired to assert `v2` for the current workflow.
2. Retention validator rejected the repository-retained `v1` receipt during the migration window.
   - Repaired to accept retained `v1` and current `v2` while preserving all hash, digest, retention, visibility, credential, and authority checks.
3. Site aggregate validation remains affected by a pre-existing workflow-inventory mismatch unrelated to local-node discovery.
   - No unrelated workflow removal or redefinition was performed.
   - The focused local-node validator was inserted before that sandbox boundary in the existing workflow.

## Durable evidence

- Merged adapter endpoint PR: https://github.com/StegVerse-org/LLM-adapter/pull/24
- Adapter validation PR: https://github.com/StegVerse-org/LLM-adapter/pull/26
- Adapter CI run: https://github.com/StegVerse-org/LLM-adapter/actions/runs/29867198411
- Site binding PR: https://github.com/StegVerse-Labs/Site/pull/29
- Active architecture issue: https://github.com/StegVerse-Labs/Site/issues/24

## Removals proposed but not performed

- Render PR #23 and retained Render files remain non-canonical but were not removed, closed, reverted, or deleted.
- No workflow, heartbeat component, deployment package, or existing runtime was removed.

## Goal delta

A StegVerse node can now publish a hash-bound, health-bound, non-authorizing endpoint advertisement, and the Site has an implemented path to discover and verify that local node instead of using Render.

## Reuse delta

The existing portable-node identity, health route, runtime supervision, Site binding layer, and validation mirrors eliminated the need for a new host, registry, discovery service, or gateway.

## Runtime evidence

The adapter node-advertisement contract executed and passed in CI. No browser-to-running-node governed request has yet been retained.

## Non-progress

- documentation and this cycle record do not advance runtime gates;
- the external live probe does not validate the operator-local node path;
- no completion percentage is increased for open PRs or source existence alone.

## Next executable step

1. Complete adapter PR #26 validation and merge it when green.
2. Obtain focused Site validation evidence for PR #29 and merge it when green.
3. Launch the existing portable node on an authorized machine with provider and Master-Records environment.
4. Execute one Site request through verified local-node discovery.
5. Retain provider, persistence, custody, reconstruction, and immutable receipt evidence.

Manual user action required: false for repository and evidence work. Provider and custody credentials remain outside repository content.
