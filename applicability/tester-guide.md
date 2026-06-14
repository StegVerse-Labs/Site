# Governed Admissibility Tester Guide

Generated: `2026-06-14`

## Purpose

This guide explains how testers in different disciplines should understand governed admissibility.

The test is not asking whether the output is interesting, fluent, useful, or impressive.

The test asks:

```text
What is this output allowed to become?
```

## Why this applies across disciplines

Governed admissibility applies whenever an output, claim, instruction, artifact, or proposed transition could become a consequential next state.

Examples:

```text
text → public claim
summary → policy posture
solver output → proof claim
agent plan → tool action
code suggestion → deployment
paper citation → evidence support
health explanation → care decision
financial summary → allocation decision
lesson output → assessment or curriculum
```

## What testers should classify

For each test object, identify:

```text
1. Declared intent
2. Domain context
3. Authority source
4. Evidence posture
5. Replayability
6. Consequence level
7. Claim limit
8. Allowed next state
```

## Core admissibility decisions

```text
ALLOW
ALLOW_AS_NOTE
ALLOW_WITH_POSTURE
REQUIRE_REVIEW
REQUIRE_TEST
REQUIRE_RECEIPT
REQUIRE_REPLAY
HOLD
FAIL_CLOSED
NOT_ADMISSIBLE
```

## Discipline examples

### AI / LLM systems

A model response may be harmless as a draft but not admissible as a public claim, instruction, or autonomous action.

Test object examples:

```text
model response
tool call
agent plan
generated artifact
```

Primary question:

```text
Can this output become a claim, tool action, instruction, or only a draft?
```

### Mathematics / formal methods

A derivation or solver artifact may be useful as a research note without being admissible as proof.

Test object examples:

```text
lemma
proof attempt
derivation
counterexample
solver artifact
```

Primary question:

```text
Can this artifact become a proof claim, or must it remain a bounded research note?
```

### Software engineering

A code suggestion becomes more consequential when it is merged, deployed, scheduled, or granted credentials.

Test object examples:

```text
pull request
script
workflow
configuration change
deployment action
```

Primary question:

```text
Is this change authorized, replayable, and safe to execute now?
```

### Cybersecurity / identity

Identity and access actions require strong authority boundaries because mistakes can create invisible trust failures.

Test object examples:

```text
token use
identity assertion
permission change
secret handling
access request
```

Primary question:

```text
Is this access or identity transition authorized, evidenced, and consequence-bounded?
```

### Legal / policy

Legal or policy text can be useful context, but it must not become advice, compliance posture, or institutional position without review.

Primary question:

```text
What claim is allowed, and what domain review is required before stronger posture?
```

### Medicine / health

Health-related output can cross from explanation into advice or care direction.

Primary question:

```text
Is this only general information, or is it being treated as care guidance requiring domain review?
```

### Finance / markets

Financial outputs can influence risk, payment, investment, or allocation decisions.

Primary question:

```text
Is this a contextual note, a risk claim, or an action recommendation requiring review?
```

### Education / learning

Educational outputs can affect learning paths, assessments, and claims about competence.

Primary question:

```text
Is this output supporting learning, replacing judgment, or creating an assessment claim?
```

### Science / research

Research outputs require source posture, reproducibility posture, and claim limits.

Primary question:

```text
What can be claimed from this evidence, and what must remain hypothesis or research note?
```

### Engineering / infrastructure

Engineering outputs may affect physical systems, uptime, safety, or maintenance.

Primary question:

```text
Is this recommendation authorized, reviewed, and safe to move into operation?
```

### Robotics / autonomy

Autonomous instructions can become physical-world actions.

Primary question:

```text
Should this plan execute, hold, require review, or fail closed?
```

### Journalism / public information

Public information outputs can become claims, narratives, or timelines.

Primary question:

```text
Is the source posture strong enough for publication, or only for draft/research use?
```

### Government / civic systems

Civic outputs can affect eligibility, services, authority, or public trust.

Primary question:

```text
Does this action have authority, evidence, replayability, and consequence review?
```

### Organizational governance

Governance decisions require authority, quorum, evidence, and refusal consequences.

Primary question:

```text
Is the decision valid now, under current authority and evidence, at commit time?
```

### Archives / records / history

Historical claims require source posture and provenance.

Primary question:

```text
Can this become a timeline claim, or must it remain a source note?
```

## Tester output shape

A tester should be able to return:

```text
Discipline:
Test object:
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

This guide explains where governed admissibility testing applies. It does not replace domain expertise, professional review, formal proof, medical review, legal review, financial review, engineering sign-off, or civic authority.
