# Claim–Artifact Correspondence Standard (CACS)

Status: Draft normative standard  
Version: 0.1.0  
Authority effect: None until adopted by an authorized governance process

## 1. Purpose

CACS defines the correspondence required among a public or internal claim, its declared scope, the machinery or formal object it concerns, the test performed, and the evidence produced.

The governing rule is:

> No claim may exceed what its identified artifacts establish at the declared scope and conditions.

CACS governs claims about system behavior. It does not itself grant execution, publication, deployment, admissibility, custody, release, or validation authority.

## 2. Core distinctions

The following objects are not interchangeable:

```text
paper != implementation
diagram != machinery
demonstration != universal assurance
observability != governance
receipt generation != receipt validity
replayability != reconstructability
production deployment != scientific validation
evidence of mechanism != proof of every consequence
```

Artifact substitution is prohibited. A claim must identify the class of evidence that supports it and the classes of conclusion that remain unestablished.

## 3. Claim object

A governed claim is a durable object with a stable identifier and explicit evidence boundary.

Minimum fields:

```json
{
  "claim_id": "stable-unique-id",
  "claim_text": "The capability being asserted",
  "claimant": {},
  "scope": {},
  "assumptions": [],
  "supporting_artifact_refs": [],
  "evidence_dimensions": {},
  "test_refs": [],
  "authority_refs": [],
  "falsification_conditions": [],
  "not_established": [],
  "correspondence_status": "supported|partially_supported|unsupported|overstated|superseded|withdrawn",
  "review_refs": [],
  "timestamp": "RFC3339",
  "hash": ""
}
```

The `not_established` field is mandatory. Silence must not be interpreted as broader assurance.

## 4. Evidence dimensions

Evidence is represented as a multidimensional profile, not a single maturity score.

| Dimension | Required question |
|---|---|
| Formalized | Are objects, assumptions, invariants, proof obligations, and falsification conditions defined? |
| Mechanized | Does executable machinery implement the claimed behavior? |
| Demonstrated | Was the behavior observed under stated and bounded conditions? |
| Refusal integrity | Was refusal produced before consequence and was the failed condition recorded? |
| Receipt integrity | Are relevant inputs, transitions, decisions, and outcomes durably represented? |
| Replay-supported | Can supplied canonical state reproduce the decision or behavior? |
| Reconstructable | Can relevant authoritative state be recovered from canonical evidence without relying on hidden assertions? |
| Publicly inspectable | Can an eligible reviewer inspect the declared artifacts and conditions? |
| Independently reproduced | Has another operator or implementation reproduced the claimed result? |
| Pilot-observed | Has the behavior been observed in a bounded external or operational pilot? |
| Production-observed | Has the behavior been observed in an identified production environment? |
| Scope-correspondent | Does the claim remain no broader than the evidence profile? |

Each dimension uses one of:

```text
ESTABLISHED
PARTIAL
NOT_ESTABLISHED
NOT_APPLICABLE
DISPUTED
SUPERSEDED
```

Production observation does not automatically establish formal correctness, independence, reconstructability, or universal operational assurance.

## 5. Artifact classes and permitted conclusions

### 5.1 Formal paper or specification

May establish:

- defined objects and vocabulary;
- assumptions and declared scope;
- laws, invariants, and proof obligations;
- falsification conditions;
- formal derivations within the stated model.

Does not alone establish:

- implementation fidelity;
- live operational behavior;
- independent reproduction;
- production assurance.

### 5.2 Architecture diagram

May establish:

- a proposed structural relationship;
- intended components, routes, and boundaries.

Does not alone establish:

- executable machinery;
- runtime enforcement;
- refusal integrity;
- receipt validity.

### 5.3 Bounded demonstration

May establish:

- behavior observed under the fixed conditions actually exercised;
- the existence of the shown path in the tested build.

Does not alone establish:

- behavior under untested conditions;
- invariance across policy, authority, timing, route, provider, or implementation changes;
- universal assurance.

### 5.4 Proof surface

A proof surface must expose, at the declared scope:

- candidate movement;
- present standing;
- failed conditions;
- permitted and refused paths;
- refusal before consequence;
- route closure or non-formation;
- receipts;
- replay inputs and results;
- declared limitations.

A proof surface establishes only the exposed, reproducible behavior within its stated boundary. The label `proof surface` must not be applied to a dashboard that only displays verdicts or to a demonstration that omits reproducible evidence.

### 5.5 Replay package

May establish:

- that supplied canonical inputs reproduce a stated result in the identified implementation and environment.

Does not alone establish:

- that the inputs were authoritative at the original decision boundary;
- that the original state can be independently reconstructed;
- that hidden dependencies were absent.

### 5.6 Reconstruction package

May establish:

- that relevant state can be recovered from canonical evidence according to the declared reconstruction method.

Does not alone establish:

- execution authority;
- admissibility;
- correctness of every reconstructed assertion;
- universal replay equivalence.

### 5.7 Independent reproduction

May establish:

- that another eligible operator or implementation reproduced the declared result from the disclosed conditions and artifacts.

It must identify material implementation, environment, policy, and test differences.

### 5.8 Pilot and production evidence

May establish:

- observed behavior in an identified operational environment and time interval.

Does not alone establish:

- universal behavior;
- scientific validity;
- absence of unobserved failure routes;
- permanent assurance after policy, authority, model, provider, or implementation changes.

## 6. Scope declaration

Every claim must declare enough scope to determine what was and was not tested. As applicable, scope includes:

- repository, component, implementation, and version;
- commit, image, package, or artifact hash;
- policy and delegation versions;
- model and provider identifiers;
- authority and standing state;
- evidence inputs;
- test vectors and environmental conditions;
- relevant timing and ordering constraints;
- known exclusions;
- reviewer eligibility and disclosure boundary.

An unspecified scope is not universal scope. It is an incomplete claim.

## 7. Falsification obligations

Every testable claim must declare at least one falsification condition.

Examples:

```text
Execution occurs after standing is invalid at commit time.
A refused route forms despite a recorded closure condition.
Replay using the declared canonical state produces a materially different decision.
The receipt cannot be linked to the tested transition.
An independent reconstruction requires an undisclosed authoritative input.
The public claim exceeds the evidence dimensions marked ESTABLISHED.
```

A claim without a meaningful failure condition may be descriptive, aspirational, or promotional, but must not be presented as verified.

## 8. Correspondence review

A Claim Review records whether correspondence exists among:

```text
claim
-> declared scope
-> mechanism or formal object
-> test
-> evidence
-> result
-> public wording
```

Review outcomes:

- `supported`: the claim is within the established evidence boundary;
- `partially_supported`: a bounded portion is established and the unsupported portion is explicit;
- `unsupported`: identified evidence does not establish the claim;
- `overstated`: some evidence exists, but the wording exceeds it;
- `superseded`: a later valid claim or evidence package replaces it;
- `withdrawn`: the claimant has retracted it.

A correspondence review is itself evidence. It does not grant authority beyond its declared reviewer role and scope.

## 9. Public communication requirements

Any public technical claim governed by CACS must expose or reference:

1. the claim identifier and exact wording;
2. the declared scope;
3. the evidence dimensions established;
4. the supporting artifacts;
5. the relevant tests and results;
6. the falsification conditions;
7. what is not established;
8. the correspondence status and reviewer identity or class;
9. material supersession or withdrawal history.

Marketing language must not silently promote:

- a proposal into an implementation;
- a demonstration into an assurance claim;
- one refusal into universal refusal integrity;
- a replay into independent reconstruction;
- a receipt into custody or validity;
- production use into scientific proof.

## 10. Fail-closed publication rule

A claim is not eligible for a `verified`, `proven`, `validated`, `production-assured`, or equivalent label unless the label is explicitly defined and its required evidence dimensions are established.

When evidence is missing, conflicting, stale, simulated, scope-incomplete, or authority-escalating, the publication posture is fail-closed:

```text
DRAFT
UNVERIFIED
PARTIALLY_SUPPORTED
DISPUTED
SUPERSEDED
WITHDRAWN
```

## 11. Integration with StegVerse records

CACS Claim and Claim Review objects may reference canonical governed events, transitions, policies, delegations, evidence, artifacts, receipts, signatures, custody records, replay packages, reconstruction reports, refusals, overrides, quarantine events, and recovery events.

The same claim may have human-readable, formatted governed, and raw machine-readable projections. Those projections must resolve to one canonical claim record and stable identifiers.

## 12. Authority boundary

```text
claim registration != claim validity
review != execution authority
publication != admissibility
demonstration != universal assurance
replay PASS != reconstructability
reconstruction PASS != execution authority
production observation != scientific validation
artifact availability != artifact authenticity
correspondence status != release authority
```

## 13. Adoption criteria

CACS may advance from draft only after:

- machine-readable schema validation exists;
- at least one supported and one overstated test vector exist;
- an independent reviewer can reproduce the correspondence decision;
- downstream Publisher, admissibility, and guardian projections preserve the authority boundary;
- versioning and supersession rules are tested.
