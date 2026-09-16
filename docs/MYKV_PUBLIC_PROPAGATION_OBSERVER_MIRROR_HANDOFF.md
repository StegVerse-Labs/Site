# MyKV Public Propagation Observer Mirror Handoff

Repository: `StegVerse-Labs/Site`  
Goal Task ID: `KV-ICLOUD-AUTOMATED-UPGRADE-001`  
COSV ID: `40000100100000`  
State: `OBSERVER_IMPLEMENTATION_PENDING_MERGE_AND_PUBLIC_PROOF`

## Purpose

Provide a credential-free, non-authorizing public HTTPS observer for the three served bodies that must be current before the owner is asked to install MyKV on the current iPhone:

- `https://stegverse.org/my-kv-install.html`
- `https://stegverse.org/my-kv.webmanifest`
- `https://stegverse.org/assets/stegverse-node-continuity.js`

The observer records HTTP status, exact served-body SHA-256 hashes, response headers, retained served bodies, and deterministic contract checks. GitHub Actions is evidence transport only and receives no runtime, deployment, KV, Node, provider, Interlock/InTr, or activation authority.

## Required served-body predicates

### Install shell

The served install shell must return HTTP 200 and retain all of the following current-main markers:

- `20260915-unified-mykv-v1`
- `single owner-facing installation surface`
- automatic establishment or reuse of the minimal resident StegOS/Node substrate
- fail-closed health gate requiring `resident_install_health == HEALTHY`
- fail-closed registered-Node gate
- stop-before-KV-host-selection language
- no separate owner-facing StegOS installation step

### Manifest

The served manifest must return HTTP 200, parse as an object, retain `display=standalone`, root scope, and exact standalone start URL `/my-kv-install.html?source=installed`.

### Node-continuity loader

The served loader must return HTTP 200 and retain the canonical same-origin chain for schema compatibility, StegOS bootstrap implementation, `20260915-unified-mykv-v1` device-local autostart, Node-continuity implementation, and `20260915-unified-mykv-v1` resident-health client.

## Evidence contract

A PASS receipt uses schema `stegverse.mykv-public-propagation-proof/v1` and records:

- Goal Task ID and COSV ID;
- observation timestamp and attempt;
- each exact public URL;
- each HTTP status;
- each exact served-body SHA-256 hash;
- deterministic predicate results;
- `authority_effect=false`;
- `activation_effect=false`;
- `execution_authority=false`;
- `github_actions_runtime_authority=false`.

The workflow retains the three served bodies, response headers, and receipt as a GitHub Actions artifact. A source merge, successful unit test, workflow existence, or repository file hash is not a substitute for the authentic public served-body PASS artifact.

## Owner-action boundary

Do not expose the owner installation action until a post-merge public observer run returns PASS from the actual `stegverse.org` origin. On PASS, reconcile the canonical `.github` handoff to owner-install-ready, then expose only the single MyKV installation action: Safari -> Share -> Add to Home Screen -> Add. After first standalone launch, stop at the first consolidated resident-health / Node-continuity result before KV-host selection.

No second user-operated device is required.
