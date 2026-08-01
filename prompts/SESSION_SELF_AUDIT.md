# Governed Session Self-Audit Prompt

Perform a session-retirement audit against the current connected GitHub repository state.

1. Identify every organization, repository, task, and goal worked on by this session.
2. For each repository, locate and read the current authoritative `*_MIRROR_HANDOFF.md` before relying on prior conversation state.
3. Read the machine-readable orchestration state, continuation prompt, task registry, standing record, receipts, issues, pull requests, and workflow evidence referenced by the handoff.
4. Compare this session's last known state, decisions, artifacts, blockers, unresolved issues, and proposed next actions against current authoritative state.
5. Classify each task as `CURRENT`, `SUPERSEDED`, `MERGE_REQUIRED`, or `ARCHIVABLE`.
6. Do not classify a task as `ARCHIVABLE` merely because the conversation is old or inactive.
7. Use `MERGE_REQUIRED` whenever material information is absent from repository authority. Identify the exact destination and merge it when repository authority permits.
8. Use `CURRENT` only when the session still owns an admitted unresolved task.
9. Use `SUPERSEDED` when newer authoritative state or another owner has advanced beyond this session and no unique state remains.
10. Use `ARCHIVABLE` only when active task ownership is false, unique unmerged state is false, no conflicting owner exists, material state locations are recorded, and a successor execution source exists when work remains.
11. Update `data/session-orchestration-registry.json` with one receipt per audited task conforming to `schemas/session-retirement.schema.json`.
12. Run `python scripts/check_session_retirement.py` and resolve all failures before declaring archive readiness.
13. Do not claim that the ChatGPT UI conversation was archived. Repository evidence establishes disposition only; UI archival remains a separate action unless a supported conversation-management interface is available.

When safe, end with:

```text
SESSION ARCHIVE DISPOSITION: SAFE TO ARCHIVE
UNIQUE UNMERGED STATE: NONE
ACTIVE TASK OWNERSHIP: NONE
SUCCESSOR EXECUTION SOURCE: <authoritative path>
```

When unsafe, end with:

```text
SESSION ARCHIVE DISPOSITION: DO NOT ARCHIVE
REASON: <specific reason>
REQUIRED ACTION: <exact action>
DESTINATION: <organization/repository/path>
```
