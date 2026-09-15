# Resident StegOS Device Health and Bounded Repair Mirror Handoff

Repository: `StegVerse-Labs/Site`
Goal Task ID: `KV-ICLOUD-AUTOMATED-UPGRADE-001`
COSV ID: `40000100100000`
Updated: 2026-09-15
State: `SOURCE_MERGED_VALIDATED / UNIFIED_MYKV_OWNER_INSTALL_PENDING`
Authority effect: `NONE`
Activation effect: `false`

## Objective

Provide one canonical resident StegOS device-health and bounded-repair client underneath MyKV. StegOS remains the minimal resident device/runtime substrate, but it is no longer a separate owner-facing installation destination. MyKV is the sole owner-facing install/launch surface and automatically loads the existing StegOS bootstrap, device-continuity, Node-continuity, and resident-health components on the same origin.

The resident StegOS/Node remains after a KV is installed or adopted on an owner-selected storage host. It is not a second KV and does not duplicate owner data.

## Source implementation

- `assets/stegos-resident-health.js` remains the canonical read-only diagnostic and bounded-repair client.
- `assets/stegverse-node-continuity.js` loads, in parser order, the existing StegOS schema compatibility layer, StegOS bootstrap implementation, device-local autostart/continuity layer, Node-continuity implementation, and resident-health client.
- `my-kv-install.html` invokes diagnosis and bounded repair automatically only after standalone/Home Screen launch, then opens canonical MyKV only when health is acceptable.
- `cloud-kv-peers.html` hides owner-selectable KV-host panels until the same resident-health contract reports `HEALTHY` and a registered Node is observed.

## Bounded repair contract

Repair remains limited to device-install infrastructure:

1. retain the pre-repair valid Node ID when one exists;
2. refresh or register the canonical same-origin StegOS service-worker shell through the existing bootstrap API;
3. establish a Node only when no valid Node exists;
4. re-diagnose and fail closed if a valid Node ID changes;
5. fail closed if already-visible KV relationship state changes during repair;
6. never create, replace, renumber, migrate, rehost, connect, sync, or expose a KV merely to repair resident device substrate.

Because MyKV loads the bootstrap implementation directly through the canonical Node-continuity loader, the owner is not required to visit a separate StegOS bootstrap site for normal installation or repair.

## Authority and identity boundaries

- Health checks remain observational and non-authorizing.
- Device-substrate repair does not grant provider, KV, relationship, governance, credential, or execution authority.
- Interlock/InTr remains the authority boundary for state-changing governed KV transitions.
- MyKV is the single owner-facing install surface; StegOS is the underlying resident substrate.
- KV identity remains separate from its storage endpoint.
- No second user-operated device is required.

## Merge evidence

The shared resident-health client originally merged through Site #1351 at `3c78c5da968ae746ddaedfe6c68c3a148fc56f0c`, with documentation reconciliation through #1352 and claim retirement through #1353.

The unified MyKV integration merged through Site #1355. Final validated source head: `2aae799336464b290b230074992b2bf3899523d2`. Merge commit: `0d5df579e98ae44ad2f4358dd89efaae5d9809ed`. All 13 workflows observed at that final head completed successfully.

## Preserved adjacent state

The pending Google Drive KV #2 request `SITE-CLOUD-KV-4347408852127319cbda574f02e03edb` remains unchanged and must not be re-emitted or replaced by this integration.

## Runtime completion boundary

Runtime proof is now one owner-facing sequence: install MyKV, launch MyKV once, observe resident StegOS/Node health and continuity, then proceed to KV-host selection only after the substrate is healthy. No separate StegOS owner installation is part of the runtime contract. Source/CI/merge do not prove that physical current-iPhone sequence has occurred.
