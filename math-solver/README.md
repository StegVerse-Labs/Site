# StegVerse Mathematics Educator / Solver Specialty

## Current product role

The mathematics capability is a specialty family consumed through the Site's single primary conversational surface, `ecosystem-chat.html`.

```text
user mathematics request
-> ecosystem-chat.html
-> mathematics intent / subject classification
-> pedagogical response
-> governed solver or verification tool when needed
-> result / receipt / replay evidence when execution occurs
```

`math-solver/index.html` remains a deep-work, tool, compatibility, and proof destination. It is **not** a competing primary chat application and does not own a separate general provider/runtime stack.

Canonical topology:

```text
parent goal: StegVerse-Labs/Site#239
mathematics capability: StegVerse-Labs/Site#240
shared capability contract: data/unified-conversational-capabilities.json
shared runtime owner: StegVerse-org/LLM-adapter
canonical StegGate owner: StegVerse-Labs/StegCore
```

## Capability scope

The mathematics educator is broader than a single equation solver. It should support ordinary-language mathematics education across subject levels and styles, including:

```text
explanation
hints
guided solutions
checking work
alternate methods
prerequisites
notation
proof structure
history and foundations
philosophy of mathematics where relevant
solver/tool execution when separately admitted
```

## Image boundary

A supported mathematics image may enter through the shared conversational surface. Image interpretation/transcription is a distinct step from solving.

```text
image
-> transcription / structural interpretation
-> confidence / ambiguity preservation
-> user correction when needed
-> mathematical classification
-> guided solution or admitted solver execution
```

Uncertain transcription must never silently become mathematical fact. The user must be able to correct the interpreted expression before downstream reasoning depends on it.

## Governance boundary

A solver or model does not gain authority from producing an answer. Tool execution must remain bounded by the applicable StegGate/tool contract, and execution evidence must remain distinguishable from explanation-only conversation.

```text
model output != proof
solver output != authority
instruction packet != completion
CI pass != public runtime
static example != real solver execution
handoff != activation
```

## Historical adapter posture

The original public Math-Solver Governance Adapter was published in June 2026 as a `RESEARCH_NOTE`. That history is preserved, but it no longer defines the product's primary topology.

Historical chain:

```text
formalism state
-> source-to-instruction mapping
-> governed instruction packet
-> solver/model task
-> returned artifact
-> admissibility result
-> receipt/replay posture
```

Those packet concepts remain useful for formalism and deep-work execution; they now sit behind the shared conversational capability rather than defining a separate public application.

## Deep-work files

```text
math-solver/index.html
math-solver/papers.html
math-solver/adapter-manifest.json
math-solver/sources/
math-solver/mappings/
math-solver/generation/
math-solver/templates/
math-solver/examples/
```

The static example lifecycle remains illustrative only and must not be represented as a real solver run or proof.

## Completion gate

The mathematics capability is not complete merely because this README, the deep-work page, schemas, examples, or tests exist. Completion requires a real mathematics request through `ecosystem-chat.html`, correct capability routing, governed tool/solver execution where applicable, result binding, and deterministic replay/verification evidence required by Site#239/#240.

No duplicate provider/runtime authority may be created to satisfy this goal.
