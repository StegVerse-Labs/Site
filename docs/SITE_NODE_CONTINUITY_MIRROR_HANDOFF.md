# Site Node Continuity Mirror Handoff

Issue: #572
Claim: SITE-NODE-CONTINUITY-572-20260828
Branch: claim/site-node-continuity-572
State: IMPLEMENTED_VALIDATED_MERGED_DEPLOYED / DIRECT_PUBLIC_OBSERVATION_PENDING

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


## Merge and validation evidence

- PR: #574
- final validated implementation head: `01e6188506c0b77f0b636291b74a5c7f43d91c96`
- merge: `7b42bb7b839bc144a66bb4baee656903dca329be`
- claim release commit: `c73a7955667fef9aa1e1f341caf0e7f1f1eaae84`

Exact-head PASS:
- Site Node Continuity `33172208438`
- Site Homepage Chat `33172208448`
- My KV Personal Information `33172208458`
- Ecosystem Heartbeat Orchestration `33172208511`
- Site Handoff Orchestrator `33172208524`
- Site Bootstrap Validate `33172208489`

Legacy VA Claim Guide Workers `33172208463` remains FAIL only because its older checker still requires five retired `va-claims-chat.html` card labels. #572's own VA completion-gate mismatch was corrected; the remaining five failures concern an unchanged surface and are not reintroduced because the current veteran-first chat intentionally retired those labels.

Public publication is a separate gate and is not inferred from merge.


## Pages deployment evidence

Latest main at publication verification:

`769caab1b03f7f001087c4be704d7c8cefc492da`

GitHub Pages run `33172285367`: SUCCESS

- workflow artifact: `9686094760`
- artifact digest: `sha256:4fbeb84a562a0a304dafe9c118bc73f9fa4ee5d1ccab997a3fe251c0121421e4`
- artifact head branch: `main`
- artifact head SHA: `769caab1b03f7f001087c4be704d7c8cefc492da`
- deploy payload `pages_build_version`: `769caab1b03f7f001087c4be704d7c8cefc492da`
- deployment created successfully for that exact SHA
- evaluated environment URL: `http://stegverse.org/`

This establishes DEPLOYED for the exact source containing #572.

Independent external observation remains open because the web crawler still returned an older cached root/chat representation after this deployment. That stale observation must not be used to downgrade the exact Pages deployment evidence, but neither is it accepted as proof that a fresh public client has observed the new bytes.

Completion distinction:

```text
source implementation: IMPLEMENTED
source validation: VALIDATED
integration: MERGED
GitHub Pages exact-SHA deployment: DEPLOYED
fresh external route observation: PENDING / stale crawler representation observed
physical user-device Node registration: NOT PERFORMED BY THIS RELEASE
cloud KV install/verify through public browser bridge: FAIL_CLOSED UNTIL BRIDGE AVAILABLE
```
