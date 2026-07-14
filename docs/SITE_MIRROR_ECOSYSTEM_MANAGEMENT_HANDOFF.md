# Site Mirror Ecosystem Management Handoff

## Purpose

This file is the Site-side ecosystem-management handoff for repository-managed continuation. It preserves enough current state for future sessions, Site automation, or ecosystem management logic to continue without prior chat context.

## Current Assessment Goal

```text
Goal: fully functional governed Ecosystem Chat request-response, provider, custody, comparison, and cross-entry usage path
```

## Current State

```text
management_state: self_managed_handoff_ready
site_state: autonomous_continuation_ready
site_repo: StegVerse-Labs/Site
local_goal_status: ready
activation_checkpoint: SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED
contract_status: PREPARED_NOT_DEPLOYED
live_transport_enabled: false
operational_workflows: validate.yml, site-task-runner.yml
remaining_dependency: destination validation, authorized deployment, conformance, custody, and reconstructability evidence
```

## Site Responsibilities

```text
1. Preserve Publisher, TT, Governance Observatory, LLM-adapter, and Master-Records authority boundaries.
2. Keep exactly two operational workflows.
3. Run declared validation through scripts/run_site_task.py.
4. Preserve same-origin session requirements and prohibit browser bearer/query/local-storage token configuration.
5. Validate Site public and machine-readable surfaces.
6. Retain current-main diagnostics and activation evidence.
7. Keep live transport disabled until every activation gate passes.
8. Keep custody_recorded=false until authenticated Master-Records custody and reconstructability PASS are observed.
```

## Destination Responsibilities

```text
StegVerse-org/LLM-adapter
  -> validate usage-session retrieval on current main
  -> integrate provider-owned usage submission
  -> deploy only under explicit destination authority
  -> emit retrieval and provider usage receipts

master-records/orchestration
  -> custody usage and comparison events
  -> provide authenticated custody receipt
  -> provide reconstructability PASS evidence

StegVerse-org/core-node-runtime-demo
  -> emit automatic runtime usage
  -> submit live governed route results
```

## Source-of-Truth Files

```text
StegVerse-Labs/Site/docs/SITE_MIRROR_HANDOFF.md
StegVerse-Labs/Site/docs/SITE_EXTERNAL_EVIDENCE_STATE.json
StegVerse-Labs/Site/docs/SITE_FINAL_GOAL_STATUS.json
StegVerse-Labs/Site/docs/SITE_FINAL_ACTIVATION_PENDING.md
StegVerse-Labs/Site/docs/SITE_SELF_MANAGED_COMPLETION.md
StegVerse-Labs/Site/scripts/run_site_task.py
StegVerse-Labs/Site/scripts/check_site_ecosystem_management_handoff.py
StegVerse-Labs/Site/.github/workflows/validate.yml
StegVerse-Labs/Site/.github/workflows/site-task-runner.yml
```

## Acceptance Criteria

The Site-side management task is complete because:

```text
A. Repository-local completion
   - TT bundle-fed status is ready.
   - Governance Observatory status is ready.
   - External evidence state is present.
   - final goal status reports ready.
   - local completion receipt is ready.

B. Self-managed handoff completion
   - This file exists.
   - The current handoff records the next exact validation action.
   - The two active workflows own validation and continuation.
   - Remaining work is external verification and authority-bound activation evidence, not manual Site evidence entry.
```

## Live Activation Criteria

Live activation is not complete until:

```text
destination current-main tests pass
same-origin authenticated deployment exists
sample response conformance passes
retrieval receipt validates
no browser secret surface is verified
Site current-main validation passes
Master-Records custody is authenticated
reconstructability PASS is recorded
```

## Current Completion Classification

```text
classification: self_managed_handoff_completion
ready_completion: repository_local_ready
activation_completion: blocked_external_authority_evidence
reason: Site-local continuation and readiness gates are repository-managed and ready; deployment, custody, and reconstructability remain external authority gates.
```

## Non-Claims

This handoff does not claim:

```text
- the usage endpoint is deployed;
- live transport is enabled;
- Site is the TT or Governance Observatory source of truth;
- Site issues commit-time permission;
- validation artifacts equal Master-Records custody;
- external evidence presence equals reconstructability;
- a release tag is authorized.
```

## Archive Readiness

```text
thread_archive_ready: true
archive_reason: Site-side state, validation progression, activation boundary, and next actions are repository-resident. No additional content from the prior chat thread is required.
```
