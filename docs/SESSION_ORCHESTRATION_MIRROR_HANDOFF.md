# Session Orchestration Mirror Handoff

## Source of truth

This file is the current handoff and task source of truth for governed ChatGPT session activation, comparison, retirement, and archive disposition within `StegVerse-Labs/Site`.

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
6. no conflicting active owner exists.

The validator fails closed when evidence is missing or contradictory.

## Implemented files

- `data/session-orchestration-registry.json`
- `schemas/session-retirement.schema.json`
- `scripts/check_session_retirement.py`
- `prompts/SESSION_SELF_AUDIT.md`
- `docs/SESSION_ORCHESTRATION_MIRROR_HANDOFF.md`

## Authority boundary

Repository evidence may establish that a conversation is safe to archive. It does not itself perform the ChatGPT UI archive or deletion action. Until a supported conversation-management interface exists, the output is an archive disposition receipt and queue entry.

## Remaining work

Destination `StegVerse-Labs/Site`:

```text
Bind scripts/check_session_retirement.py into canonical validation and CI
Add signed archive disposition receipts
Add stale heartbeat comparison against task-relative health
Add duplicate session-owner detection across repositories
Add successor-session activation packet generation
Add archive queue projection to the Site UI
Add tests for CURRENT, SUPERSEDED, MERGE_REQUIRED, ARCHIVABLE, conflicting owner, missing successor, and malformed evidence
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

Read this handoff first. Run `python scripts/check_session_retirement.py`. Continue only from validator output and current repository authority. Do not classify a session as archivable merely because it is old or inactive. Merge unique state before retirement, update the registry, emit the disposition receipt, and preserve the successor execution source.

## Archive readiness

This orchestration-design conversation is safe to archive only after the files listed above are committed and the validator reports PASS against the registry. The repository handoff then becomes the continuation source of truth.
