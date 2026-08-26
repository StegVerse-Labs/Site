# StegFin Phone SKAP InTr Route Mirror Handoff

Status: PRIMARY_GATEWAY_DOUBLE_INTERLOCK_SOURCE_VALIDATED / UPSTREAM_TVC_SOURCE_HOSTED_VALIDATED / PRODUCTION_ROUTE_KEY_AND_REAL_INGRESS_PENDING
Repository: `StegVerse-Labs/Site`
Goal ID: `SITE-SKAP-INTR-PUBLIC-ROUTE-CONSUMER-001`
Claim: `SITE-SKAP-INTR-PUBLIC-ROUTE-CONSUMER-20260825`
Updated: 2026-08-26T15:42:00-05:00

## Scope

Provide the current-user iPhone trusted interactive edge for owner authorization and browser-local sealing into the canonical credential path:

```text
Device <-InTr-> KV <-InTr-> SKAP Vault
```

Site must never gain credential plaintext custody, ordinary-KV decryption authority, SKAP private-key authority, provider-operation authority, or trading authority.

Primary public transport is the shared StegVerse Service Gateway. The resident zero-credential rotating HTTPS tunnel is fallback transport only. Neither transport may bypass either Interlock.

## Source implementation

- `assets/stegfin-phone/coinbase-skap-ingress.js`: owner authorization + browser-local P-256 ECDH/HKDF/AES-GCM sealing only.
- `assets/stegfin-phone/coinbase-skap-submission.js`: separates `STAGED_FOR_TVC` from `ADMITTED_TO_SKAP_VAULT`.
- `assets/stegfin-phone/coinbase-skap-ingress-ui.js`: submits sealed ciphertext only; no provider plaintext persistence.
- `assets/stegfin-phone/coinbase-skap-ingress-config.json`: production recipient config remains fail closed until a live TVC key lease/liveness projection exists.
- `assets/stegfin-phone/coinbase-skap-intr-route.json`: fallback descriptor remains non-authoritative and must not fabricate production routing.
- `scripts/check_stegfin_phone_projection_with_skap.py`: canonical SKAP-aware complete-page projection validator.
- `scripts/check_coinbase_skap_intr_route_consumer.py`: route/failover validation.

## State semantics

```text
STAGED_FOR_TVC
  proves: DEVICE -> KV InTr receipt + exact ciphertext staging
  does_not_prove: KV -> SKAP Vault receipt or SKAP Vault custody
  next: KV_SKAP_VAULT_INTERLOCK_ADMISSION

ADMITTED_TO_SKAP_VAULT
  proves: first receipt validated + second receipt chained + double-interlock admission + ciphertext custody
  does_not_prove: provider permission, fee state, execution or trade
  next: PROVIDER_ENDPOINT_SESSION_VERIFICATION
```

The UI must never render Gateway staging as SKAP Vault admission.

## Verified source/baseline evidence

```text
continuity-vault-kit SKAP Vault double-interlock: run 32884444828 SUCCESS
TVC SKAP Vault stage drain: run 32884923736 SUCCESS
TVC full Coinbase path: run 32884923740 SUCCESS
Site Coinbase SKAP phone ingress: run 32885823495 SUCCESS
LLM-adapter primary Gateway first-interlock/readiness: run 32885966113 SUCCESS
```

The `StegVerse-Labs/continuity-vault-kit/SKAP_INTR_REVIEW_CANDIDATE_MIRROR_HANDOFF.md` baseline has now advanced further:

```text
RC-01 Schema: PASS
RC-02 Negative topology: PASS
RC-03 Authority: PASS
RC-04 Endpoint resolution: PASS
RC-05 connected-KV runtime: PASS
```

RC-05 includes a real connected-KV non-secret replayable `DEVICE -> KV -> SKAP_VAULT` receipt/readback observation. This proves baseline KV/InTr runtime behavior only; it does not prove production recipient-key provisioning or a real provider credential.

## Upstream TVC source/runtime reconciliation

The earlier resident integration merge remains:

```text
StegVerse-Labs/TVC PR #128
0e2a5986773243efafa835f9c214e963b8d08c96
```

Later issue #119 source evidence narrows the remaining gap further:

```text
TVC deferred-decryption custody/resolver: run 32878176812 SUCCESS
shared Service Gateway Coinbase dedicated validation: run 32879101025 SUCCESS
shared Service Gateway same-commit global validation: run 32879100937 SUCCESS
TVC Gateway stage-consumer validation: run 32879237493 SUCCESS
TVC connector-only SKAP Vault persistence/filesystem boundary: run 32887404270 SUCCESS
TVC resident SKAP Vault boundary observer + negative tests: run 32887566151 SUCCESS
TVC canonical handoff/task reconciliation: 8b99c290a740b460b72d258f50cff8342c7662ba
```

Current upstream invariants now explicitly include:

- Render is not required for this goal;
- the shared StegVerse Service Gateway is the primary public ciphertext transport;
- the zero-credential rotating HTTPS tunnel remains fallback only;
- browser ciphertext persists unchanged; no public-ingress decrypt/rewrap is allowed;
- first plaintext resolution remains callback-only after exact provider endpoint/session verification and current-grant revalidation;
- `tools/skap_vault_store.py` is the only Coinbase SKAP Vault persistence connector;
- resident filesystem writes are restricted to `_Vault/SKAP/Credentials` and `_Vault/SKAP/Receipts` under the governed boundary observer.

These hosted/source accomplishments do not prove physical resident activation, live key/liveness, the real primary route, owner ingress, production custody, provider permission/fee state, or trading.

Canonical upstream handoff:
`StegVerse-Labs/TVC/docs/TVC_COINBASE_IPHONE_SKAP_ACTIVATION_MIRROR_HANDOFF.md`.

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
browser private SKAP key: NONE
STAGED_FOR_TVC != ADMITTED_TO_SKAP_VAULT
route availability != credential authority
route availability != provider authority
```

Network ambiguity remains `VERIFY_EXTERNALLY`; blind retry is forbidden.

## Current production state

```text
Site double-interlock/browser source: HOSTED PASS
CVK baseline RC-01..RC-05: COMPLETE
TVC primary Gateway/custody/resolver/persistence source: HOSTED PASS
TVC one-command resident shared-KV integration: MERGED
Site production recipient config: NOT_PROVISIONED
Site production primary Gateway endpoint: NOT_PROVISIONED/NOT OBSERVED
Site fallback route descriptor: NOT_PROVISIONED
real resident recipient key/liveness: NOT OBSERVED
resident READY_FOR_OWNER_INGRESS: NOT OBSERVED
real current-iPhone owner ingress: NOT OBSERVED
real production DEVICE -> KV receipt: NOT OBSERVED
real production KV -> SKAP_VAULT receipt: NOT OBSERVED
real double-interlock gate receipt: NOT OBSERVED
real provider credential ciphertext object: NOT OBSERVED
exact production ciphertext readback: NOT OBSERVED
real provider-authenticated permission/fee observation: NOT OBSERVED
```

## User action required

No secret/credential should be entered yet while production recipient config and route remain unprovisioned.

After the machine-side TVC lane proves a current recipient key/liveness, `READY_FOR_OWNER_INGRESS`, and a live public Gateway route, the current user must perform the remaining physical-device step on the iPhone:

1. open the trusted StegVerse ingress surface;
2. complete WebAuthn/StegID owner authorization;
3. enter the provider credential only into the browser-local sealing UI;
4. submit the sealed ciphertext packet;
5. do not paste credential plaintext into chat, Drive, GitHub, issues, logs, or screenshots.

## Machine-executable next boundary

1. TVC physically activates/observes the merged resident path against the real shared KV/SKAP root.
2. TVC produces current recipient-key activation/liveness and `READY_FOR_OWNER_INGRESS` evidence.
3. Shared Service Gateway production Coinbase readiness/ingress route is observed.
4. Only current public recipient/config/route evidence is propagated to Site.
5. Site enables trusted owner ingress.
6. After the user submits the sealed packet, retain the real `DEVICE -> KV` receipt, chained `KV -> SKAP_VAULT` receipt, double-interlock gate, custody receipt, and exact ciphertext readback.
7. Only then continue to endpoint/session-bound provider permission/fee observation.

## Completion boundary

This Site goal remains ACTIVE/WAITING until a current recipient projection and public route are live, the current iPhone performs owner-authorized sealed ingress, both production Interlock receipts are observed/chained, and the real ciphertext object/readback is retained in SKAP Vault. `IMPLEMENTED`, `HOSTED PASS`, `MERGED`, connected-KV baseline `PASS`, and production `ACTIVATED/OBSERVED` remain distinct.


## 2026-08-26 archive-boundary reconciliation

Upstream source work is no longer the limiting boundary. The canonical TVC activation handoff now records that all available repository/source integration is complete and the next state requires authorized resident Interlock/InTr execution.

```text
CVK RC-01..RC-05 baseline: COMPLETE
TVC resident activation source: IMPLEMENTED / MERGED
TVC resident boundary observer source: HOSTED PASS
Site browser/route consumer source: HOSTED PASS
physical resident key/liveness: NOT OBSERVED
READY_FOR_OWNER_INGRESS: NOT OBSERVED
public production Gateway route: NOT OBSERVED
production double-Interlock receipt chain: NOT OBSERVED
real owner iPhone ingress: NOT DUE YET
```

Site must remain fail closed. Do not provision a production recipient configuration or enable owner credential entry from source-only evidence.

The next authoritative transition is:
`StegVerse-Labs/TVC/docs/TVC_COINBASE_IPHONE_SKAP_ACTIVATION_MIRROR_HANDOFF.md`.

Only after TVC produces current recipient-key liveness, `READY_FOR_OWNER_INGRESS`, and observed public-route evidence may Site consume the public projection and expose the trusted owner-ingress step.

### Archive readiness

The Site consumer/source state, upstream owner, exact remaining InTr evidence, and user-action gate are durable. This coordinating conversation can be archived without losing Site continuation state. This does not claim route activation, credential custody, provider access, or trading completion.
