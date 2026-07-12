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
| `/external-chat.html` | Public external-framework compatibility intake and comparison surface. | `StegVerse-Labs/admissibility-wiki/docs/external-frameworks` remains source of truth for published framework findings; Site performs bounded intake only. |
| `/governed-transitions.html` | Public projection of governed transition, executor, custody, and reconstruction state. | Orchestration and Master-Records remain source authorities. |
| `/admissibility-wiki.html` | Public bridge to the Admissibility Wiki. | `StegVerse-Labs/admissibility-wiki` remains source of truth; Site is display/bridge only. |
| `/governed-ecosystem.html` | Public mirror surface for governed ecosystem transition framing. | `StegVerse-Labs/admissibility-wiki` remains source of truth; Site is display/mirror only. |
| `/tt-code-representation.html` | Public mirror surface for TT code-representation status. | `Admissible-Existence/TT` remains source of truth; Site is display/mirror only. |
| `/governance-observatory.html` | Public mirror surface for Governance Observatory source-intake status. | `StegVerse-Labs/governance-observatory` remains source of truth; Site is display/mirror only. |
| `/papers` | Public display target for mirrored Publisher papers. | `GCAT-BCAT-Engine/Publisher` remains source of truth. |
| `/docs` | Documentation and evidence packet area. | Checked-in docs plus validation scripts. |
| `/actions` | GitHub Actions workflow history. | GitHub Actions plus checked-in evidence documents. |

## Public Display Paths

```text
/
/ecosystem-chat.html
/external-chat.html
/governed-transitions.html
/admissibility-wiki.html
/governed-ecosystem.html
/tt-code-representation.html
/governance-observatory.html
/papers
/docs
```

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
data/external-chat-example.json
data/external-framework-catalog.json
data/external-framework-catalog.receipt.json
scripts/check_external_chat_compatibility.py
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/external-chat-submission-contract.md
```

External Chat may generate browser-local downloadable result and challenge packets. Packet generation does not retain or publish the raw submission and creates no standing.

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

## Boundary

Site display does not replace source authority or validation evidence.
