# Ecosystem Node Locale-Aware Renderer

## Status

Implemented for the browser-local Ecosystem Node projection.

Supported initial locales:

```text
en
es
zh-Hans
zh-Hant
```

This initial set implements the launch-priority language boundary: English, Spanish, Simplified Chinese, and Traditional Chinese.

## Architectural boundary

Locale selection changes only the human-readable renderer. It does not translate, rewrite, reorder, add, remove, or mutate canonical governed events.

```text
canonical governed event stream
-> locale-aware conversation controls
-> locale-aware governed-record labels
-> unchanged raw JSON / JSONL records
```

The canonical event stream remains authoritative. Human-facing translations are projections. Raw governed output remains machine-readable and preserves original field names and values.

## Persistence

The selected locale is stored under:

```text
stegverse-node-locale
```

The browser preference is restored on the next visit. When no preference exists, the renderer selects Spanish or the appropriate Chinese script from the browser locale and otherwise falls back to English.

## Public API

`window.StegVerseCanonicalEventStream` exposes:

```text
getLocale()
setLocale(locale)
supportedLocales
```

Unsupported locale values are rejected without changing the active renderer.

## Verification requirements

The static Ecosystem Node verifier requires:

```text
SUPPORTED_LOCALES
English / Español / 简体中文 / 繁體中文 selectors
zh-Hans and zh-Hant as distinct locale identifiers
persistent browser preference
setLocale exposure
```

Future browser tests must verify:

1. switching among all four locales;
2. persistence after reload;
3. unchanged canonical event count, order, identifiers, references, hashes, and raw exports after locale changes;
4. accessible labels for the locale control and all view controls;
5. fail-closed handling of unsupported locale identifiers.

## Authority boundary

```text
locale selection != canonical event mutation
translation != evidence alteration
translated label != translated source content
browser preference != identity claim
renderer locale != policy jurisdiction
multilingual projection != admissibility
```
