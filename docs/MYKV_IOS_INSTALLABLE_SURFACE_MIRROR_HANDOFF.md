# MyKV iPhone Installable Surface Mirror Handoff

Repository: `StegVerse-Labs/Site`
Branch: `mykv-ios-installable-webapp-20260915`
Updated: 2026-09-15
Goal Task ID: `KV-ICLOUD-AUTOMATED-UPGRADE-001`
COSV ID: `40000100100000`
State: `SOURCE_MERGED_VALIDATED / RUNTIME_OWNER_INSTALL_PENDING`
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

## Merge and exact-head validation evidence

Implementation PR: `StegVerse-Labs/Site#1348`.

Final implementation head: `d814a7ebe3d268b35f5679eb4e6e666ec4d6086d`.
Merge commit: `27622f03e7f2683ee6598c67e261f424052242bf`.

All observed final-head workflows completed successfully, including:

- Site Node Continuity `34984740764` — PASS; includes `python -m unittest -v tests.test_mykv_installable_surface`.
- Site Bootstrap Validate - No Non-TV/TVC Credential Authority `34984740516` — PASS.
- Site Handoff Orchestrator `34984740758` and metadata-triggered duplicate `34984797271` — PASS.
- Ecosystem Heartbeat Orchestration `34984740785` — PASS.
- Node IndexedDB Schema Migration `34984740693` — PASS.
- No Required Third-Party Runtime `34984740776` — PASS.
- StegSocials Post Preparation `34984740713` — PASS.
- Validate StegOS Persistent Card UX `34984740568` — PASS.
- Verify NVIDIA Hugging Face publication `34984740586` — PASS.
- Ecosystem Visual Render Transport Validate - No Credential Authority `34984740531` — PASS.
- CFP Current-Season Ingestion `34984740615` — PASS.
- Validate ERL KV Provider Proof Projection `34984740514` — PASS.

The dedicated install test deterministically verifies manifest identity/scope/display, PNG icons, iOS metadata, standalone-only redirect behavior, unchanged DEVICE_KV-first canonical MyKV markers, and absence of authority-bearing/storage/provider calls in the install shell.

## Runtime boundary

Source validation and merge do not prove that MyKV is installed on the owner's iPhone. Authentic runtime completion requires the owner to add the install shell to the current iPhone Home Screen, launch MyKV in standalone mode, and observe that canonical MyKV `Connect / verify KV` resolves the existing resident KV without creating or replacing a KV instance.

The already-emitted Google Drive KV #2 request `SITE-CLOUD-KV-4347408852127319cbda574f02e03edb` is not modified, re-emitted, renamed, or replaced by this work.

## Manual work

One installation sequence remains on the current iPhone after public propagation: open `https://stegverse.org/my-kv-install.html` in Safari, Share -> Add to Home Screen -> Add, launch MyKV, then tap `Connect / verify KV` once. If DEVICE_KV cannot verify the resident KV and the receipt fallback appears, stop rather than creating or replacing any KV.
