# Session Orchestration Mirror Handoff

## Source of truth

This file is the canonical handoff and task source of truth for governed ChatGPT session activation, comparison, succession, retirement, and archive disposition within `StegVerse-Labs/Site`.

## Current state

```text
classification: BUILD_IN_PROGRESS
activation_authority: false
active_owner: StegVerse-Labs/Site issue #114
current_coordination_task: SOR-B / issue #118
SOR-A / issue #117: COMPLETE_AND_CLOSED
SOR-B registry intake: COMPLETE_AND_VALIDATED
SOR-B successor/frontier/archive projection: COMPLETE_AND_VALIDATED
SOR-B cross-repository comparison: OPEN
SOR-C / issue #119: DEPENDENCY_BLOCKED_ON_REMAINING_SOR-B_AND_PARENT_ACTIVATION
```

The heartbeat and base Site orchestration layers are operational. Session-retirement validation is now consumed by the canonical Site orchestrator. Repository-native registry intake, successor-packet generation, execution-frontier projection, and archive-queue projection are installed and validated. Full activation remains blocked by cross-repository owner/handoff comparison, real `SUPERSEDED` and real `MERGE_REQUIRED` activation evidence, disposition receipt custody, and parent activation admission.

## Goal

Convert disposable chat sessions into bounded execution nodes that load current repository authority, compare remembered state to live state, preserve unique information, deterministically select continuation, and safely identify sessions whose project state is fully durable.

## Authority order

1. Read the target repository `*_MIRROR_HANDOFF.md`.
2. Read machine-readable orchestration and heartbeat state referenced by that handoff.
3. Read current task ownership, issues, pull requests, branches, receipts, workflows, artifacts, and successor sources.
4. Compare session state to current repository state.
5. Preserve unique unmerged information before retirement.
6. Emit machine-readable disposition and continuation evidence.
7. Fail closed on ambiguity, missing evidence, stale authority, or conflicting ownership.

Age alone never establishes archive readiness.

## Session postures

- `CURRENT`: the session still owns an admitted unresolved task.
- `SUPERSEDED`: newer authoritative state or another owner has advanced beyond the session.
- `MERGE_REQUIRED`: the session contains material information absent from authoritative state.
- `ARCHIVABLE`: the session owns no active task and contains no unique unmerged state.

## Queue states

Registry-derived projection uses bounded queue states rather than implying a UI action:

```text
CURRENT -> CLAIMED
SUPERSEDED -> SUPERSEDED
MERGE_REQUIRED -> REVIEW_REQUIRED
ARCHIVABLE -> COMPLETE + archive_candidate=true
```

`ui_archive_action_performed` is always false in repository projection. Repository evidence may establish archival disposition; it does not perform the ChatGPT UI archive/delete action.

## Implemented canonical files

```text
data/session-orchestration-registry.json
schemas/session-retirement.schema.json
scripts/check_session_retirement.py
tests/test_session_retirement.py
prompts/SESSION_SELF_AUDIT.md
.github/workflows/session-retirement-validate.yml
scripts/site_handoff_orchestrator.py
.github/workflows/site-handoff-orchestrator.yml
scripts/admit_session_consolidation.py
tests/test_admit_session_consolidation.py
.github/workflows/session-orchestration-registry-intake.yml
data/session-registry-intake-requests/
scripts/project_session_orchestration.py
tests/test_project_session_orchestration.py
.github/workflows/session-orchestration-project.yml
data/session-orchestration-successor-packets.json
data/session-orchestration-archive-queue.json
```

## SOR-A completion

Issue `#117` is closed completed. It no longer owns an active implementation claim.

Installed evidence:

```text
canonical Site-orchestrator retirement binding: 43819c4d882d4b663bd7c68a3b4e44eb7b3b2d8c
retirement posture tests: bb3e44103075a631b2dc88f3e91d06d6af26fcaa, f8c4b800773867c1f2a69be2345908ee67756ac3
duplicate CURRENT-owner detection: de46c56131aed8de52401dbbd7434f1391ee283e
retirement CI test binding: 40122cb17930c5e53e152ebdc787bbdf1685c897
Site retained retirement artifact binding: dfdaec84f75aec3745f0b9f3914ceb8394998efe
```

Hosted validation:

```text
Session Retirement Validate run 31151536007 / job 92782023502: SUCCESS
9/9 deterministic tests PASS
SESSION_RETIREMENT_PASS
artifact 8983465891 sha256 03ccef854fdd4ded015d672b4ca76a2b6db46df485fc91a8e6a50a6cf5560b31

Site Handoff Orchestrator run 31151462957 / job 92781812582: SUCCESS
orchestration artifact 8983440627 sha256 00d6e2990c6a076ac197fbba51a961b20961e1d8b0a30926b1272c70b19c8c9b
retirement artifact 8983440950 sha256 286151b1bcc42c30443b2b22cd8265dc53d6c7a91defe9b119e527f380683431
```

This establishes activation-gate validator PASS and canonical Site-orchestrator consumption.

## SOR-B registry intake completion

Issue `#118` remains the canonical owner. Bounded registry-intake claim `SOR-B-REGISTRY-INTAKE-2026-08-07` is released complete.

Installed:

```text
scripts/admit_session_consolidation.py @ ec6c4c0db535447f1c5156decc2573501e7f7f09
tests/test_admit_session_consolidation.py @ d99612b1760e7f96808a3c93b7f5fc6dad5c8091
data/session-registry-intake-requests/AUTONOMY-ROLE-AWARE-SESSION-2026-08-04.json @ f9dc7dd4e4f2a976c99c5958826302dfa9120cae
.github/workflows/session-orchestration-registry-intake.yml @ 0b2393f25328dbb21b9fde96c75d9155377e8fa0
canonical registry admission commit produced by workflow: 7502e3a2
```

Hosted evidence:

```text
run 31151898455 / job 92783098428: SUCCESS
5/5 intake tests PASS
SESSION_REGISTRY_INTAKE_PASS:ADMITTED
SESSION_RETIREMENT_PASS
intake artifact 8983603019 sha256 fd1ced97e27f12d978c201363f4885c931315132f17ec28532fd6369dbe19005
retirement artifact 8983603321 sha256 72935fb7714df551e94590f21d4fa8e25fadb3a8ba7073ac45c333898486ae14
```

The real session `autonomy-role-aware-continuation-2026-08-04` is now admitted to the canonical registry as `ARCHIVABLE`. Its complete inventory and consolidation receipt remain authoritative at:

```text
data/session-goal-inventories/AUTONOMY-ROLE-AWARE-SESSION-2026-08-04.json
data/session-consolidation-receipts/AUTONOMY-ROLE-AWARE-SESSION-2026-08-04.json
```

Its unresolved runtime requirements remain repository-native and are not reopened here: Site autonomy telemetry, `StegVerse-org/LLM-adapter`, `GCAT-BCAT-Engine/Triage`, and parent issue #114 retain their named responsibilities and machine-observable release conditions.

## SOR-B successor/frontier/archive projection completion

Bounded claim `SOR-B-SUCCESSOR-QUEUE-2026-08-07` implemented registry-derived continuation and archive projections.

Installed:

```text
scripts/project_session_orchestration.py @ 3a907df7c29e73f4135b948d991479007cc933e3
tests/test_project_session_orchestration.py @ 91a32934a648bbc06d073e027d5dfc16127343a2
.github/workflows/session-orchestration-project.yml initial @ 7e47871ff518f6a2d41fe4fc904b5754f1260c11
untracked-file commit-gate repair @ 294e611d2aebb3165d50acf0e6939c885e7c2994
race-safe latest-main regeneration repair @ 242274ea41b7b4e2c8f42dae6148417422343039
data/session-orchestration-successor-packets.json @ 3301f31c3f785171022d1535fd7a84e5f0fa1933
data/session-orchestration-archive-queue.json @ 9f8df9bdcdc3396bb75c3b833d27b8a46237e65b
```

Hosted evidence:

```text
run 31152073109 / job 92783608826: SUCCESS
6/6 projection tests PASS
SESSION_RETIREMENT_PASS
SESSION_ORCHESTRATION_PROJECTION_PASS
successor artifact 8983665857 sha256 c5c34a9d55b1c46b3b628b355cb147fac7a82f31029023bd6401d23da09fd9c2
archive queue artifact 8983666266 sha256 75e0cba569c30ebfba9ff001fca984a384e2101f4e1214e9fab5717098134dc7
retirement artifact 8983666632 sha256 e8b94a0d30435a28df1a2842f4ce05c8f569a6e2c49d460db4fa3c8ab7520bfa
```

A subsequent hosted run exposed a real false-completion defect: generated untracked projection files were uploaded as artifacts but `git diff` did not detect them for commit. That defect was corrected. A concurrent-main push then exposed a non-fast-forward race; the workflow was further hardened to fetch/rebase, rerun retirement validation, regenerate from the latest registry, recheck projection determinism, and only then push. Race-safe run `31152326036` / job `92784386128` completed SUCCESS with all projection and verification steps successful.

Current projection facts:

```text
frontier_state: READY
next_executable session: session-orchestration-activation-coordination-2026-07-31
archive candidates: 5
CURRENT queue entries: 1
UI archive action claimed: false
projection failures: 0
```

## Preserved consolidated sessions

Detailed originating goals and adjacent requirements are durable in the registry and their session inventory/receipt files. No requirement depends only on chat history.

Canonical records include:

```text
session-orchestration-design-2026-07-31 -> registry ARCHIVABLE
session-orchestration-activation-coordination-2026-07-31 -> registry CURRENT, issue #114
stegmusic-st018-continuation-2026-08-02 -> registry ARCHIVABLE; continuation data/tasks/SITE-ST018-VALIDATION-EVIDENCE.json
hil-runtime-consolidation-2026-08-02 -> registry ARCHIVABLE; continuation docs/HIL_SESSION_CONSOLIDATION_MIRROR_HANDOFF.md
continuation-authority-stack-2026-08-02 -> registry ARCHIVABLE; requirements merged into #118
Autonomy role-aware continuation 2026-08-04 -> registry ARCHIVABLE; unresolved runtime work repository-native
```

The continuation-authority stack requirements remain mandatory #118 behavior:

```text
blocked/waiting is scheduling input, never silent success
successor packets preserve originating goal, repository, branch, task, commit, authority source, claimant, release condition, collision boundaries, expected evidence, completion conditions, and nonclaims
cross-repository comparison detects stale handoffs, conflicting owners, unresolved successors, incompatible claims, duplicate work, and missing authority
archive projection distinguishes terminal, blocked, retry, review, failed, claimed, superseded, and merged semantics without claiming UI actions
frontier output states why no executable candidate exists when empty
repeated blockers and validator defects remain durable improvement observations
```

## Activation gate

The parent layer becomes activated only after all conditions are directly observed and recorded:

1. retained validator workflow PASS — **PASS**;
2. canonical Site orchestrator consumes retirement state — **PASS**;
3. one real `SUPERSEDED` disposition admitted — **OPEN**;
4. one real `MERGE_REQUIRED` disposition rejected from archival — **OPEN; deterministic rejection PASS**;
5. one real `ARCHIVABLE` disposition admitted — **PASS**;
6. no conflicting current owner — **PASS within Site registry; cross-repository proof OPEN**;
7. successor execution source resolves — **PASS within Site registry; cross-repository proof OPEN**;
8. handoff and registry carry resulting receipts — **PARTIAL; SOR-A and major SOR-B receipts installed**;
9. validated Master-Records custody return evidence exists before downstream projection — **BLOCKED on #119 after remaining SOR-B**.

## Active claims and collision boundaries

```text
#117: CLOSED, claim released
#118: ACTIVE canonical owner
  registry-intake claim: RELEASED COMPLETE
  successor/frontier/archive projection claim: RELEASED COMPLETE after race-safe hosted PASS
  cross-repository comparison: UNCLAIMED/OPEN unless a newer durable claim appears
#119: ACTIVE canonical custody owner, execution dependency-blocked
#114: ACTIVE parent activation admission and closure owner
```

No session may duplicate completed SOR-A, registry-intake, or registry-derived projection implementation. The next implementation lane must inspect live #118 and repository state again before claiming cross-repository comparison.

## Remaining work

Destination `StegVerse-Labs/Site`, canonical owner issue `#118`:

```text
Implement governed cross-repository *_MIRROR_HANDOFF.md and task-owner comparison after reading each destination handoff
Add hash-bound/signed archive-disposition receipts consistent with repository authority boundaries
Integrate task-relative stale-heartbeat comparison where canonical heartbeat state does not already supply it
Establish one real SUPERSEDED disposition from live repository evidence
Establish one real MERGE_REQUIRED rejection from live repository evidence without manufacturing unique state
Bind cross-repository comparison results into successor/frontier/archive projection
Update issue #114 with final SOR-B receipts and activation-gate result
```

Destination `master-records/orchestration`, canonical owner issue `#119`:

```text
define and validate outbound archive-disposition receipt packet
custody validated archive dispositions
verify registry lineage and reconstruction
return immutable receipt hashes and reconstruction status to Site
```

Downstream destinations only after verified activation and custody:

```text
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

## Next executable action

Read this handoff and issue #118 again. Search each intended comparison repository for its applicable `*_MIRROR_HANDOFF.md` before mutation. If no newer active claim owns cross-repository comparison, claim only that slice with exact paths, collision boundaries, timestamp, expected evidence, and release condition. Do not reopen completed SOR-A, registry intake, or Site-only projection work.

## Archive readiness

Completed SOR-A and completed SOR-B slices no longer require a chat session. Their code, workflow runs, artifacts, registry state, and canonical projections are durable. The broader orchestration activation remains non-archivable while #118 cross-repository comparison and real-disposition gates remain open and #119 custody is dependency-blocked. A session that owns no unique slice should merge into issue #118 rather than remain open for historical context.
