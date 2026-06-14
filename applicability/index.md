# Governed Admissibility Applicability Map

Generated: `2026-06-14`

## Purpose

This section defines the range of topics where governed admissibility directly applies and explains why testers in each discipline should care.

Governed admissibility is not a replacement for domain expertise. It is a boundary discipline for deciding what an output, claim, artifact, instruction, transition, or action is allowed to become before it is published, executed, relied upon, or escalated.

## Core rule

```text
Generated or proposed output
→ declared intent
→ domain context
→ authority/evidence/replay/consequence checks
→ admissibility decision
→ allowed next state
```

## Direct applicability

Governed admissibility directly applies wherever there is a proposed transition from one state to another and that transition can affect truth posture, authority, execution, safety, money, rights, access, identity, infrastructure, education, or public understanding.

## Discipline-facing map

| Discipline | Why admissibility applies | Typical test object |
|---|---|---|
| AI / LLM systems | Outputs can become claims, instructions, decisions, or automation inputs. | Model response, tool call, agent plan, generated artifact |
| Mathematics / formal methods | Proof attempts and derivations require posture before becoming claims. | Lemma, derivation, solver artifact, counterexample |
| Software engineering | Code and automation move from suggestion to execution. | Pull request, script, workflow, deployment action |
| Cybersecurity / identity | Access, secrets, credentials, and trust boundaries require explicit authority. | Token use, identity assertion, permission change |
| Data governance | Data movement changes authority, privacy, and evidence posture. | Dataset, record merge, data export, retention action |
| Legal / policy | Text can affect rights, obligations, compliance, and interpretation. | Policy draft, legal summary, compliance claim |
| Medicine / health | Outputs may become advice or care decisions. | Health explanation, risk classification, care instruction |
| Finance / markets | Claims can influence allocation, risk, payment, or investment behavior. | Financial summary, transaction proposal, risk statement |
| Education / learning | Outputs can shape assessment, curriculum, or learner development. | Lesson, assessment, tutoring response, grading rationale |
| Science / research | Findings require source posture and reproducibility before publication. | Paper summary, hypothesis, analysis result, citation map |
| Engineering / infrastructure | Recommendations may affect physical systems and operational risk. | Design decision, inspection note, maintenance recommendation |
| Robotics / autonomy | Model outputs may become physical-world actions. | Motion plan, task instruction, safety override |
| Journalism / public information | Outputs may become public claims or narratives. | Article draft, source summary, timeline entry |
| Government / civic systems | Outputs may affect authority, services, eligibility, or public trust. | Decision memo, eligibility rule, service action |
| Organizational governance | Decisions require authority, quorum, evidence, and consequence posture. | Board action, approval chain, exception, override |
| Archives / records / history | Claims require provenance and review posture. | Timeline event, source annotation, historical claim |

## Non-goal

This map does not claim domain authority in each field. It identifies where admissibility testing applies because a proposed output may become a consequential next state.

## Next stage

1. Create machine-readable discipline registry.
2. Create tester guide.
3. Map each discipline to test types.
4. Add public Site page once the registry is stable.
