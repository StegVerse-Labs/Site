# FROZEN TEST — PAIR-FIRST OUTAGE — 01

**Version:** 01 · **Frozen:** 2026-11-18 (America/Chicago) · **Status:** FROZEN
**Freeze rule:** this version never changes. Any revision is a new version number, published as a new document. A copy whose SHA-256 differs from the filed hash is not this version; the filed hash is carried in the Ecosystem KV filing record and in GitHub notices StegVerse-Labs/.github #3443 / #3472 of 2026-11-18.
**Authority:** NONE — coordination/test record only. Running this test admits nothing, settles nothing by itself, and certifies nothing; it produces evidence a reader can check.

## The question

When the network drops at the moment of a paid crossing, what does your framework do?

A verify-first system reads chain or facilitator state before it can complete a crossing, so an outage defers the crossing itself. A pair-first system decides on locally-decidable evidence, issues its proof at the crossing, and settles when the network answers. This test discriminates between the two — and it discriminates hardest at Step 4, where the only thing standing between a framework and a double settlement is a nonce, or an equivalent replay registry the framework keeps itself.

## Parameters (modeled on the reference run)

| Parameter | Value |
|---|---|
| Network | Base (eip155:8453) |
| Asset | USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Payment scheme | x402 "exact", EIP-3009 `transferWithAuthorization`, single-use authorization nonce (bytes32) |
| Crossing | Full evaluation — governance fee 15,000 µUSDC (US$0.015) plus a settlement charge quoted at challenge time |
| Reference crossing totals | 16,702 µUSDC and 16,697 µUSDC (fee + live-quoted settlement charge) |
| Payee | Fixed, server-side, stated in the challenge; the payer cannot redirect it |

A runner may substitute its own network, asset, and amounts. State every substitution in the report. The structure — a signed, single-use authorization presented to a system that then loses its network — is the test; the chain is not.

## Setup

1. Stand up the system under test in its normal production configuration.
2. Fund a payer under your own custody. Verify custody before funding (key file permissions, address re-derivation, test signature).
3. Let the system obtain whatever live quotes or prices its crossing requires, so it holds a current quote when the outage begins. (A system that has never obtained a quote may fail closed on pricing alone. That is a different result — report it as such, do not score it as Step 3.)
4. Obtain one valid, unused payment authorization for the crossing amount.

## The five steps

**Step 1 — Obtain the authorization.** As in Setup 4: a valid signed authorization, nonce unused, amount equal to the quoted crossing total.

**Step 2 — Cut the network.** The system under test loses all egress to chain RPC endpoints, explorers, and any facilitator it consults. Local storage, local signing, and local records remain available. Nothing else changes.

**Step 3 — Present the authorization (the crossing).**
Expected, pair-first: the crossing completes offline. The system decides on locally-decidable predicates — signature recovery, receptor and amount match against its own offer, validity window, and the authorization's nonce checked against the system's own records — issues its proof (the receipt record) with settlement marked pending, and returns its disposition to the payer.
Expected, verify-first: the crossing cannot complete, because the verification read has nowhere to go.

**Step 4 — Re-present the SAME authorization, still offline.**
Expected: refused, locally, from the system's own records, with no network read. The refusal is itself recorded. This is the step the nonce decides: the system must distinguish "the same payment again" from "a new payment" using only what it holds.

**Step 5 — Restore the network.**
Expected: settlement completes exactly once. The on-chain amount equals the crossing total exactly. The Step 3 disposition does not change; the settlement outcome is appended to the record, never rewritten into it. A full replay/recompute of the system's record verifies end-to-end, including the outage-period entries.

## Result-reporting table (fill in and publish)

| Step | Result (PASS/FAIL) | Evidence (record id / tx hash / error returned) | Notes |
|---|---|---|---|
| 1. Authorization obtained | | | |
| 2. Network cut (egress to chain/facilitator confirmed down) | | | |
| 3. Crossing presented offline | | | |
| 4. Same authorization re-presented offline | | | |
| 5. Network restored — settlement | | | |
| 5b. Full record replay/recompute | | | |

## Scoring

**PASS requires all three:** Step 3 completes offline **AND** Step 4 is refused from local state **AND** Step 5 settles exactly once.

Every other combination is a FAIL, named by its mode:

- Step 3 fails → **availability failure**: downtime is a lost crossing.
- Step 4 accepted → **replay failure**: the same authorization can settle twice.
- Step 5 settles zero times or more than once → **settlement integrity failure**.
- Step 4 refused only by consulting a facilitator's or the chain's state after reconnection → scored as a Step 4 FAIL: the registry was someone else's, and during the outage the framework held nothing that could refuse.

## Without a nonce

If the payment instrument carries no nonce — no unique, single-use, locally checkable replay token — Step 4 is undecidable from local state. The framework cannot tell a re-presentation from a new payment without reading state the outage has taken away. Its options are the three failure modes above: refuse Step 3 (availability failure), accept Step 4 (replay failure), or stall both until reconnection (the crossing is deferred — which is the verify-first result this test exists to expose). A hosted facilitator's nonce registry does not cure this: it is a read, and Step 2 removes reads. The registry has to be the framework's own, derived from its own record of what it has already accepted.

## Reference result — 0R10N15-8374 (StegVerse 8374, production)

Run against the production grammar, 2026-11-18:

- **Outage battery** (`outage_battery.py`, SHA-256 prefix `d55e208d` as recorded in the build record): **8/8, run twice** — no-quote fail-closed; quote persisted; blackholed crossing ALLOW with pair written PENDING under a stale-quote flag; nonce re-presentation refused locally (422 PAYMENT_NONCE_REUSED); on restore, the sweep settled on-chain exactly (run 2: tx `0x5a0b586e8624290e0599a1c74dc2f6455852bb188cf6aaa24516c9002d7e3112`, block 59301533); replay MATCH including the outage pairs; terminal-failure case receipted as its own appended record.
- **Production crossings on the pair-first path:** PAIR-000049, born PENDING, settled tx `0x6fac4964f1a4d0e44e5189d6f8a6ac50eabd46b516d463da0d5eb07d00bd9b77`, block 59302294, 16,702 µUSDC exact. PAIR-000054, born PENDING → PAIR-000055 SETTLED, tx `0x9fda13264a261f00d5fe2aed00af86e15def11c4f3a13b06831575d91c445f40`, block 59304079, 16,697 µUSDC.
- **Chain state at the reference run:** 55 pairs, replay MATCH, terminal anchor `3a8046e39b000d708b83a0b41a5ba6ee3d333761a8c1c5f9c5a40914e133b46d`.
- **Build record:** PAIR__FIRST__BUILD__RECORD__01.md, Ecosystem KV Drive `1Q7ffEc03NdGA57zw-U787C2hM251566s`.

**Inspect the live system — one link:** https://8374.stegverse.org/inspect
Live chain verdict and anchor, settled pairs with their on-chain transactions, current balance, and the determination block: which claims the evidence supports and which it does not.

## Running it

Run it against your own framework, your own funds, testnet or mainnet — state which. Publish the filled table wherever you publish your work. A result reported without the Step 4 evidence is a claim, not a run.
