# Site Personal Data Control Runtime Mirror Handoff

This file is the current task source of truth for the personal-data control runtime projection in `StegVerse-Labs/Site`.

## Determination

```text
Policy layer: BUILT in StegVerse-Labs/admissibility-wiki
Account-bearing Site runtime projection: NOT PREVIOUSLY BUILT
Current action: BUILD AND ACTIVATE THROUGH REPOSITORY-LOCAL TASK CONTROL
External tasks required: false
Manual tasks required: false
```

The public governance standard alone is insufficient. Every account-bearing surface must expose an observable request lifecycle before account-linked data collection is treated as governed.

## Required runtime states

```text
NOT_REQUESTED
RECEIVED
IDENTITY_VERIFICATION_REQUIRED
VERIFIED
PROCESSING_RESTRICTED
INVENTORY_COMPLETE
DELETION_IN_PROGRESS
PROCESSOR_PROPAGATION_PENDING
COMPLETED
PARTIALLY_DENIED
DENIED
APPEAL_OPEN
CHANNEL_FAILED
```

## Installed task

```text
Task: SITE-0001-PERSONAL-DATA-CONTROL
Task object: data/tasks/SITE-0001-PERSONAL-DATA-CONTROL.json
Runtime contract: data/personal-data-control-runtime.json
Public surface: personal-data-control.html
Validator: scripts/check_personal_data_control_runtime.py
Observer: scripts/observe_and_complete_repository_tasks.py
Workflow: .github/workflows/observe-and-complete-repository-tasks.yml
```

## Non-halting completion path

The task object is machine-admitted. The repository controller discovers eligible task objects, executes their validators, preserves the exact result, and advances completed tasks without relying on an external session.

```text
committed task object
-> automatic admission
-> executable validator
-> durable report
-> exact blocker path or COMPLETE
-> repository state advances
```

External controller responses may become evidence in framework-specific records. They are never dependencies for continuing StegVerse development.

## Authority boundary

```text
public request page != completed deletion
request receipt != identity verification
account closure != processor propagation
validator PASS != legal-compliance adjudication
external silence != development blocker
```

The complete thread is ready for archiving without any additional part of the thread needed to move forward.
