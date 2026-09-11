# Site Node IndexedDB Schema Migration Mirror Handoff

Goal Task ID: `SITE-NODE-IDB-SCHEMA-MIGRATION-001`
Parent Goal Task ID: `SS-EVIDENCE-COMPARISON-001`
COSV: `40000100100000`
Status: `ACTIVE / CLAIMED_INTEGRATION`
Canonical registry merge: `StegVerse-Labs/.github@7e36449d287f77f7502cffaddf8fac69d50eeea3`
Source incident: `StegVerse-Labs/Site#1233`
Source PR: `StegVerse-Labs/Site#1235`

## Authentic trigger

The current iPhone produced `Failed to execute 'transaction' on 'IDBDatabase': One of the specified object stores was not found.` while the registered-Node resident action remained available. This is evidence of an IndexedDB schema/readback defect, not ERL admission success.

## Repair contract

- Preserve the existing `stegos-node-v1` database, Node registration, and Receipt #1; do not delete/recreate browser storage.
- Canonical Node DB store set is `meta`, `receipts`, `intr_outbox` at version 3.
- Repair authentic legacy v1 (`meta` + `receipts`) and malformed v2 (`meta` + `receipts`, missing `intr_outbox`) through an additive version migration.
- Align every Site runtime entrypoint so canonical migration occurs before any shared-DB opener; lower fixed-version helper opens must not strand or reject an already-migrated database.
- Preserve prior source contracts rather than weakening their validators to accommodate wrapper files.
- Maintain `README.md` with the migration boundary and nonclaims before merge.
- After merge, verify live source propagation before asking for exactly one current-iPhone ERL retry.

## Implemented source

`assets/stegos-node-idb-schema-compat.js` owns the additive compatibility migration. It raises Node DB opens to canonical v3 and creates only missing canonical stores; it does not delete the database, delete a store, replace registration, or replace Receipt #1.

Static parser-time first openers now use fail-closed bootstrap wrappers. Each wrapper requires parser loading, synchronously loads the canonical compatibility layer, then loads the byte-preserved prior implementation from a `*-impl.js` path:

- `assets/stegverse-node-continuity.js` -> `assets/stegverse-node-continuity-impl.js`
- `stegos-node/stegos-node.js` -> `stegos-node/stegos-node-impl.js`
- `stegos-bootstrap/stegos-bootstrap.js` -> `stegos-bootstrap/stegos-bootstrap-impl.js`
- `stegos-bootstrap/sv001-native-resident-activation.js` -> `stegos-bootstrap/sv001-native-resident-activation-impl.js`

`stegos-node/services.js` is natively aligned to version 3 and the complete `meta`, `receipts`, `intr_outbox` store set. DEVICE_KV and HIL helper openers may follow a migration-safe first opener because the installed compatibility layer raises their lower requested version to the canonical version.

The exhaustive validator `scripts/check_stegos_node_idb_entrypoint_alignment.py` checks wrapper integrity and every repository HTML entrypoint containing a shared Node DB opener. Current validation reports 28 discovered runtime entrypoints with a migration-safe wrapper/native opener first.

Legacy semantic validators remain intact as preserved `*_impl.py` sources and their public validator paths redirect only the inspected implementation path where a bootstrap wrapper replaced the former source file. This preserves the existing Node projection, HIL sync, Master Records governance, bootstrap projection, and Node continuity assertions rather than deleting or relaxing them.

## Validation evidence

Historical repair commits include:

- `104d62dc32c9d5c05d93cfb43a768cc9b7cac10c` — initial additive v3 migration on the authentic My KV / ERL path plus deterministic v1/v2/v3 regression coverage.
- `639d8fd497b58e7d74758f45409cc83efb1b32b1` — DEVICE_KV validator reconciliation.
- `2d91f109f7a5b9d707be9a1dc0f16eb237a5c2cc` — exact Site pre-work claim.
- `cf9a0efacad6d1e9e1ab8da44b533083e3c8f9c1` — `stegos-node/services.js` canonical v3/full-store alignment.
- `370ab22a9e5a7e6371004569f65c7efc61458bd4` / `bc29d0c3da5f5c851608a040aad61ee5b0172b8a` — exhaustive runtime-entry alignment gate and focused-workflow integration.
- `15089c753a8ccd87ff9730740c71e7cacd0e4c69` — canonical first-opener bootstrap wrappers with byte-preserved implementations.
- `b979443679a1c2f6a9e026aabaebc783cf9cbcab` — Node continuity validator updated to inspect the preserved implementation while separately checking the wrapper contract.
- `f5d8560536915283b591d26134caa3624822da3b` — bootstrap/Node projection validator preservation across wrappers.
- `e855f0ab4b03e073094dd520fdfc7d0220eeef17` — Master Records governance validator preservation across bootstrap wrapper.
- `4f6d34aa68e64881f4774b9a01e7475d2458b56f` — HIL Node-sync validator preservation across Node wrapper.
- `2d2bedc83aab9b2b19ce011d3004c57b2650f4a1` — Node continuity regression tests point at the preserved implementation.

At exact head `2d2bedc83aab9b2b19ce011d3004c57b2650f4a1`, all observed PR validation lanes are green:

- Node IndexedDB Schema Migration run `34616824699` — PASS.
- Site Node Continuity run `34616824439` — PASS.
- StegOS Node Public Observation run `34616824434` — PASS.
- Validate StegOS Persistent Card UX run `34616824649` — PASS.
- StegVerse.me Origin Source Validation run `34616824553` — PASS.
- Site Bootstrap Validate — No Non-TV/TVC Credential Authority run `34616824653` — PASS.
- Site Handoff Orchestrator run `34616824534` — PASS.
- Ecosystem Heartbeat Orchestration run `34616824639` — PASS.
- My KV Directory Landing run `34616824486` — PASS.
- StegSocials Post Preparation run `34616824600` — PASS.
- No Required Third-Party Runtime run `34616824729` — PASS.

This establishes source/CI readiness only. It is not deployment or repaired-device evidence.

## Current next transition

`RECONCILE_README_AND_PR_THEN_MERGE_IF_EXACT_HEAD_REMAINS_GREEN`

After merge, the required order is:

1. verify the public source has propagated the compatibility/bootstrap repair;
2. only then permit exactly one current-iPhone ERL retry;
3. preserve the existing browser-local Node identity and Receipt #1;
4. classify the resulting runtime state without inferring ERL admission/readback from source or CI.

## Nonclaims

No merge, deployment, live-source propagation, repaired current-iPhone execution, ERL admission/readback, StegSocials draft save/readback, or evidence export is claimed by this handoff update. Source and CI evidence do not replace authentic current-device execution.

## Manual work

None. Do not clear Safari/site data, re-register the Node, or retry ERL import until this repair is merged and observed live.
