# Site Mirror Evidence Packet

## Purpose

This packet records the evidence required to complete Publisher-to-Site paper mirror activation.

It must not be marked complete until the Publisher dry-run, Publisher live dispatch, Site mirror workflow, regenerated manifest, public aliases, Site evidence completion commits, and Publisher receipt/tracker updates are all verified.

`docs/SITE_MIRROR_HANDOFF.md` remains the handoff and task source of truth.

`docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json` is the machine-readable activation-state companion for this packet.

## Current State

```text
status: pending_live_verification
goal: Site mirror activation hardening
repository: StegVerse-Labs/Site
source_repository: GCAT-BCAT-Engine/Publisher
source_path: papers
target_path: papers
live_evidence_state: docs/SITE_MIRROR_LIVE_EVIDENCE_STATE.json
```

## Required Evidence Fields

```text
publisher_dry_run_workflow_url: PENDING
publisher_dry_run_receipt_commit: PENDING
publisher_live_dispatch_workflow_url: PENDING
site_mirror_workflow_url: PENDING
site_mirror_commit_sha: PENDING
manifest_source_repository: GCAT-BCAT-Engine/Publisher
manifest_source_ref: main
manifest_source_of_truth: Publisher papers directory
alias_verification_results: PENDING
site_evidence_packet_completion_commit: PENDING
site_live_evidence_state_completion_commit: PENDING
publisher_receipt_update_commit: PENDING
publisher_verification_tracker_commit: PENDING
publisher_activation_status_update_commit: PENDING
```

## Verification Commands

Run these after the Site mirror workflow completes:

```bash
python scripts/check_paper_display_policy.py
python scripts/check_transition_table_public_copy.py
python scripts/check_papers_manifest_metadata.py
python scripts/check_paper_aliases.py
python scripts/check_site_mirror_evidence_packet.py
python scripts/check_site_mirror_live_evidence_state.py
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

The Transition Table public copy checker must also return:

```text
valid: Transition Table public copy extraction-safe
```

The Site mirror evidence packet checker must also complete without missing fields or unresolved required references:

```text
python scripts/check_site_mirror_evidence_packet.py
```

The Site mirror live evidence state checker must also complete without unresolved activation claims or Markdown/JSON evidence drift:

```text
python scripts/check_site_mirror_live_evidence_state.py
```

Pending state must print:

```text
valid: Site mirror live evidence state pending
```

Activated state must print:

```text
valid: Site mirror live evidence state activated
```

## Non-Claims

This pending packet does not claim:

- live mirror activation;
- Publisher dry-run receipt completion;
- Publisher receipt completion;
- Publisher verification tracker completion;
- Publisher activation-status completion;
- public alias verification success;
- Site evidence-packet completion;
- Site live-evidence-state completion;
- Site manifest metadata success.

## Governing Sentence

The Publisher-to-Site mirror is not activated by workflow existence alone; activation requires live dispatch evidence, Site mirror completion evidence, manifest source metadata, alias verification, Transition Table public-copy safety, Site evidence completion commits, Publisher-side dry-run receipt evidence, Publisher-side receipt/tracker/status closure, and a machine-readable live evidence state that cannot claim activation while required evidence is pending or while its human-readable packet has drifted.
