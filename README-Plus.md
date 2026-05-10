# MS-009 Release Snapshot v1

Upload-safe bundle. No leading-dot paths.

Adds:

```text
transition-release-snapshot.html
data/transition-release-snapshot-v1.json
```

Replaces:

```text
transition-milestones.html
transition-development-status.html
```

Keeps existing tool files from the previous bundle:

```text
tools/transition_experimental_orchestrator.py
tools/build_transition_pages.py
```

## What changed

- MS-009 is now unlocked and appears at the top of the milestone page.
- MS-008 and all previous milestones remain below it.
- A release snapshot page exists.
- A release snapshot JSON exists.
- Development status links to the release snapshot.

## Expected public URLs

```text
https://stegverse-labs.github.io/Site/transition-release-snapshot.html
https://stegverse-labs.github.io/Site/data/transition-release-snapshot-v1.json
https://stegverse-labs.github.io/Site/transition-milestones.html
https://stegverse-labs.github.io/Site/transition-development-status.html
```
