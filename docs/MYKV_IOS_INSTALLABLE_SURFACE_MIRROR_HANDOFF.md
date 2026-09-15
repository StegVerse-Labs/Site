# MyKV iPhone Installable Surface Mirror Handoff

Repository: `StegVerse-Labs/Site`
Branch: `mykv-ios-installable-webapp-20260915`
Updated: 2026-09-15
Goal Task ID: `KV-ICLOUD-AUTOMATED-UPGRADE-001`
COSV ID: `40000100100000`
State: `SOURCE_IMPLEMENTATION_IN_PROGRESS / RUNTIME_NOT_INSTALLED`
Authority effect: `NONE`
Activation effect: `false`

## Objective

Make the existing MyKV surface installable as a standalone iPhone web app while preserving the existing DEVICE_KV-first connection path. Installing MyKV must not create, reinstall, replace, renumber, migrate, or otherwise mutate any KnowledgeVault instance.

## Source contract

- `my-kv.webmanifest` defines MyKV app identity, start URL, scope, standalone display, theme/background colors, and app icons.
- `my-kv.html` declares the web-app manifest and iOS standalone metadata.
- `assets/my-kv-install.js` detects browser vs standalone presentation only. It has no KV authority, persistence authority, provider authority, or Node authority.
- The existing MyKV `Connect / verify KV` flow remains DEVICE_KV-first and retains the canonical receipt fallback only when live resident verification is unavailable.
- No service worker is introduced by this task; offline caching is not claimed and stale application-shell persistence is intentionally avoided until a governed cache/update contract exists.

## Runtime boundary

Source merge and public deployment do not prove that MyKV is installed on the owner's iPhone. Authentic runtime completion requires the owner to add MyKV to the iPhone Home Screen, launch it in standalone mode, and observe that `Connect / verify KV` resolves the existing resident KV without creating or replacing a KV instance.

## Validation

Pending exact-head repository validation.

## Manual work

None until source is merged and deployed. After deployment the intended owner burden is one iPhone installation action: open MyKV in Safari and choose Add to Home Screen.
