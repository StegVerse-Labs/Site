# Current iPhone KV TestFlight Static Bootstrap Mirror Handoff

Updated: 2026-09-13
Repository: `StegVerse-Labs/Site`
Goal Task ID: `KV-BOUND-EPHEMERAL-BROWSER-PROJECTION-001`
Canonical allocator task: `TASK-2026-0011`
COSV: `50000010100000`
Status: `ACTIVE / AUTHENTIC G7 FENCE7 / SAME-DEVICE KV RECOVERY PUBLIC / NATIVE TVC BUILD-UPLOAD SOURCE COMPOSED AND PUBLIC / CURRENT-IPHONE RUNTIME OBSERVATION PENDING`

## Authentic allocator evidence

```text
selected_task_id: TASK-2026-0011
claim_registry_generation: 7
claim_observation.state: CLAIM_GRANT_OBSERVED
fencing_token: 7
dependency_surface: site:current-iphone-kv-testflight-static-bootstrap
canonical_allocator_receipt.state: ALLOCATION_COMPLETE
canonical receipt sha256: sha256:3cd0aa9245be0ac5e9b81bc6c5a48aae0edc6f7c95162998e854feea04e75520
node journal sequence: 67
node journal entry sha256: 34d649f1227db25f1a9ddb38fbea709c0fdf4ff5ad0148bb781bbee5c18fb5cf
journal replay: PASS
allocator recovery/export mutation: false
```

## Public same-device entrypoint

```text
https://stegverse.org/task0011-same-device-kv-recovery.html
```

The normal path derives the exact KV-bound projection in memory and calls the public StegOS bootstrap without requiring a saved projection JSON. If resident KV installation is not verified, the existing bounded installation-receipt recovery remains available and still requires the canonical `_System/installation.receipt.json`.

## Native TVC Build Upload composition

The prior source boundary `TVC_NATIVE_BUILD_UPLOAD_BYTE_INGRESS` is implemented without a second artifact store or provider plane.

Canonical TVC receiver:

```text
StegVerse-Labs/TVC PR #428
merge commit: 46878481c23efd9b7d2cd17fc9f701616e687b22
```

The current-iPhone TVC surface accepts the existing secret-free `UPLOAD_TESTFLIGHT_BUILD` descriptor plus the already-verified signed IPA bytes in the same execution. It revalidates exact artifact ref/hash/size/bundle/app bindings, resolves current purpose-bound Apple SKAP custody, and invokes the existing native App Store Connect Build Upload transaction. The signed IPA is not persisted by the ingress; only a secret-free receipt is retained.

Canonical StegOS caller:

```text
StegVerse-Labs/StegOS PR #379
merge commit: c064c7542e113703a9fd0efe9eb08106de956937
```

The current-iPhone bootstrap keeps `signedIpa` in the same invocation, builds the existing secret-free TVC upload request, streams the bytes to TVC with `credentials: "omit"`, and validates the returned Build Upload result/receipt. Source success advances only to:

```text
TVC_NATIVE_BUILD_UPLOAD_COMMITTED
```

The next boundary is:

```text
TESTFLIGHT_PROCESSING_INSTALL_OBSERVATION
```

This source state does not assert that an Apple upload, TestFlight processing, installation, or resident execution occurred.

## Site projection and publication evidence

Site PR #1299 merged the canonical public projection at:

```text
6c1f267b49ab6e36618a2eccc8afceaf4544fbe0
```

Exact-head governing checks:

```text
Site Handoff Orchestrator run 34791706184: PASS
Ecosystem Heartbeat Orchestration run 34791706250: PASS
Site Bootstrap Validate run 34791706246: PASS
Validate StegOS Persistent Card UX run 34791706223: PASS
```

Credential-free live publication proof:

```text
StegVerse-Labs/.github workflow run 34791777867: PASS
TASK0011_NATIVE_TESTFLIGHT_UPLOAD_PUBLICATION=PASS
TASK0011_RUNTIME_PROOF_EFFECT=NONE
```

The live proof required the public bootstrap, upload-request builder, and byte-ingress client to expose the exact native-upload markers while rejecting credential/hosted-fallback markers.

## Authority boundary

- WorkerCoordinator/canonical allocator remains claim/fence authority.
- Interlock/InTr remains governed transition/admission authority.
- KV remains the private continuity/state-dependent AI boundary.
- SKAP remains credential custody beneath TV/TVC provider execution.
- TV/TVC remains Apple credential/provider/signing/release authority.
- Site remains public projection/rendezvous only.
- GitHub Actions remain validation/evidence transport only.
- HB remains carrier/observability only.
- No provider credential is exposed to Site, browser code, GitHub Actions, or the model.
- No signed IPA artifact store, second user-operated machine, or hosted fallback was introduced.
- Source, CI, and public publication do not satisfy a runtime state-transition predicate.

## Current first unresolved predicate

```text
TESTFLIGHT_CURRENT_IPHONE_RUNTIME_OBSERVED
```

The next authentic transition must come from the established current-iPhone same-device execution path. A successful execution may now reach `TVC_NATIVE_BUILD_UPLOAD_COMMITTED`, after which TestFlight processing/install observation remains required under the canonical task predicates.

## Manual work

Open `https://stegverse.org/task0011-same-device-kv-recovery.html` on the established current iPhone and tap `Use This iPhone's KV and Prepare IPA`. Preserve the complete successful result or the exact fail-closed text. Do not clear Safari/site/KV/node continuity and do not substitute an older projection JSON.
