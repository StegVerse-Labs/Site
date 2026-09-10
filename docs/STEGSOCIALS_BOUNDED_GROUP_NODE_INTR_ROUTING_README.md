# StegSocials Bounded Group Node/InTr Routing

Goal Task ID: `SS-KV-SKAP-SOCIAL-RELEASE-001`

This integration routes an already-admitted bounded StegSocials post-group use-state transition through the existing registered StegVerse Node and generated Universal InTr materialization transport to the existing resident MyKV DEVICE_KV worker. It deliberately creates no second service-worker runtime, KV store, InTr authority plane, credential path, or publication authority.

## Reused runtime surfaces

```text
StegVerseGeneratedInTr
StegVerseHBInTrCarrier
StegVerseNodeContinuity
/assets/my-kv-n-device-kv-receiver.js
/assets/my-kv-n-runtime/
stegverse-device-local-intr-v1 / kv_files
```

The bridge builds a `COMMIT_CANDIDATE` envelope whose record class is `STEGSOCIALS_BOUNDED_GROUP_USE_STATE_CAS`, binds the exact group/use index and canonical Personal-KV state path, hashes the exact CAS-request bytes, then sends the resulting materialization request through the existing registered Node outbox. HB contributes only the carrier binding and is explicitly forbidden from granting execution or transition authority.

The existing MyKV resident worker now recognizes the bounded social CAS record class under its existing `STEGVERSE_MY_KV_N_LOCAL_TRIGGER` entrypoint. It verifies the Node/outbox/materialization bindings, exact payload hash and size, canonical state destination, group/use bindings, and no-credential/no-provider-authority boundary. It then delegates only atomic persistence to `StegVerseStegSocialsBoundedGroupDeviceKVCASReceiver.commit()`.

## Evidence boundary

Deterministic CI proves source composition, worker reuse, trigger binding, request/receipt shape, and preservation of fail-closed boundaries. It does not prove that an external InTr authority admitted a real publication transition, that the current iPhone executed the route, or that any social platform publication occurred.

Authentic completion requires a current-iPhone resident observation containing the externally admitted transition identity, Node/outbox/materialization bindings, exact pre-state etag, committed next-state etag, independent DEVICE_KV readback, authentic StegBrowser publication/destruction evidence, Personal-KV custody, and Master Records reconstruction.
