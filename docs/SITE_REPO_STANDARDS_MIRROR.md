# Site Repo Standards Mirror

## Purpose

This document mirrors the current `StegVerse-Labs/repo-standards` release-candidate surface into the Site repository for public display and adoption guidance.

## Source Authority

`StegVerse-Labs/repo-standards` remains authoritative for repository standards, schemas, templates, validators, correction tooling, and release readiness.

Site is display-only. This mirror does not create repository standards, certify conformance, grant correction authority, or replace validation evidence from the source repository.

## Mirrored Source State

```text
Source repository: StegVerse-Labs/repo-standards
Source status: 0.1.0-rc.1 release-candidate surface prepared
Source handoff: REPO_STANDARDS_MIRROR_HANDOFF.md
Source release report: reports/release-candidate-status.md
```

## Core Standards Mirrored

| ID | Standard | Purpose |
| --- | --- | --- |
| ST-001 | README Source Map | README claims derive from mapped repository facts. |
| ST-002 | Workflow and Task Declaration | Repos use no more than two active workflows. |
| ST-003 | Repository Correction | Corrections follow audit, plan, minimal change, validation, receipt. |
| ST-004 | Transition Table Elements | Org AI Entity actions declare actor, action, target, authority, evidence, validation, receipt, and recovery. |
| ST-005 | Repository Layout | Required and reserved directory structure. |
| ST-006 | Metadata | Repository identity, status, capabilities, and standard references. |
| ST-007 | Evidence and Receipt | Validation and correction outputs are reconstructable. |
| ST-008 | Naming | Stable naming for standards, schemas, templates, tools, and generated artifacts. |
| ST-009 | Dependency | Standards and repo dependencies are declared explicitly. |
| ST-010 | Lifecycle | Repository maturity states and transition rules. |
| ST-011 | Validation | Validators are deterministic and fail closed. |
| ST-012 | Org AI Entity Capability | Entity capabilities and authority classes are explicit. |
| ST-013 | Standards Admissibility | Repositories prove conformance rather than merely claiming it. |

## Adoption Path

A consuming repository should add:

```text
README.md
README_SOURCE_MAP.md
readme.sources.yaml
repo.metadata.yaml
declared-tasks.yaml
```

It should keep no more than two active workflows:

```text
github/workflows/bootstrap.yml
github/workflows/declared-tasks.yml
```

Note: workflow paths are displayed without the leading period for iOS readability. Actual repository paths use the standard GitHub Actions directory.

## Validation Boundary

The Site mirror records that GitHub returned no commit statuses and no workflow runs for the latest checked `repo-standards` release-candidate commit. Therefore Site must not display the release candidate as validated release.

## Downstream Status

```text
Site mirror: installed
Publisher mirror: pending
admissibility-wiki mirror: pending
stegguardian-wiki mirror: pending
```

## Human-Readable Result

`repo-standards` is ready for validation execution and downstream mirror planning. It is not yet tagged as a validated release.
