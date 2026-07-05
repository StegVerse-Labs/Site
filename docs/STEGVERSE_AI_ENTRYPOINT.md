# StegVerse AI Entry Point

## Product target

The preferred product model is one primary StegVerse AI window.

Users should not need to understand which repo, SDK, runtime, adapter, or governance layer they need before asking. They enter a query, statement, request, or input candidate in one place. The StegVerse AI entry point then determines whether the request should be answered directly, routed, explained, compared, submitted to SDK intake, or rejected.

## One-window model

```text
User input
-> StegVerse AI entry point
-> route classification
-> governed LLM response when appropriate
-> ecosystem task guidance when appropriate
-> SDK access guidance when appropriate
-> comparison panes when requested or useful
-> receipt / reconstruction metadata when available
```

## Primary functions

The single entry point should be able to:

1. answer normal user questions as the StegVerse LLM;
2. explain StegVerse concepts and ecosystem essentials;
3. classify requests into user, research, SDK, runtime, governance, documentation, or restricted-admin routes;
4. explain how to gain access to the SDK or other ecosystem parts;
5. produce comparison outputs from external LLMs under non-authoritative labels;
6. preserve manifest, receipt, authority, and reconstruction metadata for governed transitions;
7. refuse or redirect requests that require authority the user does not have.

## Downstream pages

Downstream pages still matter, but they become focused destinations rather than the starting point.

```text
StegVerse AI Entry Point
  -> LLM comparison view
  -> SDK / API access view
  -> governance / receipts view
  -> runtime status view
  -> research workspace
  -> documentation / public proof index
```

## Boundary

The entry point is not a raw terminal, not a credential surface, not a direct repo mutation interface, and not execution authority. It can prepare transition candidates and route requests. Consequential actions require governed authority checks.

## Relationship to current pages

`ecosystem-chat.html` is the current advancement console. `stegverse-llm-console.html` is the current static LLM comparison prototype.

The next product step is to rename/reframe the user-facing entry as `Ecosystem Chat & LLM` and make the first visible interface one StegVerse AI input window with route-aware outputs underneath.
