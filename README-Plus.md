# MS-010 Metadata Consistency Fix v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
transition-milestones.html
transition-release-index.html
transition-release-snapshot.html
data/transition-release-index-v1.json
data/transition-release-snapshot-v1.json
```

## What this fixes

- `transition-milestones.html` top milestone is now:
  `MS-010 — Public Navigation Integration`
- `transition-release-index.html` current release is now:
  `MS-010 — Public Navigation Integration`
- `data/transition-release-index-v1.json` current release points to MS-010.
- `data/transition-release-snapshot-v1.json` formal milestone points to MS-010.
- `MS-011 — Public Verification Bundle` remains pending.

## Done check

After upload, these should be true:

```text
transition-milestones.html top card = MS-010
transition-release-index.html current release = MS-010
transition-release-snapshot.html says MS-010 unlocked
```
