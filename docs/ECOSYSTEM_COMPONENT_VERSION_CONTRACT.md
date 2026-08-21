# StegVerse Ecosystem Component Version Contract

## Purpose

Every major StegVerse component must expose one machine-readable version declaration that a user-facing surface can project without collapsing development, validation, release, deployment, runtime proof, or activation into one state.

This contract does not create release authority. It standardizes how existing repository truth is represented.

## Required declaration

Canonical path for a participating repository:

```text
VERSION.json
```

Required fields:

```json
{
  "schema_version": "1.0.0",
  "component_id": "stable-component-id",
  "repository": "organization/repository",
  "component_version": "repository-owned version identity",
  "version_stage": "DEVELOPMENT|RELEASE_CANDIDATE|RELEASED",
  "release": {
    "tag": null,
    "commit": null,
    "release_evidence": []
  },
  "runtime": {
    "state": "NOT_CLAIMED|PENDING|PROVEN",
    "evidence": []
  },
  "activation": {
    "state": "NOT_ACTIVATED|PENDING|ACTIVATED",
    "evidence": []
  },
  "source_of_truth": "applicable *_MIRROR_HANDOFF.md",
  "authority_effect": "NONE"
}
```

## Version identity rule

`component_version` is the repository-owned component identity and may represent a development line before release. A development version is not a release.

A component must not use `version_stage: RELEASED` unless all of the following are present and mutually consistent:

```text
release.tag
release.commit
release.release_evidence
```

A moving branch such as `main` is never a release version and must not be substituted for an exact tag/commit/release set.

## State separation

The following implications are prohibited:

```text
BUILT != VALIDATED
VALIDATED != RELEASED
RELEASED != DEPLOYED
DEPLOYED != RUNTIME_PROVEN
RUNTIME_PROVEN != ACTIVATED
COMPONENT_RELEASED != ECOSYSTEM_RELEASED
```

A declaration may therefore legitimately contain:

```text
component_version: development identity
version_stage: DEVELOPMENT
runtime.state: PROVEN
activation.state: PENDING
```

or any other evidence-supported combination.

## Aggregate ecosystem release

An ecosystem release exists only when an aggregate manifest names the exact required component set and, for every required released component, records the exact component version, tag, commit, and release evidence.

Until then:

```text
ecosystem_release.version = null
ecosystem_release.state = NOT_AGGREGATELY_RELEASED
```

Site is a projection surface for that state, not release authority.

## User-facing requirement

Human-facing status must answer, without requiring repository knowledge:

1. What can I use now?
2. What version/component identity am I looking at?
3. Is it merely built, validated, released, deployed, runtime-proven, or activated?
4. What remains before the next state?

`ecosystem-version.html` is the current Site projection surface.

## Credential and authority boundary

```text
credentials: TV/TVC_ONLY
GitHub token runtime authority: prohibited
NON-TV/TVC production authority: prohibited
model output execution authority: none
VERSION.json authority_effect: NONE
```

Version metadata records state; it does not grant execution, publication, release, custody, or activation authority.
