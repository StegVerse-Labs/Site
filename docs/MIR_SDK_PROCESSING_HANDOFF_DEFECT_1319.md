# MIR SDK processing handoff defect

Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
COSV ID: `50000000100000`

## Concrete defect

After the retained exact MIR NODE MIRROR packet binding merged, the Site return consumer could prove `STEGVERSE_RETURN_EXIT`, `SDK_EVALUATOR_INGRESS_ADMITTED`, and `EXTERNAL_COUNTERPART_RETURN_ADMITTED`, but the consumed result did not expose the admitted manifest object and continuation as a durable handoff for the SDK-owned manifest-selected processor.

That meant a downstream SDK processor could verify hashes and receipts but could not safely continue from the Site result alone without reacquiring or reconstructing the manifest from another source.

## Required boundary

The fix must not create a MIR-specific transport, scheduler, credential path, SDK processor, Publisher, egress mechanism, or authority path. It may only expose a bounded handoff packet derived from the already-admitted Site return and carried receipts.

## Repair path in this branch

`assets/external-counterpart-return-consumer.js` now emits `stegverse.site.sdk-processing-handoff/v1` with:

- exact admitted manifest object;
- manifest hash;
- response_to correlation;
- retained_packet_sha256;
- retained packet schema;
- STEGVERSE_RETURN_EXIT receipt;
- SDK_EVALUATOR_INGRESS_ADMITTED state;
- Node EXTERNAL_COUNTERPART_RETURN_ADMITTED receipt;
- next required transition `EXECUTE_MANIFEST_SELECTED_SDK_PROCESSING_AFTER_EVALUATOR_INGRESS`;
- authority effect `NONE`.

The focused runtime test verifies the handoff fields and hash. This closes only the Site-to-SDK handoff defect. Manifest-selected SDK processing itself remains SDK-owned and must be executed by the next SDK-owned transition.