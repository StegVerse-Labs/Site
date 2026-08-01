# VA Claim Assistant — Governed Session Layer

## Status

```text
state: BUILDING
public surface: va-disability-claim-guide.html
current public capability: BOUNDED_PROCEDURAL_ASSISTANT
next capability: SOURCE_GROUNDED_ASSISTANT
activation target: GOVERNED_CLAIM_SESSION
```

Repository inspection on 2026-07-31 found the public guide, deterministic procedural assistant, validator, and deployment workflow. It did not find an implemented VA-specific governed retrieval layer, source-authority registry, answer provenance contract, or document-aware claim session in Site, LLM-adapter, or TVC. This record starts that layer; it does not claim activation.

## Purpose

Help veterans organize truthful evidence and understand claim procedures using controlling federal authority, official operational material, admitted reputable non-federal sources, and user-supplied records. The assistant must not impersonate VA, an accredited representative, an attorney, or a clinician; guarantee a result; invent facts; manufacture nexus evidence; or target a disability percentage.

## Source precedence

```text
CONTROLLING
  statute -> regulation -> binding judicial precedent

OFFICIAL_OPERATIONAL
  VA forms -> official VA guidance -> M21-1 -> agency notices

PROFESSIONAL_SUPPORT
  accredited representatives -> state agencies -> legal clinics -> peer-reviewed medical sources

EXPERIENTIAL
  veteran testimony -> community reports -> forums -> social media
```

Lower classes may explain, identify practical issues, or provide leads. They may not override a higher authority class. Board of Veterans' Appeals decisions must be labeled nonprecedential unless a separate controlling authority is cited.

## Required answer record

Every substantive answer must preserve:

- question and route classification;
- claim stage and claim theory;
- source identifiers, authority classes, retrieval dates, and effective dates;
- exact support for each material proposition;
- distinction among source fact, user-record fact, assistant inference, and unresolved uncertainty;
- contrary or inconsistent evidence;
- referral triggers;
- current capability state;
- false execution, adjudication, representation, medical-opinion, and rating authority flags.

## Required routes

```text
claim_type
evidence_requirement
service_connection
rating_criteria
effective_date
appeal_or_supplemental_claim
cp_examination
document_organization
lay_statement
private_record_collection
procedural_filing
representation_referral
urgent_safety
```

## Activation gates

`GOVERNED_CLAIM_SESSION` may be displayed only after all of these are verified:

1. source registry schema and initial registry validate;
2. controlling and official sources have freshness and supersession checks;
3. non-federal sources pass admission rules;
4. answer schema and citation/provenance validator pass;
5. governed retrieval is implemented in LLM-adapter;
6. TV/TVC supplies scoped credential and protected-source execution without duplicating secrets into Site;
7. document ingestion produces source identity, page anchors, hashes, privacy class, and contradiction records;
8. fixtures verify no invented facts, no unsupported nexus, no guaranteed rating, source precedence, uncertainty preservation, and referral behavior;
9. one deployed end-to-end session returns a reconstructable, secret-free receipt;
10. the public status box reflects the verified capability exactly.

## Repository responsibilities

- `StegVerse-Labs/Site`: public interface, source display, capability status, veteran workflow, and non-authorizing projection.
- `StegVerse-org/LLM-adapter`: governed retrieval, route classification, answer generation, citations, and execution receipt.
- `StegVerse-Labs/TVC`: secret and credential custody, scoped provider/source capability, rotation, revocation, and secret-free return receipt.
- `TV`: transition and capability admission where required.
- `master-records/orchestration`: custody, hashes, reconstruction, and returned verification receipts.

## Immediate coordinated work

1. Validate `data/va-claim-assistant/source-registry.json`.
2. Implement source retrieval and answer provenance in LLM-adapter.
3. Register a TVC capability for VA source retrieval and governed model execution.
4. Add document-evidence indexing and contradiction extraction.
5. Build claim-route fixtures and activation gates.
6. Update the public page only as each capability is verified.

No absence of repository-local secrets may be declared a blocker until TV/TVC capability resolution has been attempted and returned unavailable, unauthorized, revoked, or incompatible.
