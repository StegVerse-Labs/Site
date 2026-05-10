# Transition Milestones Mobile Layout Fix v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
transition-milestones.html
```

## What changed

- Prevents long automation state strings from overflowing on mobile.
- Displays `receipt_backed_automation_ready` as `receipt backed automation ready`.
- Preserves the raw state in the HTML title attribute.
- Adds wrapping protection to stat cards and milestone metadata.
- Keeps newest milestone first and preserves all formal milestone labels.

Expected public URL:

```text
https://stegverse-labs.github.io/Site/transition-milestones.html
```
