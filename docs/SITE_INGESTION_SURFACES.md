# Site Ingestion Surfaces

## Purpose

This document defines ingestion-facing semantics for `StegVerse-Labs/Site`.

It describes how public, candidate, mirrored, generated, and workflow-produced artifacts should be interpreted before they are trusted, displayed, or used as evidence.

## Scope

```text
Repository: StegVerse-Labs/Site
Document type: ingestion surface semantics
Activation impact: supporting documentation only
Primary handoff: docs/SITE_MIRROR_HANDOFF.md
Public path companion: docs/SITE_PUBLIC_PATHS.md
Traffic companion: docs/SITE_TRAFFIC_AND_INGESTION_SIGNAL.md
```

## Core Rule

```text
Ingestion is not authority.
```

A file, payload, paper, manifest, receipt, tool, or workflow result may enter the repository or be visible from a public path without becoming effect-capable.

The repository should preserve this distinction:

```text
accepted for visibility ≠ accepted for governance
accepted for sandbox ≠ accepted for commit
accepted for display ≠ source of truth
workflow ran ≠ activation complete
```

## Ingestion Surface Classes

| Surface | Class | Default authority | Required evidence before higher trust |
|---|---|---:|---|
| `papers` | mirrored display surface | Display-only | Manifest metadata, display policy, source repository/ref/path, mirror workflow evidence. |
| `papers/papers_manifest.json` | generated mirror manifest | Source-preserving index | Metadata checker pass and source-of-truth fields. |
| `incoming` | candidate artifact surface | None by default | File-specific validation, receipt, reviewer decision, or documented promotion path. |
| `tools` | support tool surface | None by default | Tests, usage docs, safe execution boundary, and workflow integration if used in CI. |
| `data` | public data/fixture surface | None by default | Schema, provenance, validation command, and receipt if used as evidence. |
| `docs` | documentation/evidence surface | Explanatory | Matching checker scripts or receipt fields for activation claims. |
| `github/workflows` | automation surface | Operational | Successful run evidence plus matching checked-in evidence fields. |
| `/actions` | workflow evidence view | Observational | Run URL, run result, commit SHA, and referenced receipt/packet fields. |
| `/upload*` | GitHub candidate-upload route | None by default | Review, branch rules, validation, and commit provenance. |

Note: `github/workflows` is displayed without the leading dot. The actual repository path includes the leading dot.

## Required Ingestion States

Every material ingestion path should be classifiable into one of these states:

```text
candidate
sandbox_only
validated_supporting_artifact
mirrored_display_artifact
evidence_pending
evidence_complete
activation_supporting
rejected
fail_closed
```

## Default State Mapping

```text
/upload*                  -> candidate
incoming/*                -> candidate
incoming/* invalid        -> fail_closed or rejected
tools/* untested          -> sandbox_only
tools/* tested            -> validated_supporting_artifact
data/* without schema     -> sandbox_only
data/* with schema/check  -> validated_supporting_artifact
papers/* mirrored         -> mirrored_display_artifact
papers_manifest.json      -> activation_supporting only after metadata checks
docs/* status claims      -> evidence_pending unless checker-required fields are complete
/actions run              -> evidence_supporting only when recorded in evidence packet
```

## Mirror Ingestion Contract

The paper mirror path is a special ingestion surface.

It may display Publisher content, but it must not become a separate editorial source.

Required mirror fields:

```text
source_repository
source_ref
source_path
source_of_truth
target_repository
target_path
display_policy
mirror_protocol
workflow
generated_utc
count
aliases
entries
```

Required checks:

```text
python scripts/check_papers_manifest_metadata.py
python scripts/check_paper_aliases.py
python scripts/check_paper_display_policy.py
python scripts/check_site_mirror_evidence_packet.py
python scripts/check_site_mirror_live_evidence_state.py
```

## Candidate Upload Contract

Anything entering through upload-like paths must be treated as candidate material.

Default rule:

```text
uploaded ≠ accepted
accepted by GitHub ≠ validated
checked in ≠ effect-capable
```

Candidate files should not be cited as evidence unless they have at least one of:

```text
schema validation
receipt hash
workflow run URL
review record
source metadata
explicit promotion document
```

## Incoming Surface Contract

The `incoming` path, if used, should be for untrusted or not-yet-promoted artifacts.

Allowed contents:

```text
candidate receipts
external examples
public fixtures
sandbox payloads
review packets
pending evidence files
```

Disallowed assumptions:

```text
incoming material is trusted
incoming material is production-ready
incoming material has been accepted into governance state
incoming material can override Publisher or Site policy
```

Recommended file-level metadata:

```json
{
  "ingestion_state": "candidate",
  "source": "external_or_browser_or_workflow",
  "effect_capable": false,
  "validation": "pending",
  "receipt": "pending"
}
```

## Tools Surface Contract

The `tools` path may contain scripts or utilities, but tools should not be treated as safe or authoritative by placement alone.

A tool becomes validation-supporting only when it has:

```text
clear purpose
safe execution assumptions
input/output contract
repeatable command
known fixture or expected result
workflow integration if relied on by CI
```

## Data Surface Contract

The `data` path may contain fixtures, examples, manifests, or public static datasets.

A data file becomes evidence-supporting only when it has:

```text
source/provenance
schema or shape description
validation command
hash or receipt if used in activation evidence
```

## Documentation Surface Contract

Documentation may explain status, but activation status must be backed by evidence.

Any document claiming live mirror activation must align with:

```text
docs/SITE_MIRROR_EVIDENCE_PACKET.md
docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json
scripts/check_site_mirror_evidence_packet.py
scripts/check_site_mirror_live_evidence_state.py
```

If evidence remains pending, the correct language is:

```text
ready_for_live_mirror_verification
```

not:

```text
activated
```

## Workflow Evidence Contract

A workflow run becomes activation-supporting evidence only when captured with:

```text
workflow name
workflow URL
run result
commit SHA
receipt commit if applicable
matching evidence-packet field
matching live-evidence-state field if required
```

A green workflow run by itself is not enough if the required evidence packet still says `pending`.

## Public Display Decision Rules

Use the following decision rules before public display or activation claims.

```text
IF artifact has unknown source:
  classify as candidate or sandbox_only

IF artifact is uploaded through GitHub UI:
  classify as candidate until reviewed/validated

IF artifact is mirrored from Publisher:
  classify as mirrored_display_artifact only if source metadata is preserved

IF artifact is generated by workflow:
  classify as evidence_supporting only if workflow URL and commit SHA are recorded

IF evidence fields are pending:
  do not claim activation

IF validation fails:
  classify as rejected or fail_closed
```

## Receipt Expectations

For higher-trust ingestion, prefer receipts with:

```text
artifact path
artifact sha256 or Git blob SHA
source repository or source path
workflow URL if generated
commit SHA
classification
effect_capable boolean
validation command
validation result
timestamp
```

## Done Criteria

This document is complete when:

```text
ingestion surfaces have default authority states
upload routes are candidate-only by default
incoming/tools/data are non-authoritative by placement alone
paper mirror ingestion preserves Publisher authority
workflow evidence requires recorded URLs and commits
activation claims remain blocked while evidence is pending
```

## Current Status

```text
Status: ingestion_surface_semantics_documented
Activation impact: supporting_context_only
Primary next action: live Publisher/Site mirror verification evidence capture
```
