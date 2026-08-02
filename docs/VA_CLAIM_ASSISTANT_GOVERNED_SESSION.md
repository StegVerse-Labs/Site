# VA Claims Guide and Chat — Governed Product Session

## Identity

```text
Goal set: SV-VA-GOVERNED-PRODUCT-001
Repository: StegVerse-Labs/Site
Branch: main
Canonical coordination: StegVerse-Labs/Site#113
Document workspace owner: StegVerse-Labs/Site#116
Product goal contract: data/va-claim-assistant/governed-product-goals.json
Validation workflow: .github/workflows/va-governed-product-goals.yml
Public guide: va-disability-claim-guide.html
```

## Product objective

Build a governed VA Claims Guide and a governed VA Claims Chat that help veterans understand claim procedures, organize evidence, load and analyze claim documents, develop truthful claim packages, and progress toward automated filing from veteran-uploaded records.

The document workspace is intended to provide many of the practical benefits of a modern conversational document system: multi-file upload, document-grounded conversation, source and page references, summaries, evidence tables, timelines, contradiction detection, missing-evidence detection, drafting, and persistent session continuity. StegVerse adds explicit source authority, privacy, custody, reconstruction, replay, consent, and execution boundaries.

## Four governed product surfaces

### 1. Governed VA Claims Guide

The Guide must:

- use current official and controlling sources under a declared precedence policy;
- distinguish general education from claim-specific analysis;
- explain direct, secondary, increase, presumptive, exposure, aggravation, appeal, and supplemental-claim paths;
- help veterans gather, preserve, index, and review evidence;
- surface favorable, unfavorable, conflicting, and missing evidence;
- display only capabilities proven by machine-verifiable receipts;
- never claim VA, adjudicative, representative, legal, medical, rating, filing, or signature authority.

Release condition: a Guide governance receipt validates source policy, displayed capability claims, authority boundaries, and current activation state with no blockers.

### 2. Governed VA Claims Chat

The Chat must support:

- governed route classification;
- source-grounded procedural answers with proposition-level support;
- claim-stage and claim-theory context;
- document upload and multi-document sessions;
- page- and section-bound answers;
- separation of document facts, veteran statements, assistant inference, and unresolved uncertainty;
- contradiction and missing-evidence detection;
- veteran-confirmed drafting;
- reconstructable, hash-bound session receipts.

The Chat may help prepare a claim. It does not become a clinician, accredited representative, attorney, VA adjudicator, or autonomous filer.

### 3. Private claim-document workspace

The near-term document capability must provide:

- PDF, image, and text intake;
- document identity hashes and page anchors;
- multi-file indexing and retrieval;
- condition-specific evidence tables;
- supportive, unfavorable, and conflicting evidence;
- treatment and symptom timelines;
- source-bound personal-statement and evidence-index drafting;
- privacy classification, retention, deletion, and export controls;
- downloadable veteran-review packets;
- custody and reconstruction of sanitized derived records without public raw-document publication.

Public private-document upload remains disabled until upload, analysis, privacy, deletion, custody, reconstruction, and deployed-runtime gates are all verified.

### 4. Veteran-approved automated claim filing

Automated filing is a staged governed target, not an active capability.

The intended progression is:

1. derive candidate conditions and claim theories from admitted records;
2. build evidence indexes, timelines, contradiction lists, and missing-evidence tasks;
3. draft forms and supporting statements without inventing facts;
4. present a complete veteran-review packet and change log;
5. require explicit veteran confirmation of every material fact and claimed condition;
6. run current-form and current-rule pre-submission validation;
7. obtain a specific, unexpired submission-authorization receipt;
8. submit only through an authorized VA or accredited-representative integration;
9. retain submission confirmation, custody, reconstruction, and revocation evidence.

The system must not autonomously file from unreviewed uploads, invent facts, collect credentials outside an authorized integration, create a signature, or optimize toward a target disability percentage.

## Current verified capability

```text
public capability: SOURCE_GROUNDED_ASSISTANT
verified public route: evidence_requirement
bounded document fixture: VERIFIED_BOUNDED_FIXTURE_ONLY
substantive private-document interpretation: NOT VERIFIED
public private-document upload: DISABLED
automated claim filing: NOT ACTIVE
submission authority: VETERAN RETAINED
authority effect: NONE
```

The source-grounded milestone does not establish the document workspace or automated filing. Fixture validation and metadata-boundary receipts do not equal substantive document interpretation.

## Required answer and session record

Every substantive answer or document-derived output must preserve:

- question and route classification;
- claim stage and claim theory;
- source identifiers, authority classes, retrieval dates, and effective dates;
- exact support for every material proposition;
- source fact, veteran-provided fact, assistant inference, and unresolved uncertainty as separate classes;
- favorable, unfavorable, and conflicting evidence;
- missing-evidence and referral triggers;
- current capability state;
- false adjudication, representation, legal-opinion, medical-opinion, rating, execution, publication, signature, and submission authority flags;
- a stable receipt hash and custody/reconstruction references.

## Filing authority gates

No automated submission may occur until all of the following are verified:

1. veteran identity and session continuity;
2. current form and submission-channel compatibility;
3. veteran ownership or lawful authority over uploaded records;
4. privacy, retention, deletion, and export controls;
5. explicit confirmation of each material fact;
6. explicit selection of each claimed condition and theory;
7. unresolved contradictions and missing evidence are disclosed;
8. required signatures and attestations remain under veteran or valid delegate control;
9. a specific, unexpired authorization receipt binds the exact claim package and destination;
10. an authorized VA or accredited-representative submission integration exists;
11. submission confirmation is captured and reconstructable;
12. revocation, retry, duplicate-submission, and partial-failure behavior is fail-closed.

## Repository responsibilities

- `StegVerse-Labs/Site`: Guide, Chat interface, document workspace, capability status, veteran review, consent, and non-authorizing public projection.
- `StegVerse-org/LLM-adapter`: governed chat routing, retrieval, document-grounded generation, drafting, and execution receipts.
- `StegVerse-Labs/TVC`: scoped provider and document-processing capabilities, credential custody, rotation, and revocation.
- `master-records/orchestration`: sanitized derived-record custody, package custody, reconstruction, and submission confirmation receipts.
- authorized VA or accredited-representative integration: actual filing transport; no such integration is asserted active by this document.

## Machine-owned continuation

```text
Goal contract validator:
.github/workflows/va-governed-product-goals.yml

Source-grounded activation observer:
.github/workflows/va-claim-assistant-activation.yml

Document evidence validator:
.github/workflows/va-document-evidence.yml

Private fixture runtime:
.github/workflows/va-private-document-runtime.yml
```

## Immediate executable goals

1. Project the governed Guide and Chat roadmap on the public surface without representing future document upload or filing as active.
2. Complete admitted private multi-document sessions with source-bound outputs, privacy controls, export packets, and deployed execution receipts under `Site#116`.
3. Expand the governed chat runtime beyond the current bounded public-source route while unsupported routes remain fail-closed.
4. Define the filing integration contract for identity, consent, signature, preflight, exact-package authorization, submission, confirmation, revocation, and duplicate prevention.
5. Promote capability states only from directly verified receipts.

## Archive condition

These goals are archival dependencies until they are completed, superseded, or transferred into active repository-native work with exact owners and release conditions. The product contract and this session record preserve the newly established goals; they do not by themselves activate document upload or claim filing.
