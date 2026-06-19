# Site Public Paths

## Purpose

This document defines public-facing semantics for high-interest paths in `StegVerse-Labs/Site`.

It is not an activation receipt, adoption claim, endorsement claim, or production-status claim. It only explains what visitors, crawlers, indexers, automated fetchers, and future contributors should understand when they encounter common repository and site paths.

## Scope

```text
Repository: StegVerse-Labs/Site
Document type: public path semantics
Activation impact: supporting documentation only
Source of truth for mirror activation: docs/SITE_MIRROR_HANDOFF.md
Traffic context: docs/SITE_TRAFFIC_AND_INGESTION_SIGNAL.md
```

## Interpretation Boundary

Observed traffic or path interest may justify clearer public documentation.

It must not be interpreted as:

```text
adoption
production activation
institutional validation
external endorsement
successful Site mirror activation
proof that every clone or view is human-originated
```

Allowed interpretation:

```text
These paths are visible enough that their purpose, authority, and evidence boundaries should be explicit.
```

## Public Path Register

| Path | Public meaning | May contain | Must not imply | Authority source |
|---|---|---|---|---|
| `/` | Site repository landing surface and public entry point. | Overview material, links to public evidence, display pages, and documentation. | Adoption, endorsement, or activated mirror status by itself. | `StegVerse-Labs/Site` checked-in content. |
| `/admissibility-wiki.html` | Public bridge to the Admissibility Wiki. | Vocabulary bridge copy, AI-governed proposal-system explanation, transition-table element mapping, proposal transition blocks, and links to wiki source/status. | That Site accepts wiki proposals, issues wiki receipts, authors wiki decisions, or becomes proof authority. | `StegVerse-Labs/admissibility-wiki` remains source of truth for wiki records; Site is display/bridge only. |
| `/papers` | Public display target for mirrored Publisher papers. | Mirrored papers, manifest-derived listings, paper aliases, display-policy references. | That Site is the editorial source of truth. | `GCAT-BCAT-Engine/Publisher` remains source of truth. |
| `/upload` | GitHub upload route, not a StegVerse evidence intake guarantee. | User-initiated GitHub upload UI if permissions allow. | That uploaded files are automatically accepted, validated, or committed. | GitHub permissions and repository review rules. |
| `/upload/main` | GitHub upload route targeting the default branch context. | Candidate file uploads from authorized GitHub users. | That default-branch uploads bypass validation or review. | GitHub branch protections, workflows, and maintainers. |
| `/upload/main/incoming` | Candidate upload route for the `incoming` area. | Proposed incoming artifacts, fixtures, receipts, or samples if the path exists and maintainers accept them. | That incoming material is trusted, effect-capable, or authoritative. | Maintainer review plus any declared validation workflow. |
| `/upload/main/tools` | Candidate upload route for tool-related files. | Proposed tool scripts, validators, adapters, or utility documentation if accepted. | That uploaded tools are safe, approved, or production-ready. | Maintainer review plus tool validation. |
| `/tree/main` | GitHub source browser for the default branch. | Checked-in repository files. | That every checked-in file is active production behavior. | Repository history and current branch state. |
| `/tree/main/incoming` | Source browser for incoming artifacts if present. | Staged, candidate, pending, or externally supplied artifacts. | That candidate artifacts are validated or committed to governance decisions. | Repository documentation and validation receipts. |
| `/tree/main/tools` | Source browser for tool files if present. | Scripts, validators, developer utilities, and supporting tools. | That all tools are live services or public APIs. | Tool documentation, tests, and workflow evidence. |
| `/tree/main/data` | Source browser for data files if present. | Fixtures, examples, manifests, non-secret public datasets, and generated static data. | That data is private intake, verified truth, or live telemetry. | File-specific metadata, receipts, and validation scripts. |
| `/actions` | GitHub Actions workflow history. | Workflow runs, dispatches, logs, and status evidence visible under GitHub permissions. | That a workflow exists as production activation without matching evidence fields. | GitHub Actions plus checked-in evidence documents. |
| `/docs` | Documentation and evidence packet area. | Policies, handoffs, status documents, verification notes, and public-facing governance explanations. | That documentation alone activates a workflow. | Checked-in docs plus validation scripts. |

## Path Classes

### Public Display Paths

```text
/
/admissibility-wiki.html
/papers
/docs
```

These paths are primarily human-readable. They should explain the current public state without overstating activation.

### GitHub Upload Paths

```text
/upload
/upload/main
/upload/main/incoming
/upload/main/tools
```

These are GitHub interface paths. They should be treated as candidate-submission routes only.

They do not create authority by themselves.

### Repository Source Paths

```text
/tree/main
/tree/main/incoming
/tree/main/tools
/tree/main/data
```

These paths expose checked-in or browsable repository structure. They can show what exists, but existence alone does not prove validation, activation, or effect capability.

### Workflow Evidence Paths

```text
/actions
```

Workflow history is evidence only when it is tied to explicit receipt fields, commit SHAs, and validation documents.

## Public Copy Rules

Public copy for these paths should use bounded language.

Allowed:

```text
public artifact endpoint
candidate intake surface
mirror display target
workflow evidence surface
source-preserving mirror path
sandbox-only candidate material
pending validation
public bridge surface
```

Avoid:

```text
adopted
endorsed
activated
trusted by traffic
validated by upload
production-proven from views
```

## Admissibility Wiki Bridge Boundary

For `admissibility-wiki.html`, the Site repository is a public bridge surface.

The vocabulary, terminology-convergence, proposal-review, decision-record, receipt, ontology, and wiki-status authority remains:

```text
StegVerse-Labs/admissibility-wiki
```

Site may explain the AI-governed proposal system and transition-table elements, but Site must not claim that it accepts wiki proposals, issues wiki receipts, or decides wiki terminology standing.

## Mirror-Specific Boundary

For `papers`, the Site repository is a display target.

The editorial and source authority remains:

```text
GCAT-BCAT-Engine/Publisher
```

The Site mirror must preserve source metadata and must not become an independent paper source of truth.

Required companion references:

```text
docs/SITE_PAPER_DISPLAY_POLICY.md
docs/README_SITE_PAPERS_MIRROR.md
docs/SITE_MIRROR_HANDOFF.md
docs/SITE_MIRROR_EVIDENCE_PACKET.md
docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json
```

## Incoming/Tools/Data Boundary

The following paths, if present, should be treated as non-authoritative unless a file-specific receipt says otherwise:

```text
incoming
tools
data
```

Default posture:

```text
candidate or supporting material
not effect-capable by default
not trusted by placement alone
requires validation before being cited as evidence
```

## Done Criteria

This document is complete when:

```text
high-interest public paths have explicit semantics
upload routes are marked as candidate-submission routes only
papers are marked as mirror display targets only
admissibility-wiki.html is marked as public bridge only
traffic is not treated as adoption or activation
workflow history is tied to receipts and evidence fields
```

## Current Status

```text
Status: public_path_semantics_documented
Activation impact: supporting_context_only
Next dependency: docs/SITE_INGESTION_SURFACES.md
```
