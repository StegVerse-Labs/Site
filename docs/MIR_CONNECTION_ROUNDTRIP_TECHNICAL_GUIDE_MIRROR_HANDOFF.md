# MIR connection and round-trip technical guide mirror handoff

Updated: 2026-09-12
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/Site#1277`
Primary guide: `docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`
Global lifecycle contract: `StegVerse-Labs/.github/docs/CANONICAL_SOUTHBOUND_COMMUNICATION_LIFECYCLE.md`
SDK complete-manifest merge: `StegVerse-org/StegVerse-SDK@d3140a04e7405fe117c9808734d23a1027e68ead`
Status: `ACTIVE / CANONICAL SOUTHBOUND SOURCE CONTRACT MERGED / FINAL COMPLETION BLOCKED ON AUTHENTIC END-TO-END PROOF`

## Source reconciliation — 2026-09-12

The canonical SOUTH lifecycle is now source-aligned across all three governing documentation/manifest surfaces:

- `StegVerse-Labs/.github` merged the Task Registry-wide SOUTH lifecycle at `c20bd3002b3d46549d56350bf3a3f4c280097384`;
- `StegVerse-Labs/Site` merged the MIR guide/handoff correction at `efd9eb244a6a56baa2d6c3c93effa11bc4cd773b`;
- `StegVerse-org/StegVerse-SDK` merged the machine-readable complete-manifest `completion` contract, builder support, validation, tests, README, and evidence-presentation contract at `d3140a04e7405fe117c9808734d23a1027e68ead` after exact-head validation passed all triggered workflows.

Therefore the remaining blocker is **not** missing canonical source architecture. The remaining blocker is authentic runtime evidence for the declared lifecycle, including MIR transport/evaluation/return, manifest-selected processing, Publisher when declared, SDK return binding, applicable final StegVerse-side egress transition, Interlock/InTr egress, and the far-side transition.

## Goal

Maintain the independent technical and operational guide for bidirectional StegVerse <-> MIR communication and prove it with an authentic MIR-evaluated round trip that continues through the complete manifest, Publisher, SDK return assembly, governed ecosystem egress, and the far-side Interlock/InTr transition required to deliver the result to the initiating entity.

## Non-negotiable communication invariant

For this MIR connection there is exactly one communication medium:

```text
DESIGNATED UNIVERSAL INTERLOCK / INTR TRANSPORT PROTOCOL
```

Email, Gmail, shared documents, Google Docs, PDFs, manually exchanged files, generic web forms, direct provider/API calls outside the designated InTr path, or any other out-of-band channel are NOT valid StegVerse <-> MIR communication media and MUST NOT satisfy any runtime, delivery, evaluation, return, or round-trip predicate.

A source-native MIR or StegVerse object may be the payload carried by the designated Interlock/InTr protocol. That does not make the payload's storage format or originating provider a separate transport.

Any authenticated operation required to realize the designated transport remains behind TV/TVC credential custody. TV/TVC credential brokerage does not create an alternate MIR communication path.

## Canonical southbound lifecycle

`SOUTH` means the complete governed communication path toward ecosystem egress. It is not a separate authority, processor, runtime, or transport.

```text
initiating entity
-> canonical SDK manifested ingress
-> admitted manifest
-> manifest-declared processing capability + bound route
-> governed processing / required internal transitions
-> designated MIR Interlock/InTr round trip when declared by the manifest
-> returned governed processing / reconciliation as declared by the manifest
-> canonical receipts/custody
-> replay/reconstruction/evidence stages when declared by the manifest
-> Publisher presentation/evidence stage when presentation or evaluator evidence is declared
-> Publisher output returned to SDK
-> SDK return assembly bound to the original request and initiating entity
-> applicable caller-path egress adapter
-> final StegVerse-side state transition
-> designated Interlock/InTr egress
-> far-side Interlock/InTr state transition
-> initiating entity receives manifested result/evidence projection
```

No communication path is complete merely because governance, Publisher rendering, SDK return assembly, adapter emission, or local InTr egress materialization occurred. The terminal communication state requires the authentic far-side Interlock/InTr transition bound to the same manifest/request lineage and the applicable caller-side consequence/receipt.

## Complete-manifest invariant

Publisher is part of the complete manifest when presentation/report/evaluator evidence is required. It is not out-of-band post-processing.

The complete manifest must preserve the ordered relationship between:

- original initiating entity and request identity;
- processing capability and bound route;
- all required governed transitions;
- designated Interlock/InTr counterparty/evaluator round trips;
- custody/replay/reconstruction requirements;
- Publisher presentation/evidence requirements;
- SDK return projection and initiator binding;
- the final StegVerse-side egress transition;
- Interlock/InTr egress;
- the far-side transition that completes communication.

Publisher consumes authentic retained evidence and prepares the manifest-required presentation/report/evaluator package. Publisher is not governance, processing-selection, transport, caller-routing, or evidence-creation authority.

## Processing invariant

Source identity, response class, provider identity, framework identity, adapter identity, transport metadata, model identity, interface identity, or prior result may contribute provenance/policy evidence but MUST NOT independently select StegVerse processing semantics.

```text
admitted manifest
-> processing.capability
-> processing.route_id
-> installed-route resolution/admissibility
-> manifest-selected processor
```

This remains true throughout the complete southbound lifecycle.

## Framework egress / LLM Adapter invariant

For an external-framework path using the LLM Adapter, the LLM Adapter is the final StegVerse-side state-transition surface before Interlock/InTr egress.

```text
... -> Publisher -> SDK return assembly -> LLM Adapter -> Interlock/InTr -> far-side transition
```

The LLM Adapter may perform only the manifest-bound protocol/framing transformation required for egress. It may not alter evidence semantics, select or substitute processing, terminate the communication early, or become evidence/governance authority.

The LLM Adapter transition is not the terminal communication transition. The final state transition occurs on the other side of Interlock/InTr.

For initiators that do not use the LLM Adapter, the applicable manifest-bound egress surface occupies the analogous final StegVerse-side position. The far-side Interlock/InTr transition remains the terminal communication transition.

## Authority invariants

- Task Registry: work-intent/coordination truth only.
- WorkerCoordinator: execution claim/fence authority.
- MIR historical/accounting authority: MIR only.
- StegVerse governance authority: StegVerse only.
- Communication transport: designated Interlock/InTr protocol only.
- StegVerse processing selection: admitted manifest `processing.capability` + `processing.route_id` only.
- Interlock/InTr: governed ingress/egress and transition authority; not governance, historical, credential, Publisher, or processor-selection authority.
- TV/TVC: credential authority for authenticated transport operations.
- Master Records: observed-reality/custody/reconstruction authority.
- SDK: canonical manifested processing ingress and caller-return assembly bound to original request/initiator.
- Publisher: manifest-declared presentation/evidence assembly only.
- LLM Adapter: protocol/framing and, where applicable, final StegVerse-side southbound transition before InTr.
- Site: documentation/projection only.
- Heartbeat: observability only.
- GitHub Actions: source validation/evidence transport only; runtime authority `NONE`.

## Superseded invalid evidence

A previously created Google Doc/PDF and Gmail transmission were out-of-band artifacts. They are retained only as historical evidence of an incorrect attempted communication method. They DO NOT prove StegVerse -> MIR delivery, MIR receipt, MIR evaluation, MIR return, or any portion of the required round trip.

The previously frozen packet content/hash may be reused only if it is submitted as the exact payload through the designated Interlock/InTr transport and the resulting transport receipts bind that exact payload. The prior email/document transmission itself has zero qualifying runtime effect.

Therefore:

```text
qualifying outbound MIR transport observed: false
qualifying MIR ingress receipt observed: false
qualifying MIR evaluation observed: false
qualifying MIR return transport observed: false
qualifying StegVerse return ingress observed: false
Publisher -> SDK -> initiator runtime binding observed: false
final StegVerse-side egress transition observed: false
far-side Interlock/InTr final transition observed: false
roundtrip verified: false
```

## MIR return-processing boundary

When a MIR-native response arrives through the designated return transport:

1. validate the exact InTr return receipt and transport/materialization bindings;
2. retain and hash the exact MIR-native payload;
3. correlate it to the exact outbound Interlock/InTr request;
4. construct/validate canonical `stegverse.ingress-manifest.v1` for requested StegVerse processing;
5. validate `processing.capability` and `processing.route_id` against an installed admissible route;
6. dispatch only to the manifest-selected processor;
7. retain canonical receipts/custody;
8. perform comparison/delta/reconstruction only when declared by the admitted complete manifest;
9. execute the Publisher stage when presentation/report/evaluator evidence is declared;
10. return Publisher output to SDK and bind it to the original request/initiating entity;
11. execute the applicable final StegVerse-side southbound egress transition;
12. enter designated Interlock/InTr egress;
13. require the authentic far-side InTr transition before terminal communication state.

## Final completion boundary

This documentation goal MUST NOT return to `COMPLETE` until all applicable predicates of the complete manifest are authentically observed:

1. authentic StegVerse outbound materialization and matching MIR ingress receipt;
2. authentic MIR-side evaluation/accounting over the admitted payload;
3. MIR-native response payload emitted into the designated return transport;
4. exact response-to/outbound correlation and payload hashes verified;
5. authentic StegVerse return InTr ingress receipt;
6. returned payload admitted through canonical SDK manifest ingress for requested StegVerse processing;
7. manifest capability/route resolution and applicable processor receipt observed;
8. comparison/delta/reconstruction performed when declared;
9. Publisher presentation/evaluator evidence stage performed when declared;
10. Publisher output returned to SDK and bound to original request/initiator;
11. applicable final StegVerse-side egress transition observed;
12. for framework paths, LLM Adapter final StegVerse-side transition observed before InTr egress;
13. authentic Interlock/InTr egress observed;
14. authentic far-side Interlock/InTr transition and caller-side consequence/receipt observed;
15. the guide reconciled against exact observed runtime behavior.

Source merge, CI, Publisher rendering alone, SDK assembly alone, adapter emission alone, local egress staging alone, email delivery, document creation, file sharing, provider reachability, or any other out-of-band evidence cannot satisfy these predicates.

## Current blocker

Canonical source architecture is now merged across Task Registry, Site, and SDK. No qualifying MIR round-trip transport has yet been observed through the designated Interlock/InTr protocol, and none of the downstream authentic terminal predicates (Publisher runtime stage when declared, SDK return binding, final StegVerse-side egress transition, InTr egress, far-side transition) may be inferred from source merge or CI.

## Next action

Execute the complete manifest through the existing designated MIR Interlock/InTr transport path; capture authentic MIR ingress/evaluation and return evidence; execute manifest-selected StegVerse processing; retain exact custody/replay/reconstruction evidence; execute the manifest-declared Publisher stage; return the package through SDK bound to the original initiator; execute the applicable final StegVerse-side egress transition (LLM Adapter for framework paths); cross designated Interlock/InTr egress; and require the authentic far-side transition before claiming communication complete.
