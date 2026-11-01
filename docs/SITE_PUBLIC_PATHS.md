# Site Public Paths

## Purpose

This document defines public-facing semantics for high-interest paths in `StegVerse-Labs/Site`.

It is not an activation receipt, adoption claim, endorsement claim, or production-status claim. It only explains what visitors and future contributors should understand when they encounter common repository and site paths.

## Scope

```text
Repository: StegVerse-Labs/Site
Document type: public path semantics
Activation impact: supporting documentation only
Source of truth for mirror activation: docs/SITE_MIRROR_HANDOFF.md
```

## Public Path Register

| Path | Public meaning | Authority source |
|---|---|---|
| `/` | Site repository landing surface and public entry point. | `StegVerse-Labs/Site` checked-in content. |
| `/ecosystem-chat.html` | Public governed chat interface with bounded gateway and local fallback. | Gateway lifecycle and receipts remain external to Site authority. |
| `/humans-as-interoperability-layer.html` | Main HIL prepublication presentation, protocol framing, initiating trace, and future participant workflow. | `docs/HIL_SITE_MIRROR_HANDOFF.md` owns Site continuation; the Primary PDF and trace records remain the evidence references. |
| `/humans-as-interoperability-review.html` | Optional focused checklist for Sara Katpar's review of HIL-TRACE-0001, the v0.5 PDF, and the Site presentation. | `data/hil-review-state.json` and `data/hil-traces/HIL-TRACE-0001.json`; this page does not itself record approval. |
| `/humans-as-interoperability-response.html?id=HIL-RESP-...` | Public projection of one accepted HIL response record and its artifact/hash references. | `data/hil-responses.json` is the checked-in public projection; original bytes and custody receipts remain separate. |
| `/external-chat.html` | Public external-framework compatibility intake and comparison surface. | `StegVerse-Labs/admissibility-wiki/docs/external-frameworks` remains source of truth for published framework findings; Site performs bounded intake only. |
| `/external-review.html` | Delegated reviewer console for package lookup and correction receipt requests. | Reviewer identity, delegation, and receipt authority remain in the governed review service; Site stores no reviewer credential. |
| `/governed-transitions.html` | Public projection of governed transition, executor, custody, and reconstruction state. | Orchestration and Master-Records remain source authorities. |
| `/admissibility-wiki.html` | Public bridge to the Admissibility Wiki. | `StegVerse-Labs/admissibility-wiki` remains source of truth; Site is display/bridge only. |
| `/governed-ecosystem.html` | Public mirror surface for governed ecosystem transition framing. | `StegVerse-Labs/admissibility-wiki` remains source of truth; Site is display/mirror only. |
| `/tt-code-representation.html` | Public mirror surface for TT code-representation status. | `Admissible-Existence/TT` remains source of truth; Site is display/mirror only. |
| `/governance-observatory.html` | Public mirror surface for Governance Observatory source-intake status. | `StegVerse-Labs/governance-observatory` remains source of truth; Site is display/mirror only. |
| `/papers` | Public display target for mirrored Publisher papers. | `GCAT-BCAT-Engine/Publisher` remains source of truth. |
| `/real-governance-assessment-sample.html` (planned route, **not live**) | Reserved path for the accessible case-study rendering of the real governance assessment sample (REAL-GOVERNANCE-ASSESSMENT-SAMPLE-001). No page and no download exists at this path until the conditions in "Real Governance Assessment Sample Path" below are evidenced. | `StegVerse-Labs/.github` tracks the work (#3393, #3398, #3399; `docs/REAL_GOVERNANCE_ASSESSMENT_SAMPLE_MIRROR_HANDOFF.md`). Site is display/mirror only. |
| `/docs` | Documentation and evidence packet area. | Checked-in docs plus validation scripts. |
| `/actions` | GitHub Actions workflow history. | GitHub Actions plus checked-in evidence documents. |

## Public Display Paths

```text
/
/ecosystem-chat.html
/humans-as-interoperability-layer.html
/humans-as-interoperability-review.html
/humans-as-interoperability-response.html?id=HIL-RESP-...
/external-chat.html
/external-review.html
/governed-transitions.html
/admissibility-wiki.html
/governed-ecosystem.html
/tt-code-representation.html
/governance-observatory.html
/papers
/docs
```

## Humans as the Interoperability Layer Boundary

The main HIL page presents the prepublication candidate, protocol, trace, and future participant workflow. The focused review page is only a condensed checklist and need not be sent separately when the complete PDF and main presentation have already been supplied. The response-detail page resolves only records already present in `data/hil-responses.json`.

Companion references:

```text
humans-as-interoperability-layer.html
humans-as-interoperability-review.html
humans-as-interoperability-response.html
assets/hil-experiment.js
assets/hil-response.js
data/hil-experiment.json
data/hil-review-state.json
data/hil-traces/HIL-TRACE-0001.json
data/hil-responses.json
data/schemas/hil-submission.schema.json
data/schemas/hil-receiver-receipt.schema.json
docs/HIL_SITE_MIRROR_HANDOFF.md
scripts/check_hil_experiment.py
```

Permission is not final presentation approval. A review checklist does not record a participant decision. Browser-local hashing is not server custody. A generated receipt is not submission. Inclusion in the public response index requires receiver validation and publication authority. Publication is not endorsement, and recurrence among responses is not evidence of shared machine intent.

## External Chat Boundary

For `external-chat.html`, Site accepts a bounded JSON description or trace and forwards it to the governed compatibility endpoint.

The published findings source remains:

```text
StegVerse-Labs/admissibility-wiki/docs/external-frameworks
```

External Chat may return field coverage, missing fields, failure classes, a compatibility evidence receipt, and links to matching wiki reports. It does not automatically publish a wiki record, retain the raw submission, execute the submitted framework, certify compatibility, establish semantic equivalence, grant authority, or create standing.

The checked-in catalog is a receipted Site projection of known wiki report identifiers. It is not a certification directory or proof of interoperability.

Companion references:

```text
assets/external-chat.js
assets/external-chat-review.js
external-review.html
data/external-chat-example.json
data/external-framework-catalog.json
data/external-framework-catalog.receipt.json
scripts/check_external_chat_compatibility.py
scripts/check_external_review_console.py
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/external-chat-submission-contract.md
```

External Chat may generate browser-local result, challenge, and cooperative-review packets. The reviewer console may submit a correction request only after delegated lookup. Neither surface stores tokens in browser storage or grants publication authority.

A correction receipt remains distinct from a wiki-publication transition. Even `ALLOW_PUBLICATION_CANDIDATE` is not a repository write; a separately authorized mutation is still required.

## Governed Ecosystem Boundary

For `governed-ecosystem.html`, the Site repository is a public mirror surface.

The source authority remains:

```text
StegVerse-Labs/admissibility-wiki
```

Companion references:

```text
docs/SITE_GOVERNED_ECOSYSTEM_STATUS.txt
docs/SITE_MIRROR_HANDOFF.md
scripts/check_site_governed_ecosystem_mirror.py
```

## Governance Observatory Boundary

For `governance-observatory.html`, the Site repository is a public source-intake status mirror only.

The source authority remains:

```text
StegVerse-Labs/governance-observatory
```

Companion references:

```text
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.md
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.json
scripts/check_site_governance_observatory_status.py
```

The Site surface does not replace the source repository, grant execution authority, establish production standing, or convert deferred observations such as DecisionAssure or Morrison Runtime into validated adoption claims.

## Real Governance Assessment Sample Path

Status: **planned, not live, not published.** This entry is path semantics only. It does not publish anything, does not grant publication authority, and does not change the coordination state of REAL-GOVERNANCE-ASSESSMENT-SAMPLE-001, which stays PROPOSED (`StegVerse-Labs/.github#3399`).

SKAP Vault invariant (existing source, quoted):

> "SKAP Vault inside KV is the only PII and credential store for every user, the ecosystem's own included; the ecosystem holds none (HST citation pending P1 #163). (`docs/FEDERATION_DIRECTORY.md:3`)"
>
> Quoted from its existing source in `StegVerse-Labs/.github`; not restated as new. This Site holds no PII or credential, and no assessment page or download stores one.

Meaning of the path, once it exists:

- Posture is `MIRROR` first (`PUBLICATION_PROCESS.md`); `RECEIPT_BACKED` only for a claim tied to a named receipt.
- Source authority remains `StegVerse-Labs/.github` (`StegVerse-Labs/.github#3393`, `#3398`). The Site displays; it does not decide.
- The case-study page carries the digest of the edition it shows and points to the source. Edition 2 digests as recorded by Coordination: HTML `4188099a62b5792163ae797009be9effb5a27b340c34d64531609589137d8710`; report Markdown `983718840ddcd81e0ea298d01359dfa195e0e94cc5580373ffbc505a72cef3b0`; PDF `52e2a2c1514ee633b565d91b8374f0f961297ff618313f27052b9249cb2e47cd` (recorded digest only; the PDF bytes had not been located when this was written, so nothing here verifies it).
- Edition 1 digests (PDF `7a1fa85f...`, HTML `eddc8b1d...`) are superseded and must not be served or linked as current.
- Default for the downloadable PDF is **pointer plus digest only** (the `StegVerse-Labs/.github#3394` default: pointer-and-digest only, no redistribution, no public use) until the owner rules on public-use licensing. That ruling is owner-only (`SOURCE_PUBLIC_REUSE_LICENSING_OWNER_ONLY`). The procedure is in `PUBLICATION_PROCESS.md`, "Downloadable PDF Procedure".
- Publication also waits on the open dependencies DEP-RAS-SOURCE-USE-DISPOSITION, DEP-RAS-INDEPENDENT-REVIEW-ACCEPTANCE, DEP-RAS-ERL-245-RUNNER-INTEGRATION and DEP-RAS-SITE-PUBLICATION-AUTHORITY.
- Commercial inquiry stays gated separately (`StegVerse-Labs/.github#3370`).
- The route name is a proposal for the Site owner to confirm in the review of this document; changing it changes this entry only.

## Boundary

Site display does not replace source authority or validation evidence.
| `/wikis.html` | Public directory for the branded Admissibility, StegGuardian, and StegTalk wikis. | Site is navigation/display only; the linked wiki repositories remain canonical content owners. |
