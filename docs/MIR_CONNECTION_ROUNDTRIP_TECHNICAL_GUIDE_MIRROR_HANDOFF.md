# MIR connection and round-trip technical guide mirror handoff

Updated: 2026-09-12
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/Site#1277`
Primary guide: `docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`
Status: `ACTIVE / INTERLOCK-INTR-ONLY COMMUNICATION / FINAL COMPLETION BLOCKED ON AUTHENTIC MIR ROUNDTRIP`

## Goal

Maintain the independent technical and operational guide for bidirectional StegVerse <-> MIR communication and prove it with an authentic MIR-evaluated round trip.

## Non-negotiable communication invariant

For this MIR connection there is exactly one communication medium:

```text
DESIGNATED UNIVERSAL INTERLOCK / INTR TRANSPORT PROTOCOL
```

Email, Gmail, shared documents, Google Docs, PDFs, manually exchanged files, generic web forms, direct provider/API calls outside the designated InTr path, or any other out-of-band channel are NOT valid StegVerse <-> MIR communication media and MUST NOT satisfy any runtime, delivery, evaluation, return, or round-trip predicate.

A source-native MIR or StegVerse object may be the payload carried by the designated Interlock/InTr protocol. That does not make the payload's storage format or originating provider a separate transport.

Any authenticated operation required to realize the designated transport remains behind TV/TVC credential custody. TV/TVC credential brokerage does not create an alternate MIR communication path.

## Canonical architecture

```text
StegVerse source-native request/artifact
-> exact-byte/hash commitment
-> designated MIR Interlock/InTr profile
-> stegverse.universal-intr-transport/v1
-> stegverse.universal-intr-materialization-request/v1
-> registered StegOS Node write-once intr_outbox
-> materialization trigger
-> authentic matching InTr ingress receipt
-> MIR-owned evaluation/accounting
-> MIR-native response artifact
-> designated MIR Interlock/InTr return profile
-> exact response binding/correlation
-> canonical return materialization / intr_outbox
-> authentic matching StegVerse InTr ingress receipt
-> StegVerse canonical SDK manifest ingress
-> admitted stegverse.ingress-manifest.v1
-> processing.capability + processing.route_id
-> installed-route resolution/admissibility
-> manifest-selected processor
-> canonical receipts/custody
-> requested comparison/delta/reconstruction when applicable
-> completed governed transaction evidence
-> Publisher presentation/evidence package assembly
-> Publisher output returned to SDK
-> SDK binds output to original initiating request/entity
-> SDK returns requested result/evidence projection to initiator
```

No state may be inferred from any non-InTr contact or artifact movement.

## Processing invariant

The MIR source identity, response class, provider identity, transport metadata, adapter, or prior result may contribute provenance/policy evidence but MUST NOT independently select StegVerse processing semantics. After the returned MIR payload is admitted through the designated return transport, any StegVerse processing begins at canonical SDK manifest ingress and is selected only by the admitted manifest's `processing.capability` + `processing.route_id` bound to an installed admissible route.

## Authority invariants

- MIR historical/accounting authority: MIR only.
- StegVerse governance authority: StegVerse only.
- Communication transport: designated Interlock/InTr protocol only.
- StegVerse processing selection: admitted manifest `processing.capability` + `processing.route_id` only.
- Interlock/InTr: transport/admission/transition coordination; not governance, historical, credential, or processor-selection authority.
- TV/TVC: credential custody for any authenticated transport operation; not an alternate transport.
- SDK: canonical manifested processing ingress after return transport admission and canonical caller-facing result/evidence return boundary after Publisher completes presentation assembly.
- Publisher: prepares the presentation/report/evaluator-evidence package from authentic retained governed evidence after the governed transaction is complete; it does not become governance, transport, or caller-routing authority.
- Site: documentation/projection only; not a MIR communication medium.
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
roundtrip verified: false
```

## StegVerse return-processing boundary

When a MIR-native response arrives through the designated return transport:

1. validate the exact InTr return receipt and transport/materialization bindings;
2. retain and hash the exact MIR-native payload;
3. correlate it to the exact outbound Interlock/InTr request;
4. construct/validate canonical `stegverse.ingress-manifest.v1` for the requested StegVerse processing;
5. validate `processing.capability` and `processing.route_id` against an installed admissible route;
6. dispatch only to the manifest-selected processor;
7. retain canonical receipts/custody;
8. perform comparison/delta/reconstruction only when requested by the admitted manifest.

## Post-governance Publisher and caller-return boundary

For an evaluator-facing or presentation-bearing run, successful governed processing is not yet the final caller response.

After the governed transaction and required round-trip/replay/reconstruction evidence are complete:

1. Publisher consumes the authentic retained evidence package for the completed transaction;
2. Publisher prepares the presentation/report and any evidence required by the evaluator/request contract;
3. Publisher returns the completed package/artifact references to the SDK;
4. the SDK binds that Publisher output to the original request/correlation identity and initiating entity;
5. the SDK returns the requested presentation/evidence projection to the initiator.

The initiator may be the user, an external evaluator/tester, or an external framework. If an external framework entered through an adapter, the SDK remains the canonical result boundary and the adapter may translate the SDK return into the framework-native protocol without changing evidence semantics.

Publisher output is not automatically a new processing request. It is the presentation/evidence result of the already completed governed transaction unless a new admitted manifest explicitly requests further processing.

Current repository evidence supports Publisher evidence-report rendering and Run-2 Publisher consumption, but the generic `Publisher -> SDK -> original initiator` return binding has not yet been proven as an implemented SDK contract. Treat that leg as REQUIRED / NOT_PROVEN until source and runtime evidence establish it.

## Final completion boundary

This documentation goal MUST NOT return to `COMPLETE` until all of the following are observed through the designated Interlock/InTr protocol and applicable downstream return chain:

1. authentic StegVerse outbound materialization and matching MIR ingress receipt;
2. authentic MIR-side evaluation/accounting over the admitted payload;
3. MIR-native response payload emitted into the designated return transport;
4. exact response-to/outbound correlation and payload hashes verified;
5. authentic StegVerse return InTr ingress receipt;
6. returned payload admitted through canonical SDK manifest ingress for any requested StegVerse processing;
7. manifest capability/route resolution and applicable processor receipt observed;
8. comparison/delta/reconstruction performed when the manifest requests it;
9. where the request requires presentation/evaluator evidence, Publisher prepares that package from authentic retained evidence;
10. Publisher output is received by SDK and bound to the original initiating request/entity;
11. SDK returns the requested evidence/result projection to the initiator;
12. the guide is reconciled against the exact observed runtime behavior.

Source merge, CI, email delivery, document creation, file sharing, provider reachability, or any other out-of-band evidence cannot satisfy these predicates.

## Current blocker

No qualifying MIR round-trip transport has yet been observed through the designated Interlock/InTr protocol. The previous Gmail/document attempt is explicitly non-qualifying. The final Publisher -> SDK -> initiating-entity return binding is also not yet proven as a generic implemented SDK contract.

## Next action

Execute the outbound packet through the existing designated MIR Interlock/InTr transport path, capture the authentic MIR ingress/evaluation evidence, carry the MIR-native response back through the designated return profile, admit the returned payload into canonical SDK manifest ingress, execute only the manifest-selected processing, retain the exact receipt/correlation chain, then have Publisher assemble the required presentation/evaluator evidence package and prove the final Publisher -> SDK -> original-initiator return before reconciling the primary guide against the observed end-to-end behavior.
