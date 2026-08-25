# StegFin Phone SKAP InTr Route Mirror Handoff

Status: SOURCE_IMPLEMENTED_HOSTED_VALIDATION_PENDING
Repository: `StegVerse-Labs/Site`
Goal ID: `SITE-SKAP-INTR-PUBLIC-ROUTE-CONSUMER-001`
Updated: 2026-08-25

## Scope

Current-user iPhone Site surface consumes a TVC resident public InTr route without gaining credential, SKAP private-key, provider-operation or trading authority.

Canonical path:

```text
SKAP <-InTr-> KV <-InTr-> Device <-InTr-> External Network <-InTr-> Endpoint
```

For browser ingress, the public carrier is only the Device -> External Network -> resident SKAP admission edge. It transports already-sealed ciphertext to the TVC loopback receiver.

## Source implementation

- `assets/stegfin-phone/coinbase-skap-ingress.js` performs owner authorization + browser-local P-256 ECDH/HKDF/AES-GCM sealing only.
- `assets/stegfin-phone/coinbase-skap-submission.js` independently reloads recipient config + route descriptor immediately before POST, validates exact runtime/key/activation/liveness/lease equality, enforces HTTPS rotating carrier and ciphertext-only packet invariants, and maps ambiguous submission to `VERIFY_EXTERNALLY` with blind retry forbidden.
- `assets/stegfin-phone/coinbase-skap-ingress-ui.js` dispatches a sealed-capsule event; it does not submit plaintext or perform provider operations.
- `assets/stegfin-phone/coinbase-skap-intr-route.json` remains `NOT_PROVISIONED` until an actual TVC resident carrier projects a live descriptor.
- `scripts/check_coinbase_skap_intr_route_consumer.py` is the dedicated validation lane.

## Authority invariants

```text
credential_authority: TV/TVC
credential_custody_target: SKAP
transport_protocol: InTr
Site provider authority: NONE
Site trading authority: NONE
GitHub token runtime authority: NONE
browser private SKAP key: NONE
route availability != credential authority
route availability != provider authority
HTTP 201 alone != admitted custody proof
```

The accepted TVC response must prove unchanged ciphertext custody, no ingress decryption/rewrap, no returned plaintext/ciphertext, endpoint verification required before later resolution, execution authority `NONE`, and new owner authorization required for any retry.

## Production state

```text
Site route-consumer source: IMPLEMENTED
Site production recipient config: NOT_PROVISIONED
Site production route descriptor: NOT_PROVISIONED
TVC resident carrier source: HOSTED PASS (run 32878007309)
real resident route publication: NOT OBSERVED
real owner credential ingress: NOT OBSERVED
real Coinbase authenticated observation: NOT OBSERVED
```

## Known adjacent validation condition

The historical `check-stegfin-phone-projection.yml` lane currently fails because its active wallet-publication-owned `docs/STEGFIN_PHONE_PROJECTION_MIRROR_HANDOFF.md` no longer contains older exact marker strings required by `scripts/check_stegfin_phone_projection.py`. This SKAP lane does not overwrite that actively owned handoff or weaken its validator. Dedicated SKAP/InTr validation remains independently required.

## Completion boundary

This goal remains open until the dedicated hosted validation passes, an actual TVC resident route descriptor is propagated with a current recipient config, the current-user iPhone performs WebAuthn-authorized sealed ingress through that route, and TVC/KV retain only ciphertext plus non-secret custody evidence.
