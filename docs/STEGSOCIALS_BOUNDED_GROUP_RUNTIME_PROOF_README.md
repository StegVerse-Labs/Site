# StegSocials bounded-group current-device runtime proof

Goal Task ID: `SS-KV-SKAP-SOCIAL-RELEASE-001`  
COSV: `60000000102000`

This surface closes the source-level observation gap between the merged bounded-group Node/InTr route and authentic same-device evidence. It reuses the existing registered StegVerse Node, GeneratedInTr transport, HB correlation binding, `/assets/my-kv-n-device-kv-receiver.js`, and `stegverse-device-local-intr-v1 / kv_files` store.

The proof runner requires an already-produced bounded-group CAS request containing proven publication and terminal StegBrowser session destruction. Before routing it independently reads the exact DEVICE_KV row and verifies the stored bytes hash to `expected_previous_etag`. It then calls `commitObserved`, retaining the Node/outbox/materialization identities and resident receipt commitment. After the CAS completes, it independently rereads DEVICE_KV and verifies the stored bytes hash to `next_state_etag`.

The emitted evidence schema is `stegverse.site.stegsocials-bounded-group-runtime-observation/v1`. It records Node ID, Interlock ID, outbox hash, query request ID, packet/payload identity, materialization identity/hash, resident receipt hash, pre/post state hashes, CAS result, publication receipt reference, and terminal session-destruction state. Credential material is prohibited.

A generated local InTr intent/materialization and a resident worker response are not proof of externally admitted InTr execution. Therefore every local proof emitted by this surface explicitly retains `external_intr_admission_observed=false` and `external_intr_admission_receipt_ref=null`. That predicate may change only when a separately authenticated external-admission receipt is observed and exact-bound in a later runtime step.

HB remains correlation/freshness evidence only: `carrier_grants_authority=false`, `execution_authority=false`, and `authority_effect=NONE_CORRELATION_ONLY`. Interlock/InTr remains transition authority and TV/TVC remains credential authority.

Browser entry point: `stegsocials-bounded-group-runtime-proof.html`.

Source/CI success validates this instrumentation but does not manufacture current-iPhone execution, external InTr admission, live platform publication, TV/TVC-SKAP credential activation, or Master Records custody.
