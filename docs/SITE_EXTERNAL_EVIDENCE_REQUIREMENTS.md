# Site External Evidence Requirements

## Assumptions

1. `StegVerse-Labs/Site` is structurally complete for the current mirror/status build.
2. The remaining activation blocker is external workflow evidence, not another local public page, checker, or handoff document.
3. Site remains a mirror/display repository. It does not become source authority for Publisher papers, TT records, or Governance Observatory records.
4. Workflow paths displayed here without a leading period are iOS-safe display paths. Canonical workflow paths begin with a leading period.

## Done Definition

This file is done when the remaining external evidence required for goal activation is explicit, bounded, and machine-checkable.

## Required External Evidence

```text
TT sync workflow first bundle-fed commit
Governance Observatory status validation pass
Publisher paper mirror closure evidence
Publisher verification tracker activation update
Publisher activation status update
```

## TT Bundle Evidence

The TT sync workflow is:

```text
github/workflows/sync-tt-code-representation.yml
```

The canonical repository path begins with a leading period.

Required evidence:

```text
data/tt/transition-element-propagation-bundle.manifest.json exists
docs/SITE_TT_CODE_REPRESENTATION_STATUS.md is bundle-fed, not pending
docs/SITE_TT_CODE_REPRESENTATION_STATUS.json is bundle-fed, not pending
commit SHA records the bundle-fed status update
```

## Governance Observatory Evidence

The Governance Observatory validation workflow is:

```text
github/workflows/validate-governance-observatory-status.yml
```

The canonical repository path begins with a leading period.

Required evidence:

```text
workflow completes successfully
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.md remains non-authorizing
docs/SITE_GOVERNANCE_OBSERVATORY_STATUS.json remains non-authorizing
validation pass is recorded in a commit or workflow run summary
```

## Publisher Mirror Closure Evidence

Required evidence:

```text
Publisher workflow run URL
Publisher verification receipt artifact
Publisher live dispatch workflow URL
Site mirror workflow URL
Site mirror commit SHA
Site evidence artifact
Publisher closure receipt
Publisher verification tracker activation commit
Publisher activation status update commit
```

## Non-Claims

```text
External evidence does not make Site proof authority.
External evidence does not make Site source authority for TT.
External evidence does not make Site source authority for Publisher.
External evidence does not grant commit-time permission.
External evidence does not replace SPE standing determination.
```

## Current Status

```text
activation_state: pending_external_evidence
local_build_state: structurally_complete
remaining_blocker: external_workflow_evidence
```
