# MyKV Public Propagation Observer Mirror Handoff

Repository: `StegVerse-Labs/Site`  
Goal Task ID: `KV-ICLOUD-AUTOMATED-UPGRADE-001`  
COSV ID: `40000100100000`  
State: `PUBLIC_SERVED_BODY_PROOF_PASS_HANDOFF_CLOSED`

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

## Authentic proof result

Observer implementation PR `#1366` passed its exact-head validation lanes and merged as `c89a460e5d6c2d92c49af1d663e5b18d61a0a0db`.

Main-branch workflow run `35144058676` then executed against the actual public `stegverse.org` origin. Both jobs completed successfully. Artifact `mykv-public-propagation-proof-35144058676` / artifact ID `10465584595` retained the three served bodies, response headers, and receipt.

The `stegverse.mykv-public-propagation-proof/v1` receipt recorded `PASS` on attempt 1 at `2026-09-16T20:01:50.459599Z`:

- install shell: HTTP `200`, SHA-256 `93b63188b69ba2f80030b76e620dc885957bd4e883ab27c8450d67e4382d82af`;
- manifest: HTTP `200`, SHA-256 `f0ab7bdc2d86a82113ccbee353ab20d4afaaae07d462f8e35bd52c00230fda94`;
- Node-continuity loader: HTTP `200`, SHA-256 `ee23a94de59b82f57cc98b4c9725f69bd8575ea457d9ff11133892322e4bf193`.

All deterministic checks were true: shell required markers, manifest object/standalone/root-scope/exact-start-URL predicates, and loader required markers. Receipt authority fields remained false for runtime authority, activation, execution, and GitHub Actions runtime authority.

The canonical coordination repo subsequently reconciled this proof through `.github` PR `#2026`, merged as `c310c9b250bac6ab5c7fe765c0ab174d1208b2bf`, advancing `KV-ICLOUD-AUTOMATED-UPGRADE-001` to `MYKV_CURRENT_IPHONE_OWNER_INSTALL_READY` while keeping the goal `ACTIVE`.

## Evidence contract

The retained PASS receipt records:

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

The proof establishes public served-body propagation only. It does not claim current-iPhone installation, resident-health state, Node mutation, KV-host selection, or KV installation/connect verification.

## Owner-action boundary

The public-propagation prerequisite is satisfied and canonical `.github` state is owner-install-ready. The next allowed owner action is only the single MyKV installation: Safari -> Share -> Add to Home Screen -> Add. After first standalone launch, capture and stop at the first consolidated resident-health / Node-continuity result before KV-host selection.

No separate StegOS installation and no second user-operated device is required.

## Release

This observer implementation/handoff lane is complete. After this handoff-closure update merges, release the associated session-work claim in a claim-registry-only terminalization PR using only fields permitted by the Site terminalization contract. The runtime goal itself remains active under the canonical `.github` task until the current-iPhone and KV predicates are authentically satisfied.
