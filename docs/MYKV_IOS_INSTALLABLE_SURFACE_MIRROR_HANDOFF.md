# MyKV iPhone Installable Surface Mirror Handoff

Repository: `StegVerse-Labs/Site`
Branch: `mykv-ios-installable-webapp-20260915`
Updated: 2026-09-15
Goal Task ID: `KV-ICLOUD-AUTOMATED-UPGRADE-001`
COSV ID: `40000100100000`
State: `SOURCE_VALIDATED / MERGE_PENDING / RUNTIME_NOT_INSTALLED`
Authority effect: `NONE`
Activation effect: `false`

## Objective

Make the existing MyKV surface installable as a standalone iPhone web app while preserving the existing DEVICE_KV-first connection path. Installing MyKV must not create, reinstall, replace, renumber, migrate, or otherwise mutate any KnowledgeVault instance.

## Source contract

- `my-kv.webmanifest` defines MyKV app identity, install-shell start URL, same-origin scope, standalone display, theme/background colors, and PNG app icons.
- `my-kv-install.html` is a thin iPhone install shell with iOS standalone metadata and one owner instruction: Share -> Add to Home Screen.
- The install shell redirects to `/my-kv.html?source=installed` only after it is launched in standalone/Home Screen mode.
- Canonical `my-kv.html` remains unchanged by this task, preserving the existing DEVICE_KV-first `Connect / verify KV` path and receipt fallback semantics.
- The install shell contains no DEVICE_KV implementation, Node registration, IndexedDB, localStorage, provider call, or credential handling.
- No service worker is introduced by this task; offline caching is not claimed and stale application-shell persistence is intentionally avoided until a governed cache/update contract exists.
- Root `README.md` documents this install surface and its non-authorizing/runtime-unproven boundary.

## Exact-head validation evidence

Validated pre-merge source head: `dcd040943a784fac144a484106b7e8d4024fa237`.

All workflows observed for that exact head completed successfully, including:

- Site Node Continuity `34984599234` — PASS; includes `python -m unittest -v tests.test_mykv_installable_surface`.
- Site Bootstrap Validate - No Non-TV/TVC Credential Authority `34984599113` — PASS.
- Site Handoff Orchestrator `34984599118` — PASS.
- Ecosystem Heartbeat Orchestration `34984599119` — PASS.
- Node IndexedDB Schema Migration `34984599324` — PASS.
- No Required Third-Party Runtime `34984599067` — PASS.
- StegSocials Post Preparation `34984599106` — PASS.
- Validate StegOS Persistent Card UX `34984599038` — PASS.
- Verify NVIDIA Hugging Face publication `34984599098` — PASS.
- Ecosystem Visual Render Transport Validate - No Credential Authority `34984599156` — PASS.
- CFP Current-Season Ingestion `34984599346` — PASS.
- Validate ERL KV Provider Proof Projection `34984599006` — PASS.

The dedicated install test deterministically verifies manifest identity/scope/display, PNG icons, iOS metadata, standalone-only redirect behavior, unchanged DEVICE_KV-first canonical MyKV markers, and absence of authority-bearing/storage/provider calls in the install shell.

## Runtime boundary

Source validation, merge, and public deployment do not prove that MyKV is installed on the owner's iPhone. Authentic runtime completion requires the owner to add the install shell to the iPhone Home Screen, launch MyKV in standalone mode, and observe that canonical MyKV `Connect / verify KV` resolves the existing resident KV without creating or replacing a KV instance.

The already-emitted Google Drive KV #2 request `SITE-CLOUD-KV-4347408852127319cbda574f02e03edb` is not modified, re-emitted, renamed, or replaced by this work.

## Manual work

None before merge/deployment. After deployment the intended owner burden is one installation sequence on the current iPhone: open `/my-kv-install.html` in Safari, Share -> Add to Home Screen -> Add, launch MyKV, then tap `Connect / verify KV` once. If DEVICE_KV cannot verify the resident KV and the receipt fallback appears, stop rather than creating or replacing any KV.
