# Ecosystem Chat Governed Aspect Model

## Purpose

This model defines the governed dimensions that must remain separate when a chat submission, model response, artifact, decision, execution, or downstream reuse is evaluated.

No single score, token count, outcome metric, ownership assertion, or payment event may collapse these dimensions into one undifferentiated value signal.

## Core rule

```text
one interaction
!= one value
!= one owner
!= one author
!= one permissible use
!= one reward
```

Each aspect has its own evidence, authority, uncertainty, lifecycle, disputes, and receipts.

## Aspect families

### 1. Identity and participation

Defines who or what participated without assuming ownership or authorship.

Required distinctions:

```text
human participant
agent participant
model/provider participant
organization participant
infrastructure participant
anonymous or pseudonymous participant
collective participant
unknown participant
```

Participation proves presence in a governed interaction only.

### 2. Source and provenance

Defines where information, instructions, artifacts, and transformations came from.

Required distinctions:

```text
user-original
user record
user observation
user correction
public source
licensed source
derived source
model-generated
agent-generated
system-generated
unknown source
```

Provenance must preserve source references, acquisition posture, timestamps, hashes, and transformation links.

### 3. Ownership and control

Separates asserted ownership, verified ownership, possession, access, control, license, and stewardship.

```text
possession != ownership
access != control
control != license
license != assignment
asserted ownership != verified ownership
```

### 4. Consent and permission

Defines what uses are allowed, for which purpose, audience, duration, destination, and level of disclosure.

Consent must be specific enough to evaluate:

```text
collection
processing
retention
projection
reuse
commercialization
training
derivation
publication
settlement
```

Consent change, narrowing, expiry, and revocation are governed events. Historical records are preserved rather than silently rewritten.

### 5. Privacy and sensitivity

Classifies disclosure risk without treating sensitivity as an automatic value multiplier.

Possible postures include:

```text
public
private
confidential
restricted
regulated
safety-sensitive
identity-sensitive
commercially sensitive
unknown
```

### 6. Contribution

Determines whether a participant supplied information, labor, judgment, correction, evidence, context, evaluation, coordination, or infrastructure that materially affected a result.

Contribution is distinct from attendance, message count, prompt length, and compute consumption.

### 7. Causal influence

Evaluates how a contribution affected a later result.

Mechanisms may include:

```text
context
instruction
correction
evidence
constraint
evaluation
selection
coordination
artifact creation
risk identification
recovery
```

Influence must expose uncertainty, alternative causes, dependencies, and unresolved counterfactuals.

### 8. Attribution

Allocates bounded credit or responsibility among contributors, prior work, models, agents, systems, infrastructure, and institutions.

Attribution may be:

```text
individual
shared
collective
layered
provisional
contested
unresolved
non-separable
```

Attribution does not establish ownership, exclusivity, or compensation.

### 9. Authorship

Defines responsibility for expressive or technical formation of an artifact.

Human direction, human revision, model generation, agent assembly, source inheritance, and editorial control must remain distinguishable.

Authorship may coexist with separate ownership, contribution, and attribution records.

### 10. Originality and novelty

Measures whether information or artifacts are new relative to an identified evidence corpus and observation time.

```text
novel to participant
novel to session
novel to organization
novel to system
novel to public corpus
not independently established
```

Novelty claims require a declared comparison boundary.

### 11. Scarcity and substitutability

Evaluates whether a contribution was rare, difficult to replace, time-sensitive, exclusive, or broadly substitutable.

Scarcity cannot be inferred merely from privacy or restricted access.

### 12. Labor and effort

Records human and machine effort without treating effort alone as value.

Possible measures include time, review burden, expertise, coordination, physical work, emotional labor, compute, energy, and verification cost.

### 13. Compute and infrastructure

Separates model inference, storage, networking, orchestration, custody, reconstruction, security, and settlement costs.

Tokens are one compute-consumption measure, not a value measure.

### 14. Outcome and utility

Defines what changed because of the governed interaction.

Outcome classes may include:

```text
artifact created
decision improved
error corrected
risk avoided
cost avoided
revenue created
time saved
knowledge advanced
coordination improved
harm reduced
no demonstrated effect
```

### 15. Realized value

Requires observed benefit or avoided loss, a baseline, method, time window, and uncertainty.

Expected, projected, claimed, and realized value must remain separate.

### 16. Cost and externalities

Accounts for direct and indirect costs, including harms shifted to nonparticipants.

```text
compute cost
human labor cost
privacy cost
security risk
legal exposure
opportunity cost
environmental cost
social cost
institutional cost
future lock-in
```

A profitable outcome may still be inadmissible when externalized harm is unresolved.

### 17. Risk and harm

Captures foreseeable and observed harms, severity, likelihood, affected parties, reversibility, and mitigations.

Risk reduction may itself be an attributable contribution.

### 18. Admissibility

Determines whether a transition may proceed under the applicable authority, policy, consent, evidence, and boundary conditions.

```text
successful != admissible
approved != admissible
profitable != admissible
technically possible != admissible
```

### 19. Authority and delegation

Defines who may inspect, decide, authorize, execute, override, revoke, settle, or publish.

Authority must be explicit, scoped, current, and reconstructable at commit time.

### 20. Standing and capability

Records earned or assigned ability to participate in future actions.

Standing, access, reputation, capability, and authority are separate.

```text
standing != authority
capability != permission
access != admissibility
```

### 21. Reward and incentive

Defines the type of recognition that may follow from a contribution.

Possible reward classes:

```text
credit
standing
access
capability
governance participation
priority
royalty candidacy
payment
non-monetary benefit
none
```

Reward eligibility is distinct from distribution authorization and settlement.

### 22. Distribution and allocation

Defines how distributable value is divided among claims, infrastructure, prior work, collective pools, reserves, and unresolved shares.

Allocation must preserve methodology, policy, uncertainty, disputes, and rounding or residual treatment.

### 23. Settlement

Records finalized allocation through an authorized mechanism.

Settlement requires contract, policy, claimant references, custody, accounting, dispute posture, and settlement receipts.

### 24. Tax, jurisdiction, and legal posture

Records the governing jurisdiction, applicable legal classification, reporting obligations, restrictions, and unresolved legal questions.

The system must not infer universal legality from technical enforceability.

### 25. Temporal state and decay

Tracks how relevance, consent, rights, value, standing, risk, and authority change over time.

Possible temporal events include:

```text
expiry
supersession
deprecation
revocation
value decay
renewal
revalidation
context drift
policy drift
```

### 26. Dispute and competing claims

Preserves disagreement rather than collapsing it into a single ontology.

Disputes may concern provenance, ownership, consent, influence, attribution, originality, valuation, allocation, admissibility, or settlement.

### 27. Fraud, gaming, and manipulation

Detects attempts to manufacture apparent value through padding, duplication, collusion, circular citation, self-dealing, hidden agent generation, fabricated evidence, identity splitting, or artificial scarcity.

### 28. Collective and network contribution

Supports contributions that are distributed across many users, conversations, communities, datasets, tools, and prior interactions.

Collective contribution may require pooled, probabilistic, or non-separable attribution rather than forced individual allocation.

### 29. Derivation and transformation

Distinguishes captured records from interpretations, summaries, combinations, models, embeddings, evaluations, and transformed artifacts.

Every derived record must reference source records, transformation method, operator or system, uncertainty, and reuse permission.

### 30. Disclosure and projection

Defines which governed facts may be shown to which audience and destination.

Projection must be purpose-bound, minimum-disclosure, redaction-aware, and default-deny where permission is unresolved.

### 31. Custody and reconstruction

Defines where authoritative records are retained and whether the interaction, claim, decision, and settlement can be reconstructed.

```text
local persistence != custody
export != custody
replay != reconstruction
reconstruction PASS != authority
```

### 32. Confidence and uncertainty

Every interpretive claim must expose confidence, uncertainty, unresolved evidence, competing explanations, and limits of measurement.

### 33. Recovery and correction

Records corrections, retractions, reversals, appeals, restored consent, superseding evidence, and recovery actions.

Correction must preserve lineage rather than erase prior states.

### 34. Public claim and communication

Constrains how the system describes value externally.

Allowed public framing:

> Every governed submission can preserve a traceable claim. Recognition, attribution, realized value, distribution, and settlement require separate evidence and authority.

Prohibited framing includes guaranteed payment, automatic ownership, automatic originality, or automatic value based on activity volume.

## Cross-aspect invariants

1. No aspect may silently grant another aspect.
2. Missing evidence is represented as unresolved, not inferred as favorable.
3. Every authoritative change is a governed event.
4. Human-facing simplification must not remove underlying distinctions.
5. Local browser state grants no custody, admissibility, payment, or settlement authority.
6. Disagreement and competing determinations remain visible.
7. Historical records are append-only except through governed correction and supersession semantics.
8. Sensitive information is not presumed valuable, reusable, or distributable.
9. Successful outcomes do not erase invalid consent, unauthorized execution, or externalized harm.
10. Every downstream projection must preserve purpose, permission, redaction, and minimum-disclosure posture.

## Production implementation sequence

```text
aspect registry
-> canonical aspect event schema
-> evidence and policy bindings
-> renderer projections
-> validators
-> custody and reconstruction
-> cross-aspect conflict checks
-> downstream projection receipts
-> distribution and settlement services
```

## Authority boundary

This model defines governed distinctions. It does not determine ownership, grant rights, authorize processing, calculate payable value, settle claims, or create legal conclusions.