# Site T-CL Propagation Intake

## Purpose

This document records the Site-side intake of the T-CL release-candidate propagation task.

It follows the cross-repo mirror handoff rule:

```text
current repo handoff declares next target
target repo handoff is checked
target repo records bounded intake
work continues from target repo governance
```

## Source

```text
source_repository: StegVerse-Labs/T-CL
source_handoff: docs/TCL_RELEASE_CANDIDATE_MIRROR_HANDOFF.md
source_release_readiness: release/tcl_release_readiness.json
source_propagation_record: propagation/tcl_downstream_propagation_verification.json
```

## Destination

```text
destination_repository: StegVerse-Labs/Site
destination_handoff_checked: docs/SITE_MIRROR_HANDOFF.md
destination_handoff_state: pending_external_evidence
```

## Machine-Readable Intake Record

```text
docs/SITE_TCL_PROPAGATION_INTAKE.json
```

## Site Boundary

Site may display or route T-CL release-readiness status only as a Site status surface.

Site must not:

```text
redefine T-CL semantics
claim downstream propagation completion without a receipt
claim admissibility-cost savings are measured
turn release-readiness into certification or authority
```

## Required Site Action

Evaluate whether T-CL release-readiness summary, Core-Lite intake posture, fail-closed proof-claim boundary, and admissibility-cost guardrails should be displayed as Site status-only surfaces.

## Next Build Step

Create or update Site display/status artifacts only after a Site-local propagation receipt and checker are added.
