# Site Papers Mirror Bundle

## Purpose

This document describes the Site paper mirror for `StegVerse-Labs/Site`.

The mirror exists so Site can display current public paper outputs from Publisher without becoming a separate editorial source of truth.

For the governing display policy, see:

```text
docs/SITE_PAPER_DISPLAY_POLICY.md
```

For Site-side activation state, see:

```text
docs/SITE_MIRROR_ACTIVATION_STATUS.md
```

## Source Repository

The source repo is:

```text
GCAT-BCAT-Engine/Publisher
```

The source folder is:

```text
papers/
```

The target mirrored directory is:

```text
papers/
```

The primary public index page is:

```text
Papers.html
```

The mirror also maintains these aliases:

```text
papers.html
papers/index.html
publisher/papers.html
publisher/papers/index.html
```

## Source Metadata Contract

The mirror writes a machine-readable manifest at:

```text
papers/papers_manifest.json
```

The manifest must preserve:

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

The manifest is validated by:

```text
scripts/check_papers_manifest_metadata.py
```

That checker runs after `scripts/mirror_papers.py` and before the workflow commits mirrored files.

## Done Condition

The mirror is working when the Site repo contains:

```text
scripts/mirror_papers.py
scripts/check_papers_manifest_metadata.py
Papers.html
papers.html
papers/index.html
papers/papers_manifest.json
publisher/papers.html
publisher/papers/index.html
github/workflows/mirror-papers.yml
```

and the workflow:

```text
Mirror Papers from Publisher
```

runs green, validates manifest metadata, and commits any changed paper files back to the Site repo.

## Policy Boundary

Publisher remains the source of truth for paper publication state.

Site may display mirrored papers, generated indexes, and summaries, but it should not strengthen or reinterpret Publisher record status.

Site should not treat mirrored content as a separate Site-authored publication record.

## How It Works

```text
Checkout Site
Resolve source repository and source ref
Checkout Publisher into _source
Verify _source/papers exists
Copy _source/papers into Site/papers
Generate Papers.html
Generate papers.html redirect
Generate papers/index.html
Generate publisher/papers.html redirect
Generate publisher/papers/index.html redirect
Generate papers/papers_manifest.json
Validate papers/papers_manifest.json metadata
Commit changes back to Site
```

## Update Protocol

Use this order when updating the current public paper display:

```text
1. Update Publisher source record.
2. Validate Publisher source record.
3. Run or dispatch the Site mirror workflow.
4. Confirm mirrored files update under papers/.
5. Confirm Papers.html and papers/index.html update.
6. Confirm papers/papers_manifest.json preserves source_repository, source_ref, source_path, and source_of_truth.
7. Confirm aliases resolve.
8. Commit or accept the workflow commit.
```

## iOS Workflow Note

The workflow is shown here without its leading dot:

```text
github/workflows/mirror-papers.yml
```

In GitHub, it is stored at:

```text
.github/workflows/mirror-papers.yml
```

## Important Notes

This mirror runs on a schedule or manually from the Site repo.

A push to `GCAT-BCAT-Engine/Publisher` does not automatically trigger the Site workflow unless a dispatch workflow is added in the source repo later.

The workflow summary should identify:

```text
Source repository
Source ref
Source path
Target path
Public index
Aliases
Mirrored file count
```
