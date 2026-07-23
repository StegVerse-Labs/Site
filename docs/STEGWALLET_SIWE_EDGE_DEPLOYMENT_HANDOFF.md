# StegWallet SIWE Edge Deployment Handoff

Status: `AUTHORIZATION_REQUIRED`

## Purpose

Route only the five StegWallet SIWE endpoints through `stegverse.org` while preserving the existing static Site origin and blocking direct authentication against a public SIWE origin.

## Required route

`stegverse.org/api/stegwallet/siwe/*`

## Runtime contract

- Browser requests remain same-origin at `https://stegverse.org`.
- The Worker strips any client-supplied `X-StegWallet-Edge-Token` header.
- The Worker injects the secret `SIWE_EDGE_TOKEN` value.
- The SIWE origin requires the matching `STEGWALLET_SIWE_EDGE_TOKEN` for challenge, verification, session, and logout.
- The health endpoint remains tokenless for provider health checks and the canonical activation probe.
- Direct-origin authentication is prohibited.

## Deployment inputs

- Verified SIWE origin HTTPS URL.
- Cloudflare account authorization for the `stegverse.org` zone.
- A newly generated edge token of at least 32 characters.
- The same token provisioned separately to Cloudflare Worker secrets and the SIWE origin secret store.

Do not commit either secret.

## Candidate files

- `workers/stegwallet-siwe-edge/src/index.js`
- `workers/stegwallet-siwe-edge/wrangler.siwe.candidate.jsonc`
- `workers/stegwallet-siwe-edge/package.json`
- `data/stegwallet-siwe-edge-deployment.json`

## Activation sequence

1. Deploy the SIWE origin and observe its tokenless health endpoint.
2. Set the Worker `SIWE_UPSTREAM_ORIGIN` variable to the verified origin.
3. Provision `SIWE_EDGE_TOKEN` as a Worker secret.
4. Deploy the path-restricted Worker route.
5. Verify direct-origin authentication returns `403 edge_proxy_authentication_required`.
6. Verify the same request through `stegverse.org` reaches the origin.
7. Run the canonical live SIWE activation probe.
8. Promote the Site runtime only from the resulting edge-aware activation receipt.

## Authority boundary

Deployment readiness, routing, health, or wallet authentication grant no trade admissibility, signing authority, execution authority, delegation authority, custody acceptance, or settlement status.
