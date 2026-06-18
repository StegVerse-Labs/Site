# Site Mirror Activation Ledger

## Purpose

This ledger makes Site mirror activation status machine-verifiable without allowing Site-side evidence alone to claim activation.

The companion machine-readable file is:

```text
docs/SITE_MIRROR_ACTIVATION_LEDGER.json
```

## Current State

```text
activation_state: pending
repository: StegVerse-Labs/Site
source_repository: GCAT-BCAT-Engine/Publisher
source_path: papers
target_path: papers
source_of_truth: Publisher
```

## Non-Activation Rule

Site-side evidence alone does not activate the mirror. Publisher closure remains required before activation can be claimed.

## Required Evidence

```text
publisher_workflow_run_url: pending
publisher_verification_receipt_artifact: pending
publisher_live_dispatch_workflow_url: pending
site_mirror_workflow_url: pending
site_mirror_commit_sha: pending
site_evidence_artifact: pending
publisher_closure_nudge_result: pending
publisher_closure_receipt: pending
publisher_verification_tracker_activation_commit: pending
publisher_activation_status_update_commit: pending
```

## Required Checks

```text
python scripts/check_site_mirror_handoff.py
python scripts/check_site_mirror_evidence_packet.py
python scripts/check_site_mirror_live_evidence_state.py
python scripts/check_site_mirror_closure_next_build.py
python scripts/check_site_mirror_closure_guard.py
python scripts/check_site_mirror_activation_ledger.py
```

## Activation Allowed Only When

```text
1. Publisher automated dispatch workflow produces a verification receipt artifact.
2. Publisher workflow dispatches Site mirror workflow successfully.
3. Site mirror workflow completes.
4. Site mirror workflow writes and uploads Site evidence artifact.
5. Publisher closure workflow consumes Publisher and Site evidence artifacts.
6. Publisher closure workflow writes docs/mirror-activation-closures/<closure>.json.
7. Publisher verification tracker is updated to activated.
8. Publisher activation status is updated to activated.
```

## Completion Condition

This ledger is valid when:

```text
python scripts/check_site_mirror_activation_ledger.py
```

passes.

## Archive Readiness

This ledger lets a future session determine whether Site mirror activation remains pending or has sufficient evidence to proceed without reading prior chat context.
