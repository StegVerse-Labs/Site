# Site Mirror Alias Verification

Generated: 2026-06-17

## Purpose

This document defines the alias-resolution verification layer for Publisher-to-Site paper mirroring.

`docs/SITE_MIRROR_HANDOFF.md` remains the current handoff and task source of truth.

## Assumptions

The Site mirror workflow generates these public paper entry points:

```text
Papers.html
papers.html
papers/index.html
publisher/papers.html
publisher/papers/index.html
```

The Site mirror must preserve Publisher as the source of truth. Alias verification only confirms public Site paths resolve to the mirrored display page.

## Done State

Alias verification is complete when:

```text
scripts/check_paper_aliases.py exists.
Papers.html exists as the canonical paper display page.
papers.html redirects to Papers.html.
papers/index.html exists as a canonical paper display page.
publisher/papers.html redirects to ../Papers.html.
publisher/papers/index.html redirects to ../../Papers.html.
The alias checker prints valid: Site paper aliases resolve.
```

## Verification Command

```bash
python scripts/check_paper_aliases.py
```

Expected result:

```text
valid: Site paper aliases resolve
```

## Relationship To Manifest Verification

Manifest verification confirms source-preserving metadata exists in `papers/papers_manifest.json`.

Alias verification confirms the public Site paths resolve after the mirror workflow writes the paper display files.

Both checks are required for live activation.

## Live Verification Sequence Update

The Site-side verification sequence should now include:

```text
python scripts/check_paper_display_policy.py
python scripts/check_papers_manifest_metadata.py
python scripts/check_paper_aliases.py
```

## Non-Claims

This document does not activate the mirror by itself.

This document does not replace Publisher as source of truth.

This document does not verify Publisher receipt updates.

This document only adds alias-resolution evidence to the Site-side live verification gate.

## Archive Readiness

This file is sufficient for future sessions to understand how alias verification fits into the Site mirror activation flow without requiring prior chat context.
