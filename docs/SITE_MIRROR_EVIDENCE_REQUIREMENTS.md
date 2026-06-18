# Site Mirror Evidence Requirements

## Purpose

This packet defines the exact evidence required before Site mirror activation may advance beyond pending.

It exists to keep the human-readable status, machine-readable activation ledger, evidence packet, live evidence state, and handoff aligned.

## Source Of Truth

```text
Ledger: docs/SITE_MIRROR_ACTIVATION_LEDGER.json
Status: docs/SITE_MIRROR_ACTIVATION_STATUS.md
Handoff: docs/SITE_MIRROR_HANDOFF.md
```

## Non-Activation Rule

Site-side evidence alone does not activate the mirror. Publisher closure remains required before activation can be claimed.

## Required Evidence Keys

```text
publisher_workflow_run_url
publisher_verification_receipt_artifact
publisher_live_dispatch_workflow_url
site_mirror_workflow_url
site_mirror_commit_sha
site_evidence_artifact
publisher_closure_nudge_result
publisher_closure_receipt
publisher_verification_tracker_activation_commit
publisher_activation_status_update_commit
```

## Required Pending State

Until Publisher closure evidence exists, every required evidence key in `docs/SITE_MIRROR_ACTIVATION_LEDGER.json` must remain:

```text
pending
```

## Evidence Capture Boundary

Site may generate and upload Site evidence, but activation cannot advance until Publisher closure consumes the Publisher and Site evidence artifacts and updates the Publisher verification tracker and activation status.

## Required Checks

```text
python scripts/check_site_mirror_evidence_packet.py
python scripts/check_site_mirror_live_evidence_state.py
python scripts/check_site_mirror_activation_ledger.py
python scripts/check_site_mirror_activation_status.py
python scripts/check_site_mirror_evidence_requirements.py
```

## Completion Condition

This packet is valid when:

```text
python scripts/check_site_mirror_evidence_requirements.py
```

passes.

## Archive Readiness

This packet lets a future session determine exactly which evidence keys block activation without reading prior chat context.
