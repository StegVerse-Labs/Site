# StegVerse Governance Testing Suite

Generated: `2026-06-14`

## Purpose

The Governance Testing Suite is the public Site layer for showing how StegVerse governance changes what generated output, proposed claims, and proposed state movements are allowed to become.

The suite is intentionally static at this stage. It does not host an LLM. It does not determine whether a claim is true. It classifies public posture under declared authority, evidence, replay, and consequence conditions.

## Boundary

```text
Site  = public mirror
Tests = public admissibility simulations
Proof = formalism-tests / governed authority repos / receipt-backed artifacts
```

The testing suite must not be treated as proof authority until a future governed test repository or formalism source provides receipt-backed test fixtures and replay evidence.

## Governing question

```text
The question is not:
  Is the LLM answer good?

The governing question is:
  What is this answer allowed to become?
```

## Current baseline tests

| Test | Path | Purpose |
|---|---|---|
| LLM Governance Filter | `tests/governance-filter.html` | Paste output and classify admissibility posture. |
| LLM Governance Comparison | `tests/llm-governance-comparison.html` | Compare raw generated output against governed posture. |
| Transition Admissibility | `tests/transition-admissibility.html` | Classify proposed state movement. |
| Receipt Replay | `tests/receipt-replay.html` | Check replay continuity from prior state to next state. |
| Fail-Closed | `tests/fail-closed.html` | Show how missing continuity blocks unsafe public movement. |

## Machine-readable manifest

The suite manifest is published at:

```text
tests/test-manifest.json
```

It records the public posture, test list, expected input classes, output classes, decisions, and next-stage development path.

## Current posture

```text
Claim id: GOV-TEST-SUITE-001
Posture: RESEARCH_NOTE
Status: published as public testing simulation only
```

## Decision vocabulary

Current decision values include:

```text
ALLOW
ALLOW_AS_NOTE
ALLOW_PRIVATE
ALLOW_WITH_POSTURE
FAIL_CLOSED
HOLD
PARTIAL_REPLAY
REPLAY_CONFIRMED
REQUIRE_AUTHORITY
REQUIRE_INPUT
REQUIRE_REPLAY
REQUIRE_REVIEW
```

## Next stage

The next stage should not simply add more pages. It should make the existing tests more governable:

1. Extract shared test logic into a reusable script.
2. Add test vectors with expected decisions.
3. Add receipt-backed replay fixtures when authority exists.
4. Promote selected tests from static simulation to receipt-backed posture only when source authority and replay evidence exist.
