# Site Mirror Live Verification

This document records the live verification packet required before Publisher-to-Site paper mirroring can be marked activated.

Source of truth:

```text
docs/SITE_MIRROR_HANDOFF.md
```

## Required Run Order

```text
1. Publisher: Generate Papers JSON
2. Publisher: Validate Emergency AI Cases
3. Publisher: Dispatch Site Paper Mirror with dry_run: true
4. Publisher: Dispatch Site Paper Mirror with dry_run: false
5. Site: confirm Mirror Papers from Publisher completes
6. Site: confirm papers/papers_manifest.json has source metadata
7. Site: confirm aliases resolve
8. Publisher: update receipt and verification tracker to activated
```

## Evidence Capture Template

```text
publisher_dry_run_workflow_url: TODO
publisher_live_dispatch_workflow_url: TODO
site_mirror_workflow_url: TODO
site_commit_sha_generated_by_mirror_workflow: TODO
papers_manifest_source_repository: TODO
papers_manifest_source_ref: TODO
papers_manifest_source_of_truth: TODO
public_alias_Papers_html: TODO
public_alias_papers_html: TODO
public_alias_papers_index_html: TODO
public_alias_publisher_papers_html: TODO
public_alias_publisher_papers_index_html: TODO
publisher_receipt_update_commit: TODO
publisher_verification_tracker_activation_commit: TODO
```

## Site-Side Validation Commands

```bash
python scripts/check_paper_display_policy.py
python scripts/check_papers_manifest_metadata.py
```

## Activation Rule

The mirror is activated only after the live dispatch, Site workflow, manifest validation, alias verification, and Publisher receipt/tracker updates are all recorded.

## Non-Claims

This file does not make Site an editorial source of truth. Publisher remains authoritative.
