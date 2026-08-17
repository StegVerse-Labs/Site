# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-17T16:38:00-05:00

## Canonical state

```text
goal_id: SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380
originating_session_goal: correct the current-phone iOS first-passkey PREPARE double-ceremony failure while preserving TV/TVC-only credentials and USER_ONLY signing/broadcast
repository: StegVerse-Labs/Site
claim_id: SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380-20260817
claim_state: MERGED_INTO_CANONICAL_WORKSTREAM
product_state: COMPLETE_RELEASED_SITE_PUBLICATION
site_execution_responsibility: NONE
source_owner: StegVerse-Labs/stegfin-governance#79 (StegFin #79)
parent_live_owner: StegVerse-Labs/stegfin-governance#77 + current phone + USER_ONLY
credential_authority: TV/TVC
credential_requirement: NONE
non_tv_tvc_secret_or_token_allowed: false
github_token_runtime_authority: NONE
Render production runtime: PROHIBITED
wallet_signing_authority: USER_ONLY
broadcast_authority: USER_ONLY
```

Site is static transport/materialization only. The corrected first-passkey participant is published, but Site does not own wallet keys, signatures, broadcast, settlement, TV/TVC credential authority, model/runtime authority, sovereign heartbeat authority, or live current-phone activation.

## Released predecessor continuity anchors

The #380 publication handoff is a compact successor handoff, but the canonical phone validator also preserves the immutable predecessor chain below. These anchors are provenance and continuity evidence only; restoring them does not reactivate predecessor claims or grant execution authority.

```text
STEGFIN-PHONE-DIRECT-ROUTE-011
STEGFIN-PHONE-RPC-RESILIENCE-012
SITE-STEGFIN-PHONE-PROJECTION-261
SITE-STEGFIN-PHONE-EVIDENCE-EXPORT-289
SITE-STEGFIN-PHONE-STEGID-FRESHNESS-292
STEGFIN-PHONE-STEGID-FRESHNESS-016
TASK-2026-0004
Site#282
source trade contract: COMPLETE_INSTALLED
phone direct-route blob: 31ed79cb56e8d2366e6d70f22e28c70162c88fd8
RPC resilience blob: 290b567eca2cc9f83e7438a80682ebaf8006ad76
StegFin RPC resilience source merge: bcba49976a52024a233f998ce290ec4ab42618ff
STEGFIN-PHONE-WALLET-REVIEW-014
USER_ONLY wallet review app blob: 433ef5e5db9f9f7af2c7c7df4ba01acc89125403
current StegID bootstrap blob: 9cac39a990a956f16fcde3681cbcc7d47b2fc704
freshness identity blob: 1180d8ee929c161978d095c91514cbc3d873d3fd
freshness evidence-export blob: 29ddb120fe6d1bd7c5118b41c4ef061d2db90a58
StegFin PR #75
USER_ONLY wallet review
Copy canonical evidence
Share canonical evidence
unexpired StegID admission evidence required before PREPARE
WALLET_HANDOFF_READY remains unsigned until USER_ONLY review
```

These predecessor anchors remain released history. They do not authorize reuse of expired evidence, automatic signing, automatic broadcast, hosted runtime execution, Render, or any NON-TV/TVC secret/token.

## Current iOS correction release

```text
StegFin child task: STEGFIN-IOS-FIRST-PASSKEY-PREPARE-018
StegFin issue: #79 (StegFin #79)
source PR: #80
source merge: f5ff9b1aa2fad545cf9fd676c785438f306dda7a
released source/bootstrap blob: 9cac39a990a956f16fcde3681cbcc7d47b2fc704
Site issue: #380 CLOSED_COMPLETED
Site PR: #384
Site merge: 0a0e00602ec2e3bbae3c9f1d05b65af27729e101
Pages build: 1157682910 BUILT
Pages commit: 0a0e00602ec2e3bbae3c9f1d05b65af27729e101
Site claim release commit: 9456df6b3a6bcff0fd6d2e2bcc2c55fb76e42811
```

Required participant behavior:

```text
first-time/reset-state PREPARE
-> navigator.credentials.create
-> platform authenticator + residentKey + userVerification required
-> successful creation returns HUMAN_CONTINUITY / CREDENTIAL_CREATION
-> no immediate second WebAuthn operation

later PREPARE
-> new explicit user gesture
-> navigator.credentials.get
-> userVerification required
-> HUMAN_CONTINUITY / CREDENTIAL_ASSERTION
```

The historical unsigned WALLET_HANDOFF_READY candidate remains evidence only and is not made signable by this release.

## Release validation

Fresh-current-main PR #384 passed:

```text
Check StegFin Phone Projection: 32066238396 SUCCESS
Site Handoff Orchestrator: 32066238185 SUCCESS
Ecosystem Heartbeat Orchestration: 32066237444 SUCCESS
Site Bootstrap Validate: 32066238690 SUCCESS
```

The exact Pages build then reached BUILT from the exact Site merge. Publication/source validation is non-authorizing and does not establish current-phone proof or wallet settlement.

## USER_ONLY wallet handoff boundary

The previously released successor flow remains unchanged:

```text
fresh current-device WebAuthn/device-possession/PREPARE
-> fresh unsigned WALLET_HANDOFF_READY candidate
-> explicit USER_ONLY wallet handoff
-> wallet independently confirms or rejects eth_sendTransaction
-> returned hash is SUBMITTED_NOT_SETTLED
-> independent credential-free Base receipt observation
-> successful receipt requires a fresh successor PREPARE
-> fresh exit candidate
-> USER_ONLY exit signature/broadcast
-> settlement -> reconstruction/P&L -> production sizing
```

Automatic signing and automatic broadcast remain prohibited. A stale candidate, quote or simulation may not be reused.

## Wallet compatibility boundary

Only an already-injected EIP-1193 wallet is supported by the released participant. This Site release does not install WalletConnect, a relay, hosted wallet middleware, provider API keys, automatic chain switching, automatic signing or automatic broadcast. If the current phone lacks an injected provider, the live path must fail closed and that observation returns to StegFin #77 as a named compatibility task rather than introducing a credential workaround.

## Local model/runtime convergence

Formal model development and executable local runtime discovery/launch/inference/proof are already canonical and released in `StegVerse-002/micro-node-runtime`. Site must not duplicate that runtime or model authority. Remaining live model activation is machine-owned by the sovereign heartbeat -> TVC -> LLM-adapter -> Master Records chain.

## Ownership and continuation

```yaml
released_site_task:
  task_id: SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380
  state: COMPLETE_RELEASED_SITE_PUBLICATION
  worker_registry_ref: data/session-work-claims.json#SITE-STEGFIN-IOS-FIRST-PASSKEY-PREPARE-380-20260817
  release_condition: SATISFIED
  next_executable_action: NONE_SITE

human_authority_and_live_observation:
  owner: StegVerse-Labs/stegfin-governance#79 -> #77 + current phone + USER_ONLY
  state: CURRENT_PHONE_PROOF_REQUIRED
  next_executable_action: reload the published participant and perform a fresh Verify/PREPARE; only a newly generated unexpired candidate may reach wallet review
```

MERGED INTO: `StegVerse-Labs/stegfin-governance/task-state/STEGFIN-IOS-FIRST-PASSKEY-PREPARE-018.json`.

## Completion accounting

```text
Site #380 developed product/control files: 5/5
scaffolding or stubs: 0
missing required Site files: 0
Site validation: 4/4 canonical gates PASS
Site integration: exact source projection + merge + Pages + claim release = COMPLETE
Site activation: 100% for publication scope
current-phone correction proof: PENDING under StegFin/current-phone authority
wallet signature/broadcast/settlement: NOT EXECUTED / USER_ONLY
```
