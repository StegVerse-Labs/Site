# StegVerse Site Single Source Plan

## Assumptions

1. All Site pages should read public status from one source.
2. Site is a mirror only and must not become proof authority.
3. The current public `transition-release-index.html` still displays `Loading...`, which means its expected data source is missing, stale, or not aligned with the current Stage 1–31 state.
4. The correct source should be public, static, GitHub Pages-friendly JSON.
5. This bundle should avoid leading-dot paths.

## Done

This bundle is done when the Site repo contains:

```text
data/stegverse-site-state.json
data/formalism-tests-stage-1-to-31-status.json
assets/js/stegverse-site-state.js
assets/css/stegverse-site-state.css
transition-release-index.html
docs/site-single-source-plan.md
reports/site_single_source_alignment_report.json
receipts/site_single_source_alignment_receipts.jsonl
```

## Recommended single source

```text
data/stegverse-site-state.json
```

This should become the one public mirror-state source for pages that need Stage 1–31 status, StegVerse-001 status, transition release state, packet boundary, node/FinCo boundary, and production boundary.

The existing file can remain as a compatibility alias:

```text
data/formalism-tests-stage-1-to-31-status.json
```

But new pages should read:

```text
data/stegverse-site-state.json
```

## Why this source

It is:

```text
static
GitHub Pages-compatible
cacheable
easy to diff
easy to receipt
easy to mirror
easy for every HTML page to consume
```

## Source hash

```text
24715fef019337d262fa73cbb9886dd93e37e9d5d35e55a51d66d58ead3d4acc
```

## Page update rule

Each page should either:

1. Include the shared loader:

```html
<link rel="stylesheet" href="assets/css/stegverse-site-state.css">
<script src="assets/js/stegverse-site-state.js"></script>
```

2. Or link to the canonical Stage 1–31 mirror page:

```html
<a href="formalism-tests-stage-1-to-31.html">Formalism Tests Stage 1–31</a>
```

## Required public boundary language

Every status page should preserve:

```text
Site is a public mirror, not proof authority.
Production means accredited participation, not sovereign authority.
The packet is portable evidence of a proposed governed transition, not installation authority.
An install plan is a candidate transition, not installation authority.
Discovery observes, models, compares, classifies, and proposes. Discovery does not install.
```

## Pages that should be checked next

```text
index.html
formalism-tests-stage-1-to-31.html
transition-release-index.html
transition-proof-surface.html
transition-table.html
verification-guide.html
replay-packet.html
demo.html
Papers.html
```

## Immediate fix included

This bundle includes a full replacement for:

```text
transition-release-index.html
```

That replacement removes the stale `Loading...` dependency and hydrates from:

```text
data/stegverse-site-state.json
```
