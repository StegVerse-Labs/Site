# Site Color-Preserving Bulk Wiring

## Assumptions

1. The existing Site color scheme should be preserved.
2. All major pages should be wired to the same shared state and navigation sources.
3. The shared wiring should be additive and idempotent.
4. The script should not replace full HTML files.
5. The script should not set body colors, body backgrounds, font families, or theme variables.
6. No leading-dot paths are included.

## Done

This bundle is done when the Site repo contains:

```text
data/stegverse-site-state.json
data/stegverse-site-navigation.json
data/site-color-preserving-wiring-targets.json
assets/js/stegverse-color-preserving-wiring.js
assets/css/stegverse-color-preserving-wiring.css
tools/wire_site_pages_color_preserving.py
tools/tasks/site_color_preserving_wiring_tasks.json
docs/site-color-preserving-bulk-wiring.md
reports/site_color_preserving_bulk_wiring_report.json
receipts/site_color_preserving_bulk_wiring_receipts.jsonl
```

and the declared task succeeds:

```bash
python tools/run_declared_tasks.py tools/tasks/site_color_preserving_wiring_tasks.json --task-id site_color_preserving_bulk_wiring
```

## Task ID

```text
site_color_preserving_bulk_wiring
```

## What this does

The script updates each target HTML page by adding, only if missing:

```html
<link rel="stylesheet" href="assets/css/stegverse-color-preserving-wiring.css">
<div data-sv-status-mount></div>
<script src="assets/js/stegverse-color-preserving-wiring.js"></script>
```

## What this does not do

It does not replace the page content.

It does not set:

```text
body background
body color
font family
theme variables
panel colors
button colors
global layout colors
```

## Target pages

```text
index.html
demo.html
formalism-tests-stage-1-to-31.html
transition-release-index.html
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

## Shared sources

```text
data/stegverse-site-state.json
data/stegverse-site-navigation.json
```

## Boundary

```text
Site reads shared state.
Site mirrors shared state.
Site does not become proof authority.
```
