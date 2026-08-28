# Site Node Continuity Mirror Handoff

Issue: #572
Claim: SITE-NODE-CONTINUITY-572-20260828
Branch: claim/site-node-continuity-572
State: CLAIM_PENDING_ADMISSION

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
