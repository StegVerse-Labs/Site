# Site Mirror Activation Next Actions

Generated: 2026-06-17

## Source Of Truth

`docs/SITE_MIRROR_HANDOFF.md` is the current handoff and task source of truth for Publisher-to-Site paper mirror activation.

## Current State

```text
Goal: Site mirror activation hardening
Repository: StegVerse-Labs/Site
Source repository: GCAT-BCAT-Engine/Publisher
Source path: papers
Target path: papers
Activation state: ready_for_live_mirror_verification
```

## Observed Delta

The checked-in `papers/papers_manifest.json` is still pre-live-verification output.

Observed legacy fields:

```text
aliases
count
entries
generated_utc
source
target
```

Required live metadata fields:

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

## Next Actions

```text
1. Publisher generates paper data.
2. Publisher validates required paper source checks.
3. Publisher dispatches Site paper mirror with dry_run: true.
4. Publisher dispatches Site paper mirror with dry_run: false.
5. Site confirms Mirror Papers from Publisher completes.
6. Site confirms papers/papers_manifest.json has source metadata.
7. Site confirms aliases resolve.
8. Publisher updates receipt and verification tracker to activated.
```

## Site Verification Commands

```bash
python scripts/check_paper_display_policy.py
python scripts/check_papers_manifest_metadata.py
```

Expected manifest result:

```text
valid: Site papers manifest metadata
```

## Non-Claims

This document does not activate the mirror.

This document does not replace Publisher as source of truth.

This document does not mark the current checked-in manifest as live verified.
