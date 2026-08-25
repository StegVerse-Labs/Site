# StegFin Phone SKAP InTr Route Mirror Handoff

Status: PRIMARY_GATEWAY_DOUBLE_INTERLOCK_SOURCE_VALIDATED / PRODUCTION_ROUTE_KEY_AND_REAL_INGRESS_PENDING
Repository: `StegVerse-Labs/Site`
Goal ID: `SITE-SKAP-INTR-PUBLIC-ROUTE-CONSUMER-001`
Claim: `SITE-SKAP-INTR-PUBLIC-ROUTE-CONSUMER-20260825`
Updated: 2026-08-25T13:52:00-05:00

## Scope

Current-user iPhone Site surface reaches the KV-hosted SKAP Vault without gaining credential, ordinary-KV decryption, SKAP private-key, provider-operation or trading authority.

Canonical credential path:

```text
Device <-InTr-> KV <-InTr-> SKAP Vault
```

Primary public transport is the StegVerse shared Service Gateway. The resident zero-credential rotating HTTPS tunnel is an explicit fallback only. Neither transport has credential/provider/execution authority, and neither may bypass either credential interlock.

## Source implementation

- `assets/stegfin-phone/coinbase-skap-ingress.js` performs owner authorization + browser-local P-256 ECDH/HKDF/AES-GCM sealing only.
- `assets/stegfin-phone/coinbase-skap-submission.js` now distinguishes primary `STAGED_FOR_TVC` from later `ADMITTED_TO_SKAP_VAULT`:
  - primary Gateway success proves only the `DEVICE -> KV` InTr transition and returns an embedded first-boundary receipt;
  - later SKAP Vault admission requires a second `KV -> SKAP_VAULT` InTr receipt chained to the first;
  - both states remain non-authorizing for provider execution.
- `assets/stegfin-phone/coinbase-skap-ingress-ui.js` dispatches only sealed ciphertext and never persists provider plaintext.
- `assets/stegfin-phone/coinbase-skap-intr-route.json` remains `NOT_PROVISIONED`; it is fallback descriptor state, not the primary Gateway authority source.
- recipient config remains separately fail-closed until a real TVC key lease/liveness projection exists.
- `scripts/check_stegfin_phone_projection_with_skap.py` is the SKAP-aware successor projection validator for the complete page.
- `scripts/check_coinbase_skap_intr_route_consumer.py` and the dedicated workflow retain route/failover validation.

## State semantics

```text
PRIMARY_GATEWAY / STAGED_FOR_TVC
  proves: DEVICE -> KV InTr receipt + exact ciphertext staging
  does_not_prove: KV -> SKAP Vault receipt or SKAP Vault custody
  next: KV_SKAP_VAULT_INTERLOCK_ADMISSION

ADMITTED_TO_SKAP_VAULT
  proves: first receipt validated + second receipt chained + SKAP Vault custody
  does_not_prove: Coinbase permission, fee state, execution or trade
  next: COINBASE_ENDPOINT_SESSION_VERIFICATION
```

The UI must not emit the SKAP Vault admitted event from a Gateway staging receipt.

## Hosted evidence

Current aligned evidence:

```text
continuity-vault-kit SKAP Vault double-interlock: run 32884444828 SUCCESS
TVC SKAP Vault stage drain: run 32884923736 SUCCESS
TVC full Coinbase path: run 32884923740 SUCCESS
Site Coinbase SKAP phone ingress: run 32885823495 SUCCESS
LLM-adapter primary Gateway first-interlock/readiness: run 32885966113 SUCCESS
```

## Authority invariants

```text
credential_authority: TV/TVC
credential_custody_target: KV_HOSTED_SKAP_VAULT
transport_protocol: InTr
Site provider authority: NONE
Site trading authority: NONE
ordinary KV decryption authority: NONE
Device durable secret custody: NONE
Gateway credential/decryption/execution authority: NONE
fallback carrier credential/provider authority: NONE
GitHub token runtime authority: NONE
browser private SKAP key: NONE
STAGED_FOR_TVC != ADMITTED_TO_SKAP_VAULT
route availability != credential authority
route availability != provider authority
```

Network ambiguity remains `VERIFY_EXTERNALLY`; blind retry is forbidden.

## Production state

```text
Site double-interlock source: HOSTED PASS
Site production recipient config: NOT_PROVISIONED
Site production primary Gateway endpoint: NOT_PROVISIONED
Site fallback route descriptor: NOT_PROVISIONED
real shared Gateway route observation: NOT OBSERVED
real resident recipient key/liveness: NOT OBSERVED
real DEVICE/KV receipt: NOT OBSERVED
real KV/SKAP Vault receipt: NOT OBSERVED
real SKAP Vault credential object: NOT OBSERVED
real Coinbase authenticated observation: NOT OBSERVED
```

## Global Site validation reconciliation

The old `scripts/check_stegfin_phone_projection.py` validates the pre-SKAP six-script baseline and is no longer sufficient as the canonical page validator after SKAP extension. `scripts/check_stegfin_phone_projection_with_skap.py` is the successor surface validator: it validates the complete nine-script projection and may reuse the legacy checker only against a temporary normalized pre-SKAP page to retain original wallet-boundary guarantees.

The repository-wide bootstrap must invoke the SKAP-aware successor rather than rejecting the intentional extension as script-order drift.

## Next executable boundary

1. Keep the whole-Site bootstrap green using the SKAP-aware projection validator.
2. Observe actual TV/TVC recipient key activation/liveness and shared Service Gateway readiness.
3. Propagate only current public recipient/config/route evidence.
4. Perform current-user iPhone WebAuthn authorization and browser sealing.
5. Retain real DEVICE/KV and chained KV/SKAP Vault receipts plus exact ciphertext readback under `_Vault/SKAP/Credentials`.
6. Only then proceed to endpoint/session-bound Coinbase permission/fee observation.

## Completion boundary

This goal remains open until an actual current recipient projection and public route are live, the current-user iPhone performs owner-authorized sealed ingress, both Interlock receipts are observed/chained, and the real ciphertext object is retained in the SKAP Vault. Source/hosted success is not production activation.
