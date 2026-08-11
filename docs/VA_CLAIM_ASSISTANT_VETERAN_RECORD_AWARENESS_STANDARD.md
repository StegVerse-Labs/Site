# VACC Veteran Record Awareness Standard

## Purpose

When a veteran deliberately submits health records for VA disability-claim preparation, VACC performs a separate **Veteran Record Awareness** review in parallel with claim-evidence review.

This lane exists so consequential information discovered during longitudinal review is not silently discarded merely because it is not needed to establish the current disability claim.

## Boundary

Veteran Record Awareness is **not automatically part of the claim**.

A finding may enter claim development only after a separate relevance determination establishes that it bears on the claim being prepared. The veteran controls whether non-claim awareness findings are discussed with a PCP, patient advocate, accredited representative, oversight body, or another appropriate recipient.

The lane grants no adjudication, representation, medical-opinion, rating, execution, publication, or filing authority.

## Standard review classes

The review should surface evidence-grounded potential issues including:

- consequential behavioral labels such as aggressive, noncompliant, disruptive, difficult, refused treatment, drug-seeking, or comparable characterizations;
- continuity-of-care gaps;
- medication availability/refill gaps;
- failed or delayed access to care;
- contradictions between labels and surrounding chronology;
- potentially inaccurate or stale problem-list entries;
- unresolved abnormal findings;
- unresolved or failed referrals; and
- other longitudinal anomalies material to the veteran's understanding of their record.

Detection of a term alone is not a finding of wrongdoing, falsity, negligence, or causation.

## Review method

For every awareness finding, VACC must:

1. retrieve the surrounding chronology rather than presenting a label in isolation;
2. separate observable record facts from interpretation;
3. preserve evidence references to the underlying record facts;
4. identify precipitating access, appointment, refill, referral, medication, communication, or clinical events when present;
5. distinguish refusal of reasonably available care from inability to obtain care;
6. preserve contradictions and uncertainty rather than resolving them by assumption;
7. avoid assigning fault or causal responsibility without sufficient evidence;
8. state whether claim relevance has been evaluated separately; and
9. provide a bounded veteran-facing next action without silently escalating the matter.

## Behavioral-label rule

A behavioral characterization must not be treated as self-proving. Where available, review the underlying observable conduct and the events preceding the characterization.

The review should distinguish assertiveness, frustration, anger, persistence, blunt communication, emotional intensity, disagreement, repeated requests for assistance, threats, dangerous behavior, and violence rather than collapsing those states into a single label.

## Noncompliance rule

The review must distinguish intentional refusal of reasonably available treatment from circumstances such as inability to obtain an appointment, unavailable refill, expired prescription without replacement, unresolved referral, system-navigation failure, repeated unsuccessful attempts to obtain assistance, or health conditions interfering with engagement.

## Veteran-facing output

The output heading should be conceptually equivalent to:

**Veteran Record Awareness — Not Automatically Part of Your Claim**

Each finding should state:

- what the records objectively show;
- what remains interpretation or unresolved;
- the supporting evidence references;
- whether claim relevance has separately been determined; and
- what the veteran may choose to do next.

VACC must not silently inject an awareness finding into claim language.

## Escalation principle

The system surfaces evidence and preserves provenance. It does not presume institutional wrongdoing or population-level causation. Broader clinical, administrative, congressional, OIG, research, or policy escalation remains a separate veteran-controlled or independently authorized process.

## Implementation owner

Canonical owner: `StegVerse-Labs/Site#116` under Goal 3 contract/fixture/validator work.

Machine-readable contract: `data/va-claim-assistant/veteran-record-awareness.schema.json`

Synthetic fixture: `data/va-claim-assistant/fixtures/veteran-record-awareness-session.json`

Validator: `scripts/check_va_document_evidence.py`

Public private-document processing remains fail-closed until the existing Goal 2/Goal 3 activation gates are satisfied.
