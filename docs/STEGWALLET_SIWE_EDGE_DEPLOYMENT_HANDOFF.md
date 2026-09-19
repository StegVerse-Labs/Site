# StegWallet SIWE Edge Runtime Handoff

Status: `AUTHORIZATION_REQUIRED / PROVIDER-NEUTRAL`

## Purpose

Route only the five StegWallet SIWE endpoints through the canonical `stegverse.org` origin while preserving the existing Site authority boundaries. The repository retains bounded same-origin proxy source and tests, but no provider deployment adapter, provider CLI, provider account credential, or provider-owned deployment configuration is selected or shipped.

## Required route

`stegverse.org/api/stegwallet/siwe/*`

## Runtime contract

- Browser requests remain same-origin at `https://stegverse.org`.
- Client-supplied edge-authentication material is stripped before forwarding.
- An admitted runtime may inject separately authorized origin-authentication material.
- Direct-origin authentication is prohibited.
- Health observation is non-authorizing.
- Runtime selection must resolve through an admitted StegVerse-controlled/provider-neutral surface; absence fails closed.

## Current source posture

- `workers/stegwallet-siwe-edge/src/index.js` preserves bounded proxy behavior.
- `workers/stegwallet-siwe-edge/test.mjs` preserves behavior tests.
- `workers/stegwallet-siwe-edge/package.json` exposes validation only.
- `data/stegwallet-siwe-edge-deployment.json` remains `AUTHORIZATION_REQUIRED`, with no selected adapter.
- No provider deployment configuration or deployment command is retained.

## Activation sequence

1. Resolve an admitted StegVerse-controlled runtime origin.
2. Observe its tokenless health endpoint.
3. Bind the verified origin and separately authorized authentication material through the applicable TV/TVC-governed path.
4. Verify direct-origin authentication is rejected.
5. Verify the same request through `stegverse.org` reaches the admitted origin.
6. Run the canonical live SIWE activation probe.
7. Promote Site runtime state only from the resulting governed receipt.

## Authority boundary

Routing, health, deployment readiness, or wallet authentication grants no trade admissibility, signing authority, execution authority, delegation authority, custody acceptance, or settlement status.
