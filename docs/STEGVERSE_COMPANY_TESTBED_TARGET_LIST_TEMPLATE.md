# StegVerse Company Testbed Target List Template

## Purpose

This template provides a governed research and outreach surface for identifying prospective non-production StegVerse Execution Boundary Audit partners.

It is not a partnership registry, adoption list, endorsement list, customer list, or evidence of technical validation.

## Governing Boundary

```text
Research may identify a plausible fit.
Public information may support a fit hypothesis.
Outreach may request a bounded conversation.
None of those acts establishes permission, partnership, adoption, endorsement, validation, or authority.
```

Do not record private personal information, confidential third-party information, scraped contact data, inferred sensitive attributes, production credentials, or unsupported claims.

## Target Record

Copy this section once for each candidate.

```yaml
record_schema: stegverse.company_testbed.target.v1
record_id: ""
record_status: research_candidate | qualified_for_outreach | outreach_permitted | contacted | response_received | deferred | declined | closed
created_at: ""
updated_at: ""
researcher: ""

organization:
  name: ""
  public_website_reference: ""
  sector: ""
  organization_type: company | laboratory | university | nonprofit | public_sector | standards_body | other
  geography_publicly_stated: ""

candidate_workflow:
  category: ""
  public_description_reference: ""
  execution_boundary_fit_hypothesis: ""
  governed_point_of_irreversibility_hypothesis: ""
  non_production_scope_plausibility: strong | possible | weak | unknown
  production_access_required: false

relevant_role:
  role_title_or_category: ""
  named_person_recorded: false
  public_role_source_reference: ""

commit_time_questions:
  authority_question: ""
  state_transition_question: ""
  state_freshness_question: ""
  concurrency_or_aggregate_risk_question: ""
  recoverability_question: ""
  receipt_or_reconstruction_question: ""

fit_evaluation:
  authority_question_present: true | false | unknown
  state_transition_question_present: true | false | unknown
  governed_boundary_identifiable: true | false | unknown
  synthetic_or_anonymized_evidence_possible: true | false | unknown
  non_production_audit_possible: true | false | unknown
  evidence_for_fit_hypothesis: ""
  disqualifying_conditions: []

contact_and_permission:
  contact_status: not_researched | public_channel_identified | outreach_drafted | outreach_sent | response_received | do_not_contact
  public_contact_channel_reference: ""
  permission_state: not_requested | requested | granted | denied | withdrawn | not_applicable
  confidentiality_state: not_discussed | public_only | anonymized | confidential | declined
  attribution_permission: not_requested | granted | denied | conditional
  case_study_permission: not_requested | none | anonymized | named | conditional

next_action:
  next_permitted_action: ""
  action_owner: ""
  prerequisites: []
  prohibited_next_actions: []
  review_date: ""

claim_boundary:
  permitted_claim: "Prospective research candidate identified from public information."
  prohibited_claims:
    - partner
    - customer
    - adopter
    - endorsed_by
    - validated_by
    - certified
    - deployed
    - integrated
    - paid_pilot
    - production_ready

custody_and_evidence:
  public_source_references: []
  internal_notes_location: ""
  evidence_contains_personal_data: false
  evidence_contains_confidential_data: false
  master_records_custody_claimed: false
  independent_validation_claimed: false
```

## Qualification Questions

Before changing `record_status` to `qualified_for_outreach`, answer all of the following:

```text
1. Is there a publicly described workflow in which an AI, agent, automation, or human-AI process may influence a downstream action?
2. Can a plausible governed point of irreversibility be described without accessing production systems?
3. Is there a meaningful actor-authority question at commit time?
4. Is there a meaningful resulting-state admissibility question at commit time?
5. Could state freshness, concurrency, aggregate limits, or recoverability materially affect the action?
6. Could the workflow be represented with synthetic, anonymized, redacted, or non-production evidence?
7. Is the proposed outreach limited to a conversation or bounded audit qualification step?
8. Are all public statements limited to verified public information and clearly labeled hypotheses?
```

A candidate is not qualified when the only rationale is general interest in AI, brand visibility, company size, access to funding, or assumed willingness to partner.

## Outreach Transition Rules

```text
research_candidate -> qualified_for_outreach
  only after the fit questions are answered from public evidence.

qualified_for_outreach -> outreach_permitted
  only after the contact channel and claim boundary are reviewed.

outreach_permitted -> contacted
  only after a bounded message is actually sent.

contacted -> response_received
  only after a response is received through the identified channel.

Any state -> deferred | declined | closed
  when fit, permission, timing, evidence, or conduct no longer supports continuation.
```

No record may transition directly from research to partner, adopter, pilot, customer, validated, deployed, or endorsed status. Those are not statuses in this template.

## Minimum Outreach Message Boundary

A permitted outreach message should:

```text
identify the public workflow or problem that prompted the inquiry;
state that the proposed engagement is non-production and bounded;
ask whether the organization is open to discussing one representative workflow;
separate actor authority from resulting-state admissibility;
avoid requesting credentials, confidential data, or production access;
avoid implying prior association, approval, validation, or endorsement;
include attribution language when technical details are exchanged;
and permit the recipient to decline without further contact.
```

## Review Checklist

```text
[ ] Every factual statement has a public source reference.
[ ] Every unverified connection is labeled as a hypothesis.
[ ] No private personal data is recorded.
[ ] No confidential information is recorded.
[ ] No production access is requested.
[ ] The governed point of irreversibility is plausible.
[ ] Actor authority and transition admissibility are both addressed.
[ ] The next action is explicitly permitted.
[ ] Prohibited claims remain false.
[ ] Permission and confidentiality state are explicit.
[ ] The record can be closed without losing required evidence.
```

## Portfolio Summary

Use only aggregate counts that do not imply adoption or endorsement.

```yaml
summary_schema: stegverse.company_testbed.target_summary.v1
generated_at: ""
research_candidates: 0
qualified_for_outreach: 0
outreach_permitted: 0
contacted: 0
responses_received: 0
deferred: 0
declined: 0
closed: 0
partners_claimed: 0
customers_claimed: 0
adopters_claimed: 0
validated_deployments_claimed: 0
```

The final four values must remain zero unless separate authoritative evidence and explicit publication permission exist outside this research template.

## Destination And Ownership

```text
StegVerse-Labs/Site owns this blank template and its validation.
A future private research record may use the schema but must not expose confidential or personal information in the public repository.
External organizations own permission to inspect, describe, attribute, or publish their workflows.
Destination repositories own any later custody, publication, terminology, or operator-guidance integration.
```

## Archive Readiness

This template preserves the record schema, fit criteria, permission states, transition rules, claim limits, review requirements, and continuation boundary needed to research prospective company testbeds without relying on prior conversation context.
