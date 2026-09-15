# MyKV iPhone Installable Surface Mirror Handoff

Repository: `StegVerse-Labs/Site`
Branch: `mykv-ios-installable-webapp-20260915`
Updated: 2026-09-15
Goal Task ID: `KV-ICLOUD-AUTOMATED-UPGRADE-001`
COSV ID: `40000100100000`
State: `SOURCE_IMPLEMENTATION_READY_FOR_VALIDATION / RUNTIME_NOT_INSTALLED`
Authority effect: `NONE`
Activation effect: `false`

## Objective

Make the existing MyKV surface installable as a standalone iPhone web app while preserving the existing DEVICE_KV-first connection path. Installing MyKV must not create, reinstall, replace, renumber, migrate, or otherwise mutate any KnowledgeVault instance.

## Source contract

- `my-kv.webmanifest` defines MyKV app identity, install-shell start URL, same-origin scope, standalone display, theme/background colors, and app icons.
- `my-kv-install.html` is a thin iPhone install shell with iOS standalone metadata and one owner instruction: Share -> Add to Home Screen.
- The install shell redirects to `/my-kv.html?source=installed` only after it is launched in standalone/Home Screen mode.
- Canonical `my-kv.html` remains unchanged by this task, preserving the existing DEVICE_KV-first `Connect / verify KV` path and receipt fallback semantics.
- The install shell contains no DEVICE_KV implementation, Node registration, IndexedDB, localStorage, provider call, or credential handling.
- No service worker is introduced by this task; offline caching is not claimed and stale application-shell persistence is intentionally avoided until a governed cache/update contract exists.

## Runtime boundary

Source merge and public deployment do not prove that MyKV is installed on the owner's iPhone. Authentic runtime completion requires the owner to add the install shell to the iPhone Home Screen, launch MyKV in standalone mode, and observe that canonical MyKV `Connect / verify KV` resolves the existing resident KV without creating or replacing a KV instance.

## Validation

`tests/test_mykv_installable_surface.py` deterministically checks manifest identity/scope/display, iOS metadata, standalone-only redirect behavior, unchanged DEVICE_KV-first canonical MyKV markers, and absence of authority-bearing/storage/provider calls in the install shell. Exact-head repository CI remains required before merge.

## Manual work

None until source is merged and deployed. After deployment the intended owner burden is one iPhone installation action: open `/my-kv-install.html` in Safari and choose Add to Home Screen. Runtime KV binding is verified only after launching installed MyKV and using the existing `Connect / verify KV` control.
