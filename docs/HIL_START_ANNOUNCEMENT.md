# Humans as the Interoperability Layer — Start Announcement

## Publication state

```text
announcement_status: READY_TO_PUBLISH
experiment_version: HIL-PROTOCOL-v1.1
canonical_service: https://stegverse.org/hil/upload/
operational_receiver: https://receiver.stegverse.com
receiver_behavior: FAIL_CLOSED_UNTIL_CONFORMING_READY
public_acquisition_claim: CONDITIONAL_ON_LIVE_READINESS
publication_authority_effect: NONE
```

## Canonical public announcement

The **Humans as the Interoperability Layer** experiment is beginning.

The study asks a narrow, testable question: when people carry concepts, distinctions, and outputs between otherwise bounded AI conversations, do humans function as an interoperability layer between those systems?

Participants receive the same canonical v1.1 paper and exact prompt, request one complete response PDF from an AI system, and return that unchanged PDF through the governed StegVerse intake path.

The process preserves the response bytes, binds the submission to the canonical paper and prompt, captures participant-controlled publication preferences, and separates receipt, review, publication, and endorsement as distinct states.

Participation begins here:

https://stegverse.org/hil/upload/

The intake is fail-closed. The upload control becomes available only when the external receiver returns the conforming readiness record for the exact protocol, paper, prompt, provenance schema, and participant-metadata contract. An unavailable receiver is not represented as active, and no failed attempt is represented as accepted.

This is not a request for agreement with the paper. Disagreement, uncertainty, counterexamples, limitations, and alternative explanations are part of the experiment.

## Compact LinkedIn version

The **Humans as the Interoperability Layer** experiment is beginning.

Can people act as an interoperability layer between otherwise bounded AI conversations by carrying concepts, distinctions, and outputs across those boundaries?

Every participant receives the same canonical paper and prompt, requests one complete response PDF from an AI system, and returns that unchanged PDF through a governed, hash-bound intake path.

Agreement is not the objective. Disagreement, uncertainty, counterexamples, and limitations are part of the data.

Participate: https://stegverse.org/hil/upload/

The intake is fail-closed and becomes available only when the external receiver proves the exact readiness contract. Receipt, review, publication, and endorsement remain separate states.

#AIResearch #AIGovernance #Interoperability #HumanInTheLoop #StegVerse

## First comment

The experiment is designed to preserve more than the visible answer. It records which canonical source and prompt were used, the exact returned PDF hash, participant-controlled publication posture, and the distinction between a received artifact and a later public determination.

The research question is not whether models produce identical language. It is whether concepts or distinctions introduced in one bounded context appear later in another—and what evidence is sufficient to say a human participated in that transition.

## Required claim boundaries

The announcement may state:

- the experiment is beginning;
- the canonical participant service is published;
- the browser intake checks the external receiver before enabling upload;
- accepted submissions receive a verifiable receipt and participant review transition;
- participant publication preference is separate from final publication disposition.

The announcement must not state, without new evidence:

- that the receiver is currently READY;
- that a submission was durably stored;
- that Master Records custody or reconstruction has occurred;
- that any response has been approved or published;
- that Site activation, downstream ingestion, or scientific validation is complete.

## Announcement completion receipt template

After the public post is issued, record:

```json
{
  "schema_version": "HIL-START-ANNOUNCEMENT-RECEIPT-v1",
  "announced_at": "<RFC3339>",
  "channel": "<channel>",
  "public_reference": "<post reference>",
  "canonical_service": "https://stegverse.org/hil/upload/",
  "protocol": "HIL-PROTOCOL-v1.1",
  "announcement_text_version": "docs/HIL_START_ANNOUNCEMENT.md",
  "receiver_ready_observed_at_announcement": false,
  "submission_received_by_announcement": false,
  "publication_authority_effect": false
}
```

## Next governed transition

```text
READY_TO_PUBLISH
-> public announcement issued
-> announcement receipt preserved
-> live receiver readiness observed independently
-> first controlled participant submission
-> verified receiver receipt
-> authenticated review disposition
-> separately authorized publication
```
