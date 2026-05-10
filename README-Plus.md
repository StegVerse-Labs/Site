# Page Contract MS-012 Stabilized Fix v1

Upload-safe bundle. No leading-dot paths.

Replaces:

```text
tools/page_contract_check.py
data/page-contracts-v1.json
```

## What changed

The contract is now split correctly:

```text
Site-wide homepage checks:
- index.html

Transition release checks:
- transition-periodic-table.html
- transition-table.html
- transition-milestones.html
- transition-development-status.html
- transition-release-snapshot.html
- transition-release-index.html
- transition-verification-guide.html
- transition-replay-packet.html
```

The checker now tolerates:

```text
spaces
hyphens
underscores
line breaks
visual heading joins
```

The JSON checks remain strict.

## Important

If the Release Index still does not list:

```text
Replay Packet v1
data/transition-replay-packet-v1.json
```

the workflow should still fail. That is a real page-state failure, not a checker failure.

## Done check

Run:

```text
Actions → Page Contract Check → Run workflow
```

If it fails, use the uploaded artifact:

```text
page-contract-report.md
```
