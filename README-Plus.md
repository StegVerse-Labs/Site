# MS-010 Public Navigation Integration v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
transition-table.html
transition-periodic-table.html
transition-milestones.html
transition-development-status.html
transition-release-snapshot.html
transition-release-index.html
data/transition-release-index-v1.json
data/transition-release-snapshot-v1.json
```

Keeps existing tool files from the previous bundle:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What changed

- Primary research pages now link to:
  - Milestones
  - Development Status
  - Release Snapshot
  - Release Index
- MS-010 is now unlocked and appears at the top of the milestone page.
- MS-011 is now the next pending milestone.

## Expected public URLs

```text
https://stegverse-labs.github.io/Site/transition-table.html
https://stegverse-labs.github.io/Site/transition-periodic-table.html
https://stegverse-labs.github.io/Site/transition-milestones.html
https://stegverse-labs.github.io/Site/transition-release-index.html
```
