# Governed Admissibility Discipline Test Matrix

Generated: `2026-06-14`

## Purpose

This matrix tells discipline testers which governed admissibility tests apply to their work and why.

The tests do not certify domain correctness. They classify what an output, claim, artifact, instruction, transition, or action is allowed to become.

## Test surfaces

| Test | Path | What it classifies |
|---|---|---|
| Governance Filter | `tests/governance-filter.html` | Whether output can become a public claim, research note, repo action, code change, governance decision, professional advice, or private note. |
| LLM Governance Comparison | `tests/llm-governance-comparison.html` | Difference between raw output and governed publication/action posture. |
| Transition Admissibility | `tests/transition-admissibility.html` | Whether a proposed state movement has authority, evidence, replay posture, and consequence posture sufficient for next state. |
| Receipt Replay | `tests/receipt-replay.html` | Whether prior state, decision receipt, next state, and authority continuity can be replayed. |
| Fail-Closed | `tests/fail-closed.html` | Whether missing authority/evidence/replay or high consequence requires hold, review, or fail-closed posture. |
| Math-Solver Adapter | `math-solver/index.html` | How formalism-development work moves from source to instruction packet, artifact return, admissibility result, and claim posture. |

## Discipline routes

| Discipline | Recommended test route | Why |
|---|---|---|
| AI / LLM systems | Governance Filter → LLM Governance Comparison → Fail-Closed | Separates fluent model output from allowed publication, action, tool use, or agent execution. |
| Mathematics / formal methods | Math-Solver Adapter → Receipt Replay → Transition Admissibility | Separates derivation/proof attempts from receipt-backed proof posture and bounded research-note status. |
| Software engineering | Transition Admissibility → Receipt Replay → Fail-Closed | Tests whether code, workflow, or deployment changes are authorized, replayable, and safe to execute now. |
| Cybersecurity / identity | Fail-Closed → Transition Admissibility → Receipt Replay | Prioritizes authority, consequence, credential boundary, and replay posture before access movement. |
| Data governance | Transition Admissibility → Receipt Replay → Governance Filter | Tests whether data movement has provenance, authority, retention posture, and allowed claim limits. |
| Legal / policy | Governance Filter → LLM Governance Comparison → Fail-Closed | Keeps legal or policy text from becoming advice, compliance posture, or institutional position without review. |
| Medicine / health | Governance Filter → Fail-Closed → Transition Admissibility | Distinguishes general information from care guidance, risk classification, or high-stakes instruction. |
| Finance / markets | Governance Filter → Transition Admissibility → Fail-Closed | Separates contextual notes from allocation, payment, investment, or risk actions requiring review. |
| Education / learning | Governance Filter → LLM Governance Comparison → Transition Admissibility | Tests whether outputs support learning, replace judgment, or create assessment/curriculum claims. |
| Science / research | Governance Filter → Math-Solver Adapter → Receipt Replay | Preserves source posture, reproducibility posture, and claim limits before research publication. |
| Engineering / infrastructure | Transition Admissibility → Fail-Closed → Receipt Replay | Tests whether recommendations that affect physical systems have authority, review, replay, and consequence posture. |
| Robotics / autonomy | Transition Admissibility → Fail-Closed → Receipt Replay | Classifies whether a plan may execute, hold, require review, or fail closed before physical action. |
| Journalism / public information | Governance Filter → LLM Governance Comparison → Receipt Replay | Separates draft/source notes from public claims, timelines, and narratives requiring source posture. |
| Government / civic systems | Transition Admissibility → Fail-Closed → Receipt Replay | Tests authority, eligibility, service action, public notice, and administrative consequence posture. |
| Organizational governance | Transition Admissibility → Receipt Replay → Fail-Closed | Tests authority, quorum, evidence, refusal, override, and commit-time validity. |
| Archives / records / history | Receipt Replay → Governance Filter → Transition Admissibility | Tests provenance and replay posture before source notes become timeline or historical claims. |

## Tester return shape

```text
Discipline:
Test object:
Recommended route:
Declared intent:
Authority source:
Evidence posture:
Replay posture:
Consequence level:
Decision:
Allowed next state:
Required follow-up:
Claim limit:
```

## Boundary

The matrix maps applicability and route selection. It does not certify factual truth, professional correctness, proof closure, medical correctness, legal correctness, financial suitability, or engineering safety.
