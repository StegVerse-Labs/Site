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
- Canonical Node DB store set is `meta`, `receipts`, `intr_outbox`.
- Canonical migration target is version 3.
- Repair authentic legacy v1 (`meta` + `receipts`) and malformed v2 (`meta` + `receipts`, missing `intr_outbox`) through an additive version migration.
- Align every Site runtime opener/entrypoint of `stegos-node-v1` with canonical version/schema ownership so a partial opener cannot strand the database at a version that lacks required stores and a lower fixed-version opener cannot raise `VersionError` after migration.
- Add deterministic migration coverage for v1 -> current, malformed-v2 -> current, and current -> current reopen, including exact registration/Receipt #1 preservation.
- Maintain `README.md` with the migration boundary and nonclaims before merge.
- After exact-head validation and merge, verify live source propagation before asking for exactly one current-iPhone ERL retry.

## Implemented branch evidence

- `104d62dc32c9d5c05d93cfb43a768cc9b7cac10c` installed the additive v3 compatibility migration on the authentic failing My KV / ERL entrypoint plus deterministic regression coverage and task handoff.
- `639d8fd497b58e7d74758f45409cc83efb1b32b1` reconciled stale DEVICE_KV validation assumptions with the current fail-closed target and generated positional carrier-binding contract.
- `2d91f109f7a5b9d707be9a1dc0f16eb237a5c2cc` added the exact Site pre-work claim. At that exact head, Node IndexedDB Schema Migration, Site Bootstrap Validate, Site Handoff Orchestrator, Ecosystem Heartbeat Orchestration, My KV Directory Landing, and StegSocials Post Preparation all passed.
- `cf9a0efacad6d1e9e1ab8da44b533083e3c8f9c1` aligned `stegos-node/services.js` from legacy version 1 / two-store behavior to version 3 with the complete `meta`, `receipts`, `intr_outbox` schema. Focused migration validation and StegVerse.me Origin Source Validation passed.
- `370ab22a9e5a7e6371004569f65c7efc61458bd4` added an exhaustive HTML runtime-entry alignment validator.
- `bc29d0c3da5f5c851608a040aad61ee5b0172b8a` wired that validator into the focused migration workflow. The migration regression passed; the alignment gate failed closed and produced the exact remaining entrypoint inventory below.

## Remaining runtime-entry alignment inventory

These 27 HTML entrypoints still load a `stegos-node-v1` opener without first loading the canonical compatibility layer at the current branch head:

- `canonical-runtime-proof/index.html`
- `cloud-kv-peers.html`
- `device-kv-install.html`
- `ecosystem-chat.html`
- `hugging-face-analysis.html`
- `hugging-face.html`
- `index.html`
- `kv-testflight-projection.html`
- `my-kv-instances.html`
- `my-kv.html`
- `node-status.html`
- `nodes.html`
- `stegos-bootstrap/command.html`
- `stegos-bootstrap/ecosystem-chat-bridge.html`
- `stegos-bootstrap/hil-activate.html`
- `stegos-bootstrap/index.html`
- `stegos-bootstrap/native-resident-activate.html`
- `stegos-node/index.html`
- `stegos-node/services.html`
- `stegos-node/stegverse-me-services-origin.html`
- `stegos-node/sv-dn1-bootstrap.html`
- `stegsocials-bounded-group-runtime-proof.html`
- `stegsocials-prepare.html`
- `sv002-observe/index.html`
- `sv002-observe/runtime-evidence-test.html`
- `va-disability-claim-guide.html`
- `workspace.html`

`my-kv-directory.html` is already aligned and is not in this failure set.

## Current next transition

`ALIGN_REMAINING_NODE_DB_RUNTIME_ENTRYPOINTS_THEN_REVALIDATE`

Do not merge #1235 until the exhaustive alignment gate, focused migration workflow, and broad Site validation pass at the same exact branch head and README reconciliation is present.

## Nonclaims

No merge, deployment, live-source propagation, repaired current-iPhone execution, ERL admission/readback, StegSocials draft save/readback, or evidence export is claimed. The repository/CI evidence does not replace authentic current-device execution.

## Manual work

None. Do not clear Safari/site data, re-register the Node, or retry ERL import until this repair is validated, merged, and observed live.
