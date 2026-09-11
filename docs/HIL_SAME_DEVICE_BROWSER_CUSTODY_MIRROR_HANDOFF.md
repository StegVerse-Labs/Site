# HIL Same-Device Browser Custody Mirror Handoff

Updated: 2026-09-11
Repository: `StegVerse-Labs/Site`
Issue: `#1238`
Parent goal: `SHWP-HIL-SOVEREIGN-RECEIVER-001`
Canonical parent handoff: `StegVerse-Labs/.github/docs/HIL_RESIDENT_SESSION_MANIFOLD_ACTIVATION_MIRROR_HANDOFF.md`
Parent COSV at source-task start: `50000000102000`

## Purpose

Continue the accepted current-iPhone ESRL `LEASE_OPEN` lineage into the first unresolved `HIL_RECEIVER_READY_AND_CUSTODY` stage without creating a second user-operated machine, replacement WorkerCoordinator claim/fence, second receiver authority, third-party production runtime, or GitHub runtime authority.

This handoff governs source readiness only. Source, CI, merge, cache generation, or public propagation must not be represented as authentic receiver custody. The parent HIL task remains ACTIVE until exact current-iPhone custody evidence, post-restart exact-byte proof, and TVC lifecycle evidence satisfy their independent predicates.

## Accepted predecessor lineage

```text
task = SHWP-HIL-SOVEREIGN-RECEIVER-001
request = RESIDENT-EXEC-HIL-SOVEREIGN-RECEIVER-002
runtime surface = CURRENT_USER_IPHONE_BROWSER
browser context = ctx_d151139d2db1eeecb6512f5844058246
node = stegnode-web-f24e3bfb7f5343cb37323187a88e51f3
claim = SHWP-SHWP-HIL-SOVEREIGN-RECEIVER-001-G25
fence = 25
ESRL state = LEASE_OPEN
lease = HIL-BROWSER-ESRL-7bafde4a280e847758da157e
exact ESRL SHA256 = a6756c54da15f09cd6a3dbb201375891803f6589fd644db4c545be39ebe41b92
```

The accepted ESRL artifact explicitly carries `custody_observed=false`; therefore ESRL acceptance alone cannot satisfy receiver custody.

## Canonical owner projection gap

StegOS canonical registry `specs/universal-intr-connector-profiles.v1.json` already defines:

- `hil-submission / SUBMIT`
- `hil-ingress-custody / ACCEPT_CUSTODY`
- `hil-tvc-lifecycle / ADMIT_LIFECYCLE`

The current Site generated browser projection includes `hil-submission` but omits the two downstream HIL profiles. Site must refresh the generated projection from canonical StegOS rather than locally redefining either boundary.

## Existing same-device source reused

`assets/hil-direct-upload-v1.js` already stages exact response bytes, provenance, the canonical `hil-submission` transport intent, and its materialization request in IndexedDB `stegverse-hil-v3 / response_files`, then re-reads and SHA-256 verifies the packet.

The successor must reuse that exact staged packet. It must not mint a substitute response, operation, request, claim, or fence merely to obtain favorable custody evidence.

## Required custody contract

A same-device custody successor may assert a bounded receiver/custody result only after it independently verifies all of the following in the current browser context:

1. retained accepted ESRL `LEASE_OPEN` lineage is present and matches the accepted G25 task/request/context/node/claim/fence;
2. the staged HIL packet is present in IndexedDB and its exact response bytes re-hash to the staged response SHA-256;
3. provenance is canonical HIL v1.1 and binds the same response, Primary, and Prompt identities;
4. the staged `hil-submission` InTr intent and materialization request hashes verify;
5. the canonical generated InTr connector contains the StegOS-owned downstream HIL profiles;
6. an ingress receipt and `hil-ingress-custody` intent/receipt are built only with canonical generated primitives and preserve prior-receipt hash lineage;
7. exact bytes plus bounded custody/registry metadata are persisted write-once in same-device durable browser storage and re-read byte/hash-identically before `EXACT_BYTES_PERSISTED` / `RECORDED` is asserted;
8. the next `hil-tvc-lifecycle` intent is generated and retained, but TVC admission remains false until TVC independently admits it;
9. output is explicitly non-authorizing for execution, review, publication, Master Records, credential, or lifecycle admission.

If any predicate is missing or mismatched, the successor fails closed and does not emit a qualifying custody receipt.

## Authority boundaries

```text
credential authority = TV/TVC
GitHub runtime authority = NONE
heartbeat execution authority = NONE
ESRL lease authority expansion = NONE
same-device execution required = true
second user-operated machine required = false
replacement claim/fence allowed = false
TVC admission authority = TVC only
review/publication/Master Records authority = false
```

## README maintenance

Because this adds a materially new same-device runtime continuation surface, Site README must document that browser custody is an event-ephemeral same-device receiver implementation using canonical StegOS generated InTr profiles, and that source/CI/merge do not prove runtime custody.

## Completion boundary

This Site source task is source-complete only when:

- generated browser InTr projection includes the canonical downstream HIL profiles and validates against StegOS provenance;
- same-device custody source and deterministic tests are merged;
- README and this handoff accurately describe the authority/evidence boundary.

Authentic parent advancement beyond `HIL_RECEIVER_READY_AND_CUSTODY` additionally requires an exact current-iPhone custody artifact to be observed and preserved. Only then may the parent readiness classifier advance to `POST_RESTART_EXACT_BYTE_PROOF`.
