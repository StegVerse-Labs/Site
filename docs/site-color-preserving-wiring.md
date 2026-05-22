# Site Color-Preserving Wiring Bundle

## Assumptions

1. The live `index.html` already has the preferred Site visual identity.
2. The previous global wiring bundle introduced a new shell palette and should not be used as a full visual replacement if exact visual continuity matters.
3. This bundle preserves the current color scheme by avoiding page-level color, font, background, and body styling.
4. This bundle wires pages to shared state and navigation without forcing a new visual theme.
5. No leading-dot paths are included.

## Done

This bundle is done when the Site repo contains:

```text
data/stegverse-site-state.json
data/stegverse-site-navigation.json
assets/js/stegverse-color-preserving-wiring.js
assets/css/stegverse-color-preserving-wiring.css
docs/site-color-preserving-wiring.md
docs/index-color-preserving-wiring-snippet.html
reports/site_color_preserving_wiring_report.json
receipts/site_color_preserving_wiring_receipts.jsonl
```

## What this changes

It adds a shared state source:

```text
data/stegverse-site-state.json
```

It adds a shared navigation source:

```text
data/stegverse-site-navigation.json
```

It adds lightweight CSS and JavaScript that use the existing page theme.

## What this does not change

It does not replace the live `index.html`.

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

## How to wire `index.html`

Add this in the existing `<head>`:

```html
<link rel="stylesheet" href="assets/css/stegverse-color-preserving-wiring.css">
```

Add this where the Stage 1–31 proof status should appear:

```html
<div data-sv-status-mount></div>
```

Optionally replace or supplement a navigation area with:

```html
<nav data-sv-global-nav aria-label="StegVerse navigation"></nav>
```

Add this before `</body>`:

```html
<script src="assets/js/stegverse-color-preserving-wiring.js"></script>
```

## Site rule

```text
Site reads shared state.
Site mirrors shared state.
Site does not become proof authority.
```

## Source hashes

```text
site_state_sha256: 223166db80f59e1942e25741feae88eddbb42fd45abf26f7c5ef58333703aa66
navigation_sha256: 2938d14f4d8a0c2c12dae032d8605219d501dcc8d0b8098e94e402ceeadb9ab0
```
