# StegWallet Base App and Web3 Domain Strategy

## Decision

Use a dual-domain model:

```text
stegverse.org
  durable HTTPS application and governance origin

stegverse.base.eth (candidate; registration not yet performed)
  onchain identity, payment alias, profile/discovery name, and optional routing metadata
```

The Basename does not replace DNS, TLS, hosting, Site custody, admissibility, or execution authority.

## Base App posture

The Base App now treats applications as standard mobile web applications using an injected wallet, ordinary web authentication such as SIWE where required, and Base.dev project metadata. The StegWallet Site surface therefore remains an ordinary HTTPS application and uses EIP-1193 directly.

## Advantages of the Basename

- memorable wallet and project identity;
- Base ecosystem profile and discovery alignment;
- human-readable receiving address where supported;
- composable ENS-derived identity across compatible EVM applications;
- onchain text records that can point users to the canonical HTTPS origin;
- reduced address-copying risk when the resolver and destination are independently verified.

## Non-advantages and risks

- registration does not host the web application;
- renewal is required and expiration can release the name;
- onchain profile data is public;
- one Basename currently resolves to one address at a time;
- wallet and application support for resolution varies;
- name resolution does not prove that a transaction or application action is admissible;
- a compromised resolver or transferred name must not change canonical StegVerse governance records.

## Runtime requirements

```text
canonical web origin = HTTPS stegverse.org origin
canonical account identity = wallet address
optional display identity = Basename
name resolution result = observed evidence only
domain ownership = no execution authority
wallet signature = Mode 1 execution authority
HPS receipt + capped signer = Mode 2 prerequisite
```

## Registration boundary

No registration transaction is authorized by this document. Before purchase:

1. confirm exact availability and price in the official Basenames interface;
2. select the owning StegVerse wallet and renewal responsibility;
3. produce a registration intent with duration and maximum total cost;
4. review public onchain profile fields;
5. sign registration in the owning wallet;
6. retain transaction, resolver, address, renewal, and profile receipts;
7. set the HTTPS origin text record only after the deployed origin is verified.

## Candidate

```text
stegverse.base.eth
```

Availability, reservation status, registration price, and ownership are not yet verified.
