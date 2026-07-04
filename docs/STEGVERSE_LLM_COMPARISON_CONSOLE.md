# StegVerse LLM Comparison Console

## Product target

The target user experience is a public webpage that presents like a familiar chat UI while preserving StegVerse governance boundaries.

A user enters a query, statement, file-derived prompt, or other allowed input. The page returns:

1. a primary StegVerse governed LLM response; and
2. separate comparison panes for external LLM responses.

The StegVerse response is the governed response surface. External responses are comparison inputs unless they pass through the same StegVerse governance path.

## Target layout

```text
User input

Primary output
  StegVerse LLM response
  - governed transition candidate
  - admissibility status
  - authority status
  - receipt / reconstruction metadata

Comparison outputs
  ChatGPT response
  Claude response
  Other provider response
```

## Required distinction

```text
StegVerse LLM response == governed ecosystem output candidate
External LLM response == comparison output only
External LLM response authority == false unless governed
```

## Minimum MVP behavior

The first MVP can be fixture-first and non-networked:

```text
user input
-> local StegVerse governed-response scaffold
-> mock external model panes
-> manifest preview
-> receipt preview
-> no live provider call
-> no execution authority
```

## Later activation behavior

A later governed backend can replace mock panes with provider adapters:

```text
user input
-> ingestion
-> fingerprint/hash
-> StegVerse governed LLM response path
-> external provider adapter calls
-> per-provider response capture
-> comparison display
-> admissibility/reconstruction metadata
```

## Boundary

The console must not claim that external LLMs are governed, authoritative, endorsed, or correct. It may display their outputs for comparison only. Any output that affects execution, publication, memory mutation, repo mutation, user-impacting action, or ecosystem state change must become a governed transition candidate before consequence.

## Relationship to Ecosystem Chat

`ecosystem-chat.html` is currently an advancement console and governed task-boundary surface. The StegVerse LLM Comparison Console is a product goal beyond that page: it is a user-facing query/response console with the StegVerse governed answer first and external LLM comparison panes below.
