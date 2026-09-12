# MIR connection and round-trip technical guide mirror handoff

Updated: 2026-09-12
Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`
Canonical issue: `StegVerse-Labs/Site#1277`
Primary guide: `docs/MIR_CONNECTION_AND_ROUNDTRIP_TECHNICAL_GUIDE.md`
Status: `ACTIVE / SOURCE MERGED + VALIDATED / FINAL DOCUMENTATION COMPLETION BLOCKED ON AUTHENTIC MIR ROUNDTRIP`

## Goal

Maintain an independent technical document describing the process, techniques, state model, authority boundaries, transport bindings, response correlation, evidence requirements, and failure/retry behavior used to establish and verify bidirectional StegVerse <-> MIR communication.

The guide remains independent of any individual MIR test or experiment. Tests may instantiate the architecture, but they do not define it. Final documentation completion requires at least one authentic end-to-end MIR-evaluated round trip proving that the documented connection procedure works in practice and reconciling any runtime deviations back into the guide.

## Canonical architecture

Outbound transport and MIR processing remain source-native and profile-bounded. On return to StegVerse, the MIR artifact does not select its own processor merely because it came from MIR or carries a particular response class.

```text
source-native request/artifact
-> exact-byte/hash commitment
-> bounded transport/profile adapter
-> Universal Interlock/InTr transport/materialization as applicable
-> authentic MIR receipt/evaluation
-> MIR-native response artifact
-> exact response binding/correlation
-> StegVerse canonical SDK manifest ingress
-> admitted stegverse.ingress-manifest.v1
-> processing.capability + processing.route_id
-> installed-route resolution/admissibility
-> manifest-selected processor
-> canonical receipts/custody
-> requested comparison/delta/reconstruction when applicable
```

The MIR source identity, response class, provider identity, transport, adapter, or prior result may contribute provenance/policy evidence but MUST NOT independently select StegVerse processing semantics. A current test may choose evaluator/read-review through its manifest; that is a property of that manifest, not a universal MIR return rule.

Shared documents may act as the interoperability carrier when they preserve exact revision/content commitments. An API is an optional provider-specific surface and must remain behind TV/TVC credential custody when authentication is required.

## Authority invariants

- MIR historical/accounting authority: MIR only.
- StegVerse governance authority: StegVerse only.
- StegVerse processing selection: admitted manifest `processing.capability` + `processing.route_id` only.
- Source/provider/framework/adapter/transport identity: provenance/policy input only; not processor-selection authority.
- Universal Interlock/InTr: transport/admission/transition coordination according to the installed profile; not governance, historical, or processor-selection authority.
- TV/TVC: credential custody and bounded provider-operation brokerage when authenticated provider operations are required.
- SDK: canonical StegVerse manifested processing ingress and route-resolution boundary.
- Site: documentation, projection, packet intake/initiation surfaces only.
- Heartbeat: observability/carrier only.
- GitHub Actions: source validation/evidence transport only; runtime authority `NONE`.

## Source implementation evidence

Primary guide PR #1278 merged at `383dadb8cfa5b86012ecfbf7ea6026a8ce80b4e3` after exact-head Site Handoff, Bootstrap, and Heartbeat validation. Discoverability/handoff reconciliation PR #1279 merged at `ae82feb80a87165e1c58ae936c305958c1545d3a` after exact-head validation. Completion-boundary correction PR #1281 merged at `e7cd32994f2fe884c05fee4bff8faca54cf1669b`. These prove source/documentation state only.

## Authentic round-trip validation now in progress

The previous documentation completion boundary was too weak because it allowed the guide to be marked complete without proving the documented connection against MIR itself. That completion claim is superseded.

An authentic outbound validation packet was frozen and transmitted to MIR on 2026-09-12 through MIR's official partner contact channel.

Carrier/evidence:

- Google Doc title: `MIR × StegVerse Authentic Round-Trip Communication Validation — 2026-09-12`
- Google Doc ID: `1U3c2Q177biIMn50xAM7EaNFM3lPUfU1EhOZFnPH5kHk`
- packet class: `stegverse.mir.roundtrip-validation-packet.v1`
- committed packet SHA-256: `sha256:16a27d8af1ff2b138ca9aa2a89129e5a3b934a15b2cb95859355f33567baa626`
- exported PDF transmitted through Gmail to MIR official partner address `partners@mirregistry.org`
- Gmail outbound message ID: `1a096b13104f30c5`

The packet uses retained authentic StegVerse sovereign governance/runtime evidence from the 2026-08-13 canonical production-validation lane, including exact retained T0/T1-A/T1-B `manifest_receipt_id` and `route_manifest_id` values and the canonical ten-transition route sequence. It is not presented as a new Run-2 execution and is not a synthetic MIR result.

The response contract was frozen before transmission. MIR is required to return a source-native artifact/revision bound to the committed packet hash and to state what records it considers received, missing, changed, unsupported, or semantically non-representable, plus any valid MIR-native historical/continuity output and responder provenance.

As of the latest 2026-09-12 return-channel observation, no MIR-authored response from `partners@mirregistry.org` or attributable `@mirregistry.org` source has been observed.

## StegVerse return-processing boundary

When an authentic MIR-native return is observed:

1. retain the exact MIR artifact/source-native revision;
2. verify source/provenance and bind it to the committed outbound packet;
3. hash the exact returned artifact;
4. construct/validate canonical `stegverse.ingress-manifest.v1` for the StegVerse processing request;
5. validate `processing.capability` and `processing.route_id` against an installed admissible route;
6. only then dispatch to the manifest-selected processor;
7. retain canonical receipts/custody independent of caller return projection;
8. perform comparison/delta/reconstruction only when the admitted manifest requests the applicable processing capability.

No adapter may hardwire `MIR_HISTORICAL_ACCOUNTING`, MIR identity, response class, or carrier to `SDK:EvaluatorReviewIngress`, governance, evidence reconciliation, or any other processor before canonical manifest admission and route resolution.

## Final completion boundary

This documentation goal MUST NOT return to `COMPLETE` until all of the following are observed:

1. authentic StegVerse -> MIR packet delivery;
2. authentic MIR-side historical/accounting evaluation;
3. MIR-native returned artifact/revision retained without semantic rewriting;
4. exact `response_to` / packet-hash correlation verified;
5. returned artifact hashed and passed through canonical SDK manifest ingress for any StegVerse processing;
6. manifest capability/route resolution and applicable downstream processor receipt observed;
7. comparison/delta and reconstruction performed when requested by the admitted manifest;
8. the guide reconciled against observed runtime behavior, including deviations, retry requirements, unsupported semantics, carrier constraints, and processing-route behavior discovered during the test.

Source merge, CI, packet transmission, email delivery, document creation, transport admission, or source identity alone do not satisfy these predicates.

## Current blocker

Outbound packet transmission has occurred. No MIR-authored return artifact has yet been observed. Therefore MIR-side data evaluation, StegVerse return ingestion, manifest-selected processing, and the complete loop remain unproven, and the documentation remains ACTIVE.

A separate admitted TV/TVC MIR API/provider session also remains unobserved. MIR provider credentials must not be obtained or bypassed outside TV/TVC custody.

## Next action

Observe the authentic MIR return; retain and hash it; correlate it to `sha256:16a27d8af1ff2b138ca9aa2a89129e5a3b934a15b2cb95859355f33567baa626`; admit any requested StegVerse processing through canonical SDK manifest ingress; resolve the manifest-declared capability/route; execute only the selected installed processor; retain applicable receipts/custody; perform comparison/delta/reconstruction when requested; then revise and finalize the primary technical guide from the observed round-trip evidence.
