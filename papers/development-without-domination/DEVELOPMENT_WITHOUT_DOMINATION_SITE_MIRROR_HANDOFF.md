# Development Without Domination — Site Mirror Handoff

## Source of truth

This file is the paper-specific handoff for the StegVerse public Site projection of:

> **Development Without Domination: Reciprocal Developmental Sovereignty as a Foundation for Human-AI Relations**

Repository: `StegVerse-Labs/Site`

Branch: `publication/development-without-domination-v1`

Issue: `StegVerse-Labs/Site#128`

Pull request: `StegVerse-Labs/Site#129`

## Current determination

```text
layer_exists: true
layer_state: BUILDING
activation_state: NOT_ACTIVATED
execution_class: PARALLEL_SAFE
external_tasks: none
repository_owned_observer: scripts/observe_development_without_domination_publication.py
repository_owned_registration: scripts/register_development_without_domination_workstream.py
repository_owned_workflow: .github/workflows/development-without-domination-publication.yml
```

The paper layer is being built inside StegVerse. It is not waiting on an unnamed external actor. Every incomplete gate must resolve to a repository, path, issue, and executable action.

## Orchestration admission

Task ID:

```text
SITE-0001-DEVELOPMENT-WITHOUT-DOMINATION-PUBLICATION
```

Registration location:

```text
data/site-orchestration-state.json
```

Registration controller:

```text
scripts/register_development_without_domination_workstream.py
```

The task is `PARALLEL_SAFE` and does not supersede the HIL upload surface or Site issue #24.

## Artifact identity

Expected PDF path:

```text
papers/development-without-domination/Development_Without_Domination_Rigel_Randolph_Final.pdf
```

Expected SHA-256:

```text
c2fcb0ce76f5eaba1a6dd4ccdd358fcae29b32b3110767b5f2b5b2ffa347c29d
```

Expected editable source identity:

```text
Development_Without_Domination_Rigel_Randolph_Final.docx
fa7d9c2069ce17e26f1c7f5f4a6bb983ccd4229c11ebc1fd8c788b8d7d2fc2ab
```

A declared hash is not repository custody. The exact bytes must be committed and independently hashed by the observer.

## Autonomous observation and completion

Observer:

```text
scripts/observe_development_without_domination_publication.py
```

Workflow:

```text
.github/workflows/development-without-domination-publication.yml
```

Machine-readable state:

```text
papers/development-without-domination/site-publication-status.json
```

Activation receipt:

```text
papers/development-without-domination/site-mirror-receipt.json
```

The observer advances only through evidence-backed states:

```text
BUILDING
-> SOURCE_OBSERVED
-> SITE_BYTES_VERIFIED
-> ROUTE_READY
-> ACTIVATED
```

Every incomplete gate is written into `remaining_tasks` with these required fields:

```text
repository
path
issue
action
```

No `external blocker`, `external task`, or ownerless waiting state is valid.

## Concrete remaining task locations

### Exact PDF custody

Repository: `StegVerse-Labs/Site`

Path:

```text
papers/development-without-domination/Development_Without_Domination_Rigel_Randolph_Final.pdf
```

Owner record:

```text
StegVerse-Labs/Site#128
StegVerse-Labs/Site#129
```

### Public landing route

Repository: `StegVerse-Labs/Site`

Path:

```text
papers/development-without-domination/index.html
```

Owner record:

```text
StegVerse-Labs/Site#128
StegVerse-Labs/Site#129
```

### Site mirror receipt

Repository: `StegVerse-Labs/Site`

Path:

```text
papers/development-without-domination/site-mirror-receipt.json
```

Generator:

```text
scripts/observe_development_without_domination_publication.py
```

### Publisher observation

Repository: `GCAT-BCAT-Engine/Publisher`

Paths:

```text
papers/development-without-domination/publication-manifest.json
papers/development-without-domination/publication-receipt.json
```

Owner record:

```text
GCAT-BCAT-Engine/Publisher#21
GCAT-BCAT-Engine/Publisher#22
```

Publisher is an ecosystem repository, not an external task. The Site observer reads its repository evidence directly.

## Activation gate

The Site paper layer becomes `ACTIVATED` only when:

```text
exact PDF exists at the declared Site path
computed PDF SHA-256 equals the expected identity
public_route is recorded
route verification is recorded
site-mirror-receipt.json is generated
```

## Authority boundary

```text
preparation != publication
repository presence != deployed availability
Publisher manifest != Site custody
Site custody != route verification
publication != admissibility
LinkedIn distribution != StegVerse source authority
```

## Continuation instruction

Run or allow the repository workflow to run. The workflow first registers the task, then observes repository evidence, updates the status, and commits evidence-backed state transitions. Repair any failing repository-local gate at the exact path recorded in `remaining_tasks`; do not convert it into an external waiting state.
