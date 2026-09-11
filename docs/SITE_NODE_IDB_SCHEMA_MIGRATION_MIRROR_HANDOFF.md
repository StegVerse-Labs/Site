# Site Node IndexedDB Schema Migration Mirror Handoff

Goal Task ID: `SITE-NODE-IDB-SCHEMA-MIGRATION-001`
Parent Goal Task ID: `SS-EVIDENCE-COMPARISON-001`
COSV: `40000100100000`
Status: `ACTIVE / CLAIMED_INTEGRATION`
Canonical registry merge: `StegVerse-Labs/.github@7e36449d287f77f7502cffaddf8fac69d50eeea3`
Source incident: `StegVerse-Labs/Site#1233`

## Authentic trigger

The current iPhone produced `Failed to execute 'transaction' on 'IDBDatabase': One of the specified object stores was not found.` while the registered-Node resident action remained available. This is evidence of an IndexedDB schema/readback defect, not ERL admission success.

## Repair contract

- Preserve the existing `stegos-node-v1` database, Node registration, and Receipt #1; do not delete/recreate browser storage.
- Canonical Node DB store set is `meta`, `receipts`, `intr_outbox`.
- Repair authentic legacy v1 (`meta` + `receipts`) and malformed v2 (`meta` + `receipts`, missing `intr_outbox`) through an additive version migration.
- Align every Site runtime opener of `stegos-node-v1` with the canonical version/schema ownership so a partial opener cannot strand the database at a version that lacks required stores.
- Add deterministic migration coverage for v1 -> current, malformed-v2 -> current, and current -> current reopen, including exact registration/Receipt #1 preservation.
- Maintain `README.md` with the migration boundary and nonclaims.
- After exact-head validation and merge, verify live source propagation before asking for exactly one current-iPhone ERL retry.

## Current implementation inventory

Known shared-DB openers include:

- `assets/stegverse-node-continuity.js`
- `stegos-node/stegos-node.js`
- `stegos-node/device-kv-intr-sync.js`
- `stegos-node/hil-intr-sync.js`
- `stegos-bootstrap/stegos-bootstrap.js`
- `stegos-bootstrap/sv001-native-resident-activation.js`
- `stegos-node/services.js`

The repository currently contains mixed fixed versions, including version 1 and version 2. No source repair is claimed by this handoff alone.

## Next transition

`IMPLEMENT_CANONICAL_NODE_DB_MIGRATION`

## Manual work

None. Do not clear Safari/site data, re-register the Node, or retry ERL import until this repair is validated, merged, and observed live.
