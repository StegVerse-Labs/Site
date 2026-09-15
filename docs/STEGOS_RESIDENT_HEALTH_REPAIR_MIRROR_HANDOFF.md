# Resident StegOS Device Health and Bounded Repair Mirror Handoff

Repository: `StegVerse-Labs/Site`
Goal Task ID: `KV-ICLOUD-AUTOMATED-UPGRADE-001`
COSV ID: `40000100100000`
Updated: 2026-09-15
State: `SOURCE_MERGED_VALIDATED / RUNTIME_OWNER_INSTALL_PENDING`
Authority effect: `NONE`
Activation effect: `false`

## Objective

Provide one canonical resident StegOS device-health and bounded-repair client that runs automatically whenever a page loads the StegOS bootstrap or canonical Node-continuity loader. This covers the StegOS bootstrap surface and MyKV without making MyKV the KV, the storage host, or the required device substrate.

The minimal resident StegOS/Node infrastructure remains on the current device after a KV is installed or adopted on an owner-selected storage host. Storage host selection remains independent of KV identity; iCloud Drive, Google Drive, device-local storage, and other admitted endpoints remain host classes rather than identity classes.

## Source implementation

- `assets/stegos-resident-health.js`
  - exposes `window.StegOSResidentHealth`;
  - automatically runs a read-only diagnosis on `DOMContentLoaded`;
  - renders one resident-health card when the page has a body;
  - reports local runtime readiness, Node identity/registration state, device-continuity visibility, schema-loader compatibility, StegOS service-worker state/freshness, governed transition-surface availability, and only already-visible KV relationship state;
  - does not emit DEVICE_KV queries, provider operations, or KV mutation requests during diagnosis;
  - exposes repair only when diagnosis reports `REPAIR_REQUIRED`.
- `assets/stegverse-node-continuity.js`
  - loads the shared resident-health client after the canonical Node-continuity implementation, making MyKV and other Node-continuity surfaces run the same client automatically.
- `stegos-bootstrap/stegos-bootstrap.js`
  - loads the same client after `stegos-bootstrap-impl.js`, making the StegOS bootstrap run the same health contract automatically.

## Bounded repair contract

Repair is explicitly owner-invoked and is limited to device-install infrastructure:

1. retain the pre-repair valid Node ID when one exists;
2. refresh or register the canonical same-origin StegOS service-worker shell through the existing StegOS bootstrap API;
3. call `establishNode()` only when no valid Node was observed and only when the StegOS bootstrap API is already present;
4. when MyKV lacks the StegOS bootstrap API, return a same-origin handoff to `/stegos-bootstrap/index.html?resident_repair=1` rather than registering a replacement Node from MyKV;
5. re-diagnose and fail closed if an existing valid Node ID changed;
6. fail closed if already-visible KV relationship state changed during repair.

The resident-health client contains no KV creation, replacement, renumbering, migration, rehosting, provider-operation, DEVICE_KV materialization, or credential-authority path.

## Merge and exact-head validation evidence

Implementation PR: `StegVerse-Labs/Site#1351`.

Final validated implementation head: `803e93da7d57f4eb3c4ee67836a8775b147519df`.
Merge commit: `3c78c5da968ae746ddaedfe6c68c3a148fc56f0c`.

All observed exact-head pull-request workflows completed successfully before merge:

- Site Node Continuity `34989541856` — PASS; includes `tests.test_stegos_resident_health` and JavaScript syntax checks for the shared client/loaders.
- Site Handoff Orchestrator `34989541896` — PASS.
- Ecosystem Heartbeat Orchestration `34989541954` — PASS.
- Site Bootstrap Validate - No Non-TV/TVC Credential Authority `34989541857` — PASS.
- Node IndexedDB Schema Migration `34989541865` — PASS.
- Validate StegOS Persistent Card UX `34989542015` — PASS.

An earlier branch head failed only because the new implementation claim omitted repository-required field `next_task_after_release`; the claim contract was repaired without changing the resident-health architecture.

## Current limitations

- The browser cannot claim hardware-level residence or hardware attestation; the resident substrate here is the same-origin iPhone web-app/service-worker/IndexedDB continuity surface already used by StegOS.
- MyKV diagnosis deliberately does not issue a DEVICE_KV query merely to enrich the health card. It reports only relationship state already visible on the current page. A governed KV query remains a separate operation.
- Source/CI/merge cannot prove that the owner has installed StegOS on the physical iPhone or that iOS retained the web-app/service-worker state; those are runtime predicates.
- Root `README.md` still requires explicit documentation reconciliation. That omission does not change the merged source contract and is not treated as runtime evidence.

## Runtime completion boundary

After merge and public propagation, runtime proof requires an owner-observed current-iPhone sequence:

1. open the deployed StegOS bootstrap route in Safari;
2. add StegOS to the Home Screen;
3. launch StegOS and observe resident health;
4. verify the existing Node is reused or, only when genuinely absent, establish the device Node once;
5. select the KV storage host separately;
6. install/adopt and verify the KV on that selected host;
7. confirm later StegOS and MyKV visits report resident health without silently changing Node or KV identity.

The pending Google Drive KV #2 request `SITE-CLOUD-KV-4347408852127319cbda574f02e03edb` is unchanged by this work.
