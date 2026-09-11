# Site Interlock / InTr connection documentation mirror handoff

Updated: 2026-09-11
Goal Task ID: `SITE-INTERLOCK-INTR-CONNECTION-DOCS-001`
Issue: `StegVerse-Labs/Site#1243`
PR: `StegVerse-Labs/Site#1245`
COSV ID: `NOT_YET_ESTABLISHED`
Status: `ACTIVE / PUBLIC DOCS + LIVE PROFILE PREFLIGHT IMPLEMENTED / PRE-WORK CLAIM REGISTERED / EXACT-HEAD REVALIDATION PENDING`

## Goal

Provide a public Site connection guide analogous to the HIL user flow: a counterparty response packet is submitted, exact packet identity is retained, the receiving profile adapter binds it to the existing registered StegOS Node and Universal InTr transport/materialization path, and that submission becomes the event that initiates the connection attempt.

The documentation must preserve the distinction between packet acceptance, Node outbox staging, InTr ingress admission, and actual downstream connection establishment.

## Implemented surfaces

- `interlock-intr-connections.html`
  - public response-packet-to-connection flow;
  - connection state vocabulary;
  - live discovery-only `/intr/profile` probe;
  - local response-packet metadata preflight;
  - explicit block when requested profile is not advertised;
  - HIL reference links;
  - no generic packet submission is promoted into Node-outbox origin or authority.

- `docs/INTERLOCK_INTR_CONNECTION_GUIDE.md`
  - normative documentation of the reusable packet -> adapter -> Node outbox -> InTr trigger -> ingress receipt -> downstream receipt sequence;
  - adapter responsibilities;
  - retry/continuity semantics;
  - HIL mapping;
  - shared-document/external-system use;
  - authority boundaries.

- `fixtures/interlock-intr/response-packet.example.json`
  - documentation-level source-owned response handoff;
  - requests initiation but grants no governance, execution, credential, Node, or Interlock authority;
  - canonical transport remains `stegverse.universal-intr-transport/v1`.

- `scripts/check_interlock_intr_connection_docs.py`
  - deterministic documentation/authority-boundary validator.

- `.github/workflows/interlock-intr-connection-docs.yml`
  - exact-source validation carrier only; grants no runtime or transition authority.

- `data/session-work-claims.d/site-interlock-intr-connection-docs-1243.json`
  - collision-bounded pre-work claim for this exact branch and documentation surface;
  - no HIL runtime/profile ownership and no authority effect.

## Architectural rule

```text
response packet submitted
-> PACKET_ACCEPTED
-> profile adapter validates and binds local Node/Interlock
-> OUTBOX_STAGED
-> InTr trigger emitted
-> CONNECTION_INITIATED
-> authentic ingress receipt
-> INGRESS_ADMITTED
-> profile-specific downstream evidence
-> CONNECTION_ESTABLISHED
```

A counterparty response packet is never allowed to self-assert `STEGOS_NODE_OUTBOX`, Node identity, Interlock identity, governance admission, credentials, or connection success.

## HIL relationship

HIL is the concrete working reference implementation and should remain linked from the generic Site guide. The general guide does not replace the HIL adapter or create a second transport. It documents the reusable shape already demonstrated by:

- `humans-as-interoperability-layer.html`
- `hil-receipt.html`
- `stegos-node/stegos-node-impl.js`
- `stegos-node/hil-intr-sync.js`
- `intr-service-worker.js`

## Validation trajectory

At PR #1245 head `971e4e604841aaa9d748ee2e688d3dd21caf6c42`:

- Interlock InTr Connection Docs Validation run `34655543087`: PASS.
- Node IndexedDB Schema Migration run `34655542900`: PASS.
- Site Bootstrap, Site Handoff Orchestrator, and Ecosystem Heartbeat failed because the branch had no active pre-work claim, not because the documentation validator failed.
- The exact orchestration failure was: `pull request branch must resolve to exactly one active pre-work claim: site-interlock-intr-connection-docs-001`.

The branch now contains an append-only active claim fragment for the exact branch. The next required evidence is fresh exact-head validation after that repair.

## README impact

README was reviewed. Its public-page table does not yet contain this new page. README has **not** been modified in this branch yet; do not claim otherwise. The public HTML page and direct Markdown guide are already implemented, and README navigation remains a bounded documentation follow-up rather than a reason to misstate validation.

## Remaining work

1. Re-run exact-head Site claim/orchestration/bootstrap/dedicated documentation validation after the pre-work claim registration.
2. Add README public-page navigation and a direct link to the relevant `INTERLOCK_INTR_CONNECTION_GUIDE.md` section when that large shared projection can be updated without colliding with another active workload.
3. Merge only if exact-head validation is green or any remaining failure is independently demonstrated to be unrelated and non-blocking under Site policy.
4. Register a COSV/canonical task pointer only if this docs lane requires independent ecosystem coordination beyond Site.
5. Future profile-specific adapters (for MIR or another system) should reuse this documentation/state model and the existing Universal InTr transport rather than creating a bespoke transport.

## Non-claims

This work does not claim:

- that every documented profile is already installed;
- that packet preflight is InTr admission;
- that Site has governance/execution authority;
- that `/intr/profile` grants authority;
- that connection establishment occurred without a profile-specific downstream receipt;
- that Heartbeat grants admission/routing/transition authority;
- that GitHub Actions is runtime execution.
