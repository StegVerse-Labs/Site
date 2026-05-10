# Transition Page Contract Checker v1

Upload-safe bundle.

This adds an automated public-page checker for the Transition Periodic Table site.

## Files

```text
tools/page_contract_check.py
data/page-contracts-v1.json
github/workflows/page-contract-check.yml
```

Note: `github/workflows/page-contract-check.yml` is displayed without the leading dot here. The bundle preserves the correct `.github/workflows/page-contract-check.yml` path for GitHub.

## What this checks

The checker verifies:

```text
transition-periodic-table.html
transition-table.html
transition-milestones.html
transition-development-status.html
transition-release-snapshot.html
transition-release-index.html
transition-verification-guide.html
transition-replay-packet.html
```

It also verifies:

```text
data/transition-release-index-v1.json
data/transition-release-snapshot-v1.json
data/transition-verification-bundle-v1.json
data/transition-replay-packet-v1.json
```

## What the workflow produces

The workflow uploads:

```text
page-contract-report.json
page-contract-report.md
```

## Manual run

After upload:

1. Open GitHub Actions.
2. Select `Page Contract Check`.
3. Run workflow.
4. Download `page-contract-report`.

## Done condition

The workflow passes only if the required pages, JSON files, nav links, milestone markers, and replay packet entries are visible on the public site.
