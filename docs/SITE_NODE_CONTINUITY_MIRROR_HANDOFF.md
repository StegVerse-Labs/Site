# Site Node Continuity Mirror Handoff

Issue: #572
Claim: SITE-NODE-CONTINUITY-572-20260828
Branch: claim/site-node-continuity-572
State: IMPLEMENTED / VALIDATION_PENDING

## Goal

Use one StegVerse Node continuity chain for My KV onboarding, optional VA Claims Guide progress, and Ecosystem Chat Node-aware LLM entitlement.

## Invariants

- Existing public StegOS Node Receipt #1 remains the registration/genesis contract.
- This lane does not rewrite the StegOS Node page or mint an alternate Node identity.
- Registered-node progress is reconstructed from the same IndexedDB Node receipt chain.
- Capability receipts contain state/evidence metadata only; no personal-information values, credentials, secrets, medical content, or provider tokens.
- My KV does not use localStorage as authoritative completion state.
- VA Claims Guide Node use is optional. Without Node participation, its existing browser-local guide progress may remain local-only.
- Ecosystem Chat resolves Node status before admitted model execution.
- An unregistered browser receives at most 10 locally enforced admitted LLM executions.
- Registration removes the unregistered allowance boundary but grants no other capability authority.
- TV/TVC remains credential authority.


## Implemented source

- `assets/stegverse-node-continuity.js`
  - reads the existing `stegos-node-v1` Node store;
  - validates Receipt #1 before trusting registration;
  - creates the same existing Site `NODE_REGISTERED` genesis contract when registration is requested from My KV/VA;
  - appends privacy-bounded `stegos.node_capability_receipt.v1` records;
  - reconstructs capability/step progress from the chain;
  - enforces a local unregistered maximum of 10 successful model executions;
  - registered Node state removes only that unregistered trial boundary.
- `my-kv.html`
  - VA-guide-style five-step onboarding;
  - explicit StegVerse-does-not-maintain-personal-information statement;
  - Node Receipt #1 registration;
  - device/cloud installation bridge with fail-closed absence;
  - optional Personal Information with existing multi-email/SKAP boundary;
  - optional Vault/Connections;
  - cloud verification bridge with fail-closed absence;
  - every registered-Node completion is reconstructed from the Node chain.
- `va-disability-claim-guide.html`
  - optional Node use;
  - existing browser-only mode retained;
  - local completed steps may be migrated as privacy-bounded completion receipts;
  - Node-backed completed steps restore on return.
- Ecosystem Chat / homepage
  - Node/trial status displayed;
  - model execution checks entitlement before execution;
  - only successful model-backed results consume the unregistered allowance;
  - deterministic/source-only results do not consume the allowance;
  - VA specialty model path is covered to prevent a category bypass.

## Important bounded limitation

The public Site currently has no live canonical browser bridge capable of independently installing the user's KV into cloud storage or verifying that user's configured cloud destination. Steps 2 and 5 therefore fail closed when `StegVerseKVInstallationBridge` is absent. They do not mark success from a click, filename, or folder label.

This is a truthful live UI/state-chain implementation, not a fabricated cloud activation claim.
