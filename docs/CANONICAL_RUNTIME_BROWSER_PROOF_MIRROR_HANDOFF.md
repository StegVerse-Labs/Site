# Canonical Runtime Browser Proof Mirror Handoff

Updated: 2026-08-30
Repository: `StegVerse-Labs/Site`
Issue: #745
Cross-repo owner: `StegVerse-Labs/StegOS#115`
State: IMPLEMENTED_ON_BRANCH / AUTHENTIC DEVICE RUN REQUIRED

## Purpose

Obtain the first authentic end-to-end observation of the canonical runtime lease fabric from an already-valid StegVerse Node.

This is not device-node validation. The page accepts either of the two already-established browser continuity contracts that exist on `stegverse.org`: (1) the newer `StegVerseNodeContinuity` Receipt #1 store, or (2) the established `stegos-web-bootstrap-v1` journal used by the browser-native first-node/SV-DN-1 lane. The legacy path replays the complete journal, verifies the `stegos.web_node.v1` origin/TV-TVC boundary, verifies `stegos.web_device_continuity_root.v1`, and requires the `stegos.web_device_node_binding_receipt.v1` relation before reuse. It never calls `registerDevice()` and never mints a replacement node.

## First execution substrate

The first lease uses an actual isolated browser Web Worker on the valid Node:

```text
existing valid Node continuity (Receipt #1 OR verified web-bootstrap journal)
-> Universal InTr request intent
-> lease REQUESTED
-> ADMITTED
-> PROVISIONING
-> Web Worker instantiated
-> worker READY
-> LOCAL_READY
-> LEASE_OPEN
-> request ingress RECEIVED
-> exactly one bounded SHA-256 operation
-> TRANSITION_RECORDED
-> response egress FORWARDED
-> egress prior receipt = ingress receipt hash
-> RETURN_QUEUED
-> evidence retained in local durable browser storage
-> EVIDENCE_EXPORTED
-> RELEASING
-> Web Worker terminated
-> LEASE_CLOSED
-> closure retained
-> canonical-runtime-proof capability receipt appended to existing Node receipt chain
```

No public/server rendezvous is claimed by this profile. `rendezvous_requirement=NOT_REQUIRED`.

## Authenticity

A run claims `CANONICAL_RUNTIME_LANE_OBSERVED` only when executed at the exact secure origin `https://stegverse.org` and the existing Node proof validates.

Source/CI may validate the page and state machine but cannot satisfy runtime observation.

## Evidence

The successful bundle is `stegverse.canonical-runtime-proof-bundle/v1` and includes:

- Node continuity binding (Receipt #1 or verified web-bootstrap journal tail);
- lease/runtime/run IDs;
- request Universal InTr intent;
- ingress `RECEIVED` receipt;
- exactly-one bounded execution result;
- response Universal InTr intent hash;
- egress `FORWARDED` receipt;
- direct prior-receipt chaining;
- pre-release durable retention receipt;
- complete lease history ending `LEASE_CLOSED`;
- terminal closure retention receipt;
- Node capability receipt binding the closure hash.

## Boundary

This first substrate proof does not claim that a public server receiver exists. It proves the canonical lease lifecycle itself on a real StegVerse Node. Runtime profiles that require public ingress use the same lease fabric with `rendezvous_requirement=REQUIRED`.
