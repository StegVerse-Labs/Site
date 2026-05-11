# MS-013A Vaulted Capability Automation Runset Extension

## Purpose

MS-013A connects the vaulted capability gate into the existing transition automation runset.

This makes TV/TVC a detectable consequence of the table without issuing real tokens, settling payments, exposing secrets, or changing workflows.

## Added task

```text
data/headless-tasks/vaulted-capability-gate-v1.json
```

## Existing controller path

The existing controller calls:

```text
tools/headless_task_runset.py
```

against:

```text
data/headless-task-runsets/transition-discovery-automation-runset-v1.json
```

So this bundle updates only the runset data.

## Expected result

When the automation sequence runs, the vault gate should emit:

```text
vault_reports/vaulted-capability-gate-report.json
vault_reports/vaulted-capability-gate-report.md
headless_cmd_reports/vaulted-capability-gate-v1.receipt.json
headless_cmd_reports/vaulted-capability-gate-v1.report.md
```

The example request should likely produce:

```text
HOLD_FOR_VAULT_REVIEW
```

because the example owner claim is intentionally unverified and the pricing basis is demo-only.

## Still locked

```text
real token issuance
payment settlement
raw credential storage
raw credential release
workflow mutation
public financial promises
```
