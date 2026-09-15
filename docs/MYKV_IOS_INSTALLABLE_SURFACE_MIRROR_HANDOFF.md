# MyKV iPhone Installable Surface Mirror Handoff

Repository: `StegVerse-Labs/Site`
Updated: 2026-09-15
Goal Task ID: `KV-ICLOUD-AUTOMATED-UPGRADE-001`
COSV ID: `40000100100000`
State: `UNIFIED_MYKV_INSTALL_SOURCE_IMPLEMENTED / VALIDATION_PENDING`
Authority effect: `NONE`
Activation effect: `false`

## Objective

MyKV is the **single owner-facing installation surface** for the current iPhone. Installing and first-launching MyKV automatically establishes or reuses the minimal resident StegOS/Node substrate, runs the canonical resident-health diagnostic, and performs only bounded device-install repair when required before any KV-host choice is exposed.

MyKV remains distinct from the KnowledgeVault itself and from the selected storage host. The unified install flow must not create, reinstall, replace, renumber, migrate, or rehost a KnowledgeVault merely to establish the resident device substrate.

## Canonical owner flow

1. Owner installs MyKV once from the StegVerse-controlled MyKV install surface.
2. First standalone launch loads the canonical Node-continuity loader.
3. That loader brings in the existing StegOS bootstrap implementation, device-local continuity/autostart support, Node-continuity implementation, and resident-health client on the same origin.
4. MyKV diagnoses the resident substrate.
5. When required, MyKV performs only bounded device-side repair through the existing resident-health contract; valid Node identity and visible KV relationship state must be preserved or the flow fails closed.
6. MyKV opens the canonical management page only after resident health is `HEALTHY` and a valid Node is observed.
7. KV storage-host choices are hidden until resident substrate health is acceptable.
8. The owner may then select iCloud Drive, Google Drive, device-local storage, or another supported endpoint without changing KV identity merely because its host differs.

There is no separate owner-facing StegOS website or second StegOS installation step.

## Source contract

- `my-kv.webmanifest` defines the standalone MyKV app identity and describes the automatic resident StegOS/Node bootstrap.
- `my-kv-install.html` is the sole owner-facing install shell.
- In ordinary Safari browsing, the install shell does not automatically mutate device state merely because it was visited.
- On standalone/Home Screen launch, the install shell invokes the resident-health client, repairs only the resident substrate when required, and redirects to canonical `my-kv.html` only after healthy readback.
- `assets/stegverse-node-continuity.js` now loads the existing StegOS bootstrap implementation and device-local autostart before canonical Node continuity and resident health, so MyKV can diagnose/repair the resident substrate in place rather than handing the owner to a separate StegOS bootstrap site.
- `cloud-kv-peers.html` keeps owner-selectable storage-host panels hidden until the same resident-health contract reports `HEALTHY` with a valid registered Node.
- Existing DEVICE_KV, provider, Interlock/InTr, and storage-endpoint request boundaries remain separate from device-substrate bootstrap.

## Identity and authority boundaries

- Resident StegOS/Node is device/runtime substrate, not a KV instance.
- MyKV is the owner-facing install and management surface, not the KV and not its host.
- KV identity is independent of storage endpoint.
- Establishing/repairing resident substrate does not authorize KV creation, migration, rehosting, provider execution, relationship mutation, data movement, replication, or AI-corpus exposure.
- Existing valid Node identity must be reused/preserved.
- No second user-operated device is required.
- Credential authority remains TV/TVC; no GitHub-token runtime authority is introduced.

## Preserved adjacent state

The already-emitted Google Drive KV #2 request `SITE-CLOUD-KV-4347408852127319cbda574f02e03edb` remains unchanged. The unified MyKV flow must not regenerate, replace, rename, reauthorize, or otherwise disturb it.

## Runtime boundary

Source and CI can prove the unified install contract exists; they cannot prove the owner has installed MyKV on the physical iPhone, that iOS retained the standalone web app/service worker/IndexedDB state, or that a live Node/KV relationship has been observed. Those remain owner-observed runtime predicates.
