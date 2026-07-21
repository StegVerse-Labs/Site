# StegVerse Reuse-First Build Directive

## Canonical URLs

Use these URLs as the durable references for the directive and current Ecosystem Chat build path.

### Site source of truth

- Site repository: https://github.com/StegVerse-Labs/Site
- Site mirror handoff: https://github.com/StegVerse-Labs/Site/blob/main/docs/SITE_MIRROR_HANDOFF.md
- Site mirror handoff check: https://github.com/StegVerse-Labs/Site/blob/main/docs/SITE_MIRROR_HANDOFF_CHECK.md
- Ecosystem Chat surface: https://github.com/StegVerse-Labs/Site/blob/main/ecosystem-chat.html
- Ecosystem Chat client runtime: https://github.com/StegVerse-Labs/Site/blob/main/assets/ecosystem-chat.js
- Universal Translator surface: https://github.com/StegVerse-Labs/Site/blob/main/universal-translator.html
- Universal Translator client runtime: https://github.com/StegVerse-Labs/Site/blob/main/assets/universal-translator.js
- Universal Translator contract: https://github.com/StegVerse-Labs/Site/blob/main/docs/UNIVERSAL_TRANSLATOR_CONTRACT.md

### Runtime and provider owner

- LLM adapter repository: https://github.com/StegVerse-org/LLM-adapter
- Canonical deployment-recovery issue: https://github.com/StegVerse-org/LLM-adapter/issues/18
- Universal Translator gateway issue: https://github.com/StegVerse-org/LLM-adapter/issues/21
- Canonical StegDeploy bootstrap: https://github.com/StegVerse-org/LLM-adapter/blob/main/scripts/stegdeploy_bootstrap.py
- Ecosystem Chat live verifier: https://github.com/StegVerse-org/LLM-adapter/blob/main/scripts/verify_live_ecosystem_chat_activation.py
- Live activation workflow: https://github.com/StegVerse-org/LLM-adapter/blob/main/.github/workflows/ecosystem-chat-live-activation.yml

### Custody, reconstruction, publication, admissibility, and guardian destinations

- Master-Records organization: https://github.com/master-records
- Publisher repository: https://github.com/GCAT-BCAT-Engine/Publisher
- Admissibility Wiki: https://github.com/StegVerse-Labs/admissibility-wiki
- Admissibility mirror handoff: https://github.com/StegVerse-Labs/admissibility-wiki/blob/main/ADMISSIBILITY_MIRROR_HANDOFF.md
- StegGuardian Wiki: https://github.com/StegVerse-002/stegguardian-wiki
- StegTalk repository: https://github.com/StegVerse-Labs/StegTalk
- Comms Gateway: https://github.com/StegVerse-Labs/Comms-Gateway

## Primary Rule: Integrate Before Building

Do not treat StegVerse work as greenfield.

Before creating a new component, abstraction, workflow, monitor, status file, scheduler, service, schema, adapter, or repository:

1. Identify the exact capability required by the active goal.
2. Search the existing StegVerse ecosystem for implementations, partial implementations, compatible components, retained artifacts, handoffs, receipts, schemas, workflows, tests, and deployed services that may already provide it.
3. Classify each candidate as directly reusable, reusable with bounded modification, reusable through an adapter, or unsuitable because of a specific conflict.
4. Prefer direct reuse, configuration, interface binding, small repair, adapter, extension, and only then replacement or new implementation.

Existing components do not need to be perfect. Reuse them when they are sufficiently correct, secure, governable, maintainable, and compatible with the active goal.

## New-Build Decision Requirement

Do not begin a new build merely because it appears cleaner, easier, more modern, or more observable.

Before building a new component, record:

- required capability;
- existing candidates evaluated, including repository and path;
- current behavior and reusable portion;
- missing behavior or incompatibility;
- adaptation cost and risk;
- options for reuse unchanged, bounded modification, adapter, or replacement;
- goal progress, effort, technical risk, governance implications, consumer effects, reversibility, and recommendation.

When the choice would materially alter architecture, duplicate a core capability, or replace existing work, stop for explicit approval.

## Goal-Progress Test

A change counts only when it directly enables, executes, verifies, secures, or retains evidence for a required step in the active end-to-end goal.

Current Ecosystem Chat path:

```text
request
-> governed provider response
-> usage persistence
-> custody
-> reconstruction
-> immutable verified receipt
-> Site activation
-> downstream propagation
```

Portable-node Ecosystem Chat path:

```text
portable-node identity
-> local request
-> governed provider or peer response
-> local vault persistence
-> receipt generation
-> heartbeat-bound continuity
-> offline/online continuity
-> optional governed custody
-> verified synchronization
```

Documentation, monitoring, scheduling, status representation, or orchestration does not substitute for missing runtime execution.

## Vertical-Slice Priority

1. Execute the real path.
2. Observe the actual failure.
3. Repair the failure using existing ecosystem capabilities where possible.
4. Rerun the path.
5. Retain durable proof.
6. Propagate the verified result.
7. Harden and broaden only after the slice works.

Do not build generalized automation around a path that has not run successfully.

## Heartbeat Boundary

The StegVerse heartbeat is the governing runtime system of record operating at applicable runtime frequencies and pulse classes.

It is not a GitHub Actions cron, hourly scheduler, fifteen-minute status update, repository commit frequency, CI liveness file, or substitute for runtime continuity.

GitHub Actions may validate, test, package, publish, or retain evidence derived from runtime. It must not define heartbeat cadence, continuity, authority, or existence.

Do not modify heartbeat architecture without locating and reviewing its authoritative design and implementation records.

## No Unilateral Removal

Before deleting, removing, disabling, renaming, superseding, replacing, reverting, or deprecating anything, provide a removal proposal containing:

- repository;
- exact path or component;
- proposed action;
- reason;
- conflict evidence;
- dependencies;
- downstream effects;
- lost information or capability;
- restoration method;
- safer alternatives;
- recommendation.

No removal occurs without explicit approval.

## Preserve Installed Value

Account for existing repositories, prior architecture, deployed infrastructure, provider integrations, continuity and receipt systems, Master-Records, ingestion engines, reconstruction logic, governance and admissibility controls, StegTalk, portable-node work, heartbeat architecture, automated workflows, tests, evidence, and AI or cloud assistance.

Plans and estimates must begin from the actual integrated state, not a generic greenfield comparison.

## Source-of-Truth Review

At the start of work:

1. Read the Site mirror/build handoff.
2. Read the active goal record.
3. Read the active building/status record.
4. Inspect repositories and files directly involved in the next runtime step.
5. Separate completed, declared, and evidence-proven states.

## Site Goal and Active-Building Updates

Every meaningful build cycle must update both Site records with the actual end-to-end goal, completion criteria, runtime path, owners, progress definition, blocker, next executable step, manual-action requirement, work performed, reused components, modifications, adapters, new-build rationale, executed tests, observed results, exact failures, durable evidence, commit references, removal proposals, and current next step.

State labels must remain distinct:

```text
DESIGNED
IMPLEMENTED
INTEGRATED
EXECUTED
VERIFIED
DEPLOYED
LIVE
PROPAGATED
```

Code existence, workflow installation, documentation, or intended behavior does not justify a later state.

## Progress Accounting

End every cycle with:

- goal delta;
- reuse delta;
- runtime evidence;
- non-progress;
- next critical step.

Do not increase completion percentages for documentation alone, status files alone, handoffs alone, monitors that do not enable runtime, unexecuted scheduled workflows, consumers waiting for nonexistent evidence, duplicated architecture, or speculative future integration.

## Decision Discipline

When blocked:

1. identify the exact failing boundary;
2. identify its owner;
3. inspect existing implementations;
4. repair or integrate the narrowest viable path;
5. retain the exact blocker if unrepaired;
6. continue only with another independent step still required by the same goal.

Do not manufacture secondary automation to make a blocker appear more active.

## Operating Authority

Continue without routine manual user actions, but stop before removals, destructive changes, replacement of core architecture, heartbeat redefinition, duplicate core systems, declared-goal changes, or unauthorized release, deployment, execution, custody, or governance grants.

## Required Session Output

At the beginning state:

- Active goal
- Current proven state
- Next missing runtime step
- Existing components being evaluated for reuse

At the end state:

- What became functional
- What existing capability was reused
- What remains unproven
- What was proposed but not changed
- Next executable step

## Standing Instruction

Optimize for a functioning, verified, integrated StegVerse system, not for file, workflow, abstraction, repository, document, or commit count.

Reuse acceptable existing capabilities. Repair and connect before replacing. Discuss meaningful alternatives when new construction is genuinely necessary. Never remove anything without an explicit removal list and approval.
