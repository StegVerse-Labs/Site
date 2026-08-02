# Session Orchestration Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for governed ChatGPT session activation, comparison, retirement, and archive disposition within `StegVerse-Labs/Site`.

## Current state

```text
classification: BUILD_IN_PROGRESS
activation_authority: false
active_owner: StegVerse-Labs/Site issue #114
current_coordination_task: SOR-0001 through SOR-0008
```

The core layer exists, but activation is not yet established. A workflow definition alone is not execution evidence, and an archive disposition is not valid without a passing validator result and current ownership comparison.

## Goal

Convert disposable chat sessions into bounded execution nodes that load current repository authority, compare their remembered state to live state, preserve unique information, and deterministically declare whether they remain current or are safe to archive.

## Authoritative comparison order

1. Read the target repository `*_MIRROR_HANDOFF.md`.
2. Read the machine-readable orchestration state referenced by that handoff.
3. Read current task ownership, issues, pull requests, branches, receipts, and continuation prompts.
4. Compare the session's last known state to the current repository state.
5. Preserve any unique unmerged information before retirement.
6. Emit a machine-readable archive disposition receipt.

## Session postures

- `CURRENT`: the session still owns an admitted unresolved task.
- `SUPERSEDED`: newer authoritative state or another owner has advanced beyond the session.
- `MERGE_REQUIRED`: the session contains material information absent from the current repository state.
- `ARCHIVABLE`: the session owns no active task and contains no unique unmerged state.

Age alone never establishes archive readiness.

## Archive gate

A session may be marked `ARCHIVABLE` only when all conditions are true:

1. `active_task_ownership` is false.
2. `unique_unmerged_state` is false.
3. every material decision, artifact, blocker, receipt, and next action is represented in an authoritative repository location;
4. a successor execution source exists when work remains;
5. repository and handoff references are current and resolvable;
6. no conflicting active owner exists;
7. the retirement validator reports PASS against the current registry.

The validator fails closed when evidence is missing or contradictory.

## Implemented files

- `data/session-orchestration-registry.json`
- `schemas/session-retirement.schema.json`
- `scripts/check_session_retirement.py`
- `prompts/SESSION_SELF_AUDIT.md`
- `docs/SESSION_ORCHESTRATION_MIRROR_HANDOFF.md`
- `.github/workflows/session-retirement-validate.yml`

## Active coordinated work

Authoritative tracker: `StegVerse-Labs/Site` issue `#114`.

```text
SOR-0001 Validation activation
SOR-0002 Canonical Site-orchestrator integration
SOR-0003 Deterministic posture and failure fixtures
SOR-0004 Successor activation packet generation
SOR-0005 Cross-repository handoff and ownership comparison
SOR-0006 Validated archive queue projection
SOR-0007 Master-Records custody and reconstruction
SOR-0008 Publisher and wiki downstream projection after activation
```

## Consolidated StegMusic and ST-018 session

Registry entry:

```text
data/session-orchestration-registry.json
session_id: stegmusic-st018-continuation-2026-08-02
task_id: STEGMUSIC-ST018-SESSION-CONSOLIDATION-001
```

Original and adjacent goals transferred:

```text
six-track StegMusic and StegDJ public browser runtime
six-track adaptive ranking with active-track exclusion
target-device audibility and lifecycle evidence without authority escalation
repository-native completion workers for inaccessible work
repository-grounded session archival determination
```

Canonical continuation locations:

```text
docs/STEGMUSIC_LIVE_MIRROR_HANDOFF.md
StegVerse-Labs/Site issue #39
data/tasks/SITE-ST018-VALIDATION-EVIDENCE.json
StegVerse-Labs/Site issue #141
docs/SESSION_ORCHESTRATION_MIRROR_HANDOFF.md
StegVerse-Labs/Site issue #114
```

Implementation convergence:

```text
StegMusic implementation and validation are owned by Site main and issue #39.
ST-018 implementation is machine-owned by .github/workflows/capture-validation-evidence.yml and issue #141.
Session orchestration activation remains owned by issue #114.
This session must not create a competing implementation lane.
```

Observed transfer evidence:

```text
PR #145 merged ST-018 implementation.
PR #147 merged execution and receipt-writer repair at 7ab221e63740db495a6864c2ccc3ed401c25d124.
PR #148 merged worker trigger coverage at 3c48af9e7e10be6cf509264547373b59b77b09ac.
Task-state trigger commit b4ff66072dba37e18a10776cceb9e6c20478c18f requests native-main completion evidence.
Session registry commit 2c6d9abd2c2815dd007316e3ddbe89013777760c preserves the complete session inventory and collision boundaries.
```

Current consolidation posture:

```text
MERGE_REQUIRED
active_task_ownership: false
distinct_support_role: integration and evidence inspection
unique_unmerged_state: false
release_condition: observe native-main ST-018 artifact and issue #141 custody receipt, then admit ARCHIVABLE or SUPERSEDED disposition
```

## Activation gate

The layer becomes activated only after all of the following are directly observed and recorded:

1. validator workflow PASS with retained run, job, and report evidence;
2. `scripts/site_handoff_orchestrator.py` consumes retirement state;
3. one real `SUPERSEDED` disposition is admitted;
4. one real `MERGE_REQUIRED` disposition is rejected from archival;
5. one real `ARCHIVABLE` disposition is admitted;
6. no conflicting current owner exists;
7. the successor execution source resolves;
8. the handoff and registry carry the resulting receipts.

## Authority boundary

Repository evidence may establish that a conversation is safe to archive. It does not itself perform the ChatGPT UI archive or deletion action. Until a supported conversation-management interface exists, the output is an archive disposition receipt and queue entry.

## Remaining work

Destination `StegVerse-Labs/Site`:

```text
Execute and retain the session-retirement validator workflow evidence
Bind scripts/check_session_retirement.py into canonical Site orchestration and validation
Add signed archive disposition receipts
Add stale heartbeat comparison against task-relative health
Add duplicate session-owner detection across repositories
Add successor-session activation packet generation
Add archive queue projection to the Site UI
Add tests for CURRENT, SUPERSEDED, MERGE_REQUIRED, ARCHIVABLE, conflicting owner, missing successor, and malformed evidence
Observe the native-main ST-018 artifact and issue #141 custody receipt for stegmusic-st018-continuation-2026-08-02
```

Destination `master-records/orchestration`:

```text
Custody archive disposition receipts
Verify registry lineage and reconstruction
Return receipt hashes and reconstruction status
```

Downstream destinations after verified implementation:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

## Next execution session prompt

Read this handoff first, then issue #114. Run `python scripts/check_session_retirement.py`. Continue the highest-priority incomplete SOR task without creating duplicate ownership. Do not classify a session as archivable merely because it is old or inactive. Merge unique state before retirement, update the registry, emit the disposition receipt, and preserve the successor execution source.

For `stegmusic-st018-continuation-2026-08-02`, inspect issue #141 and the native-main artifacts produced by `.github/workflows/capture-validation-evidence.yml`. After direct custody evidence exists, update the registry posture to `SUPERSEDED` or `ARCHIVABLE`; do not reopen StegMusic or ST-018 implementation work in another session.

## Archive readiness

The StegMusic and ST-018 session has transferred all unique design and implementation state into repository authority, but remains temporarily non-archivable until the native-main ST-018 custody artifact and issue #141 receipt are directly observed and the registry posture is updated.

The broader coordination session is not safe to archive while it owns unresolved issue #114 coordination or until that ownership is transferred into a successor session and the registry records no unique unmerged state. When no coordination task remains, the response must announce `ARCHIVE THIS SESSION` at both top and bottom.
