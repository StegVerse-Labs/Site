# StegFin Phone Participant Projection Mirror Handoff

Updated: 2026-08-24T23:14:00-05:00
Repository: `StegVerse-Labs/Site`
Canonical issue: #388
Goal ID: `SITE-STEGFIN-IOS-LOCAL-WALLET-TRANSPORT-388`

## Canonical role

Site is a static participant/publication projection only. It does not own Coinbase credentials, TV/TVC authority, SKAP private/root keys, wallet signing, broadcast, settlement, or production runtime authority.

Current user-operated physical surface:

```text
CURRENT_USER_IPHONE
```

Credential authority:

```text
TV/TVC ONLY
```

No second user-operated machine, GitHub-token runtime authority, Render/Vercel/Cloudflare production authority, durable Device credential custody, automatic signing, or automatic broadcast is permitted.

## Existing phone/WebAuthn surface

`assets/stegfin-phone/stegid-device-wallet-bootstrap.js` retains the real WebAuthn `navigator.credentials.create/get` ceremonies with `userVerification='required'`. UVPAA remains advisory only; HUMAN_CONTINUITY is granted by the actual ceremony.

The page still states: `This phone is the StegVerse machine`.

## Coinbase browser->SKAP ingress surface

Implemented source:
- `assets/stegfin-phone/coinbase-skap-ingress.js` — browser P-256 ECDH + HKDF-SHA256 + AES-256-GCM sealing;
- `assets/stegfin-phone/coinbase-skap-ingress-ui.js` — fail-closed local credential capture/field clearing;
- `assets/stegfin-phone/coinbase-skap-ingress-config.json` — independent recipient-key and receiver provisioning gates;
- `assets/stegfin-phone/coinbase-skap-submission.js` — ciphertext-only governed receiver client;
- `stegfin-trade.html` — projects the above surface.

Browser credential plaintext is not deliberately written to localStorage, sessionStorage, IndexedDB, cookies, URLs, logs, GitHub or repository evidence. The phone receives no SKAP private/root key.

## Independent activation gates

The Site config currently and intentionally contains:

```text
status: NOT_PROVISIONED
recipient_key_id: null
recipient_public_jwk: null
submission_status: NOT_PROVISIONED
submission_endpoint: null
activation_effect: NONE
```

Both gates must become valid before credential capture can be enabled:

1. ACTIVE TVC/SKAP P-256 recipient public-key lease;
2. governed StegVerse-native ciphertext receiver.

Provisioning one without the other must not enable credential capture/submission.

## Ciphertext-only submission contract

`coinbase-skap-submission.js` listens only after local sealing and accepts only the browser-sealed ingress packet.

Receiver requirements:
- HTTPS only;
- origin exactly `https://stegverse.org` or `https://www.stegverse.org`;
- no URL credentials/query/fragment;
- `redirect:'error'`;
- `credentials:'omit'`;
- `referrerPolicy:'no-referrer'`;
- `cache:'no-store'`;
- POST JSON ciphertext packet only.

The client rejects packets claiming plaintext, Device secret custody, KV resolution authority, GitHub secret access, SKAP private-key export, or authority transfer. It rejects common plaintext credential field names in the outbound serialized packet.

Accepted response must be:

```text
schema: stegverse.tvc.coinbase_browser_ingress_response/v1
decision: ADMITTED
canonical_ciphertext_returned: false
credential_plaintext_returned: false
execution_authority: NONE
may_authorize_order: false
retry_policy: NEW_OWNER_AUTHORIZED_PACKET_REQUIRED
```

Network/ambiguous submission failure becomes:

```text
VERIFY_EXTERNALLY
blind_retry_allowed: false
```

No automatic retry of the same owner-authorized packet is permitted.

## Hosted validation

Dedicated validator: `scripts/check_coinbase_skap_phone_ingress.py`.

It now verifies:
- P-256/ECDH/HKDF/AES-GCM source invariants;
- no private JWK `d` in provisioned public config;
- exact TV/TVC/current-iPhone authority boundaries;
- recipient-key fail-closed state;
- governed receiver fail-closed state;
- StegVerse receiver origin allowlist;
- redirect denial;
- ambiguous => `VERIFY_EXTERNALLY`;
- blind retry disabled;
- no browser credential persistence/logging calls;
- WebAuthn `userVerification='required'` remains intact;
- credential inputs default disabled.

`Coinbase SKAP Phone Ingress Validation` run `32808115231` completed `SUCCESS`, including validation-only authority proof.

## Current state

```text
phone WebAuthn source: HOSTED VALIDATED
browser->SKAP local encryption source: HOSTED VALIDATED
ciphertext-only submission client: HOSTED VALIDATED
recipient public-key production lease: OPEN
receiver production endpoint: OPEN
real current-iPhone Coinbase ingress: OPEN
real SKAP admission/provider observation: OPEN
wallet signing/broadcast: USER_ONLY / NOT EXECUTED BY THIS LANE
```

## Cross-repository continuation

```text
Site current-iPhone browser surface
-> TVC governed ciphertext receiver
-> continuity-vault-kit browser admission bridge
-> canonical SKAP custody
-> TVC provider-bound authenticated observation
-> crypto-bot bounded maker proof/reconciliation
```

TVC hosted provider-session validation: `32807570916` SUCCESS.  
continuity-vault-kit browser->canonical SKAP bridge validation: `32807856275` SUCCESS.

## Next executable work

1. Build/validate the TVC HTTP receiver adapter around `coinbase_browser_skap_ingress_service.py`.
2. Route a StegVerse-owned HTTPS path to that receiver without making Site/Cloudflare/third-party hosting credential or execution authority.
3. Establish production TVC/SKAP P-256 recipient-private-key custody + ACTIVE public-key lease.
4. Only then project the public key + receiver URL into this config and perform real current-iPhone owner-authorized ingress.

## Non-claims

The Site is not currently enabled for Coinbase credential entry because the production key and receiver are not provisioned. No real Coinbase credential has been submitted by this work. No live Coinbase order has been executed by this lane.
