# StegFin SKAP InTr Submit Mirror Handoff

Status: IMPLEMENTATION_IN_PROGRESS
Repository: `StegVerse-Labs/Site`
Goal ID: `SITE-STEGFIN-SKAP-INTR-SUBMIT-001`
Claim: `SITE-STEGFIN-SKAP-INTR-SUBMIT-20260825`
Updated: 2026-08-25T12:24:00-05:00

## Purpose

Bind the current-user iPhone StegFin SKAP browser-sealed Coinbase capsule to the live TVC-resident public InTr carrier without granting Site, Device, GitHub, the carrier, or the browser provider-operation authority or durable provider-secret custody.

Canonical topology remains:

```text
SKAP <—> KV <—> Device <—> external network <—> Endpoint
```

The `<—>` relationship is the InTr/interlock transport protocol. This implementation does not introduce an additional transport authority component between those participants.

## Existing source reused

- `assets/stegfin-phone/coinbase-skap-ingress.js` already performs browser-local P-256 ECDH + HKDF-SHA256 + AES-256-GCM sealing after owner authorization.
- `assets/stegfin-phone/coinbase-skap-submission.js` already rejects plaintext-bearing packets, submits ciphertext only, rejects redirects, treats network ambiguity as `VERIFY_EXTERNALLY`, forbids blind retry, and validates a non-authorizing TVC custody response.
- TVC now owns the resident public carrier contract/projector/runtime under `StegVerse-Labs/TVC`; Site does not create or operate that carrier.

## Required change

Recipient-key configuration and public route discovery are separate state objects:

```text
recipient config = how/where the capsule is sealed
route descriptor = where the current InTr carrier terminates
```

Before submission Site must require both and prove they refer to the same current TVC resident state:
- `runtime_instance_id` exact match;
- `recipient_key_id` exact match;
- `activation_receipt_hash` exact match;
- `liveness_receipt_hash` exact match;
- `lease_expires_at` exact match and still current;
- `transport_protocol=InTr`;
- `credential_authority=TV/TVC`;
- `credential_custody_target=SKAP`;
- route status exactly `ROUTE_LIVE`;
- route cannot claim public-route or provider-operation authority;
- route endpoint must be HTTPS with the bounded `/v1/skap/coinbase/ingress` path and no credentials/query/fragment.

Immediately before POST, both configuration objects must be fetched and cross-validated again. A previously resolved route is insufficient.

## Production fail-closed state

`assets/stegfin-phone/coinbase-skap-intr-route.json` remains `NOT_PROVISIONED` until an actual TVC resident carrier has produced a current route descriptor from live recipient-key/activation/liveness evidence. Source or hosted validation must not populate a synthetic production origin.

## Authority boundaries

- credential authority: `TV/TVC`
- credential custody target: `SKAP`
- Site credential custody: `NONE`
- Device durable credential custody: `NONE`
- public carrier credential authority: `NONE`
- provider-operation authority from route availability: `NONE`
- GitHub-token runtime authority: `NONE`
- Render: `PROHIBITED`
- wallet signing/broadcast authority: unchanged `USER_ONLY`

## Current evidence

- Site pre-work claim validation: `SESSION_WORK_CLAIMS_PASS`
- Site orchestration validation: `SITE_HANDOFF_ORCHESTRATION_PASS`
- TVC public InTr carrier hosted validation: `Infrastructure Credential Authority` run `32877284179` — `SUCCESS`
- Site bootstrap run `32877408599` is red only on pre-existing StegFin projection-validator drift; the claim/orchestration steps themselves passed.

## Completion boundary

This Site goal is source-complete only after route/config cross-binding, route freshness checks, ciphertext-only POST, ambiguity/no-blind-retry behavior, sanitized response validation, and deterministic hosted validation are all retained. Production activation remains separately open until a TVC resident route descriptor and recipient configuration are actually live and a real owner-authorized iPhone ciphertext admission is observed.
