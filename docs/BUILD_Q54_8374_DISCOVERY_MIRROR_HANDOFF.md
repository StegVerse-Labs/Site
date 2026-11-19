# BUILD-Q-54 8374 discovery fallback mirror handoff

Queue: StegVerse-Labs/.github#3443/7014647758. CODEX claim: .github#3472/7022219415. Source scope: ecosystem Site discovery-mirror leg only. Native Goal/COSV UNBOUND; no borrowed authority. Canonical coordination parent remains PROPOSED.

Create immutable, hash-pinned public /offer, /openapi.json and /.well-known/x402 snapshots under 0r10n15-8374/discovery/. These preserve the exact captured JSON text from the existing endpoint; sidecar provenance identifies a historical static projection and current challenges remain authoritative for any payment. Browser-only relative links keep the snapshots readable without the endpoint. No automatic failover for signed operations is introduced.

Acceptance: local Site copy serves all three snapshots with the source origin unavailable; JSON parses, all declared hashes/lengths match, links are local, and the face states snapshot age and payment restrictions. README and source claim must be updated with the same change. Protected integration, deployed byte verification, actual payment, central suite adoption and lane-host operation remain separate owner work.


## Source implementation and checks — 2026-11-19

The three captured documents are offer.json (5,825 bytes), openapi.json (3,189 bytes), and x402.json (529 bytes), captured at 2026-11-19T21:10:52.705Z. Exact body SHA-256 values are in discovery/manifest.json. They were obtained as fresh public primary-origin response bodies via maxAge=0 fetch; origin wire headers and signatures were not independently verified. Historical offer x402Version=1 and flat OpenAPI x-payment-info are preserved, disclosed limitations, not silently changed or used for payment.

The new checker verifies the three exact JSON bodies, schema/source/capture/authority limits and local links. Normal and optimized Python both passed: 3 documents, 8 rejected negative controls, and 5 loopback HTTP byte comparisons with zero requests to the origin. The Site base's 429 existing claim fragments were read by immutable native Git blob ID; all 429 reconstructed bytes matched. Existing claim checker passes; COSV checker passes with 69 active claims and zero unindexed tasks. Two of those are this new source claim and the existing domain-connection claim (the base denominator was 68, while its index still reported 67). The existing domain claim is projected exactly in its current CLAIMED_FOR_IMPLEMENTATION state; its source/owner/lifecycle is not changed. This new publication task uses the existing NOT_ESTABLISHED exemption and emits no native COSV.

Registration commit08b9e835f6f1c4e37a787ff89119e89140c567cb introduced the exclusive source claim, this handoff and the necessary projection updates atomically before implementation. Source branch codex/build-q54-8374-discovery-mirrors-20261119 is based on82703dc88d05e61a11fc6c0015a9c35ac62a945b. Keep existing validate/heartbeat/reconcile gates; no test or gate relaxation. Protected integration remains owner-executed. Retain this active branch claim through integration; release it by the existing separate terminalization path after merge/readback, or record an explicit incomplete disposition if abandoned.

## Remaining acceptance

Inspect all exact-head PR checks; current-main changes require a fresh expected-head reconciliation. After owner integration, independently fetch all three Site snapshot bodies plus the manifest/page and compare the exact source hashes. That is a distinct propagation verification, not already proven by local HTTP. Existing BUILD-Q-54 lane-host/custody/funding, central GEN12 suite/native authority and actual external routed crossing remain with their original owners. No release tag or runtime version increase is justified by this static mirror alone.
