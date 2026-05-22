# Site Global Wiring Plan

## Assumptions

1. The remaining Site pages should be wired together.
2. Status/proof/release information should come from one public source.
3. Navigation should come from one public navigation source.
4. Site must remain a public mirror, not proof authority.
5. This bundle starts by wiring `index.html` and providing the shared shell that other pages can adopt.

## Done

This bundle is done when the Site repo contains:

```text
index.html
data/stegverse-site-state.json
data/stegverse-site-navigation.json
assets/js/stegverse-site-shell.js
assets/css/stegverse-site-shell.css
docs/site-global-wiring-plan.md
reports/site_global_wiring_report.json
receipts/site_global_wiring_receipts.jsonl
```

## Single Sources

Status source:

```text
data/stegverse-site-state.json
```

Navigation source:

```text
data/stegverse-site-navigation.json
```

## Why wire the whole Site

The current public home page is live and presents the right high-level StegVerse message, including execution-layer risk, demo links, FinCo, support, product, methodology, and about pages. It does not yet appear to be wired into the Stage 1–31 proof source or shared navigation state.

The rest of the Site should be wired so every page can expose:

```text
current roadmap status
proof authority boundary
Site mirror boundary
Stage 1–31 public mirror link
transition release link
production boundary
packet boundary
install-plan boundary
node / FinCo boundary
```

## Page Wiring Pattern

Every HTML page should include:

```html
<link rel="stylesheet" href="assets/css/stegverse-site-shell.css">
<script src="assets/js/stegverse-site-shell.js"></script>
```

Every page should include a shared navigation target:

```html
<nav class="sv-nav" data-sv-global-nav></nav>
```

Every page that displays proof state should use:

```html
<span data-sv-roadmap-status></span>
<span data-sv-work-entity></span>
<span data-sv-proof-authority></span>
<span data-sv-site-role></span>
```

## Pages to update next

```text
demo.html
formalism-tests-stage-1-to-31.html
transition-proof-surface.html
transition-table.html
verification-guide.html
replay-packet.html
stegfinco.html
support.html
product.html
pricing.html
methodology.html
guarantees.html
about.html
Papers.html
```

## Boundary Rule

```text
Site reads shared state.
Site mirrors shared state.
Site does not become proof authority.
```

## Source hashes

```text
site_state_sha256: cf530f5807d7329aa630deaabc2c59fed8279de0d65b6401d12e324263b5ffee
navigation_sha256: 5b74b5e205b1f048bebf0bca508fe5b8f9cd191f38098ef1ec89418ab2661727
```
