# MS-011 Release Marker v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
transition-verification-guide.html
transition-release-index.html
transition-milestones.html
transition-development-status.html
transition-release-snapshot.html
transition-table.html
transition-periodic-table.html
data/transition-release-index-v1.json
data/transition-release-snapshot-v1.json
data/transition-verification-bundle-v1.json
```

## What this does

- Marks `MS-011 — Public Verification Bundle` as released.
- Sets the current release to `public_verification_bundle_released`.
- Keeps the automation basis as `receipt_backed_automation_ready`.
- Sets `MS-012 — Independent Replay Packet` as the next pending milestone.

## Done check after upload

```text
transition-verification-guide.html says MS-011 released
transition-milestones.html top milestone = MS-011
transition-release-index.html current release = MS-011
transition-development-status.html current development milestone = MS-011
transition-release-snapshot.html says MS-011 unlocked
MS-012 remains pending
```
