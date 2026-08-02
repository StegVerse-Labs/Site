# Texas Tech–NVIDIA Outreach Disclosure Boundary

## Purpose

Define the claims permitted in exploratory outreach concerning StegVerse, Texas Tech University, NVIDIA, and the `SV-TTU-MRE-001` experiment.

## Permitted statements

- StegVerse is an experimental governance and evidence-continuity framework for agentic AI systems.
- StegVerse-Labs has prepared a research concept and a locally runnable minimal experiment concerning commit-time authority, policy and delegation drift, evidence freshness, execution boundaries, deterministic decisions, and reconstruction receipts.
- Texas Tech publicly announced next-generation NVIDIA accelerated-computing infrastructure in February 2026.
- Texas Tech's public HPCC materials describe sponsored external research-partner access through a TTU faculty/staff sponsor and the university's account process.
- StegVerse seeks an exploratory conversation about research fit, sponsorship routes, reproducibility, and possible scaling requirements.
- The current experiment uses synthetic inputs and does not require institutional data or privileged infrastructure.

## Prohibited statements without written authorization

Do not state or imply that:

- Texas Tech or NVIDIA is collaborating with, sponsoring, endorsing, validating, funding, hosting, deploying, or using StegVerse;
- StegVerse has access to Texas Tech or NVIDIA systems;
- any TTU faculty member, laboratory, center, or administrator has agreed to participate;
- the experiment has been independently reproduced or peer reviewed;
- local deterministic tests establish general safety, security, admissibility, or production readiness;
- Texas Tech marks, NVIDIA marks, personnel names, or private correspondence may be used publicly;
- the announced platform is available to StegVerse or external users outside an authorized university process.

## Personal-history boundary

Until Rigel Randolph approves a verified statement, external materials may say only:

> I have prior personal history with Texas Tech and am seeking the correct current institutional route for an exploratory research conversation.

Do not state a degree, enrollment period, employment, department, title, alumni status, research appointment, or institutional standing unless supported by records and approved for outreach.

## Evidence-level labels

```text
CONCEPT: research framing exists
SPECIFIED: experiment specification exists
IMPLEMENTED: executable artifacts are committed
LOCALLY_VALIDATED: deterministic local tests have passed
WORKFLOW_VALIDATED: repository-hosted workflow has passed
INDEPENDENTLY_REPRODUCED: a separate implementation or reviewer reproduced results
INSTITUTIONALLY_AUTHORIZED: written authority from the relevant institution exists
```

Never collapse one evidence level into the next.

## Data and security boundary

- synthetic, non-sensitive data only;
- no CUI, regulated, medical, personal, export-controlled, proprietary, or institutional data;
- no credentials in repositories, emails, fixtures, reports, or receipts;
- no external side effect before an explicit `ALLOW` decision;
- missing or unresolved evidence must fail closed;
- public artifacts must exclude private correspondence and account identifiers.

## Publication and IP boundary

Before disclosing patentable implementation details to an institution or publicly expanding the repository record, evaluate whether Research Commercialization or other IP review is appropriate. The existence of this repository does not assign ownership, grant a license, or create a joint invention.

## Required outreach footer

> This is an independent exploratory proposal. It does not represent or imply a current Texas Tech or NVIDIA collaboration, endorsement, sponsorship, compute allocation, or validation.

## Enforcement owner

```text
owner_repository: StegVerse-Labs/Site
owner_issue: 17
release_condition: written institutional authorization may narrow a specific non-claim, but only the authorizing institution can grant that change
```
