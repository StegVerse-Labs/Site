# Ecosystem Chat Interaction Telemetry

## Purpose

This document defines the Site preview contract for the future StegVerse Ecosystem LLM interaction meter.

Ecosystem Chat is intended to become the user-facing interface for the StegVerse ecosystem. A response should not only provide text. It should also show which classes of ecosystem work were involved in producing that response.

## Preview fields

Every preview payload may include:

```json
{
  "interaction_bands": ["intra", "inter", "research", "provider", "solver", "receipt"],
  "interaction_profile": {
    "intra": 0,
    "inter": 0,
    "research": 0,
    "provider": 0,
    "solver": 0,
    "receipt": 0
  },
  "math_solver_supported": true
}
```

The current Site implementation is display-only. Values are deterministic local preview values from the browser script.

## Band meanings

| Band | Meaning |
|---|---|
| `intra` | StegVerse-local records, repos, manifests, docs, standards, and continuity material. |
| `inter` | Connected adapters, partner systems, external ecosystem nodes, and provider-client surfaces. |
| `research` | Networked public sources outside the ecosystem when current outside evidence is required. |
| `provider` | Model/provider routing, fallback, cost, latency, and quota accounting. |
| `solver` | Math-problem solving, calculation traces, unit conversion, symbolic checks, and proof-step verification. |
| `receipt` | Hash, replay, reconstruction, admissibility, continuity, and authority-evidence load. |

## Site-side status

```text
Interaction band UI: installed
Local interaction profile: installed
Fixture coverage: installed
Boundary checker coverage: installed
Contract checker coverage: installed
Live gateway telemetry: pending backend activation
Live math solver: pending backend activation
Live provider accounting: pending backend activation
Live research routing: pending backend activation
```

## Non-claims

```text
A local preview value is not a live measurement.
A local preview value is not proof of source access.
A local preview value is not a receipt.
A solver preview route is not a solved answer.
A provider preview route is not a model call.
A research preview route is not a network lookup.
```

## Next integration target

The governed backend gateway should accept and return the same fields so the static preview can be replaced by measured runtime telemetry without changing the public page contract.
