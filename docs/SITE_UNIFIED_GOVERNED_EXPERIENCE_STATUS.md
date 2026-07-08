# Site Unified Governed Experience Status

## Status

```text
Repository: StegVerse-Labs/Site
Goal: unified-governed-experience
Status: phase-2-local-intent-engine-installed
Primary operating surface: ecosystem-chat.html
Homepage posture: single primary Ecosystem Chat entry plus governed transition menu
Intent catalog: data/ecosystem-chat-transition-intents.json
Execution authority: none from Site
Receipt authority: none from Site
```

## Product Shape

The Site is no longer intended to behave as a flat collection of equal public entry points.

```text
User request
  -> Ecosystem Chat
  -> intent classification
  -> boundary check
  -> evidence route
  -> transition destination
  -> receipt / replay path when live authority exists
```

## Required Homepage Contract

```text
Primary hero action: Open Ecosystem Chat -> ecosystem-chat.html
Secondary hero action: View transition menu -> #transition-menu
Transition menu required: yes
Primary framing required: Everything else is a governed transition.
```

## Transition Intent Engine

Phase 2 installs a local preview intent engine. It does not call a model provider, search the network, write repositories, or execute tasks.

```text
Catalog: data/ecosystem-chat-transition-intents.json
Browser classifier: assets/ecosystem-chat.js
Validator: scripts/check_ecosystem_chat_boundary.py
Declared task: data/headless-tasks/ecosystem-chat-boundary-check-v1.json
```

Required categories:

```text
Explain
Demonstrate
Compare
Research
Build
Replay
Runtime
Formalism
SDK
Implementation
Solver
```

Each chat preview response should include:

```text
Transition intent
Suggested transition
Transition destination
Transition boundary
```

## Transition Destinations

The homepage may keep destination links, but they must be framed as governed transitions instead of competing starting points.

```text
Explain admissibility -> admissibility-wiki.html
Demonstrate governance -> demo.html
Evaluate a runtime -> governance-observatory.html
View governed ecosystem model -> governed-ecosystem.html
Inspect transition table -> transition-table.html
Inspect TT implementation mirror -> tt-code-representation.html
Use math-solver adapter -> math-solver/index.html
Read the research -> Papers.html
Review product boundary -> product.html
Inspect proof stages -> formalism-tests-stage-1-to-31.html
Review STCM -> formalisms/stcm.html
Review RTG -> formalisms/rtg.html
```

## Non-Claims

```text
Homepage transition links are not execution authority.
Ecosystem Chat preview is not live backend activation.
A transition destination is not a proof receipt.
The Site is still a public mirror and transition-router preview.
The local intent engine is not model reasoning, not authority, and not a live backend.
```

## Next Phase

```text
Phase 3: contextual continuation panel
```

The next phase should show contextual "Continue to..." destinations beside the chat response, derived from the same transition intent classification.
