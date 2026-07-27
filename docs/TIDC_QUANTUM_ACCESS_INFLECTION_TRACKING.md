# TIDC Quantum Access-Inflection Tracking Note

## Status

```text
posture: RESEARCH_NOTE
research_state: PILOT_NOT_CONFIRMATORY
ledger_event_added: false
tracked_case_id: QAI-2025-JP-OSAKA
```

## Why this case is being tracked

The July 28, 2025 launch of the University of Osaka-led fully Japan-made superconducting quantum computer is relevant to Technology-Induced Discovery Clustering because it combines four transition-enabling conditions:

```text
domestic hardware and system integration
+ cloud-accessible execution
+ browser-facing public interaction
+ an open-source operational software ecosystem
```

The case does not yet demonstrate a discovery cluster. It is tracked as a candidate access-layer inflection event that may precede broader capability-exploration activity.

## Research interpretation

TIDC distinguishes a device-construction cluster from a capability-discovery cluster. The Osaka system may mark movement between them:

```text
specialized device construction
-> remotely available experimentation
-> wider participant exposure
-> self-capability characterization
-> technology-native methods
-> external application discovery
```

The relevant mechanism is not merely the existence of another quantum computer. It is the simultaneous reduction of access, learning, inspection, and experimentation barriers.

A provisional relationship is:

```text
potential discovery-cluster intensity
~ (effective capability * accessibility * inspectability)
  / (learning cost * experimental cost)
```

This is a directional research expression, not an estimated law.

## Primary-source basis

The University of Osaka and RIKEN reported that the system began operation on July 28, 2025 and that its major components, parts, and software were made in Japan. The University of Osaka also reported that the front-end-to-back-end software ecosystem uses the open-source Open Quantum Toolchain for Operators and Users (OQTOPUS).

OQTOPUS was publicly released in March 2025 as a customizable open-source operating environment spanning quantum-computer cloud execution and operations.

## Coding decision

This case is not entered into `pilot-events-v0.1.json` as a discovery event because the launch itself is an infrastructure and exposure event, not yet a mathematical or scientific discovery produced through the technology.

It is instead registered as a tracked precursor with the following provisional coding:

```text
case_id: QAI-2025-JP-OSAKA
event_class: access_infrastructure_inflection
technology_wave: Quantum computing
orientation: Self-capability precursor
candidate_date: 2025-07-28
access_mode: Cloud and browser-facing public interaction
software_openness: Open-source operational stack
hardware_posture: Fully Japan-made system integration claim
confidence: High for launch and stack posture; unresolved for downstream clustering effect
```

## Longitudinal measures

Future tranches should attempt to record:

1. operational-access and public-access dates;
2. hardware architecture and qubit count;
3. eligibility restrictions for users;
4. browser, API, notebook, and local-access modes;
5. source-code availability and component coverage;
6. documentation, tutorials, and educational materials;
7. registered users, institutions, and executed jobs where available;
8. external repositories, papers, patents, experiments, and applications citing or using the platform;
9. time from access opening to independently verifiable downstream results;
10. the proportion of self-capability studies versus external applications over time.

## Testable expectation

If access-layer inflections contribute to clustering, the period after effective access should show measurable growth in participant diversity, experimentation volume, self-capability research, technology-native methods, or external applications beyond an appropriate baseline.

A future empirical comparison may be expressed as:

```text
Delta C_q(t) = C_after_access(t) - C_counterfactual(t)
```

where `C_q` may represent contributors, experiments, repositories, publications, distinct topics, or accepted external applications.

## Falsification and caution

This interpretation is weakened if:

- effective access remains restricted despite public-facing claims;
- the open stack is not practically usable outside the originating institutions;
- downstream activity does not change relative to comparable systems or background growth;
- resulting work remains almost entirely device-characterization research;
- observed growth is attributable to funding, publicity, or unrelated platform expansion;
- outputs cannot be independently reproduced or traced to use of the system.

The case must not be described as proof that a quantum discovery cluster has begun.

## Governance boundary

Open source and browser access improve inspectability and participation but do not by themselves establish trustworthy execution. Future quantum research records should distinguish:

```text
submitted circuit
-> compiler and transpiler transformations
-> calibration state
-> execution request
-> hardware execution
-> measurement
-> error mitigation
-> reported result
```

Accessibility is not admissibility. Open code is not execution provenance. A reported result is not reconstructable merely because the surrounding stack is public.

## Current disposition

```text
mention_in_public_paper: yes
weight: brief tracked case study
role: candidate access-layer inflection
confirmatory_evidence: no
pilot_event_ledger_changed: no
next_action: collect downstream adoption and output evidence longitudinally
```

## Sources

- University of Osaka, “Japan launches fully domestically produced quantum computer,” July 28, 2025.
- RIKEN, “Fully domestically produced quantum computer begins operation,” July 28, 2025.
- University of Osaka, “The University of Osaka and research partners launch open-source quantum computer OS,” March 24, 2025.
