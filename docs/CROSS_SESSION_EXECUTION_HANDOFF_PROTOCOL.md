# Cross-Session Execution and Handoff Protocol

## Purpose

This document governs continuation when a StegVerse task must move between ChatGPT, Codex, GitHub-connected, Cloudflare-connected, or other tool-bounded sessions.

A session prompt can transfer instructions and state. It cannot transfer credentials, connector availability, account authorization, hidden workflow permissions, or runtime access. Every new session must therefore discover its actual tools before selecting an execution path.

## Mandatory opening sequence for every continuation session

1. Read this document.
2. Read the task-specific canonical handoff named by the user's prompt.
3. Read the task-specific execution prompt named by the user's prompt.
4. Inspect the repository's latest commits and machine-readable status files before relying on narrative status.
5. Discover the tools and connectors actually available in the current session.
6. Use direct provider controls when available; use repository workflows only when direct controls are unavailable or when workflows are the governed execution mechanism.
7. Do not claim that a connector is available merely because a prior session had it, the user enabled it elsewhere, or a prompt says it should exist.
8. Do not stop after creating scaffolding, documentation, triggers, diagnostics, or workflows when the requested operational outcome remains unverified.

## Required task handoff contents

Every canonical task handoff must contain:

- repository and organization names;
- current goal;
- end goal and terminal success criteria;
- verified current state;
- exact known failures, including run IDs, commit SHAs, URLs, response codes, and failing steps;
- architecture and authority boundaries;
- relevant source files, scripts, workflows, control files, and status records;
- prior attempted solutions and their outcomes;
- current external dependencies and whether each is verified, assumed, or unavailable;
- the shortest known execution path;
- forbidden shortcuts and false-completion conditions;
- one exact next action for each likely tool environment;
- instructions to update the handoff before ending the session.

## Mandatory closing sequence for every work session

Before responding to the user, the session must:

1. Update the task-specific canonical handoff with all material changes.
2. Update machine-readable status files when the repository architecture supports them.
3. Record exact failures rather than generic states such as `blocked`, `pending`, or `deployment_failed`.
4. Include a ready-to-paste **Next-session prompt** at the end of the response.
5. Point that prompt directly to this protocol and every task-specific handoff required for continuation.
6. Tell the next session to inspect actual connector availability before choosing a path.
7. Preserve the user's no-repeat requirement: do not ask for information already present in the handoff or repository.

## Next-session prompt requirements

The prompt appended to each response must:

- identify the exact repository;
- identify the current operational goal;
- name this protocol;
- name the canonical task handoff;
- name any execution-session prompt;
- direct the next session to inspect the latest repository state and connected tools;
- direct autonomous execution through success or a single proven external-authority block;
- prohibit broad status recaps and repeated discovery;
- require updating all handoffs before the next response.

## Authority and continuity rules

```text
prompt continuity != connector continuity
connector installed elsewhere != connector available in this session
repository write access != provider deployment access
workflow installed != workflow authorized
credential name present != credential value available
prior-session observation != current-session verification
handoff written != task complete
```

## Standing user instruction

At the end of every substantive StegVerse work response, provide a ready-to-paste next-session prompt that points directly to the applicable documentation and handoffs. Maintain those documents so they contain previous task history, current goals, end goals, exact relevant details, and the latest verified execution state.
