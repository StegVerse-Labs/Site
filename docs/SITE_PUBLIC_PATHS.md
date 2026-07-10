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
/admissibility-wiki.html
/governed-ecosystem.html
/tt-code-representation.html
/governance-observatory.html
/papers
/docs
```

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
