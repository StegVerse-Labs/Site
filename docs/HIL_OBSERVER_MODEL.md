# HIL Observer Model

## Status

```text
Model: HIL-OBSERVER-MODEL-v0.1
Experiment family: Humans as the Interoperability Layer
Posture: FORMALIZATION_CANDIDATE
Authority: NONE
Activation effect: NONE
```

This document formalizes the observer question raised by long-window human–machine interaction. It does not activate intake, review, publication, custody, execution, or Master Record authority.

## Core problem

A long-running interaction may distribute three governance functions across different entities or surfaces:

1. **Proposer** — produces a candidate interpretation, response, or action.
2. **Committer** — determines whether a candidate changes an operative or shared state.
3. **Observer** — records enough evidence to distinguish a generated proposal from a transition that actually entered reality.

The roles are functional, not necessarily identical to participants. One participant may occupy more than one role, and the observer may be a reconstructable evidence surface rather than a contemporaneous person.

## Long-window asymmetry

Let `C_A(t)` be the accumulated state of a context that can commit across a long window, and let `P_B(t)` be a proposal produced by another context at time `t`.

```text
C_A(t + Δt) = COMMIT(C_A(t), P_B(t), E_t)
P_B(t)      = PROPOSE(C_A(t), C_B(t), Q_t)
```

`E_t` is the evidence available at the transition boundary. The asymmetry is that `A` may retain and harden context over time while `B` is repeatedly required to propose into the already-developed state of `A`.

A proposal is not itself proof of a committed transition:

```text
PROPOSED(P_B(t)) != COMMITTED(P_B(t))
```

## Observer function

The observer function must distinguish at least four states:

```text
O_t = OBSERVE(
  pre_state,
  proposal,
  commit_decision,
  post_state,
  evidence
)
```

A minimally sufficient observer record contains:

- identity or stable reference for each functional role;
- pre-transition state reference;
- exact proposal bytes or canonical proposal hash;
- commit decision and decision authority;
- post-transition state reference;
- timing and ordering evidence;
- interpretation asserted by each participant;
- evidence showing whether the proposal became consequential;
- reconstruction limits and unresolved ambiguity.

## Candidate observer locations

### 1. Participant observer

A participant directly records the transition and can explain why the proposal did or did not alter the operative state.

Risk: the observer may also be the committer and may collapse observation into self-report.

### 2. Independent observer

A third party records the interaction without controlling proposal or commitment.

Risk: visibility does not imply interpretive or governance authority.

### 3. Instrumented record

Conversation history, timestamps, hashes, receipts, edits, reactions, and state snapshots jointly provide an observer surface.

Risk: preserved structure may still omit why a particular interpretation became admissible.

### 4. Retrospectively reconstructed observer

No complete observer exists at interaction time. A later verifier reconstructs the transition from preserved evidence.

Risk: reconstruction may establish sequence and integrity without establishing participant meaning or significance.

### 5. Emergent relational observer

The observer role is produced by the relation among proposer, committer, and record rather than residing in any single entity.

Risk: unless the relation is explicitly instrumented, the observer becomes a philosophical claim rather than a testable function.

## Distinguishable layers

The experiment should not collapse these layers:

```text
STRUCTURE      = observable data and relations
INTERPRETATION = participant-produced reading of that structure
SIGNIFICANCE   = value or consequence attributed to the interpretation
COMMITMENT     = authorized state change caused by or associated with it
OBSERVATION    = evidence sufficient to distinguish the above transitions
```

The same structure can support different interpretations. The same interpretation can receive different significance. Significance can exist without commitment. Commitment can occur without a complete observer record.

## Primary experiment question

> During a long-window interaction in which one context accumulates commitment and another repeatedly proposes, what entity or reconstructable mechanism determines whether a proposal actually crossed into the shared reality of the participants?

## Testable hypotheses

### H1 — Proposal/commit separation

A response can be generated, transmitted, and acknowledged without changing the committed state of either participant.

### H2 — Temporal asymmetry

The participant with persistent long-window context has greater practical control over which interpretations become consequential, even when the other participant produces more candidate interpretations.

### H3 — Structural preservation insufficiency

Exact preservation of messages and ordering is insufficient to reconstruct meaning unless the record also preserves participant-relative interpretation and commit evidence.

### H4 — Observer distribution

No single participant or artifact consistently satisfies the full observer function; the required evidence is distributed across participants, records, and later verification.

### H5 — Observer authority separation

The ability to observe or reconstruct a transition does not itself grant authority to accept, reject, publish, or govern that transition.

## Proposed event record

```json
{
  "schema": "HIL-OBSERVER-EVENT-v0.1",
  "event_id": "stable-event-id",
  "observed_at": "RFC3339 timestamp",
  "proposer": {
    "participant_ref": "participant-or-system-ref",
    "context_ref": "pre-proposal-context-hash"
  },
  "proposal": {
    "content_sha256": "hex",
    "media_type": "text/plain",
    "created_at": "RFC3339 timestamp"
  },
  "committer": {
    "participant_ref": "participant-or-system-ref",
    "authority_ref": "authority-or-none"
  },
  "commit": {
    "result": "ACCEPTED|REJECTED|UNRESOLVED|NO_COMMIT",
    "decision_at": "RFC3339 timestamp or null",
    "pre_state_ref": "hash-or-reference",
    "post_state_ref": "hash-or-reference"
  },
  "observer": {
    "mode": "PARTICIPANT|INDEPENDENT|INSTRUMENTED|RECONSTRUCTED|RELATIONAL",
    "observer_ref": "participant-system-or-record-ref",
    "evidence_refs": [],
    "limitations": []
  },
  "interpretations": [],
  "significance_claims": [],
  "continuity": {
    "previous_event_sha256": "hex-or-null",
    "event_sha256": "hex"
  }
}
```

## Admissibility conditions

An observer claim is admissible only when the evidence supports the specific claim being made.

```text
message preserved        != interpretation reconstructed
interpretation recorded  != significance established
significance asserted    != commitment proven
commitment proven        != authority validated
observation available    != publication authorized
```

When the evidence cannot establish whether a proposal entered shared reality, the required result is `UNRESOLVED`, not inferred acceptance.

## Required experiment extensions

1. Add observer-mode declaration to the experiment manifest.
2. Preserve proposal and pre/post-state references separately.
3. Require explicit commit-result recording rather than inferring commitment from continued conversation.
4. Permit multiple participant-relative interpretations for the same event.
5. Preserve timing windows so long-window context accumulation can be measured.
6. Add reconstruction tests that intentionally preserve structure while withholding interpretation evidence.
7. Add authority checks showing that observer status grants no commit or publication authority.

## Relationship to the v1.1 provenance path

The current v1.1 response provenance and receiver receipt can establish response identity, exact-byte continuity, transfer, and custody-related events. They do not by themselves establish that a response changed participant meaning, acquired significance, or entered a committed shared state.

The observer model therefore extends the research interpretation layer while remaining subordinate to the existing fail-closed technical activation path.
