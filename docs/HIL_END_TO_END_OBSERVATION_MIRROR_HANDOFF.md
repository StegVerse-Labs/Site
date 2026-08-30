# HIL End-to-End Observation Mirror Handoff

Updated: 2026-08-30
Repository: `StegVerse-Labs/Site`
Goal: `HIL-END-TO-END-OBSERVATION-001`
Credential authority: `TV/TVC`
GitHub token runtime authority: `NONE`
Authority effect: `NONE`

## Purpose

Provide the HIL equivalent of the successful SV-DN-1 / Hugging Face authentic browser observation pattern: reuse an already-established StegVerse web node, execute the real public transaction, preserve a local fenced claim/terminal/reconstruction chain, and emit one canonical observation object that says `OBSERVED` only when live network evidence actually exists.

This test is an observation surface, not production authority. It does not replace WorkerCoordinator, TV/TVC, HIL receiver custody, private review, publication, Master Records, or runtime lifecycle authority.

## Execution surface

`stegos-node/hil-end-to-end-observation.html`

The page:

1. opens the existing `stegos-web-bootstrap-v1` IndexedDB without creating a database or node identity;
2. verifies the established Node/device binding and journal hash chain;
3. optionally accepts an already-exported `stegos.web_bootstrap_evidence_bundle.v1` if the current browser storage context cannot expose live IndexedDB;
4. derives a fresh device-local observation claim/fencing token from the existing journal;
5. creates a deterministic controlled PDF marked as observation-only, not participant research data;
6. hashes the exact PDF bytes;
7. creates the canonical HIL v1.1 provenance and Universal InTr transport intent;
8. POSTs the exact packet to `/api/hil/submissions` with no Authorization header or non-TV/TVC credential;
9. requires a real `HIL-RECEIVER-RECEIPT-v2`;
10. requires `EXACT_BYTES_PERSISTED` and `RECORDED`;
11. verifies the HIL InTr receipt chain through `DEVICE_SYSTEM -> STEGOS_ECOSYSTEM -> HIL:Custody` and the next `TVC:HIL-Lifecycle` intent;
12. retrieves the stored PDF back from `/api/hil/submissions/{submission_id}/content`;
13. independently rehashes the returned bytes and requires exact SHA-256 equality;
14. appends terminal and reconstruction receipts to the established web-node journal;
15. emits `stegverse.hil.canonical-observation-evidence/v1` with `state=OBSERVED` only after all predicates pass.

## What OBSERVED means

A PASS establishes:

```text
public Site HIL ingress transaction: OBSERVED
HIL receiver receipt: OBSERVED
exact-byte receiver custody: OBSERVED
HIL InTr device->ecosystem receipt: OBSERVED
HIL custody Interlock receipt: OBSERVED
TVC lifecycle next intent: OBSERVED
exact-byte content retrieval/reconstruction: PASS
existing StegVerse web-node continuity: VERIFIED
claim/terminal/reconstruction journal lineage: PASS
credential use: false
GitHub token use: false
participant research submission: false
```

A PASS does **not** claim:

```text
TVC receiving receipt: NOT YET OBSERVED BY THIS TEST
receiver restart/replacement reconstruction: NOT YET OBSERVED BY THIS TEST
private review: NOT CLAIMED
publication: NOT CLAIMED
Master Record: NOT CLAIMED
whole-product runtime activation: NOT CLAIMED
```

The exported evidence therefore explicitly preserves:

```text
tvc_receiving_receipt_observed=false
receiver_restart_reconstruction_observed=false
runtime_activation_claimed=false
authority_effect=NONE
```

## Failure semantics

Any HTTP failure, receiver-receipt mismatch, custody-state mismatch, InTr receipt-chain mismatch, journal lineage failure, or returned-byte hash mismatch produces `NOT OBSERVED`. Source presence or CI cannot turn this into `OBSERVED`.

## Current lifecycle standing

```text
source implementation: IMPLEMENTED
source validation: VALIDATED
integration: MERGED
merge: e14f66d849b40f2bb7a884536b841c2546ac52da
public Pages deployment containing merge: DEPLOYED
deployment head: 2be7d8c31eed8b74f100fe157513f3e8ebd57d6d
deployment run: 33290435363 SUCCESS
merge ancestry at deployment: INCLUDED
authentic established-node browser execution: NOT YET OBSERVED
canonical HIL observation evidence: NOT YET PRODUCED
PUBLIC_HTTPS_INGRESS typed capability observation: NOT YET ADMITTED TO KV
user action required for current machine work: false
authority_effect: NONE
```

The successful Pages deployment head is 20 commits ahead of the HIL merge with the HIL merge in its ancestry. Deployment therefore satisfies the publication/deployment gate for this observation surface, but it does not satisfy the browser-resident runtime observation gate.

The source implementation claim created for PR #662 has been terminalized and merged separately through PR #671 / merge `d113bdff2d35735986f02f3dceb7a5890619a931`.

KnowledgeVault now has a merged typed transport capability model and evidence-admission adapter. A valid `stegverse.hil.canonical-observation-evidence/v1` from this surface can advance only `PUBLIC_HTTPS_INGRESS`; it cannot advance unrelated transport, TVC lifecycle, provider, credential, Interlock-runtime, or authority facts.

## Source validation

`tests/test_hil_end_to_end_browser_observation.py` verifies the observation contract, authority exclusions, exact live POST requirement, exact returned-byte rehash requirement, and fail-closed `NOT OBSERVED` behavior.

## Next runtime action

Machine-side source, validation, merge, deployment verification, typed-transport governance, and evidence-admission preparation are complete.

The remaining observation predicate requires execution inside an already-established StegVerse web-node browser continuity context. Do not infer this from deployment or CI.

When that browser action becomes the next unblocked step, the user instruction must be stated explicitly as `USER ACTION: REQUIRED` with the exact live URL, exact button, and exact evidence output. Until then:

```text
USER ACTION: NONE
```

If the browser execution reports `OBSERVED`, preserve/export its canonical evidence and admit only `PUBLIC_HTTPS_INGRESS` into KV typed transport facts. TVC receiving receipt and controlled receiver restart/replacement reconstruction remain separate downstream HIL lifecycle predicates.
