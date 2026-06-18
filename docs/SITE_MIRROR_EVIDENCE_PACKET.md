# Site Mirror Evidence Packet

## Purpose

This packet records the evidence required to complete Publisher-to-Site paper mirror activation.

It must not be marked complete until the Publisher dry-run, Publisher live dispatch, Site mirror workflow, regenerated manifest, public aliases, and Publisher receipt/tracker updates are all verified.

`docs/SITE_MIRROR_HANDOFF.md` remains the handoff and task source of truth.

## Current State

```text
status: pending_live_verification
goal: Site mirror activation hardening
repository: StegVerse-Labs/Site
source_repository: GCAT-BCAT-Engine/Publisher
source_path: papers
target_path: papers
```

## Required Evidence Fields

```text
publisher_dry_run_workflow_url: PENDING
publisher_dry_run_receipt_commit: PENDING
publisher_live_dispatch_workflow_url: PENDING
site_mirror_workflow_url: PENDING
site_mirror_commit_sha: PENDING
manifest_source_repository: PENDING
manifest_source_ref: PENDING
manifest_source_of_truth: PENDING
alias_verification_results: PENDING
publisher_receipt_update_commit: PENDING
publisher_verification_tracker_commit: PENDING
publisher_activation_status_update_commit: PENDING
```

## Verification Commands

Run these after the Site mirror workflow completes:

```bash
python scripts/check_paper_display_policy.py
python scripts/check_papers_manifest_metadata.py
python scripts/check_paper_aliases.py
python scripts/check_site_mirror_evidence_packet.py
```

## Activation Completion Condition

Mirror activation may only be marked complete when every evidence field is replaced with real evidence and the Site manifest metadata checker returns:

```text
valid: Site papers manifest metadata
```

The Site alias checker must also return:

```text
valid: Site paper aliases resolve
```

The Site mirror evidence packet checker must also complete without missing fields or unresolved required references:

```text
python scripts/check_site_mirror_evidence_packet.py
```

## Non-Claims

This pending packet does not claim:

- live mirror activation;
- Publisher dry-run receipt completion;
- Publisher receipt completion;
- Publisher verification tracker completion;
- Publisher activation-status completion;
- public alias verification success;
- Site manifest metadata success.

## Governing Sentence

The Publisher-to-Site mirror is not activated by workflow existence alone; activation requires live dispatch evidence, Site mirror completion evidence, manifest source metadata, alias verification, Publisher-side dry-run receipt evidence, and Publisher-side receipt/tracker/status closure.
