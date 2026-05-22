# StegVerse Site Ideal Theme Lock

## Assumptions

1. The screenshot provided by the user is the preferred Site visual identity.
2. Future Site wiring should preserve this dark navy, cyan, aqua, mint, and soft-slate panel scheme.
3. Shared wiring should not accidentally replace the visual identity.
4. This bundle defines the theme source of truth without forcing every page to change immediately.
5. No leading-dot paths are included.

## Done

This bundle is done when the Site repo contains:

```text
data/stegverse-site-theme.json
assets/css/stegverse-ideal-theme.css
docs/site-ideal-theme-lock.md
reports/site_ideal_theme_lock_report.json
receipts/site_ideal_theme_lock_receipts.jsonl
```

## Ideal Theme Summary

The ideal Site color scheme is:

```text
deep navy page background
near-black blue header/background depth
soft slate/navy cards
bright white heading text
muted blue-gray body text
cyan/aqua accent outlines
cyan-to-mint primary action gradient
gold-to-cyan support gradient
dark slate secondary buttons
rounded cards and pill outlines
```

## Theme Rule

```text
Future Site updates should preserve this visual identity unless the user explicitly approves a visual redesign.
```

## Recommended Use

Add the theme CSS globally only if it does not conflict with current page CSS:

```html
<link rel="stylesheet" href="assets/css/stegverse-ideal-theme.css">
```

For color-preserving wiring, prefer using the CSS variables and utility classes without replacing existing page layout.

## Key Tokens

```text
--sv-bg: #071424
--sv-bg-deep: #03101d
--sv-surface: #101d31
--sv-surface-elevated: #13233b
--sv-text: #f3f7ff
--sv-text-muted: #aebbd0
--sv-accent-cyan: #64dff2
--sv-accent-aqua: #6be7f2
--sv-accent-mint: #55f29a
--sv-accent-gold: #ffd86b
--sv-gradient-primary: linear-gradient(135deg, #65dff2 0%, #55f29a 100%)
--sv-gradient-support: linear-gradient(135deg, #ffd86b 0%, #65dff2 100%)
```

## Boundary

This theme lock controls visual consistency only.

It does not control proof authority, production accreditation, node status, FinCo eligibility, or install authority.
